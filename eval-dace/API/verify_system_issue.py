# verify_system_issue.py
import requests
import json
import time

def test_different_formats():
    """测试不同消息格式"""
    url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions"
    headers = {"Authorization": "Bearer FAKE_API_KEY", "Content-Type": "application/json"}
    
    test_cases = [
        {
            "name": "1. 只有user消息",
            "messages": [{"role": "user", "content": "Hello"}],
            "expected": "应该成功"
        },
        {
            "name": "2. system + user消息",
            "messages": [
                {"role": "system", "content": "You are helpful."},
                {"role": "user", "content": "Hello"}
            ],
            "expected": "可能失败"
        },
        {
            "name": "3. 多个user消息（对话历史）",
            "messages": [
                {"role": "user", "content": "Previous question"},
                {"role": "assistant", "content": "Previous answer"},
                {"role": "user", "content": "New question"}
            ],
            "expected": "应该成功"
        },
        {
            "name": "4. 将system内容放在user消息中",
            "messages": [
                {"role": "user", "content": "System: You are helpful. User: Hello"}
            ],
            "expected": "应该成功"
        }
    ]
    
    for test in test_cases:
        print(f"\n{test['name']} - {test['expected']}")
        
        data = {
            "model": "orm",
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 50,
            "messages": test["messages"]
        }
        
        try:
            start = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            elapsed = time.time() - start
            
            print(f"  Status: {response.status_code}, Time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"  ✓ Success: {content[:50]}...")
            else:
                print(f"  ✗ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def test_model_capabilities():
    """测试模型能力端点"""
    print("\n" + "="*60)
    print("Testing model capabilities...")
    
    try:
        # 查看模型信息
        models_url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/models"
        response = requests.get(models_url, timeout=10)
        print(f"Models endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Models endpoint error: {e}")

if __name__ == "__main__":
    print("验证系统角色问题")
    print("="*60)
    
    # 先等待服务稳定
    print("等待5秒确保服务稳定...")
    time.sleep(5)
    
    test_different_formats()
    test_model_capabilities()
