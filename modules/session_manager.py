"""
세션 상태 관리 관련 함수들
"""
import streamlit as st


def initialize_session_state():
    """세션 상태 초기화"""
    default_values = {
        "messages": [],
        "interview_history": [],
        "interview_completed": False,
        "user_info": {},
        "greeted": False,
        "awaiting_gpt": False,
        "recommendation_sets": [],
        "recommend_count": 0,
        "completed": False
    }
    
    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_session():
    """세션 완전 초기화"""
    keys_to_reset = [
        "messages", "interview_history", "interview_completed",
        "user_info", "greeted", "completed", "interview_started",
        "recommendation_sets", "recommend_count", "awaiting_gpt"
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    # 초기화 후 재실행
    st.rerun()


def add_message(role, content):
    """메시지 추가"""
    st.session_state.messages.append({"role": role, "content": content})
    st.session_state.interview_history.append({"role": role, "content": content})


def is_interview_completed():
    """인터뷰 완료 상태 확인"""
    return st.session_state.interview_completed


def is_recommendations_completed():
    """추천 완료 상태 확인"""
    return st.session_state.get("completed", False)


def mark_interview_completed(user_info):
    """인터뷰 완료 처리"""
    st.session_state.interview_completed = True
    st.session_state.user_info = user_info


def mark_recommendations_completed():
    """추천 완료 처리"""
    st.session_state["completed"] = True


def add_recommendation_set(result):
    """추천 결과 세트 추가"""
    st.session_state.recommend_count += 1
    st.session_state.recommendation_sets.append(result)
