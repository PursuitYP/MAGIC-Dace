# minimal_test_after_restart.py
import requests
import json
import time

def wait_for_service(max_wait=180):
    """等待服务重启"""
    print("Waiting for service to restart...")
    for i in range(max_wait // 5):
        try:
            resp = requests.get(
                "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/health",
                timeout=5
            )
            if resp.status_code == 200:
                print(f"✓ Service is UP after {i*5} seconds")
                return True
        except:
            pass
        
        if (i+1) % 6 == 0:  # 每30秒打印一次
            print(f"  Still waiting... {(i+1)*5}s")
        time.sleep(5)
    
    print("✗ Service did not start in time")
    return False

def test_minimal_api():
    """测试最简API调用"""
    url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions"
    
    # 测试1：极简请求
    test_cases = [
        {
            "name": "1. 极简用户消息",
            "data": {
                "model": "orm",
                "temperature": 0.1,
                "max_tokens": 10,
                "stream": False,
                "messages": [{"role": "user", "content": "ping"}]
            }
        },
        {
            "name": "2. 短系统+短用户",
            "data": {
                "model": "orm",
                "temperature": 0.1,
                "max_tokens": 10,
                "stream": False,
                "messages": [
                    {"role": "system", "content": "Help."},  # 4 chars
                    {"role": "user", "content": "Say OK"}
                ]
            }
        },
        {
            "name": "3. 流式极简请求",
            "data": {
                "model": "orm",
                "temperature": 0.1,
                "max_tokens": 10,
                "stream": True,  # 流式
                "messages": [{"role": "user", "content": "test"}]
            }
        }
    ]
    
    headers = {
        "Authorization": "Bearer FAKE_API_KEY",
        "Content-Type": "application/json"
    }
    
    for test in test_cases:
        print(f"\n{test['name']}")
        
        try:
            if test["data"]["stream"]:
                resp = requests.post(url, headers=headers, json=test["data"], timeout=30, stream=True)
                if resp.status_code == 200:
                    print("  ✓ Streaming request sent successfully")
                    # 简单读取流
                    for line in resp.iter_lines():
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                if line_str[6:] == '[DONE]':
                                    break
                                print(f"  Received chunk")
                    print("  ✓ Streaming completed")
                else:
                    print(f"  ✗ Status: {resp.status_code}")
            else:
                resp = requests.post(url, headers=headers, json=test["data"], timeout=30)
                print(f"  Status: {resp.status_code}")
                if resp.status_code == 200:
                    result = resp.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"  ✓ Response: {content}")
                else:
                    print(f"  ✗ Error: {resp.text[:100]}")
                    
        except Exception as e:
            print(f"  ✗ Exception: {e}")

if __name__ == "__main__":
    print("Service Recovery Test")
    print("="*60)
    
    if wait_for_service():
        print("\nService is ready. Testing minimal API calls...")
        test_minimal_api()
    else:
        print("\nService is not available. Need manual restart.")
