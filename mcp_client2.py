import subprocess
import json

# MCP 서버의 도구(tool)를 호출하는 함수
def call_mcp_tool(prompt: str):
    # MCP 서버를 서브프로세스로 실행 (mcp_server2.py를 실행)
    process = subprocess.Popen(
        ["python", "mcp_server2.py"],           
        stdin=subprocess.PIPE,           
        stdout=subprocess.PIPE,             
        stderr=subprocess.PIPE,            
        encoding='utf-8',                     
        bufsize=1               
    )

    # MCP 툴에 보낼 요청 형식 정의
    mcp_request = {
        "args": {
            "input": prompt    
        }
    }

    # JSON 문자열로 직렬화 후 개행 문자 추가
    json_str = json.dumps(mcp_request) + "\n"
    print("[DEBUG] 요청 JSON:", json_str.strip())

    # MCP 서버에 요청 전송
    process.stdin.write(json_str)
    process.stdin.flush()

    # MCP 서버 응답 수신 대기 루프
    while True:
        response_line = process.stdout.readline()  # 한 줄씩 읽기
        if not response_line:
            break
        response_line = response_line.strip()
        print("[DEBUG] 응답 원본:", response_line)
        try:
            # JSON 응답 파싱
            response = json.loads(response_line)
            print("[✅ 응답]:", response.get("result"))
            break
        except Exception:
            continue  # JSON 형식이 아니면 무시하고 계속 읽기

    # 서브프로세스 종료
    process.terminate()

# 테스트 실행
if __name__ == "__main__":
    call_mcp_tool("1+1=?")
