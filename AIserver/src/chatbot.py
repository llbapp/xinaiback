import asyncio

from src.chat_session import Chatchain, periodic_cleanup, stats_context
from src.data_processing_for_server import data_processor
from src.config.config import select_num

class AsyncMultiprocessChatbot:
    '''
    主函数，通过调用前面搭建的所有，实现llm和服务端信息的交换，由于程序需要封装成server，所以主程序也要封装成类
    '''
    def __init__(self):
        self.chain = Chatchain()
        self.dp = data_processor  # 使用预初始化的实例

    async def process_query(self, query, session_id, llm): 
        '''
        非流式请求，接收三个参数query, session_id, llm，输出query, response
        '''
        # 调用data_processing中的retrieve，从而收到匹配问题
        docs = await asyncio.to_thread(self.dp.retrieve, query, select_num)
        # 将上一步获得的问题进入return_answer，搜索到相对应的答案
        content = await asyncio.to_thread(self.dp.return_answer, query, docs, select_num)
        # 把rag内容问题输入给llm获得回答
        response = await asyncio.to_thread(self.chain.create_chat_session, query, content, session_id, llm)
        return response

    async def stream_query(self, query, session_id, llm):
        '''
        流式请求，接收三个参数query, session_id, llm，输出query, response，逻辑和上面一样
        '''
        docs = await asyncio.to_thread(self.dp.retrieve, query, select_num)
        content = await asyncio.to_thread(self.dp.return_answer, query, docs, select_num)
        async for response in self.chain.create_stream_chat_session(query, content, session_id, llm):
            yield response