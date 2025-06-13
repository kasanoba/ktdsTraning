## 프로젝트 기획서: AI 기반 레거시 & 현대 개발 지원 에이전트 (금융권 특화)

### 1. 프로젝트 개요

- **추진배경**: 금융권중 정보계 서비스는 아직 COBOL로 되어 있는곳이 많고 언어전환 사업기회가 많음
- **목표**: 금융권 개발자들이 사용하는 레거시 코드(COBOL 등)를 Python/Java로 자동 변환하고, 현대 개발에서 반복되는 작업(문서화, 테스트 생성, 코드 리뷰 등)을 자동화하는 AI 에이전트를 개발한다.
- **형태**: 웹 기반 서비스 (Streamlit UI 사용)

---

### 2. 핵심 기능 요약

| 기능              | 설명                                     |
| --------------- | -------------------------------------- |
| COBOL 코드 자동 변환  | COBOL 코드를 Python 또는 Java로 변환           |
| 코드 설명 생성        | 기존 코드 또는 변환된 코드에 주석/자연어 설명 추가          |
| 테스트 코드 자동 생성    | 변환된 코드에 대한 단위 테스트 자동 생성 (예: pytest)    |
| 금융권 규정 검토 (RAG) | 규제 문서를 기반으로 보안, 로깅, 오류처리 등 검토          |
| 문서화 자동 생성       | 함수/클래스별 docstring 또는 Markdown 문서 자동 생성 |
| 자연어 질의응답        | "이 함수의 역할은?", "보안 문제가 있나?" 등 질의 대응     |

---

### 3. 아키텍처 (Azure 기반)

```plaintext
사용자 (Streamlit를 활용한 Web UI)
   ↓
FastAPI Backend (Azure App Service)
   ├─▶ Azure OpenAI (GPT-4 / GPT-4-turbo)
   └─▶ Azure Cognitive Search (금융권 문서 기반 RAG)
```

- **UI**: Streamlit (향후 필요시 React Web + API 연동)
- **Backend**: FastAPI (모듈화된 기능 API)
- **LLM**: Azure OpenAI GPT-4 (코드 변환, 설명, 질의응답)
- **RAG**: Azure AI Search + 금융권 개발 규정 문서

---

### 4. 사용자 흐름

1. 사용자가 COBOL 또는 Python 코드 입력(입력 방법은 화면에서 작성 또는 파일 업로드)
2. 시스템 처리:
   - COBOL → Python or JAVA 코드 자동 변환(선택에 따른)
   - 각 함수에 주석 및 설명 자동 추가
   - 테스트 코드 자동 생성
   - 금융권 가이드 문서 기반 규제 검토 (RAG)
3. 출력 결과 제공:
   - 변환된 코드
   - 설명 및 문서
   - 테스트 코드
   - 잠재적 규제 위반 사항 리포트

---

### 5. 초기 코드 스켈레톤

#### 디렉토리 구조(안)

```plaintext
project_root/
├── app/
│   ├── main.py           # FastAPI 진입점
│   ├── services/
│   │   ├── convert.py    # 코드 변환 로직 (LLM 호출)
│   │   ├── explain.py    # 코드 설명 생성
│   │   ├── testgen.py    # 테스트 코드 자동 생성
│   │   └── rag.py        # RAG 기반 규제 검토
├── ui/
│   └── streamlit_app.py  # 사용자 입력/출력 UI
├── docs/
│   └── finance_guides/   # 금융권 규정 문서 모음
├── requirements.txt
└── README.md
```

#### 예시 FastAPI Endpoint (`convert.py`)

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

### 6. 기술 스택

| 구성 요소    | 기술                                 |
| -------- | ---------------------------------- |
| 언어       | Python 3.10+                       |
| 모델 API   | Azure OpenAI GPT-4                 |
| 프레임워크    | FastAPI, Streamlit                 |
| 배포       | Azure App Service 또는 Container App |
| 검색 (RAG) | Azure Cognitive Search + 문서 인덱싱    |

---

### 7. 향후 확장 방향

- 사용자별 변환 히스토리 저장 (Azure Table 또는 Cosmos DB)
- 코드 실행 및 결과 시뮬레이션 기능 (코랩 통합 등)
- VS Code 확장 프로그램으로 기능 연동
- 다국어 문서 및 코드 주석 대응
- 정적 분석 도구 (SAST) 연계로 보안 품질 검토 강화

---

### 8. 최대 고려사항
- 금융권은 폐쇄망으로 구성되어 있어 해당 서비스를 어떤 형식으로 제공 가능한지 확인 필요
