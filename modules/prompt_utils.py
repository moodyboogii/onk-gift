# 통합 프롬프트 유틸리티 - 언어별 분기 처리

from modules.prompt_utils_ko import (
    get_system_prompt_ko, 
    make_user_prompt_ko, 
    make_budget_parsing_prompt_ko, 
    extract_price_range_ko
)
from modules.prompt_utils_en import (
    get_system_prompt_en, 
    make_user_prompt_en, 
    make_budget_parsing_prompt_en, 
    extract_price_range_en
)


def get_system_prompt(language="ko"):
    """언어에 따른 시스템 프롬프트 반환"""
    if language == "en":
        return get_system_prompt_en()
    else:
        return get_system_prompt_ko()


def make_user_prompt(user_info: dict, items: list, language="ko"):
    """언어에 따른 사용자 프롬프트 생성"""
    if language == "en":
        return make_user_prompt_en(user_info, items)
    else:
        return make_user_prompt_ko(user_info, items)


def make_budget_parsing_prompt(budget_input: str, language="ko"):
    """언어에 따른 예산 파싱 프롬프트 생성"""
    if language == "en":
        return make_budget_parsing_prompt_en(budget_input)
    else:
        return make_budget_parsing_prompt_ko(budget_input)


def extract_price_range(response_text, language="ko"):
    """언어에 따른 가격 범위 추출"""
    if language == "en":
        return extract_price_range_en(response_text)
    else:
        return extract_price_range_ko(response_text)
