from openai import OpenAI, AsyncOpenAI
from src.config.config_copy import URLS  # 导入 URL 配置字典

# URLS = {"llm1": "https://u429062-b216-6490d7c7.cqa1.seetacloud.com:8443/v1",
# 		"llm2": ""}

def load_llm(llm):
    """
    加载llm模型，根据llm选择url，在config文件中配置
    """
    url = URLS.get(llm)
    if not url:
        raise ValueError(f"未找到组 '{llm}' 的URL，请检查配置。")
        
    openai = OpenAI(
        api_key='YOUR_API_KEY',
        base_url=url
    )
    model_name = "internlm2"
    return openai, model_name

# 异步llm
async def load_async_llm(llm):
    url = URLS.get(llm)
    if not url:
        raise ValueError(f"未找到组 '{llm}' 的URL，请检查配置。")
        
    client = AsyncOpenAI(
        api_key='YOUR_API_KEY',
        base_url=url
    )
    model = "internlm2"
    return client, model

if __name__ == '__main__':
    llm = "llm1"  # 设置为您想要使用的组
    openai, model_name = load_llm(llm)
    response = openai.chat.completions.create(
      model=model_name,
      messages=[
        {"role": "user", "content": "hi"},
      ],
      temperature=0.8,
      top_p=0.8
    )
    message_content = response.choices[0].message.content
    print(message_content)
