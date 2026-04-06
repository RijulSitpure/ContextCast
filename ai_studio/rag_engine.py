import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

def get_context_from_pdf(pdf_path, query):
    if not os.path.exists(pdf_path):
        return "No PDF found. Defaulting to general knowledge."
    
    print(f"--- 📂 Analyzing PDF: {pdf_path} ---")
    
    # 1. Load and Split
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    chunks = text_splitter.split_documents(pages)
    
    # 2. Vectorize (Create a local database in RAM)
    embeddings = FastEmbedEmbeddings()
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    
    # 3. Retrieve the top 3 most relevant sections
    search_results = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in search_results])
    
    return context