import streamlit as st
import asyncio
import websockets
import json
import uuid

# 配置 WebSocket 地址
WS_URL = "ws://localhost:6006/stream_chat"

# 初始化 Streamlit 页面
st.set_page_config(page_title="WebSocket Chat", layout="wide")

# 确保 `x_session_id` 存储在 Streamlit 的会话状态中
if "x_session_id" not in st.session_state:
    st.session_state.x_session_id = ""
if "full_response" not in st.session_state:
    st.session_state["full_response"] = ""

# 用户输入 ID
st.sidebar.title("Chat Configuration")
st.sidebar.text("Enter your session ID below:")
x_session_id_input = st.sidebar.text_input("Session ID", value=st.session_state.x_session_id)
if st.sidebar.button("Set Session ID"):
    if x_session_id_input.strip():
        st.session_state.x_session_id = x_session_id_input.strip()
        st.sidebar.success(f"Session initialized with ID: {st.session_state.x_session_id}")
    else:
        st.sidebar.error("Session ID cannot be empty!")

# LLM 选择
llm = st.sidebar.selectbox("Choose LLM", ["llm1", "llm2"])

# 对话框
st.title("WebSocket Chat")
query = st.text_input("Your Message:")
send_button = st.button("Send")

# 显示对话部分
st.subheader("Chat Output")
chat_output = st.empty()  # 用于动态更新输出

# 调用 WebSocket
async def send_message():
    st.session_state["full_response"] = ""  # 每次对话清空之前的内容
    async with websockets.connect("ws://localhost:6006/stream_chat") as websocket:
        init_message = json.dumps({
            "user_id": st.session_state.x_session_id,
            "query": query.strip(),
            "llm": llm
        })
        await websocket.send(init_message)
        
        # full_response = ""
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                # 去除换行符并追加到响应内容
                st.session_state["full_response"] += response.replace("\n", "").replace("\r", "")
                # 更新显示内容
                chat_output.text(st.session_state["full_response"])
            except asyncio.TimeoutError:
                break

# 点击发送按钮时触发异步函数
if send_button and query.strip():
    asyncio.run(send_message())
