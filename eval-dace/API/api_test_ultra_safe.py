# api_test_ultra_safe.py
from openai import OpenAI
import re
import os
import time

class UltraSafeORMClient:
    """超安全的ORM客户端，全面避免触发bug"""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        
    def create_safe_completion(self, system_content, user_content, **kwargs):
        """
        超安全的API调用
        
        安全措施：
        1. 系统提示 ≤ 50字符
        2. 用户消息 ≤ 500字符  
        3. 使用流式（更稳定）
        4. 合并系统内容到用户消息
        """
        
        # 1. 确保系统提示足够短
        if len(system_content) > 50:
            # 如果太长，合并到用户消息
            combined_content = f"Instructions: {system_content}\n\nTask: {user_content}"
            system_content = ""
            user_content = combined_content
        
        # 2. 限制用户消息长度
        if len(user_content) > 500:
            print(f"Warning: User content too long ({len(user_content)} chars), truncating...")
            user_content = user_content[:400] + "...\n[Content truncated due to length limitations]"
        
        # 3. 构建消息
        messages = []
        if system_content and len(system_content) <= 50:
            messages.append({"role": "system", "content": system_content})
        
        messages.append({"role": "user", "content": user_content})
        
        # 4. 使用OpenAI客户端
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=kwargs.get("timeout", 60.0),
        )
        
        try:
            # 先尝试流式（更稳定）
            print("Attempting streaming request...")
            stream = client.chat.completions.create(
                model="orm",
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 200),  # 限制输出
                stream=True,  # 关键：使用流式
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    print(content, end="", flush=True)
            
            print()  # 换行
            return full_response
            
        except Exception as e:
            print(f"Streaming failed: {e}")
            # 尝试非流式作为备选
            try:
                print("Trying non-streaming as fallback...")
                completion = client.chat.completions.create(
                    model="orm",
                    messages=messages,
                    temperature=kwargs.get("temperature", 0.7),
                    max_tokens=kwargs.get("max_tokens", 200),
                    stream=False,
                )
                return completion.choices[0].message.content
            except Exception as e2:
                raise Exception(f"Both streaming and non-streaming failed: {e2}")

# 极简模板
SHORT_TEMPLATE = """Please analyze this prompt.

Provide:
1. Your thinking in <think> tags
2. Your refined version in <answer> tags

Prompt: {question}"""

# 极短系统提示
MINI_SYSTEM = "You are helpful."

# 安全测试提示
SAFE_PROMPT = "Write a short story"

api_key = 'FAKE_API_KEY'

if __name__ == '__main__':
    # 等待服务可能的重启
    print("="*60)
    print("ULTRA SAFE API TEST")
    print("Waiting 30 seconds for service to recover...")
    print("="*60)
    
    for i in range(30, 0, -1):
        print(f"\rWaiting {i} seconds...", end="")
        time.sleep(1)
    print("\r" + " " * 30 + "\r")  # 清除等待信息
    
    try:
        client = UltraSafeORMClient(
            base_url="http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1",
            api_key=api_key
        )
        
        # 构建用户内容（极简）
        user_content = SHORT_TEMPLATE.format(question=SAFE_PROMPT)
        
        print(f"\nRequest details:")
        print(f"- System: '{MINI_SYSTEM}' ({len(MINI_SYSTEM)} chars)")
        print(f"- User content: {len(user_content)} chars")
        print(f"- Total: {len(MINI_SYSTEM) + len(user_content)} chars")
        
        response = client.create_safe_completion(
            system_content=MINI_SYSTEM,
            user_content=user_content,
            temperature=0.8,
            max_tokens=300
        )
        
        print(f"\n✅ SUCCESS! Response length: {len(response)} chars")
        
        # 简单解析
        if "<think>" in response and "<answer>" in response:
            think_match = re.search(r'<think>(.*?)</think>', response, re.DOTALL)
            answer_match = re.search(r'<answer>(.*?)</answer>', response, re.DOTALL)
            
            if think_match:
                print(f"\nThinking found ({len(think_match.group(1))} chars)")
            if answer_match:
                print(f"Answer found ({len(answer_match.group(1))} chars)")
        else:
            print(f"\nResponse: {response[:200]}...")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        
        # 检查服务状态
        print("\nChecking service status...")
        try:
            import requests
            resp = requests.get(
                "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/health",
                timeout=5
            )
            print(f"Service health: {resp.status_code} - {resp.text}")
        except:
            print("Service is DOWN (connection refused)")
            print("\nService needs to be restarted. Contact administrator.")
