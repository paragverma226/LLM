
# 🎯 RAG Chatbot using LangChain + Streamlit

This project is a **Retrieval-Augmented Generation (RAG)** chatbot built with [LangChain](https://www.langchain.com/) and [Streamlit](https://streamlit.io/). It uses semantic search over a corpus of activity suggestions and generates short, personalized responses using a language model.

You can use either **OpenAI GPT models** or local LLMs like **LLaMA2 via Ollama**.

---

## 🧠 What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It improves the accuracy of language models by:
1. **Retrieving** the most relevant documents based on a user query
2. **Augmenting** the prompt with those documents
3. **Generating** an answer using a language model (LLM)

---

## 📦 Features

✅ Activity recommendation chatbot  
✅ Multi-turn memory (remembers previous messages)  
✅ Vector similarity search using `FAISS`  
✅ HuggingFace embeddings  
✅ Modular, production-ready Python structure  
✅ Optional Ollama (local LLM) support  

---

## 🏁 Prerequisites

- Python 3.8+
- OpenAI API Key (if using GPT models) or Ollama (for local models)

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot/rag_app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Chatbot
```bash
streamlit run main.py
```

---

## 🔁 Using a Local Model (Optional)

To use **LLaMA2 locally via Ollama**:

### 1. Install Ollama  
[https://ollama.com/download](https://ollama.com/download)

### 2. Pull the model
```bash
ollama pull llama2
```

### 3. Update `rag_chain.py`:
Replace:
```python
from langchain.llms import OpenAI
llm = OpenAI(temperature=0.5)
```
With:
```python
from langchain_community.llms import Ollama
llm = Ollama(model="llama2")
```

---

## 📁 Project Structure

```
rag_app/
├── main.py                        # Entry point for Streamlit
├── app/chat.py                   # UI logic
├── chains/rag_chain.py           # RAG pipeline logic
├── memory/conversation.py        # Memory for chat history
├── retriever/vector_store.py     # FAISS + embeddings
├── requirements.txt              # Dependencies
└── .streamlit/config.toml        # Streamlit config
```

---

## ✨ Example Questions

- "I want to relax and enjoy some nature."
- "What can I do with friends and food?"
- "I’m looking for something exciting outdoors."

---

## 🧠 Technologies Used

- LangChain
- Streamlit
- FAISS
- HuggingFace Transformers
- OpenAI API / Ollama
- SentenceTransformers for embeddings

---

## 📌 To-Do (Optional Enhancements)

- ✅ Add PDF/CSV/Text file loader
- ✅ Deploy as FastAPI REST API
- ✅ Add chat history persistence
- ✅ Integrate with Pinecone or Qdrant
- ✅ Support images or multi-modal inputs

---

## 📃 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙋‍♂️ Need Help?

Open an issue or contact [parag_verma226@yahoo.com](mailto:parag_verma226@yahoo.com)

Happy building! 🚀
