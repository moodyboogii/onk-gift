import streamlit as st
import openai
import json
import random

# 임포트 에러 방지를 위한 안전한 임포트
try:
    from modules.prompt_utils import (
        get_system_prompt,
        make_user_prompt,
        make_budget_parsing_prompt,
        extract_price_range
    )
    from modules.data_utils import load_and_filter_products
except ImportError as e:
    st.error(f"모듈 임포트 오류: {e}")
    st.stop()


# ✅ 1. GPT 추천 실행 함수
def run_chatflow(user_info):
    # 이미 추천된 상품들 가져오기
    from modules.session_manager import get_recommended_products, get_language
    exclude_products = get_recommended_products()
    current_language = get_language()
    
    # 1️⃣ 예산 범위 파싱 (언어별)
    budget_prompt = make_budget_parsing_prompt(user_info["예산"], current_language)
    budget_result = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": budget_prompt}]
    )
    budget_response_text = budget_result.choices[0].message.content
    price_min, price_max = extract_price_range(budget_response_text, current_language)

    # 2️⃣ 필터링된 상품 목록 불러오기 (언어별 엑셀 파일) - 중복 제외
    filtered_items = load_and_filter_products(price_min, price_max, language=current_language, exclude_products=exclude_products)
    
    # 상품 수가 부족한 경우 처리
    if len(filtered_items) < 3:  # 최소 3개 상품이 필요하다고 가정
        if current_language == "en":
            st.warning("⚠️ There are insufficient new recommendation products in this budget range. Please refer to existing recommendations.")
            # 제외 목록 없이 다시 시도
            filtered_items = load_and_filter_products(price_min, price_max, language=current_language, exclude_products=None)
            st.info("💡 We've recommended again targeting all products.")
        else:
            st.warning("⚠️ 해당 예산 범위에서 새로운 추천 상품이 부족합니다. 기존 추천을 참고해주세요.")
            # 제외 목록 없이 다시 시도
            filtered_items = load_and_filter_products(price_min, price_max, language=current_language, exclude_products=None)
            st.info("💡 모든 상품을 대상으로 다시 추천해드렸습니다.")

    # ✅ 진단용 로그
    print(f"🌐 현재 언어: {current_language}")
    print(f"🔍 예산 범위: {price_min} ~ {price_max}")
    print(f"🚫 제외할 상품 수: {len(exclude_products)}")
    print(f"📦 상품 개수 (필터링 후): {len(filtered_items)}")
    for i, p in enumerate(filtered_items, 1):
        print(f"{i}. {p['상품명']} | {p['판매가']} | {p['상품 링크']}")

    # 3️⃣ GPT에 전달할 프롬프트 생성 (언어별)
    messages = [
        {"role": "system", "content": get_system_prompt(current_language)},
        {"role": "user", "content": make_user_prompt(user_info, filtered_items, current_language)}
    ]

    # 4️⃣ GPT 추천 요청
    chat_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    response_text = chat_response.choices[0].message.content.strip()

    # ✅ 코드블럭 제거
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").strip()
    if response_text.endswith("```"):
        response_text = response_text[:-3].strip()

    return response_text

# ✅ 2. 추천 결과 카드로 보여주기
import streamlit as st
import json
import random

