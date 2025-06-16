from retriever.vector_store import get_vectorstore
from memory.conversation import get_memory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI  # Replace with Ollama if needed
from langchain_community.llms import Ollama


def get_rag_chain():
    retriever = get_vectorstore().as_retriever()
    memory = get_memory()

    template = '''
You are a helpful assistant that recommends activities based on the user's past and current inputs.

Context:
{context}

Chat History:
{chat_history}

User: {question}
Assistant:
'''
    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=template,
    )

    # llm = OpenAI(temperature=0.5)
    llm = Ollama(model="llama2")
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    return chain

