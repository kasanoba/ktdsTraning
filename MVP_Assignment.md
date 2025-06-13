
# 프로젝트 기획서  
## AI 기반 레거시 & 현대 개발 지원 에이전트 (금융권 특화)

---

### 1. 프로젝트 개요

- **추진 배경**  
  금융권 정보계 시스템의 상당 부분이 여전히 **COBOL**로 구성되어 있으며, 이를 현대 언어로 전환하는 **레거시 마이그레이션** 수요가 존재. 동시에, 현대 개발자들이 반복적으로 수행하는 테스트 작성, 문서화 등의 작업을 자동화할 수 있는 **AI 지원 시스템의 필요성** 증가.

- **목표**  
  금융권 개발자들이 사용하는 레거시 코드(COBOL 등)를 Python/Java로 자동 변환하고, 현대 개발 과정에서 반복되는 작업(문서화, 테스트 생성, 코드 리뷰 등)을 자동화하는 AI 기반 개발 지원 에이전트 구축.

- **형태**  
  웹 기반 서비스 (초기: Streamlit UI → 향후 React + API 확장 가능)

---

### 2. 핵심 기능 요약

| 기능                    | 설명 |
|------------------------|------|
| COBOL 코드 자동 변환    | COBOL 코드를 Python 또는 Java로 변환 |
| 코드 설명 생성          | 주요 로직 및 함수에 주석/자연어 설명 추가 |
| 테스트 코드 자동 생성   | `pytest` 또는 `unittest` 기반 테스트 코드 자동 생성 |
| 금융권 규정 검토 (RAG)  | 보안, 로깅, 오류처리 등 금융권 규제 기준 기반 검토 |
| 문서화 자동 생성        | 함수/클래스별 `docstring` 또는 Markdown 문서 생성 |
| 자연어 질의응답         | "이 함수의 역할은?", "보안 문제 있나?" 등 질문에 응답 |

---

### 3. 시스템 아키텍처 (Azure 기반)

```
[사용자] ─▶ [Streamlit Web UI]
               │
               ▼
     [FastAPI Backend - Azure App Service]
               ├──▶ [Azure OpenAI GPT-4]
               └──▶ [Azure Cognitive Search (RAG)]
```

- **UI**: Streamlit (간단한 MVP UI, 추후 React로 확장 가능)
- **Backend**: FastAPI (모듈화된 API 설계)
- **LLM 서비스**: Azure OpenAI GPT-4 (코드 처리 및 질의응답)
- **RAG 구성**: Azure Cognitive Search + 금융권 규제 문서

---

### 4. 사용자 흐름

1. 사용자가 Streamlit UI를 통해 COBOL 또는 Python 코드 입력 (직접 입력 or 파일 업로드)
2. 시스템 처리 단계:
   - 선택에 따라 COBOL → Python 또는 Java 변환
   - 주석 및 설명 자동 생성
   - 테스트 코드 자동 생성
   - 금융권 규정 기반 자동 검토 (RAG)
3. 사용자에게 출력 제공:
   - 변환된 코드
   - 설명 및 문서화 결과
   - 테스트 코드
   - 규제 위반 가능성 리포트

---

### 5. 초기 디렉토리 스켈레톤

```
project_root/
├── app/
│   ├── main.py            # FastAPI 진입점
│   ├── services/
│   │   ├── convert.py     # 코드 변환 (GPT 호출)
│   │   ├── explain.py     # 주석 및 설명 생성
│   │   ├── testgen.py     # 테스트 코드 생성
│   │   └── rag.py         # RAG 기반 규정 검토
├── ui/
│   └── streamlit_app.py   # 사용자 인터페이스
├── docs/
│   └── finance_guides/    # 금융권 규제 문서
├── utils/
│   └── llm.py             # GPT 호출 유틸
├── config/
│   └── settings.py        # 환경변수/설정 관리
├── tests/
│   └── test_convert.py    # 기능별 테스트
├── requirements.txt
└── README.md
```

---

### 6. FastAPI 예시 (convert.py)

```python
from fastapi import APIRouter, Request
from utils.llm import call_openai

router = APIRouter()

@router.post("/convert")
async def convert_code(request: Request):
    data = await request.json()
    cobol_code = data.get("code")
    prompt = f"""
    아래 COBOL 코드를 Python으로 변환하고, 주요 로직마다 주석을 추가해 주세요:

{cobol_code}
    """
    result = call_openai(prompt)
    return {"converted_code": result}
```

---

### 7. 기술 스택 요약

| 구성 요소 | 기술 |
|-----------|------|
| 언어 | Python 3.10+ |
| 웹 프레임워크 | FastAPI, Streamlit |
| 모델 API | Azure OpenAI GPT-4 (또는 turbo) |
| 배포 | Azure App Service, Container Apps |
| 검색 기반 QA (RAG) | Azure Cognitive Search |
| 문서 저장 | Azure Blob, Table, 또는 Cosmos DB |

> 추가 도구: pytest, httpx, pydantic, python-dotenv 등

---

### 8. 향후 확장 방향

- 사용자별 히스토리 저장 (Azure Table/Cosmos DB 활용)
- 코드 실행 시뮬레이터 통합 (예: Google Colab, Docker sandbox)
- VS Code 확장 프로그램으로 기능 연동
- 다국어 문서 및 코드 주석 자동 번역
- 정적 분석 도구(SAST) 연계로 보안 품질 검토 강화
- LLM 프롬프트 성능 개선 및 학습 자동화 (Prompt Flow or LangChain)

---

### 9. 최대 고려사항

> **금융권 폐쇄망/내부망 환경을 고려한 서비스 전달 방식 필요**

- LLM API 호출이 불가한 환경에서는:
  - LLM 사내 배포 필요 (Azure Stack 기반 GPT-4)
  - 또는 에이전트 기능을 오프라인 인퍼런스 가능한 형태로 재설계
- On-Prem 배포 또는 컨테이너 패키지로 납품 구조 필요
