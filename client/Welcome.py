import os
import time
import chromadb
import random
import streamlit as st
from chromadb.config import Settings
from app.questgen.paper import Paper
from app.db.vector_db import VectorDB
from langserve import RemoteRunnable
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings as Hf_embeddings
from app.prompts.conversation import basic_prompt


hf_token = os.environ.get('HF_TOKEN')

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Hi . 👋")
st.sidebar.header("Welcome")

st.title("Let's discuss...")

llama = RemoteRunnable("http://server:7200/models/llama/")
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

client = chromadb.HttpClient(host='vector-store', port=8000, settings=Settings(allow_reset=True))

embedding_function = Hf_embeddings(model="sentence-transformers/all-MiniLM-l6-v2", huggingfacehub_api_token=hf_token)
db = VectorDB(
    client=client,
    collection_name="Modern_India",
    embedding_func=embedding_function
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask  your doubts here ..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        context = format_docs(db.get_retriever().invoke(prompt))
        final_prompt = basic_prompt.format(user_prompt=prompt, system_prompt=context, chat_history=st.session_state.chat_history)
        st.session_state.chat_history+= f"user: {prompt}\n"


    with st.chat_message("assistant"):
        stream = llama.stream(final_prompt)
        response = st.write_stream(stream)
        st.session_state.chat_history+=f"assistant: {response}\n"
    st.session_state.messages.append({"role": "assistant", "content": response})
        
    