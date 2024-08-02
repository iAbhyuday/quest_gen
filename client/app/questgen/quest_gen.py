import uuid
import chromadb
import random
from chromadb.config import Settings
from pprint import pp
from app.questgen.paper import Paper
from app.questgen.subject import Subject
from app.questgen.topic import Topic
from app.db.vector_db import VectorDB
from app.prompts.basic import basic_prompt,inst
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langserve import RemoteRunnable
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings as Hf_embeddings

llama = RemoteRunnable("http://localhost:7200/models/llama/")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

client = chromadb.HttpClient(host='172.18.0.2', port=8000, settings=Settings(allow_reset=True))
# client.reset()
# collection = client.get_or_create_collection("Modern_India")

embedding_function = Hf_embeddings(model="sentence-transformers/all-MiniLM-l6-v2")

# loader = TextLoader("data/modern_india.txt")
# docs = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=200)
# docs = text_splitter.split_documents(docs)

# embeddings = embedding_function.embed_documents([d.page_content for d in docs])

# for i, doc in enumerate(docs):
#     collection.add(embeddings=embeddings[i], ids=[str(uuid.uuid1())], metadatas=doc.metadata, documents=doc.page_content)

db = VectorDB(
    client=client,
    collection_name="Modern_India",
    embedding_func=embedding_function
)

paper = Paper("GS1")



for i in range(4):
    print(f"\n{i}. =====================================================================")
    subject = paper.get_subject()
    topic = subject.get_topic()
    qtype = topic.get_qtype()["type_desc"]
    context = format_docs(db.get_retriever().invoke(f"{topic.desc}"))
    option = random.choice(["a","b","c","d"])
    prompt = basic_prompt.format(subject=f"{subject.name} ({topic.name})", question_type=qtype, system_prompt=context, topic=random.choice(topic.desc),option=option)
    
    response = llama.invoke(prompt)
    #qtype= response

    print(response)

class QuestGen:

    def __init__(self, inference_endpoint: str, mode: str, name:str):
        self.inference_endpoint = inference_endpoint
        self.mode = mode
        self.papier = 

    def generate_question(self):
        if self.mode=="full":



        
