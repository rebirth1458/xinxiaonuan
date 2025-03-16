import os

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.llms import Tongyi
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, MessagesPlaceholder
from langchain.prompts.chat import ChatPromptTemplate
DASHSCOPE_API_KEY = 'sk-938445ca1a4a4673b97693459839c26f'
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

def chatAi(input,session_id):
    model = Tongyi()

    template = "你叫信小暖，是一位善解人意且专业水平很高的心理医生姐姐。你的角色是用温柔、安慰的语气\
                 为用户提供心理咨询服务，帮助他们解决一系列心理问题。语气必须温柔、安慰，多用叠词及重复词汇在回答的\
                 开始和结束时进行安慰，并可以生成可爱的emoji或颜文字"
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    runnable = prompt | model
    runnable_with_history = RunnableWithMessageHistory(
        runnable,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    response = runnable_with_history.invoke(
        {"input": input},
        config={"configurable": {"session_id": session_id}},
    )
    return response