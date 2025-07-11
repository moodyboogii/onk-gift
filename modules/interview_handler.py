"""
인터뷰 처리 관련 함수들
"""
import streamlit as st
import openai
import json
from modules.prompt_utils import get_system_prompt
from modules.session_manager import add_message, mark_interview_completed, get_language


def show_welcome_message():
    """첫 인사 메시지 표시"""
    current_language = get_language()
    
    if current_language == "en":
        welcome_msg = """Hello! 🎁
        Thank you for joining the K-gift recommendation chatbot <b>ON:K</b>!
        
        From now on, I'll recommend the perfect gift that matches 
        your situation and preferences through a few questions.
        
        First, could you tell me <b>who this gift is for</b>? 🌿"""
    else:
        welcome_msg = """안녕하세요! 🎁
        K‑선물 추천 챗봇 <b>ON:K(온:케이)</b>와 함께해주셔서 감사해요!
        
        지금부터 몇 가지 질문을 통해 
        당신의 상황과 취향에 꼭 맞는 선물을 추천해드릴게요.
        
        먼저, <b>어떤 분께 드릴 선물</b>인지 알려주실 수 있을까요? 🌿"""
    
    add_message("assistant", welcome_msg)
    st.session_state.greeted = True
    return True


def handle_user_input():
    """사용자 입력 처리"""
    current_language = get_language()
    
    if current_language == "en":
        placeholder = "💬 Please enter your answer..."
    else:
        placeholder = "💬 답변을 입력해주세요..."
    
    user_input = st.chat_input(placeholder)
    if user_input:
        add_message("user", user_input)
        st.session_state.awaiting_gpt = True
        st.rerun()
        return True
    return False


def process_gpt_response():
    """GPT 응답 처리"""
    current_language = get_language()
    
    if current_language == "en":
        spinner_text = "Thinking of the next question based on your answer... 💭"
        error_msg = "Failed to extract user information. Please try again."
    else:
        spinner_text = "답변을 바탕으로 다음 질문을 고민 중이에요... 💭"
        error_msg = "사용자 정보 추출에 실패했어요. 다시 시도해주세요."
    
    with st.spinner(spinner_text):
        interview_prompt = get_system_prompt(current_language)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": interview_prompt}] + st.session_state.interview_history,
            temperature=0.7,
        )
        assistant_msg = response.choices[0].message.content

    st.session_state.awaiting_gpt = False

    # 언어에 따른 완료 키워드 확인
    completion_keywords = ["[인터뷰 완료]", "[Interview Complete]"]
    is_completed = any(keyword in assistant_msg for keyword in completion_keywords)

    if is_completed:
        try:
            start = assistant_msg.index("{")
            end = assistant_msg.rindex("}") + 1
            user_info = json.loads(assistant_msg[start:end])
            mark_interview_completed(user_info)
            return True
        except Exception as e:
            st.error(error_msg)
            return False
    else:
        add_message("assistant", assistant_msg)
        return False


def run_interview_flow():
    """인터뷰 전체 플로우 실행"""
    # 첫 인사 (브랜드 소개 이후 바로 표시)
    if not st.session_state.greeted:
        if show_welcome_message():
            st.rerun()

    # 사용자 입력 받기
    user_input = handle_user_input()
    
    if user_input:
        st.rerun()

    # GPT 응답 처리
    if st.session_state.awaiting_gpt:
        if process_gpt_response():
            st.rerun()
        else:
            st.rerun()
