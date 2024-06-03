from dotenv import load_dotenv # type: ignore
load_dotenv()
from typing import Any, List, Tuple
from pypdf import PdfReader # type: ignore
from langchain.schema.document import Document # type: ignore
from langchain_openai import OpenAIEmbeddings # type: ignore
# from langchain_community.embeddings import HuggingFaceEmbeddings
# https://python.langchain.com/v0.1/docs/integrations/vectorstores/pinecone/
from langchain_pinecone import PineconeVectorStore # type: ignore
from langchain_openai import OpenAI # type: ignore
from langchain.chains.summarize import load_summarize_chain # type: ignore

from dotenv import load_dotenv # type: ignore
load_dotenv()

import streamlit as st
import os
os.environ['OPENAI_API_KEY']=st.secrets['OPENAI_API_KEY']
os.environ['PINECONE_API_KEY']=st.secrets['PINECONE_API_KEY']
pinecone_index_name= st.secrets['PINECONE_INDEX_NAME']




#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



# iterate over files in 
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list, unique_id):
    docs=[]
    for filename in user_pdf_list:
        
        chunks=get_pdf_text(filename)

        #Adding items to our list - Adding data & its metadata
        docs.append(Document(
            page_content=chunks,
            metadata={"name": filename.name,"id":filename.file_id,"type=":filename.type,"size":filename.size,"unique_id":unique_id},
        ))

    return docs


#Create embeddings instance
def create_embeddings_load_data():
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings


#Function to push data to Vector Store - Pinecone here
def push_to_pinecone(embeddings,docs,pinecone_index_name=pinecone_index_name):
    vectordb = PineconeVectorStore.from_documents(docs, embeddings, index_name=pinecone_index_name)
    return vectordb

def similar_docs(vectordb: object, query: str, k: int, unique_id: Any) -> List[Tuple[Any, float]]:
    similar_docs = vectordb.similarity_search_with_score(query,int(k),{"unique_id":unique_id})
    return similar_docs

# Helps us get the summary of a document
def get_summary(current_doc):
    llm = OpenAI(temperature=0)
    #llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.invoke([current_doc])
    return summary




    