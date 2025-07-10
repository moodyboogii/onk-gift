import pandas as pd
import random

def parse_price(price_str):
    """₩12,000 같은 문자열을 숫자형 가격으로 변환"""
    if isinstance(price_str, str):
        return int(''.join(filter(str.isdigit, price_str)))
    return price_str

def load_and_filter_products(price_min, price_max, filepath="data/상품리스트_kr.xlsx", max_items=15):
    df = pd.read_excel(filepath)

    # 원화 기호(₩), 쉼표 등 제거 후 숫자형으로 변환
    df["판매가"] = df["판매가"].replace("[₩,원,\s,\,]", "", regex=True).astype(int)

    # 예산 범위에 해당하는 상품만 필터링
    filtered = df[(df["판매가"] >= price_min) & (df["판매가"] <= price_max)]

    # 딕셔너리 목록으로 변환
    items = filtered.to_dict("records")

    # 무작위로 최대 max_items개 추출 (갯수가 적으면 전체)
    return random.sample(items, min(len(items), max_items))

## 연습

if __name__ == "__main__":
    from data_utils import load_and_filter_products

    price_min, price_max = 50000, 70000
    products = load_and_filter_products(price_min, price_max)

    for p in products:
        print(f"{p['상품명']} - {p['판매가']} - {p['상품 링크']} - {p['상품 이미지']}")
