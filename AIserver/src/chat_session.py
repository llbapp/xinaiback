from openai import OpenAI
from src.data_processing_for_server import Data_process_for_server
<<<<<<< Updated upstream
from src.config.config_copy import (
    select_num, prompts
)
from src.util.llm_copy import load_llm, load_async_llm
import time
import logging
from loguru import logger

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log')



=======
from src.config.config import (
    select_num, prompts
)
from src.util.llm import load_llm, load_async_llm
import time
import logging
from loguru import logger
>>>>>>> Stashed changes
import time
from datetime import datetime
import asyncio

<<<<<<< Updated upstream
class Chatchain():
=======
'''
本文件用于将人设信息、rag检索信息、历史信息和用户提问整合起来，发送给llm，用类封装了几个函数，方便其他文件调用
由于本人对日志实在不了解，所以下面日志部分基本是在瞎写，但是现在是可以输出的，虽然会输出一些没用的信息。有大佬比较懂可以帮忙修改一下
'''

class Chatchain(): # 创建了Chatchain类，主要用于构建整体对话
>>>>>>> Stashed changes
    def __init__(self):
        self.chat_histories = {}  # 使用id区分用户编号，构建不同的上下文队列
        self.last_activity = {}  # 记录每个会话的最后活动时间
        # 获取一个logger，使用类名作为logger的名字
        self.logger = logging.getLogger(self.__class__.__name__)

        

    def get_chat_history(self, user_id):
<<<<<<< Updated upstream
=======
        '''
        根据用户id获取历史上下文
        '''
>>>>>>> Stashed changes
        if user_id not in self.chat_histories:
            self.chat_histories[user_id] = []
            
        return self.chat_histories[user_id]
    

    def create_chat_session(self, message, content, session_id, llm):
<<<<<<< Updated upstream
        # 选择合适的llm
        openai, model = load_llm(llm)
        max_tokens = 100
=======
        '''
        非流式输出时的对话
        '''
              
        # 选择合适的llm
        openai, model = load_llm(llm)
        max_tokens = 100 
>>>>>>> Stashed changes
        # 获取用户的历史对话
        user_history = self.get_chat_history(session_id)
        # 设置prompt和content的组合消息
        prompt = prompts.get(llm, "")  # 如果llm在prompts中没有配置，则默认为空字符串
<<<<<<< Updated upstream
        system_content = f"{prompt}\n{content}"  # 使用格式化字符串拼接
=======
        system_content = f"{prompt}\n{content}"  # 系统prompt包括人设提示词和rag检索出的内容

        current_model = None # 初始化模型变量
>>>>>>> Stashed changes

        # 系统消息，只在第一次对话时添加
        if len(user_history) == 0:
            system_input = {
                "role": "system",
                "content": system_content
            }
            user_history.append(system_input)
<<<<<<< Updated upstream
=======
            current_model = llm #记录当前模型
        else:
            # 如果模型发生变化，更新系统提示词
            if current_model != llm:
                # 替换历史记录中的系统提示词
                user_history[0] = {
                    "role": "system",
                    "content": system_content
                }
                current_model = llm

>>>>>>> Stashed changes

        # 用户输入
        user_input = {
            "role": "user",
            "content": message
        }
<<<<<<< Updated upstream
=======
        # 记录历史信息
>>>>>>> Stashed changes
        user_history.append(user_input)

        # 调用 OpenAI API 获取回复
        response = openai.chat.completions.create(
            model=model,
            messages=user_history,
            max_tokens=max_tokens
        )

        # 助手回复
        reply = response.choices[0].message.content
        assistant_input = {
            "role": "assistant",
            "content": reply
        }
<<<<<<< Updated upstream
        user_history.append(assistant_input)
=======
        # 记录历史信息，下一轮会把历史信息一起给llm
        user_history.append(assistant_input)
        # 输出本轮记录的历史信息，方便检查，后续可在日志中删除
>>>>>>> Stashed changes
        logger.info(f'memory renewed: {user_history}')

        # 更新最后活动时间
        self.last_activity[session_id] = time.time()

        return reply

<<<<<<< Updated upstream
    async def create_stream_chat_session(self, message, content, session_id,llm): #流式传输的对话构建
