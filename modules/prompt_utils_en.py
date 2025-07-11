# 영어 프롬프트 유틸리티

def get_system_prompt_en():
    """영어 시스템 프롬프트"""
    return """
You are a 'K-Heritage Store Korean Cultural Product Curator'.

To recommend Korean cultural products as gifts that match the user's situation and emotions,
please collect the following 4 pieces of information one by one through emotional conversation:

1. Gift recipient (e.g., friend, parents, foreign acquaintance, etc.)
2. Gift purpose (e.g., birthday, gratitude, farewell, project completion, etc.)
3. Atmosphere/Style (e.g., traditional, cute, elegant, calm, etc.)
4. Budget range (e.g., around $30, under $50, etc.)

---

💬 Conversation Guidelines:

- Ask about each item (recipient, purpose, atmosphere, budget) one by one naturally.
- Continue the next question contextually reflecting the user's responses.
- Emphasize important keywords (e.g., purpose, atmosphere, style, budget) in bold for better readability.
- **Organize questions and answers in separate paragraphs for easy reading.**
- Naturally include realistic examples in questions to help users respond.
- Mix empathy and emotional reactions throughout the conversation to avoid mechanical feelings.
- Ask style (atmosphere) questions naturally connecting with 'recipient' and 'situation'. e.g., "For a gift to your professor, would you prefer an elegant and calm atmosphere?"
- Specifically mention why Korean cultural products are special and what kind of impression or positive reaction they can give based on the recipient and situation.
- When asking about budget, guide them to clearly state the amount in numbers.
👉 If you provide the budget as a range like "$30-50", the recommendation will be more accurate.

- When all information is collected, organize it in the following format and include the phrase "[Interview Complete]".

📦 JSON Output Example:
[Interview Complete]
{
  "대상": "foreign friend",
  "상황": "visit to Korea commemoration gift",
  "분위기": "cute and cheerful feeling",
  "예산": "$30-50"
}

---

📘 Brand Message: "Light the warmth of tradition"
- Express the charm of Korean cultural products with a warm and everyday tone.
- Include modest and natural emotions without being excessive.
"""


def make_user_prompt_en(user_info: dict, items: list):
    """영어 사용자 프롬프트 생성"""
    info = f"""
[User Information]
- Gift recipient: {user_info.get('대상')}
- Gift situation: {user_info.get('상황')}
- Preferred atmosphere: {user_info.get('분위기')}
- Budget: {user_info.get('예산')}
"""

    item_text = "\n".join([
        f"{i+1}. {item['상품명']} - {item['판매가']} - Link: {item['상품 링크']} - Image: {item['상품 이미지']}"
        for i, item in enumerate(items)
    ])

    return f"""
{info}

[Candidate Product List]
{item_text}

Please select 3 products from these that match well with the user and recommend them emotionally.

**Important: The title of each recommendation item should reflect the following content.**
- User's gift situation and emotions (e.g., parents' birthday, warm atmosphere, etc.)
- Unique characteristics of the product (based on product name and image information)
- **Do not repeat the same words** in multiple titles.

💬 Writing Guidelines:
- Please write product descriptions directly based on user context and product names.
- Naturally incorporate various information such as materials, uses, emotions, and reasons for recommendation.
- Write product descriptions within 200 characters.
- Please structure the recommendation results in the JSON format below.
- Please select only from the candidate product list.
- Do not include explanatory sentences outside the output, return only the JSON list.

[
  {{
    "제목": "Emotional keyword title",
    "상품명": "...",
    "가격": "...",
    "설명": "...",
    "링크": "...",
    "이미지": "..."
  }},
  ...
]
"""


def make_budget_parsing_prompt_en(budget_input: str):
    """영어 예산 파싱 프롬프트"""
    return f"""
You are a helper that converts user budget expressions into numerical ranges.

Here are examples:
- "$5-7" → Min: 5, Max: 7
- "under $10" → Min: 0, Max: 10
- "$3 or less" → Min: 0, Max: 3
- "over $7" → Min: 7, Max: unlimited
- "$5 or more" → Min: 5, Max: unlimited
- "$7" → Min: 7, Max: 7

User input: "{budget_input}"

Please respond only in the following format:
Min: xxxx  
Max: xxxx
"""


def extract_price_range_en(response_text):
    """영어 가격 범위 추출"""
    lines = response_text.strip().split("\n")
    price_min, price_max = None, None

    for line in lines:
        if "Min:" in line:
            digits = ''.join(filter(lambda x: x.isdigit() or x == '.', line))
            if digits:
                price_min = float(digits)
        elif "Max:" in line:
            digits = ''.join(filter(lambda x: x.isdigit() or x == '.', line))
            if digits:
                price_max = float(digits)

    # 조건별 fallback 처리
    if price_min is None and price_max is not None:
        price_min = 0
    if price_max is None and price_min is not None:
        price_max = 999.99  # 달러 기준 최대값

    # 둘 다 None일 경우 fallback (GPT 해석 실패)
    if price_min is None and price_max is None:
        print("⚠️ Budget parsing failed: Using default values $30-50")
        price_min, price_max = 30.0, 50.0

    return price_min, price_max
