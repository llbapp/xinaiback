import asyncio
import aiohttp


SERVER_URL = "wss://u429062-ac1f-fc3bdb72.westc.gpuhub.com:8443"


async def test_chat():
    async with aiohttp.ClientSession() as session:
        x_session_id = "1"
        query = "我要报告"
        llm = "llm1"
        async with session.post(f"{SERVER_URL}/chat", json={"user_id": x_session_id, "query": query, "llm": llm}) as response:
            result = await response.json()
            print("Chat Result:", result)

async def test_batch_chat():
    async with aiohttp.ClientSession() as session:
        # 定义每个请求的 user_id, llm 和 query
        x_session_ids = ["1", "2", "3"]
        llm = ["llm1", "llm1", "llm1"]
        queries = ["What is machine learning?", "Explain deep learning", "What are neural networks?"]

        # 构造 items 列表
        items = [{"user_id": user_id, "llm": model, "query": query} for user_id, model, query in zip(x_session_ids, llm, queries)]

        # 发送 POST 请求
        async with session.post(f"{SERVER_URL}/batch_chat", json={"items": items}) as response:
            if response.status == 200:
                results = await response.json()
                print("Batch Chat Results:")
                for result in results:
                    print(f"User ID: {result['user_id']}")
                    print(f"LLM: {result['llm']}")
                    print(f"Query: {result['query']}")
                    print(f"Response: {result['response']}")
                    print("---")
            else:
                print(f"Error: Received status code {response.status}")



async def main():
    print("Testing /chat endpoint")
    await test_chat()
    print("\nTesting /batch_chat endpoint")
    await test_batch_chat()


if __name__ == "__main__":
    asyncio.run(main())