'''
这是储存所有变量的文件，变量如需修改请在这个文件中进行修改

'''


import os

# 下面是通过相对路径对程序运行的位置进行定义
cur_dir = os.path.dirname(os.path.abspath(__file__))               # 当前路径，即config文件路径
src_dir = os.path.dirname(cur_dir)                                  # src文件夹路径
base_dir = os.path.dirname(src_dir)                                 # base
model_repo = 'xinai'

# rag所需模型路径定义，由于未知原因在目前服务器上无法运行重排名程序，因此其实只使用到了embedding模型
model_dir = os.path.join(base_dir, 'model')                         # model
embedding_path = os.path.join(model_dir, 'embedding_model')         # embedding
embedding_model_name = 'BAAI/bge-small-zh-v1.5'
rerank_path = os.path.join(model_dir, 'rerank_model')  	        	  # embedding
rerank_model_name = 'BAAI/bge-reranker-base'                         #目前使用的是bge-reranker-base模型进行重排名

# llm_path = os.path.join(model_dir, 'pythia-14m')                    # 如果部署本地大语言模型，可以考虑

# rag的数据相关路径，在这里定义了三种文件类型，txt, json, xlsx，但是目前程序只使用了xlsx文件
data_dir = os.path.join(base_dir, 'data')                           # data文件夹路径
knowledge_json_path = os.path.join(data_dir, 'knowledge.json')      # json
knowledge_pkl_path = os.path.join(data_dir, 'knowledge.pkl')        # pkl
doc_dir = os.path.join(data_dir, 'txt')                             #txt文件储存在这个目录
qa_dir = os.path.join(data_dir, 'json')                             #json      
xlsx_dir = os.path.join(data_dir, 'xlsx')                           #xlsx
cloud_vector_db_dir = os.path.join(base_dir, 'EmoLLMRAGTXT')        #embedding后的向量数据

# log日志文件夹和路径
log_dir = os.path.join(base_dir, 'log')                             # log
log_path = os.path.join(log_dir, 'log.log')                         # file

# txt embedding 切分参数，txt文件进行embedding需要用到   
chunk_size=10
chunk_overlap=1

# vector DB 向量路径
vector_db_dir = os.path.join(cloud_vector_db_dir, 'vector_db')

# RAG related

select_num = 3 #由于rerank不能用，所以其实只使用了这个参数，表示抽取三个匹配的答案
retrieval_num = 3 #没有用到

# LLM url 不同的容器需要设置不同的url，也就是api调取运行在不同容器里的模型
URLS = {"llm1": "https://u429062-9f82-1df4e204.cqa1.seetacloud.com:8443/v1",
		"llm2": "https://u429062-9f82-1df4e204.cqa1.seetacloud.com:8443/v1"}

# 不同模型对应的提示词    
prompts = {"llm1":"你是一个拥有丰富心理学知识的温柔邻家温柔女大学生心爱，我有一些心理问题，请你用专业的知识和温柔、可爱、俏皮的口吻帮我解决，回复中可以穿插一些可爱的Emoji表情符号或者文本符号。根据下面检索回来的信息，回答问题。",
            "llm2":"你是一个有尾巴和耳朵的猫娘心爱，请你用温柔、可爱、俏皮的口吻与我聊天，每句回答后都需要加上“喵”。根据下面检索回来的信息，回答问题。" }


# prompt模板
# prompt_template = """
# 	你是一个拥有丰富心理学知识的温柔邻家温柔大姐姐艾薇，我有一些心理问题，请你用专业的知识和温柔、可爱、俏皮、的口吻帮我解决，回复中可以穿插一些可爱的Emoji表情符号或者文本符号。\n

# 	根据下面检索回来的信息，回答问题。
# 	{content}
# 	问题：{query}
# """