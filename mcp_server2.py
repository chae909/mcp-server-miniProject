from mcp.server.fastmcp import FastMCP
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests
import sys
import json

# Ollama LLM을 LangChain의 LLM 인터페이스에 맞게 구현한 클래스
class OllamaLLM(LLM):
    model: str = "llama3.2:latest"
    base_url: str = "http://192.168.2.6:11434"

    # LangChain에서 LLM 호출 시 사용하는 내부 메서드
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        print(f"[MCP 서버] OllamaLLM _call 호출됨, prompt: {prompt}", flush=True)
        url = f"{self.base_url}/api/generate"  # Ollama 요청 엔드포인트
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            # POST 요청을 통해 모델 응답 받기
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "[응답 없음]")
        except Exception as e:
            # 오류 발생 시 로그 출력 및 메시지 반환
            print("[OllamaLLM 오류]", e, flush=True)
            return f"[오류 발생]: {e}"

    # LangChain에서 사용할 LLM 타입 이름 정의
    @property
    def _llm_type(self) -> str:
        return "ollama"

    # 모델 식별을 위한 파라미터 반환
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model}

# MCP 서버 인스턴스 생성 및 커스텀 LLM 설정
mcp = FastMCP("Ollama MCP")
mcp.llm = OllamaLLM()

# MCP 도구 정의: 기본 LLM 호출 도구
@mcp.tool(name="llm", description="기본 LLM 호출 도구")
def call_llm(input: str) -> str:
    return mcp.llm._call(input)

# MCP 도구 정의
@mcp.tool()
def add(a: int, b: int) -> int:
    print("[MCP 서버] add 함수 호출됨", flush=True)
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b





if __name__ == "__main__":
    print("[MCP 서버] stdio 모드 실행 중...", flush=True)

    # stdin에서 요청을 받아 처리하는 루프
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            args = req.get("args", {})
            # 입력 파라미터에 따라 도구 호출 분기 처리
            if "input" in args:
                result = call_llm(args["input"])  # LLM 호출
            elif "a" in args and "b" in args:
                result = add(args["a"], args["b"])  # 덧셈 호출
            else:
                result = "[❗잘못된 요청]"
            resp = {"result": result}
        except Exception as e:
            # 예외 발생 시 오류 메시지 반환
            resp = {"result": f"[❌ 서버 오류]: {e}"}
        # 결과를 JSON 형태로 stdout에 출력
        print(json.dumps(resp), flush=True)

    # stdio 기반 MCP 서버 실행 (위 루프 이후에 추가 실행됨)
    print("[MCP 서버] stdio 모드 실행 중...", flush=True)
    mcp.run(transport="stdio")
