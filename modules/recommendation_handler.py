"""
추천 처리 관련 함수들
"""
import streamlit as st
import json
from modules.chatflow_utils import run_chatflow, display_recommendations
from modules.session_manager import add_recommendation_set, mark_recommendations_completed, add_recommended_products, get_language


def generate_recommendations():
    """추천 생성 및 처리"""
    from modules.ui_components import display_recommendation_title, scroll_to_bottom
    
    current_language = get_language()
    
    if current_language == "en":
        spinner_text = "Recommending gifts that suit your situation... 🎁"
    else:
        spinner_text = "사용자 상황에 어울리는 선물을 추천 중이에요... 🎁"
    
    with st.spinner(spinner_text):
        result = run_chatflow(st.session_state.user_info)
        
        # 추천된 상품명들 추출하여 중복 방지 목록에 추가
        try:
            items = json.loads(result)
            product_names = [item.get('상품명', '') for item in items if item.get('상품명')]
            add_recommended_products(product_names)
            
            print(f"🎁 새로 추천된 상품들: {product_names}")
            print(f"📝 총 추천된 상품 수: {len(st.session_state.get('recommended_products', []))}")
            
        except json.JSONDecodeError:
            print("⚠️ 추천 결과 파싱 실패 - 상품명 추출 불가")
        
        # 추천 결과 저장 (누적)
        add_recommendation_set(result)
        mark_recommendations_completed()
        
        # 자동 스크롤
        scroll_to_bottom()
        
        return True


def display_all_recommendations():
    """모든 추천 결과 누적 출력"""
    from modules.ui_components import display_recommendation_title
    
    current_language = get_language()
    
    # 추천 결과가 있는지 확인
    if not hasattr(st.session_state, 'recommendation_sets') or not st.session_state.recommendation_sets:
        if current_language == "en":
            st.warning("No recommendation results available.")
        else:
            st.warning("추천 결과가 없습니다.")
        return
    
    # 모든 추천 세트를 순서대로 출력
    for i, rec in enumerate(st.session_state.recommendation_sets, start=1):
        # 첫 번째 추천에는 브랜드 소개와 구분하는 실선 추가
        if i == 1:
            st.markdown("---")
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        # 두 번째부터는 추천 간 구분선 추가
        elif i > 1:
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
        st.session_state["is_retry_mode"] = True  # 재추천 모드 표시
        # 기존 추천은 유지하고 새로운 추천만 추가되도록 함
        st.rerun()
    
    if restart_button:
        # 완전 초기화 (모든 추천 내역 삭제)
        reset_session()

