import asyncio
import websockets
import uuid
import json

WS_URL = "ws://localhost:6006"

async def test_stream_chat():
    
    

    async with websockets.connect(f"{WS_URL}/stream_chat") as websocket:
        # 初始化消息，包含 llm 和 query
<<<<<<< Updated upstream
        x_session_id = str(uuid.uuid4())
        query = "你是一个什么样的人？"
        llm = "llm1"
=======
        x_session_id = "1"
        query = "我要报告"
        llm = "llm2"
>>>>>>> Stashed changes
     
        init_message = json.dumps({"user_id": x_session_id, "query": query, "llm": llm})
        
        # 发送初始化消息
       
        await websocket.send(init_message)
        print(f"Sent init message: {init_message}")
        
        full_response = ""
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received: {response}")
                full_response += response
            except asyncio.TimeoutError:
                print("Stream completed or timed out")
                break
        
        print("Full streamed response:", full_response)


async def main():
    print("\nTesting /stream_chat WebSocket")
    await test_stream_chat()

if __name__ == "__main__":
    asyncio.run(main())
