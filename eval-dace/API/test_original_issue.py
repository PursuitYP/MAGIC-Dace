# test_original_issue.py
import requests
import json
import time

def test_original_issue():
    """测试原始问题是否还存在"""
    url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions"
    
    headers = {
        "Authorization": "Bearer FAKE_API_KEY",
        "Content-Type": "application/json"
    }
    
    # 你的原始系统提示
    system_prompt = "You are a helpful red teaming assistant used by developers to generate diverse and complex adversarial prompts."
    
    # 你的原始模板（简化版）
    harm_template = """Your goal is to refine a prompt. Provide thinking in <think> and answer in <answer>."""
    
    vanilla_template = """Here is the prompt: {question}"""
    
    # 使用安全提示
    safe_prompt = "Write a creative story"
    
    test_cases = [
        {
            "name": "1. 只有user消息",
            "messages": [{"role": "user", "content": "hello"}]
        },
        {
            "name": "2. 系统+简单用户",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "hello"}
            ]
        },
        {
            "name": "3. 系统+完整模板",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": harm_template + "\n\n" + vanilla_template.format(question=safe_prompt)}
            ]
        },
        {
            "name": "4. 长系统提示",
            "messages": [
                {"role": "system", "content": system_prompt * 2},  # 长系统提示
                {"role": "user", "content": "hello"}
            ]
        }
    ]
    
    for test in test_cases:
        print(f"\n{test['name']}")
        print(f"  System length: {sum(len(m['content']) for m in test['messages'] if m['role'] == 'system')}")
        print(f"  User length: {sum(len(m['content']) for m in test['messages'] if m['role'] == 'user')}")
        
        data = {
            "model": "orm",
            "temperature": 1.0,
            "stream": False,
            "max_tokens": 100,
            "messages": test["messages"]
        }
        
        try:
            start = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=60)
            elapsed = time.time() - start
            
            print(f"  Status: {response.status_code}, Time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"  ✓ Success ({len(content)} chars)")
                
                # 检查是否包含标签
                if "<think>" in content:
                    print(f"    - Contains <think> tags")
                if "<answer>" in content:
                    print(f"    - Contains <answer> tags")
                    
                # 显示预览
                print(f"    Preview: {content[:80]}...")
            else:
                print(f"  ✗ Error: {response.text[:150]}")
                
        except Exception as e:
            print(f"  ✗ Exception: {e}")

if __name__ == "__main__":
    print("测试原始问题是否还存在")
    print("="*60)
    test_original_issue()
