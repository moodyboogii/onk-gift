"""
ON:K - K-선물 추천 챗봇 메인 애플리케이션
"""
import os
import sys
import streamlit as st
from dotenv import load_dotenv
import openai

# 바이트코드 생성 비활성화
sys.dont_write_bytecode = True

# 안전한 모듈 임포트
try:
    from modules.ui_components import (
        setup_page_config, render_custom_styles, render_header, 
        render_brand_introduction, render_copyright
    )
    from modules.session_manager import initialize_session_state
except ImportError as e:
    st.error(f"모듈 임포트 오류: {e}")
    st.error("force_clean.py를 실행한 후 다시 시도해주세요.")
    st.stop()


def setup_environment():
    """환경 설정"""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            st.stop()
        openai.api_key = api_key
    except Exception as e:
        st.error(f"환경 설정 중 오류가 발생했습니다: {str(e)}")
        st.stop()


def render_chat_messages():
    """채팅 메시지들 렌더링"""
    try:
        from modules.ui_components import render_chat_bubble, scroll_to_bottom
        
        for msg in st.session_state.messages:
            if isinstance(msg["content"], str):
                render_chat_bubble(msg["role"], msg["content"])
        scroll_to_bottom()
    except Exception as e:
        st.error(f"채팅 메시지 렌더링 오류: {str(e)}")
        st.info("페이지를 새로고침해주세요.")


def main():
    """메인 애플리케이션 실행"""
    try:
        # 1. 환경 및 페이지 설정
        setup_environment()
        setup_page_config()
        render_custom_styles()
        render_header()
        
        # 2. 세션 상태 초기화
        initialize_session_state()
        
        # 3. 현재 상태 확인
        from modules.session_manager import is_interview_completed, is_recommendations_completed
        
        # 4. 브랜드 소개 표시 (항상 표시)
        if not is_interview_completed():
            # 인터뷰 미완료 시 - 시작 버튼 포함
            button_disabled = st.session_state.get('interview_started', False)
            start_clicked = render_brand_introduction(disabled=button_disabled)
            
            if start_clicked and not button_disabled:
                st.session_state.interview_started = True
                st.rerun()
        else:
            # 인터뷰 완료 후 - 시작 버튼 없이 브랜드 소개만 표시
            render_brand_introduction(disabled=True)
        
        # 5. 채팅 메시지 렌더링
        render_chat_messages()
        
        # 6. 플로우 처리
        _handle_flow_logic()
        
        # 7. 저작권 표시 (처음 방문 시 또는 추천 완료 후 표시)
        if not st.session_state.get('interview_started', False) or (is_interview_completed() and is_recommendations_completed()):
            render_copyright()
        
    except Exception as e:
        st.error("🚨 애플리케이션 실행 중 예상치 못한 오류가 발생했습니다.")
        st.error(f"오류 내용: {str(e)}")
        
        if st.button("🔄 페이지 새로고침"):
            st.rerun()


def _handle_flow_logic():
    """플로우 로직 처리 (내부 함수)"""
    try:
        from modules.session_manager import is_interview_completed, is_recommendations_completed
        
        if not is_interview_completed() and st.session_state.get('interview_started', False):
            # 인터뷰 단계
            try:
                from modules.interview_handler import run_interview_flow
                run_interview_flow()
            except ImportError as e:
                st.error(f"인터뷰 모듈 오류: {e}")
                st.error("force_clean.py를 실행해주세요.")
                return
            
        elif is_interview_completed() and not is_recommendations_completed():
            # 추천 생성 단계
            try:
                from modules.recommendation_handler import generate_recommendations
                if generate_recommendations():
                    st.rerun()
            except ImportError as e:
                st.error(f"추천 모듈 오류: {e}")
                st.error("force_clean.py를 실행해주세요.")
                return
                
        elif is_interview_completed() and is_recommendations_completed():
            # 추천 결과 표시 및 액션 처리 단계
            try:
                from modules.recommendation_handler import display_all_recommendations, handle_recommendation_actions
                
                display_all_recommendations()
                handle_recommendation_actions()
            except ImportError as e:
                st.error(f"추천 표시 모듈 오류: {e}")
                st.error("force_clean.py를 실행해주세요.")
                return
                
    except Exception as e:
        st.error(f"애플리케이션 실행 중 오류가 발생했습니다: {str(e)}")
        st.error("페이지를 새로고침하거나 force_clean.py를 실행해주세요.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 페이지 새로고침"):
                st.rerun()
        with col2:
            st.info("또는 force_clean.py 실행 후 재시작")


if __name__ == "__main__":
    main()
