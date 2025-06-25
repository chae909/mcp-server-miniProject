# mcp-server-kosa

AI 기반 소득세 질의응답 및 문서 검색 시스템

## 소개

이 프로젝트는 LangChain, OpenAI, MCP(Multi-Chain Protocol) 등을 활용하여, 자연어로 소득세 관련 질문을 하면 관련 문서를 검색하고 답변을 생성하는 Python 기반 에이전트/서버 시스템입니다.

## 주요 기능

- `.docx` 문서(예: tax.docx)에서 세법 관련 정보를 추출 및 임베딩
- OpenAI LLM을 통한 자연어 질의응답
- MCP 기반 도구(tool) 등록 및 호출
- 스트리밍 방식의 응답 처리
- 다양한 클라이언트 예제 제공 (`mcp_client.py`, `mcp_client3.py`, `mcp_client4.py`)

## 실행 방법

### 서버 실행

```sh
python mcp_server.py
```

### 클라이언트 실행

- 기본 클라이언트:
  ```sh
  python mcp_client.py
  ```
- 스트리밍 클라이언트:
  ```sh
  python mcp_client3.py
  ```
- 고급 스트리밍 및 타이밍 출력 클라이언트:
  ```sh
  python mcp_client4.py
  ```

## 폴더 구조

- `mcp_server.py` : MCP 서버 및 도구 정의
- `mcp_client*.py` : 다양한 클라이언트 예제
- `tax.docx` : 세법 관련 문서
- `chroma-tax/` : Chroma 벡터스토어 데이터

## 참고

- [LangChain 공식 문서](https://python.langchain.com/)
- [OpenAI API 문서](https://platform.openai.com/docs/)