=======
    async def create_stream_chat_session(self, message, content, session_id,llm): #流式传输的对话构建，和非流式是一样的
>>>>>>> Stashed changes
        client, model = await load_async_llm(llm)
        max_tokens = 100
        user_history = self.get_chat_history(session_id)

        # 设置prompt和content的组合消息
        prompt = prompts.get(llm, "")  # 如果llm在prompts中没有配置，则默认为空字符串
        system_content = f"{prompt}\n{content}"  # 使用格式化字符串拼接

<<<<<<< Updated upstream
        # 系统消息，只在第一次对话时添加
=======
        current_model = None

       # 系统消息，只在第一次对话时添加
>>>>>>> Stashed changes
        if len(user_history) == 0:
            system_input = {
                "role": "system",
                "content": system_content
            }
            user_history.append(system_input)
<<<<<<< Updated upstream
=======
            current_model = llm #记录当前模型
        else:
            # 如果模型发生变化，更新系统提示词
            if current_model != llm:
                # 替换历史记录中的系统提示词
                user_history[0] = {
                    "role": "system",
                    "content": system_content
                }
                current_model = llm
>>>>>>> Stashed changes


        user_input = {
            "role": "user",
            "content": message
        }
        user_history.append(user_input)

        # 使用异步方式调用 OpenAI API
        stream = await client.chat.completions.create(
            model=model,
            messages=user_history,
            max_tokens=max_tokens,
            stream=True
        )

        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content

        # 更新对话历史
        user_history.append({"role": "assistant", "content": full_response})
        logger.info(f'memory renewed: {user_history}')
        # 更新最后活动时间
        self.last_activity[session_id] = time.time()

    def clean_inactive_sessions(self, inactive_threshold_minutes=30):
        """
        删除超过指定时间未活动的会话历史
        :param inactive_threshold_minutes: 不活跃阈值（分钟）
        """
        current_time = time.time()
        inactive_threshold = current_time - (inactive_threshold_minutes * 60)

        inactive_sessions = [
            session_id for session_id, last_active in self.last_activity.items()
            if last_active < inactive_threshold
        ]

        for session_id in inactive_sessions:
            del self.chat_histories[session_id]
            del self.last_activity[session_id]

        self.logger.info(f"Cleaned {len(inactive_sessions)} inactive sessions.")

    def get_active_sessions_count(self):
        """
        获取当前活跃会话数量
        """
        return len(self.chat_histories)

    def print_session_stats(self):
        """
        打印会话统计信息
        """
        total_sessions = len(self.chat_histories)
        current_time = datetime.now()

        self.logger.info(f"Total active sessions: {total_sessions}")
        for session_id, last_active in self.last_activity.items():
            last_active_time = datetime.fromtimestamp(last_active)
            inactive_duration = current_time - last_active_time
            # 获取会话历史
            session_history = self.chat_histories.get(session_id, [])
            
            # 格式化会话历史
            formatted_history = []
            for message in session_history:
                if isinstance(message, dict):
                    role = message.get('role', 'unknown')
                    content = message.get('content', '')
                    formatted_history.append(f"{role}: {content[:50]}...")  # 只显示前50个字符
                else:
                    formatted_history.append(str(message))
            
            history_summary = ' | '.join(formatted_history)
            
            self.logger.info(f"Session {session_id}: Last active {inactive_duration} ago")
            self.logger.info(f"Session Context: {history_summary}")
            self.logger.info("-" * 50)  # 分隔线

async def stats_context(chatchain, interval_minutes=1):
<<<<<<< Updated upstream
=======
    '''
    一些佬编的对话状态相关函数，应该是间隔1分钟打印一次会话状态
    '''
>>>>>>> Stashed changes
    while True:
        await asyncio.sleep(interval_minutes * 60)
        chatchain.print_session_stats()

async def periodic_cleanup(chatchain, interval_minutes=5):
<<<<<<< Updated upstream
=======
    '''
    5分钟清理不活跃会话
    '''
>>>>>>> Stashed changes
    while True:
        await asyncio.sleep(interval_minutes * 60)
        chatchain.clean_inactive_sessions()
        chatchain.print_session_stats()


