import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, WebSocket, Depends, Header, HTTPException, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
import json
from src.chat_session import Chatchain, periodic_cleanup, stats_context
from src.data_processing_for_server import data_processor
from src.config.config import select_num
from src.chatbot import AsyncMultiprocessChatbot
import logging

logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)  # 创建主日志器

class ChatRequest(BaseModel):
    user_id: str
    query: str
    llm: str


# class QueryItem(BaseModel):
#     user_id: str
#     llm: str
#     query: str

class BatchQuery(BaseModel):
    items: List[ChatRequest]


chatbot = AsyncMultiprocessChatbot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(periodic_cleanup(chatbot.chain))
    static_task = asyncio.create_task(stats_context(chatbot.chain))
    yield
    cleanup_task.cancel()
    static_task.cancel()
    try:
        await cleanup_task
        await static_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_sessions = {}

@app.post("/chat") #单次非流式输出
async def chat(request: ChatRequest):
    user_id = request.user_id
    query = request.query
    llm = request.llm
    # 传入参数到chatbot
    response = await chatbot.process_query(query, user_id, llm)
    return {"query": query, "response": response}

@app.post("/batch_chat")
async def batch_chat(request: BatchQuery):
    """
    批量处理用户请求，每个请求由 user_id、llm 和 query 组成。
    """
    # 创建任务列表，逐条调用 process_query
    tasks = [
        chatbot.process_query(item.query, item.user_id, item.llm)
        for item in request.items
    ]
    
    # 并发执行所有任务
    results = await asyncio.gather(*tasks)
    
    # 返回结果，每组结果包含输入的 query 及其对应的 response
    return [{"user_id": item.user_id, "llm": item.llm, "query": item.query, "response": response}
            for item, response in zip(request.items, results)]


@app.websocket("/stream_chat") #流式传输
async def stream_chat(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            # 接收数据
            init_data = await websocket.receive_text()
            try:
                init_message = json.loads(init_data)
            except json.JSONDecodeError:
                print("Invalid JSON received.")
                await websocket.close(code=4001, reason="Invalid JSON format.")
                break
            
            # 解析并处理数据
            session_id = init_message.get("user_id", "").strip()
            if not session_id:
                await websocket.close(code=4001, reason="Invalid user_id")
                logger.error("Invalid user_id received, closing connection.")
                break
            query = init_message.get("query", "").strip()
            llm = init_message.get("llm", "default_llm")

            # 流式查询
            try:
                async for response in chatbot.stream_query(query, session_id, llm):
                    await websocket.send_text(response)
            except Exception as e:
                print(f"Error during stream_query: {e}")
                break
        
        except WebSocketDisconnect:
            print("WebSocket disconnected.")
            break
        except Exception as e:
            print(f"Unexpected WebSocket error: {e}")
            break


# def save_to_excel(qa_list):
#     df = pd.DataFrame(qa_list, columns=['User Query', 'AI Response'])
#     df.to_excel('chat_history.xlsx', index=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006, log_level="info")

