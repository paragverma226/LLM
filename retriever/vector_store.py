from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

def get_vectorstore():
    documents = [
        "Take a leisurely walk in the park and enjoy the fresh air.",
        "Visit a local museum and discover something new.",
        "Attend a live music concert and feel the rhythm.",
        "Go for a hike and admire the natural scenery.",
        "Have a picnic with friends and share some laughs.",
        "Explore a new cuisine by dining at an ethnic restaurant.",
    ]
    docs = [Document(page_content=doc) for doc in documents]
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return vectorstore
