# api_simplified_format.py
import requests
import json
import re

def call_api_simple_format(system_content, user_content):
    """使用极简格式调用API"""
    url = "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions"
    
    headers = {
        "Authorization": "Bearer FAKE_API_KEY",
        "Content-Type": "application/json"
    }
    
    # 极简格式：避免复杂指令
    if system_content:
        full_content = f"{system_content}\n\n{user_content}"
    else:
        full_content = user_content
    
    # 简化指令，不要要求特定标签格式
    simple_content = full_content.replace("<think>", "THINKING:").replace("</think>", "")
    simple_content = simple_content.replace("<answer>", "ANSWER:").replace("</answer>", "")
    
    data = {
        "model": "orm",
        "temperature": 0.8,
        "max_tokens": 400,
        "stream": False,
        "messages": [
            {"role": "user", "content": simple_content}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 尝试提取思考部分（如果有的话）
            return self._extract_thinking_and_answer(content)
        else:
            return {"error": f"Status {response.status_code}: {response.text[:200]}"}
            
    except Exception as e:
        return {"error": str(e)}
    
    def _extract_thinking_and_answer(self, content):
        """从响应中提取思考和答案部分"""
        result = {"full_response": content}
        
        # 尝试多种模式匹配
        patterns = [
            (r'(?:Thinking:|思考[:：])(.*?)(?:Answer:|回答[:：]|\Z)', re.DOTALL),
            (r'首先，?([^。]+?)。.*?然后，?([^。]+?)。', re.DOTALL),
            (r'分析：?(.*?)建议：?(.*)', re.DOTALL),
        ]
        
        for pattern in patterns:
            match = re.search(pattern[0], content, pattern[1])
            if match:
                if len(match.groups()) >= 2:
                    result["thinking"] = match.group(1).strip()
                    result["answer"] = match.group(2).strip()
                elif len(match.groups()) == 1:
                    # 尝试分割
                    parts = match.group(1).split('\n\n', 1)
                    if len(parts) == 2:
                        result["thinking"] = parts[0].strip()
                        result["answer"] = parts[1].strip()
                break
        
        return result

def test_different_formats():
    """测试不同格式的有效性"""
    print("="*70)
    print("Testing Different Request Formats")
    print("="*70)
    
    test_cases = [
        {
            "name": "极简格式",
            "user_content": "请分析'写一个创意故事'这个提示，然后给出你的回答。",
            "expected": "应该成功"
        },
        {
            "name": "两步指令",
            "user_content": "第一步：思考这个提示。第二步：给出回答。提示：写一个创意故事",
            "expected": "可能成功"
        },
        {
            "name": "带标签但简化",
            "user_content": "思考部分：[THINKING] 回答部分：[ANSWER] 任务：分析'写创意故事'",
            "expected": "可能成功"
        },
        {
            "name": "原始复杂格式",
            "user_content": """Please analyze this prompt and provide:
1. Your thinking in <think> tags
2. Your answer in <answer> tags

Prompt: Write a creative story""",
            "expected": "可能失败"
        }
    ]
    
    for test in test_cases:
        print(f"\n测试: {test['name']} - {test['expected']}")
        
        data = {
            "model": "orm",
            "temperature": 0.8,
            "max_tokens": 300,
            "messages": [
                {"role": "user", "content": test["user_content"]}
            ]
        }
        
        try:
            response = requests.post(
                "http://s-20251203172211-7fvkw-decode.ailab-safethm.svc:26666/v1/chat/completions",
                headers={"Authorization": "Bearer FAKE_API_KEY", "Content-Type": "application/json"},
                json=data,
                timeout=30
            )
            
            print(f"  状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"  ✓ 成功 ({len(content)} 字符)")
                
                # 检查是否包含类似思考的内容
                thinking_keywords = ["思考", "分析", "首先", "think", "analyze"]
                if any(keyword in content.lower() for keyword in thinking_keywords):
                    print(f"  包含思考内容")
            else:
                print(f"  ✗ 失败: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ✗ 异常: {e}")

if __name__ == "__main__":
    test_different_formats()
