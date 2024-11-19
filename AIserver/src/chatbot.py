import asyncio

from src.chat_session import Chatchain, periodic_cleanup, stats_context
from src.data_processing_for_server import data_processor
from src.config.config_copy import select_num

class AsyncMultiprocessChatbot:
    def __init__(self):
        self.chain = Chatchain()
        self.dp = data_processor  # 使用预初始化的实例

    async def process_query(self, query, session_id, llm):
        docs = await asyncio.to_thread(self.dp.retrieve, query, select_num)
        content = await asyncio.to_thread(self.dp.return_answer, query, docs, select_num)
        response = await asyncio.to_thread(self.chain.create_chat_session, query, content, session_id, llm)
        return query, response

    async def stream_query(self, query, session_id, llm):
        docs = await asyncio.to_thread(self.dp.retrieve, query, select_num)
        content = await asyncio.to_thread(self.dp.return_answer, query, docs, select_num)
        async for response in self.chain.create_stream_chat_session(query, content, session_id, llm):
            yield response