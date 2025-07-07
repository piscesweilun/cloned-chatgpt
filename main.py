import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import get_chat_response

st.title("💬 Cloned ChatGPT")

with st.sidebar:
    openai_api_key = st.text_input("請輸入 OpenAI API Key：", type="password")
    st.markdown("[取得 OpenAI API key](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "您好，我是您的 AI 助手，有什麼可以幫您的嗎？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("請輸入您的 OpenAI API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI 正在思考中，請稍候..."):
        response = get_chat_response(prompt, st.session_state["memory"],
                                     openai_api_key)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)