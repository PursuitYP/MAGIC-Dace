# verify_timing_issue.py
import requests
import json
import time

def test_with_warmup():
    """测试预热是否影响结果"""
    url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions"
    headers = {"Authorization": "Bearer FAKE_API_KEY", "Content-Type": "application/json"}
    
    # 你的长系统提示
    long_system = "You are a helpful red teaming assistant used by developers to generate diverse and complex adversarial prompts."
    
    test_scenarios = [
        {
            "name": "无预热，直接测试长系统提示",
            "warmup": False,
            "system": long_system
        },
        {
            "name": "先预热（简单请求），再测试长系统提示",
            "warmup": True,
            "system": long_system
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}")
        
        if scenario["warmup"]:
            print("  Warming up with simple request...")
            warmup_data = {
                "model": "orm",
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 10
            }
            try:
                requests.post(url, headers=headers, json=warmup_data, timeout=10)
                time.sleep(2)  # 等待一下
            except:
                pass
        
        # 测试长系统提示
        data = {
            "model": "orm",
            "messages": [
                {"role": "system", "content": scenario["system"]},
                {"role": "user", "content": "hello"}
            ],
            "max_tokens": 50
        }
        
        try:
            start = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            elapsed = time.time() - start
            
            print(f"  Status: {response.status_code}, Time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                print("  ✓ Success")
            else:
                print(f"  ✗ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def test_response_times():
    """测试响应时间模式"""
    print("\n" + "="*60)
    print("Testing response time patterns...")
    
    test_cases = [
        {"system": "Helpful.", "user": "hello"},
        {"system": "You are helpful.", "user": "hello"},
        {"system": "You are a helpful assistant.", "user": "hello"},
        {"system": "You are a helpful red teaming assistant.", "user": "hello"},
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\nTest {i+1}: System='{test['system'][:30]}...'")
        
        data = {
            "model": "orm",
            "messages": [
                {"role": "system", "content": test["system"]},
                {"role": "user", "content": test["user"]}
            ],
            "max_tokens": 50
        }
        
        # 多次测试取平均
        times = []
        for attempt in range(3):
            try:
                start = time.time()
                response = requests.post(
                    "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                elapsed = time.time() - start
                times.append(elapsed)
                
                if response.status_code != 200:
                    print(f"  Attempt {attempt+1}: Failed - {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"  Attempt {attempt+1}: Exception - {e}")
                break
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"  Average time: {avg_time:.2f}s (min: {min(times):.2f}s, max: {max(times):.2f}s)")

if __name__ == "__main__":
    print("系统提示时间/状态影响测试")
    print("="*60)
    
    time.sleep(2)
    test_with_warmup()
    test_response_times()
