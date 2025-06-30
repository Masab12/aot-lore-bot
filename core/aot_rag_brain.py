# This script was crafted by Masab Farooque to power our LoreBot
# It's the 'brain' that understands the Attack on Titan world.
# This version uses the Groq API!

import os
from langchain_groq import ChatGroq  
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory

# Let's set up the path to our precious knowledge base
KNOWLEDGE_BASE_PATH = os.path.join("knowledge_base", "aot_lore.txt")

def create_the_rumbling_chain():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("API NOT FOUND")

    founding_titan_llm = ChatGroq(
        api_key=groq_api_key,
        model_name="llama3-8b-8192", 
        temperature=0.1
    )
    loader_from_archives = TextLoader(KNOWLEDGE_BASE_PATH)
    documents_of_eldia = loader_from_archives.load()
    text_splitter_of_ymir = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_texts = text_splitter_of_ymir.split_documents(documents_of_eldia)
   
    the_coordinate_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_titan_storage = FAISS.from_documents(split_texts, the_coordinate_embeddings)

    survey_corps_retriever = vector_titan_storage.as_retriever(search_kwargs={"k": 3})

    titan_shifter_memory = ConversationBufferWindowMemory(
        memory_key="chat_history", 
        return_messages=True,
        k=4
    )

    # 8. The Final Chain of Command (The RAG Chain)
    rumbling_chain = ConversationalRetrievalChain.from_llm(
        llm=founding_titan_llm,
        retriever=survey_corps_retriever,
        memory=titan_shifter_memory,
        chain_type="stuff",
        verbose=False 
    )

    print("The Rumbling Chain is ready and connected via Groq. Dedicate your hearts!")
    return rumbling_chain