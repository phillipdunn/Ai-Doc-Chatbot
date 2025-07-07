# 🧠 LlamaIndex Flask AI Chat Backend

This is a Flask-based backend API that allows you to upload documents, index them using **LlamaIndex**, and interact with them through a conversational interface powered by OpenAI.

---

## 🚀 Features

- Upload a document (`.txt`, `.pdf`, etc.)
- Automatically index it using `LlamaIndex`
- Ask questions with conversational history
- Uses OpenAI's GPT model to provide contextual responses

---

## 📦 Requirements

- Python 3.8+
- OpenAI API key

---

## 🔧 Running Instructions

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install flask flask-cors requests llama-index openai

python server.py
