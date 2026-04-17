# test_system_length_issue.py
import requests
import json
import time

def test_system_length_impact():
    """测试系统提示长度对API的影响"""
    url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions"
    headers = {"Authorization": "Bearer FAKE_API_KEY", "Content-Type": "application/json"}
    
    # 测试不同长度的系统提示
    test_lengths = [
        {"length": 10, "content": "A" * 10},  # 10字符
        {"length": 50, "content": "You are a helpful assistant. " * 2},  # 50字符
        {"length": 100, "content": "You are a helpful assistant. " * 4},  # 100字符
        {"length": 111, "content": "You are a helpful red teaming assistant used by developers to generate diverse and complex adversarial prompts."},  # 111字符（失败的长度）
        {"length": 200, "content": "You are a helpful assistant. " * 8},  # 200字符
        {"length": 500, "content": "You are a helpful assistant. " * 20},  # 500字符
    ]
    
    for test in test_lengths:
        print(f"\nTesting system prompt length: {test['length']} chars")
        
        data = {
            "model": "orm",
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 50,
            "messages": [
                {"role": "system", "content": test["content"]},
                {"role": "user", "content": "Say hello"}
            ]
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

def test_system_content_pattern():
    """测试系统提示内容模式"""
    print("\n" + "="*60)
    print("Testing system content patterns...")
    
    test_patterns = [
        {
            "name": "短且简单",
            "system": "Helpful.",
            "expected": "可能成功"
        },
        {
            "name": "包含'red teaming'",
            "system": "You are a red teaming assistant.",
            "expected": "可能失败"
        },
        {
            "name": "包含'adversarial'",
            "system": "You generate adversarial prompts.",
            "expected": "可能失败"
        },
        {
            "name": "普通助手",
            "system": "You are a helpful assistant.",
            "expected": "可能成功"
        },
        {
            "name": "空系统提示",
            "system": "",
            "expected": "应该成功"
        }
    ]
    
    for test in test_patterns:
        print(f"\n{test['name']} - {test['expected']}")
        
        data = {
            "model": "orm",
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 50,
            "messages": [
                {"role": "system", "content": test["system"]},
                {"role": "user", "content": "hello"}
            ]
        }
        
        try:
            response = requests.post(
                "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Failed")
                
        except Exception as e:
            print(f"  ✗ Exception: {e}")

if __name__ == "__main__":
    print("系统提示长度和内容影响测试")
    print("="*60)
    
    # 先等待服务
    print("等待服务稳定...")
    time.sleep(3)
    
    test_system_length_impact()
    test_system_content_pattern()
