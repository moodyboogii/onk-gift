import pandas as pd
import random

def parse_price_krw(price_str):
    """한국어 원화 가격 문자열을 숫자로 변환"""
    if isinstance(price_str, (int, float)):
        return int(price_str)
    
    if isinstance(price_str, str):
        # 원화 기호(₩), '원', 쉼표, 공백 등 제거
        import re
        clean_str = re.sub(r"[₩,원,\s]", "", price_str)
        try:
            return int(clean_str)
        except ValueError:
            return 0
    return 0

def parse_price_usd(price_str):
    """영어 달러 가격 문자열을 숫자로 변환"""
    if isinstance(price_str, (int, float)):
        return float(price_str)
    
    if isinstance(price_str, str):
        # 달러 기호($), 쉼표, 공백 등 제거하되 소수점은 유지
        import re
        clean_str = re.sub(r"[\$,\s]", "", price_str)
        try:
            return float(clean_str)
        except ValueError:
            return 0.0
    return 0.0

def parse_price(price_str, language="ko"):
    """가격 문자열을 숫자형으로 변환 (언어별 처리) - 호환성 유지"""
    if language == "en":
        return parse_price_usd(price_str)
    else:
        return parse_price_krw(price_str)

def load_and_filter_products(price_min, price_max, language="ko", exclude_products=None, max_items=15):
    # 언어에 따라 다른 파일 선택
    if language == "en":
        filepath = "data/상품리스트_en.xlsx"
        price_col = "Price "  # 영어 파일은 뒤에 공백이 있음
        name_col = "Product Name"
        link_col = "Link"
        image_col = "Image"
    else:
        filepath = "data/상품리스트_kr.xlsx"
        price_col = "판매가"
        name_col = "상품명"
        link_col = "상품 링크"
        image_col = "상품 이미지"
    
    df = pd.read_excel(filepath)

    # 언어별 가격 처리
    if language == "en":
        # 달러 기호($), 쉼표 등 제거 후 float으로 변환
        df[price_col] = df[price_col].apply(parse_price_usd)
    else:
        # 원화 기호(₩), 쉼표 등 제거 후 int로 변환
        df[price_col] = df[price_col].apply(parse_price_krw)

    # 예산 범위에 해당하는 상품만 필터링
    filtered = df[(df[price_col] >= price_min) & (df[price_col] <= price_max)]
    
    # 이미 추천된 상품들 제외
    if exclude_products:
        filtered = filtered[~filtered[name_col].isin(exclude_products)]

    # 딕셔너리 목록으로 변환 - 표준 컬럼명으로 통일
    items = []
    for _, row in filtered.iterrows():
        item = {
            "상품명": row[name_col],
            "판매가": row[price_col],
            "상품 링크": row[link_col],
            "상품 이미지": row[image_col]
        }
        items.append(item)

    # 무작위로 최대 max_items개 추출 (갯수가 적으면 전체)
    return random.sample(items, min(len(items), max_items))

## 연습

if __name__ == "__main__":
    from data_utils import load_and_filter_products

    price_min, price_max = 50000, 70000
    products = load_and_filter_products(price_min, price_max)

    for p in products:
        print(f"{p['상품명']} - {p['판매가']} - {p['상품 링크']} - {p['상품 이미지']}")
