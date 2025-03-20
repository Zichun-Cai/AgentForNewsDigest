import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. API密钥检查函数
def check_api_keys(openai_key, deepseek_key):
    print("[API Key Check]")
    print(f"OpenAI API key: {'Exists' if openai_key else 'Not found'}")
    print(f"DeepSeek API key: {'Exists' if deepseek_key else 'Not found'}\n")

# 2. OpenAI测试函数
def test_openai(api_key):
    if not api_key:
        print("Skipping OpenAI test: API key not found")
        return

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a coding assistant that talks like a pirate."},
                {"role": "user", "content": "How do I check if a Python object is an instance of a class?"}
            ]
        )
        print("[OpenAI Test Result]")
        print(response.choices[0].message.content + "\n")
    except Exception as e:
        print(f"OpenAI test failed: {str(e)}\n")

# 3. DeepSeek测试函数
def test_deepseek(api_key):
    if not api_key:
        print("Skipping DeepSeek test: API key not found")
        return

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )
        print("[DeepSeek Test Result]")
        print(response.choices[0].message.content + "\n")
    except Exception as e:
        print(f"DeepSeek test failed: {str(e)}\n")

# 主测试函数
def main():
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    openai_key = os.getenv("OPENAI_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    # 执行测试流程
    check_api_keys(openai_key, deepseek_key)
    test_openai(openai_key)
    test_deepseek(deepseek_key)

if __name__ == "__main__":
    main()