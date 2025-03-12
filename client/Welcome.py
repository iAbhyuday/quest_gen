import os
import logging
import time
import chromadb
import random
import streamlit as st
from chromadb.config import Settings
from app.questgen.paper import Paper
from client.app.indexer.indexer import VectorDB
from langserve import RemoteRunnable
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings as Hf_embeddings
# from app.prompts.conversation import qa_prompt
from langchain.prompts import load_prompt

hf_token = os.environ.get('HF_TOKEN')
loaded_prompt = load_prompt("/src/prompt_siggi.yaml")

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Hi . 👋")
st.sidebar.header("Welcome")

st.title("How can I help you today ?")

llama = RemoteRunnable("http://server:7200/models/llama/")
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def dic_to_history(history, mode=None, model="openai"):
    msg=""
    for n,i in enumerate(history):
        if mode=="prompt":
            if model=="openai":
                if n<len(history)-1:
                    msg+= f"{i['role']}: {i['content']}\n"
            else:    
                if n<len(history)-1:
                    msg+= f"<|start_header_id|>{i['role']}<|end_header_id|> {i['content']}<|eot_id|>\n"
        else:
            msg+= f"{i['role']}:  {i['content']}\n"

    return msg

client = chromadb.HttpClient(host='vector-store', port=8000, settings=Settings(allow_reset=True))

collections = client.list_collections()
st.write(collections)
collections = [c.name for c in collections]
#collections = [c.replace("-", " ") for c in collections]
collection = st.selectbox(
        "Select Collection", collections
        ) 

# logging.info(collections)
 
chat_history=""
if collection:
    embedding_function = Hf_embeddings(model="sentence-transformers/all-MiniLM-l6-v2", huggingfacehub_api_token=hf_token)
    db = VectorDB(
        client=client,
        collection_name=collection,
        embedding_func=embedding_function
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask  your doubts here ..."):

        

        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            context = format_docs(db.get_retriever().invoke(prompt))
            final_prompt = loaded_prompt.format(
                input=prompt,
                context=context,
                chat_history=dic_to_history(st.session_state.messages, mode="prompt")
                )
            
        with st.chat_message("assistant"):
            stream = llama.stream(final_prompt)
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

