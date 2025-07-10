"""
UI 컴포넌트 관련 함수들을 모아둔 모듈
"""
import streamlit as st
import re


def setup_page_config():
    """페이지 기본 설정"""
    st.set_page_config(
        page_title="ON:K | K‑선물 추천 챗봇",
        page_icon="🎁",
    )


def render_custom_styles():
    """커스텀 CSS 스타일 적용 - 심플하고 깔끔한 디자인"""
    st.markdown("""
        <style>
        /* 메인 컨테이너 패딩 조정 */
        .stMainBlockContainer,
        .block-container,
        .st-emotion-cache-1w723zb,
        .elbt1zu4 {
            padding-top: 3rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* 메인 타이틀 스타일 */
        .onk-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            line-height: 1.2;
            letter-spacing: -1px;
            color: #333;
            text-align: center;
        }
        
        /* 서브타이틀 스타일 */
        .onk-subtitle {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            margin-top: 0.2rem;
            line-height: 1.3;
            color: #333;
            text-align: center;
        }
        
        /* 채팅 말풍선 컨테이너 */
        .bubble-container {
            display: flex;
            margin: 15px 0;
            align-items: flex-end;
        }
        
        /* AI 어시스턴트 말풍선 - 심플한 디자인 */
        .bubble-assistant {
            background: #e9e5d3;
            color: #222;
            border-radius: 18px 18px 18px 4px;
            padding: 12px 16px;
            max-width: 70%;
            font-size: 1rem;
            margin-left: 8px;
        }
        
        /* 사용자 말풍선 - 심플한 디자인 */
        .bubble-user {
            background: #f1f2f6;
            color: #222;
            border-radius: 18px 18px 4px 18px;
            padding: 12px 16px;
            max-width: 70%;
            font-size: 1rem;
            margin-right: 8px;
        }
        
        /* 사용자 말풍선 컨테이너 */
        .bubble-container.user {
            flex-direction: row-reverse;
        }
        
        /* Primary 버튼 스타일 - 심플한 디자인 */
        .stButton > button[kind="primary"] {
            background-color: #a89660 !important;
            border: none !important;
            color: white !important;
            font-weight: 500 !important;
            padding: 0.6rem 1rem !important;
            border-radius: 0.5rem !important;
            min-height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 0.9rem !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #998550 !important;
            border: none !important;
            color: white !important;
        }
        .stButton > button[kind="primary"]:active {
            background-color: #8a7440 !important;
            border: none !important;
            color: white !important;
        }
        
        /* 일반 버튼 스타일 - 심플한 디자인 */
        .stButton > button:not([kind="primary"]),
        .stButton > button[data-testid="baseButton-secondary"],
        .stButton button {
            padding: 0.6rem 1rem !important;
            border-radius: 0.5rem !important;
            min-height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            border: 1px solid #ccc !important;
            background-color: #f8f9fa !important;
            color: #333 !important;
        }
        .stButton > button:not([kind="primary"]):hover,
        .stButton > button[data-testid="baseButton-secondary"]:hover,
        .stButton button:hover {
            background-color: #e9ecef !important;
            border-color: #adb5bd !important;
        }
        
        /* Disabled 버튼 스타일 */
        .stButton > button:disabled,
        .stButton > button[disabled] {
            padding: 0.6rem 1rem !important;
            border-radius: 0.5rem !important;
            min-height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 0.9rem !important;
            opacity: 0.6 !important;
        }
        
        /* 링크 버튼 스타일 - 심플한 디자인 */
        .stLinkButton > a {
            background-color: #f8f9fa !important;
            border: 1px solid #ccc !important;
            color: #333 !important;
            text-decoration: none !important;
            font-weight: 500 !important;
            padding: 0.6rem 1rem !important;
            border-radius: 0.5rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
            min-height: 40px !important;
            font-size: 0.9rem !important;
        }
        .stLinkButton > a:hover {
            background-color: #e9ecef !important;
            border-color: #adb5bd !important;
            color: #333 !important;
            text-decoration: none !important;
        }
        .stLinkButton > a:active {
            background-color: #dee2e6 !important;
            border-color: #adb5bd !important;
            color: #333 !important;
            text-decoration: none !important;
        }
        
        /* 모바일 반응형 스타일 */
        @media (max-width: 768px) {
            .stButton > button[kind="primary"] {
                padding: 0.7rem 1rem !important;
                font-size: 1rem !important;
                min-height: 44px !important;
            }
            
            .stButton > button:not([kind="primary"]),
            .stButton > button[data-testid="baseButton-secondary"],
            .stButton button,
            .stButton > button:disabled,
            .stButton > button[disabled] {
                padding: 0.7rem 1rem !important;
                font-size: 1rem !important;
                min-height: 44px !important;
            }
            
            .stLinkButton > a {
                padding: 0.7rem 1rem !important;
                font-size: 1rem !important;
                min-height: 44px !important;
            }
        }
        
        @media (max-width: 480px) {
            .stButton > button[kind="primary"] {
                padding: 0.65rem 0.8rem !important;
                font-size: 1rem !important;
                min-height: 42px !important;
            }
            
            .stButton > button:not([kind="primary"]),
            .stButton > button[data-testid="baseButton-secondary"],
            .stButton button,
            .stButton > button:disabled,
            .stButton > button[disabled] {
                padding: 0.65rem 0.8rem !important;
                font-size: 1rem !important;
                min-height: 42px !important;
            }
            
            .stLinkButton > a {
                padding: 0.65rem 0.8rem !important;
                font-size: 1rem !important;
                min-height: 42px !important;
            }
        }
        
        /* 강력한 버튼 통일 스타일 */
        div[data-testid="stButton"] > button,
        .stButton button,
        button[kind] {
            padding: 0.6rem 1rem !important;
            border-radius: 0.5rem !important;
            min-height: 40px !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-sizing: border-box !important;
        }
        
        /* Primary 버튼만 별도 색상 */
        div[data-testid="stButton"] > button[kind="primary"],
        .stButton button[kind="primary"] {
            background-color: #a89660 !important;
            border: none !important;
            color: white !important;
            font-weight: 500 !important;
        }
        
        div[data-testid="stButton"] > button[kind="primary"]:hover,
        .stButton button[kind="primary"]:hover {
            background-color: #998550 !important;
        }
        
        div[data-testid="stButton"] > button[kind="primary"]:active,
        .stButton button[kind="primary"]:active {
            background-color: #8a7440 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    """페이지 헤더 렌더링"""
    st.markdown('<div class="onk-title">ON:K | K‑선물 추천 챗봇</div>', unsafe_allow_html=True)
    st.markdown('<div class="onk-subtitle">한국의 아름다움을 담은 선물로, 온기를 켜다</div>', unsafe_allow_html=True)


def bold_markdown_to_html(text):
    """마크다운 bold를 HTML로 변환"""
    text = re.sub(r"\n", "<br>", text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def render_chat_bubble(role, content):
    """채팅 말풍선 렌더링"""
    html_content = bold_markdown_to_html(content)
    if role == "user":
        st.markdown(f'<div class="bubble-container user"><div class="bubble-user">{html_content}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-container"><div class="bubble-assistant">{html_content}</div></div>', unsafe_allow_html=True)


def scroll_to_bottom():
    """페이지 하단으로 스크롤 - 심플한 버전"""
    st.markdown("""
        <script>
            window.scrollTo(0, document.body.scrollHeight);
        </script>
    """, unsafe_allow_html=True)


def render_action_buttons():
    """하단 액션 버튼들 렌더링 - 업로드된 디자인 적용"""
    # 모바일에서도 잘 보이도록 레이아웃 개선
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        retry_button = st.button("🎁 한번 더 추천받기", use_container_width=True)
    
    with col2:
        restart_button = st.button("💬 처음부터 다시하기", use_container_width=True)
    
    with col3:
        st.link_button("K-헤리티지 스토어 방문하기", "https://khstore.or.kr/", use_container_width=True)
    
    return retry_button, restart_button


def display_recommendation_title(index=1):
    """추천 제목 표시"""
    if index == 1:
        title_msg = "💝 온:케이의 K-선물 추천 리스트"
    else:
        title_msg = f"💝 {index}번째 K-선물 리스트"
    
    st.markdown(f"<div style='font-size:1.8rem; font-weight:700; margin-top:1rem;'>{title_msg}</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


def render_brand_introduction(disabled=False):
    """브랜드 소개 및 시작 버튼 렌더링 - 업로드된 디자인 적용"""
    with st.container():
        # 헤리티지 이미지
        st.image("static/heritage_img.jpg", use_container_width=True)
        
        # 브랜드 소개 카드 - 업로드된 디자인 스타일 적용 (앵커 링크 제거)
        st.markdown(
            """
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-top: -5px;">
                <div style="color: #333; font-size: 20px; font-weight: bold; margin-top: 5px; margin-bottom: 10px;">❤️ 당신의 온기를 K-선물로 전해보세요</div>
                <p style="color: #555; font-size: 16px; margin-bottom: 5px;"><b>ON:K</b>(온:케이)는 <b>대화형 AI를 활용한 K-헤리티지 스토어 상품 추천 서비스</b>입니다.<br>
                전통과 현대가 어우러진 <b>한국 문화 상품 중에서 당신의 상황에 딱 맞는 특별한 선물</b>을 찾아드려요.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        # 버튼 표시 로직 - 심플화
        if not disabled and not st.session_state.get('interview_completed', False) and not st.session_state.get('interview_started', False):
            # 인터뷰 시작 전에만 버튼 표시
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                return st.button("🎁 선물 추천받기", use_container_width=True, type="primary")
        # 인터뷰 시작 후 또는 완료 후 - 버튼 없이 브랜드 소개만 표시
        return False


def render_copyright():
    """저작권 표시 렌더링"""
    st.markdown("""
        <div style="
            text-align: center; 
            color: #666; 
            font-size: 0.85rem; 
            margin-top: 2rem; 
            margin-bottom: 1rem; 
            padding: 1rem; 
            border-top: 1px solid #e9ecef;
        ">
            © 2025 ON:K | Yoonjeong Heo × K-헤리티지 스토어<br>
            <span style="font-size: 0.8rem; color: #888;">
                한국의 아름다운 전통문화 상품을 상황에 맞게 추천해주는 AI 챗봇
            </span>
        </div>
    """, unsafe_allow_html=True)
