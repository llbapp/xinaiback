from openai import OpenAI, AsyncOpenAI
from src.config.config import URLS  # 导入 URL 配置字典



def load_llm(llm):
    """
    加载llm模型，根据llm选择url，在config文件中配置
    """
    url = URLS.get(llm) # 根据llm参数获取URLS中的api地址
    if not url:
        raise ValueError(f"未找到组 '{llm}' 的URL，请检查配置。") # 一个报错
        
    openai = OpenAI(
        api_key='YOUR_API_KEY', # 这个参数不需要改，因为我们是引用的自己部署的模型，因此谬也apikey，这是占位符
        base_url=url
    ) # 使用openai方法调用llm
    model_name = "internlm2" # 名字是根据部署时命名的，貌似没有用到这个变量
    return openai, model_name

# 异步llm
async def load_async_llm(llm):
    """
    加载llm模型，根据llm选择url，在config文件中配置，使用了异步方法，用于流式请求
    """
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
    '''
    一些测试，在正常运行中不会运行下面的代码
    '''
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
