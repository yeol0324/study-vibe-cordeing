import os
import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# 환경변수 로드
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Gemini LLM 프롬프트 템플릿
PROMPT_TEMPLATE = """
아래 상품명에 대해 인터넷에서 최저가를 찾아, 가격과 구매사이트 링크를 표로 정리해줘.
- 표 컬럼: 사이트명 | 가격 | 구매링크
- 3~5개 대표 쇼핑몰(네이버쇼핑, 11번가, G마켓 등) 위주로 찾아줘.
- 가격은 숫자만, 링크는 실제 구매페이지로.
- 예시:
| 사이트명 | 가격 | 구매링크 |
|---|---|---|
| 네이버쇼핑 | 12,900 | https://... |
| 11번가 | 13,200 | https://... |
| G마켓 | 13,500 | https://... |

상품명: {query}
"""

def crawl_naver_shopping(query):
    url = f"https://search.shopping.naver.com/search/all?query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = []
    for item in soup.select("div.product_info_area")[:1]:
        title = item.select_one("a.product_link__TrAac").get_text(strip=True)
        price = item.select_one("span.price_num__S2p_v").get_text(strip=True)
        link = item.select_one("a.product_link__TrAac")['href']
        items.append(("네이버쇼핑", price, link))
    return items

def crawl_11st(query):
    url = f"https://search.11st.co.kr/Search.tmall?kwd={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = []
    for item in soup.select("div.c_card_info")[:1]:
        title = item.select_one(".c_prd_name").get_text(strip=True)
        price = item.select_one(".c_prd_price strong").get_text(strip=True)
        link = item.select_one("a.c_prd_name")['href']
        if not link.startswith("http"): link = "https://www.11st.co.kr" + link
        items.append(("11번가", price, link))
    return items

def crawl_gmarket(query):
    url = f"https://browse.gmarket.co.kr/search?keyword={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = []
    for item in soup.select("div.box__item-container")[:1]:
        title = item.select_one("span.text__item").get_text(strip=True)
        price = item.select_one("strong.text__value").get_text(strip=True)
        link = item.select_one("a.link__item")['href']
        items.append(("G마켓", price, link))
    return items

# LLM + 크롤링 결합

def get_price_table(query):
    # 크롤링 데이터
    results = []
    try:
        results += crawl_naver_shopping(query)
    except Exception:
        pass
    try:
        results += crawl_11st(query)
    except Exception:
        pass
    try:
        results += crawl_gmarket(query)
    except Exception:
        pass
    # LLM 보정(크롤링 결과가 부족할 때)
    if len(results) < 2:
        prompt = PROMPT_TEMPLATE.format(query=query)
        response = model.generate_content(prompt)
        return response.text
    # 표 형태로 변환
    table = "| 사이트명 | 가격 | 구매링크 |\n|---|---|---|\n"
    for site, price, link in results:
        table += f"| {site} | {price} | {link} |\n"
    return table

# Streamlit UI
st.title("상품 최저가 검색 Agent (Gemini + 크롤링)")
query = st.text_input("상품명을 입력하세요:")

if query:
    with st.spinner("최저가 검색 중..."):
        result = get_price_table(query)
        st.markdown(result, unsafe_allow_html=True) 