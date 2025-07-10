"""
추천 처리 관련 함수들
"""
import streamlit as st
from modules.chatflow_utils import run_chatflow, display_recommendations
from modules.session_manager import add_recommendation_set, mark_recommendations_completed


def generate_recommendations():
    """추천 생성 및 처리"""
    from modules.ui_components import display_recommendation_title, scroll_to_bottom
    
    with st.spinner("사용자 상황에 어울리는 선물을 추천 중이에요... 🎁"):
        result = run_chatflow(st.session_state.user_info)
        
        # 추천 결과 저장 (누적)
        add_recommendation_set(result)
        mark_recommendations_completed()
        
        # 추천 완료 메시지
        current_count = len(st.session_state.recommendation_sets)
        if current_count > 1:
            st.success(f"🎉 {current_count}번째 추천이 완성되었어요!")
        else:
            st.success("🎉 추천이 완성되었어요!")
        
        # 자동 스크롤
        scroll_to_bottom()
        
        return True


def display_all_recommendations():
    """모든 추천 결과 누적 출력"""
    from modules.ui_components import display_recommendation_title
    
    # 추천 결과가 있는지 확인
    if not hasattr(st.session_state, 'recommendation_sets') or not st.session_state.recommendation_sets:
        st.warning("추천 결과가 없습니다.")
        return
    
    # 모든 추천 세트를 순서대로 출력
    for i, rec in enumerate(st.session_state.recommendation_sets, start=1):
        # 구분선 추가 (두 번째부터)
        if i > 1:
            st.markdown("---")
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        display_recommendation_title(i)
        display_recommendations(rec)
        
        # 각 추천 세트 사이에 여백 추가
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)


def handle_recommendation_actions():
    """추천 관련 액션 처리"""
    from modules.ui_components import render_action_buttons
    from modules.session_manager import reset_session
    
    retry_button, restart_button = render_action_buttons()
    
    if retry_button:
        # 새로운 추천을 받기 위해 completed 상태만 False로 변경
        # recommendation_sets는 유지하여 누적 표시
        st.session_state["completed"] = False
        # 기존 추천은 유지하고 새로운 추천만 추가되도록 함
        st.rerun()
    
    if restart_button:
        # 완전 초기화 (모든 추천 내역 삭제)
        reset_session()