def display_recommendations(gpt_response: str):
    from modules.session_manager import get_language
    current_language = get_language()
    
    try:
        items = json.loads(gpt_response)
    except json.JSONDecodeError:
        print("[GPT 응답 파싱 에러] 원본 응답:")
        print(gpt_response)
        if current_language == "en":
            st.error("There was a problem loading the recommendation results. Please try again! (Admin: Check the original response in the console)")
        else:
            st.error("추천 결과를 불러오는 데 문제가 발생했어요. 다시 시도해 주세요! (관리자: 콘솔에서 원본 응답을 확인하세요)")
        return

    # 언어별 텍스트 설정
    if current_language == "en":
        price_label = "Price: "
        button_text = "View Product"
    else:
        price_label = "가격: "
        button_text = "상품 보러가기"

    # 아이콘 목록 (랜덤 선택용)
    icons = ["🎁", "✨", "🪄", "🎉", "🌟", "💝", "🧧"]

    # 모바일 대응 카드 스타일 - 심플하고 깔끔한 디자인
    st.markdown("""
        <style>
        .recommendation-card {
            background: white;
            border-radius: 8px;
            border: 1px solid #ddd;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .card-content {
            display: flex;
            flex-direction: row;
            gap: 20px;
            align-items: stretch;
            padding: 20px;
            max-width: 100%;
            width: 100%;
            box-sizing: border-box;
            min-height: 320px;
        }
        .card-text {
            flex: 1 1 0%;
            min-width: 0;
            width: 100%;
            word-break: keep-all;
            white-space: normal;
            line-height: 1.6;
            font-size: 1.05rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 8px;
        }
        .card-text-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .card-text > div {
            display: block;
        }
        .product-image {
            border-radius: 6px;
            width: 280px;
            height: 280px;
            object-fit: contain;
            display: block;
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            flex-shrink: 0;
        }
        /* 상품 카드 내 버튼 스타일 - 심플한 디자인 */
        .product-link-button {
            background-color: #a89660 !important;
            border: none !important;
            color: white !important;
            text-decoration: none !important;
            font-weight: 400 !important;
            padding: 0.7rem 1rem !important;
            border-radius: 0.5rem !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            min-height: 44px !important;
            cursor: pointer !important;
            font-size: 1rem !important;
            width: 100% !important;
            box-sizing: border-box !important;
            margin-top: auto !important;
        }
        .product-link-button:hover {
            background-color: #998550 !important;
            color: white !important;
        }
        .product-link-button:active {
            background-color: #8a7440 !important;
            color: white !important;
        }
        @media (max-width: 600px) {
            .card-content {
                flex-direction: column;
                align-items: stretch;
                gap: 15px;
                min-height: auto;
            }
            .product-image {
                width: 100%;
                max-width: 300px;
                height: auto;
                margin: 0 auto;
            }
            .card-text {
                justify-content: flex-start;
            }
            .product-link-button {
                padding: 0.7rem 1rem !important;
                font-size: 1rem !important;
                min-height: 44px !important;
            }
        }
        @media (max-width: 480px) {
            .product-link-button {
                padding: 0.65rem 0.8rem !important;
                font-size: 1rem !important;
                min-height: 42px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    for idx, item in enumerate(items, start=1):
        with st.container():
            icon = random.choice(icons)

            # 언어별 가격 표시 처리
            raw_price = item["가격"]
            try:
                if current_language == "en":
                    # 달러 표시
                    price_number = float(str(raw_price).replace("$", "").replace(",", "").strip())
                    price = f"${price_number:.2f}"
                else:
                    # 원화 표시 (천 단위 쉼표 + '원' 붙이기)
                    price_number = int(str(raw_price).replace("원", "").replace(",", "").strip())
                    price = f"{price_number:,}원"
            except ValueError:
                if current_language == "en":
                    price = raw_price if "$" in str(raw_price) else f"${raw_price}"
                else:
                    price = raw_price if "원" in str(raw_price) else f"{raw_price}원"

            st.markdown(f"""
            <div class="recommendation-card">
                <div style="padding: 15px 20px 15px; background: #f8f9fa; border-bottom: 1px solid #e9ecef;">
                    <div style="margin: 0; color: #333; font-size: 1.2rem; font-weight: 600; line-height: 1.5;">
                        {idx}. {item['제목']}
                    </div>
                </div>
                <div class="card-content">
                    <img src="{item['이미지']}" class="product-image" alt="상품 이미지" />
                    <div class="card-text">
                        <div class="card-text-content">
                            <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 8px;">
                                🎁 {item['상품명']}
                            </div>
                            <div style="font-size: 1.1rem; color: #333; font-weight: 600; margin-bottom: 8px;">
                                {price_label}{price}
                            </div>
                            <div style="color: #666; line-height: 1.6; margin-bottom: 15px;">
                                ✨ {item['설명']}
                            </div>
                        </div>
                        <div>
                            <a href="{item['링크']}" target="_blank" style="text-decoration: none;">
                                <button class="product-link-button">
                                    {button_text}
                                </button>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


