
import os
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

# 🔧 환경 변수 로드 및 OpenAI 설정
load_dotenv()
openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model = os.getenv("CHAT_MODEL")

chat_client = AzureOpenAI(
    api_key=openai_api_key,
    azure_endpoint=openai_endpoint,
    api_version="2024-12-01-preview"
)

# treamlit UI 구성
st.set_page_config(page_title="COBOL Modernizer", layout="wide")
st.title("🛠️ COBOL Modernization Tool")

# 파일 업로드
uploaded_file = st.file_uploader("COBOL 파일을 업로드하세요", type=["cbl", "cob"])

# 변환 언어 선택
target_lang = st.radio("변환할 언어를 선택하세요", options=["Python", "Java"])

# 변환 옵션
keep_comments = st.checkbox("주석 유지", value=True)
modularize_code = st.checkbox("함수 구조 유지", value=True)

if uploaded_file:
    cobol_source = uploaded_file.read().decode("utf-8")

    system_msg = f"""
    너는 COBOL 전문가이자 {target_lang}로의 코드 변환 전문가야.
    사용자가 제공한 COBOL 코드를 {target_lang}로 변환해줘.
    {"주석은 유지해줘." if keep_comments else "주석은 제외해도 돼."}
    {"함수 단위로 모듈화해줘." if modularize_code else "전체를 한 파일로 변환해줘."}
    """

    prompt = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": cobol_source}
    ]

    if st.button("변환 실행"):
        with st.spinner("AI가 코드를 변환 중입니다..."):
            response = chat_client.chat.completions.create(
                model=chat_model,
                messages=prompt
            )
            result_code = response.choices[0].message.content
            st.code(result_code, language="python" if target_lang == "Python" else "java")
            st.download_button("📥 결과 다운로드", result_code, file_name=f"converted.{target_lang.lower()}")

# 추가 질문 기능
st.subheader("코드 관련 질문하기")
user_q = st.text_input("궁금한 점을 입력하세요")
if user_q and uploaded_file:
    explain_prompt = [
        {"role": "system", "content": "너는 COBOL 코드를 분석해서 자연어로 설명해주는 AI야."},
        {"role": "user", "content": f"아래 COBOL 코드를 설명해줘:\n{cobol_source}\n\n질문: {user_q}"}
    ]
    if st.button("설명 요청"):
        with st.spinner("AI가 설명을 작성 중입니다..."):
            explanation = chat_client.chat.completions.create(
                model=chat_model,
                messages=explain_prompt
            )
            st.success(explanation.choices[0].message.content)
