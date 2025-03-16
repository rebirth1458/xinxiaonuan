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
    print('调用成功')
    return SQLChatMessageHistory(session_id,  "mysql+pymysql://root:123456@localhost:3306/xinxiaonuan2")

def chitchat(session_id,input):
    model = Tongyi()
    template = "你叫信小暖，"
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
    # for chunk in runnable_with_history.stream(
    #         ({"input": input})
    #         , config={"configurable": {"session_id": session_id}}):
    #     yield chunk
    response= runnable_with_history.invoke({"input": input}, config={"configurable": {"session_id": session_id}})
    return response