import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import constants

# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

from llama_index.core import VectorStoreIndex, download_loader, StorageContext, load_index_from_storage
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.prompts import Prompt
from llama_index.core.llms import ChatMessage, MessageRole
import traceback

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = 'uploads'
INDEX_DIR = 'index'

def create_llama_index():
    try:
        print("Creating directories...")
        os.makedirs(INDEX_DIR, exist_ok=True)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        documents = []

        for filename in os.listdir(UPLOAD_DIR):
            filepath = os.path.join(UPLOAD_DIR, filename)
            print(f"Processing file: {filename}")

            if filename.endswith('.docx'):
                print("Using DocxReader...")
                DocxReader = download_loader("DocxReader")
                loader = DocxReader()
                docs = loader.load_data(file=filepath)
                print(f"Loaded {len(docs)} documents from DOCX")
                documents.extend(docs)

            elif filename.endswith('.txt'):
                print("Using SimpleDirectoryReader...")
                from llama_index.core import SimpleDirectoryReader
                reader = SimpleDirectoryReader(input_files=[filepath])
                docs = reader.load_data()
                print(f"Loaded {len(docs)} documents from TXT")
                documents.extend(docs)

            else:
                print(f"Unsupported file format: {filename}")

        if not documents:
            return jsonify({'error': 'No supported documents found'}), 400

        print("Creating index...")
        index = VectorStoreIndex(documents)
        index.storage_context.persist(persist_dir=INDEX_DIR)

        print("Indexing complete.")
        return jsonify({'message': 'File indexed successfully'})

    except Exception as e:
        print("❌ Exception occurred:")
        traceback.print_exc()
        return jsonify({'error': f"Indexing failed: {str(e)}"}), 500



def get_custom_prompt():
    return Prompt("""\
Rephrase the conversation and subsequent message into 
a self-contained question while including all relevant details. 
Conclude the question with: Only refer to this document.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")


def get_chat_history(history='[]'):
    try:
        history = json.loads(history)
        custom_chat_history = []
        roles = {"left_bubble": "ASSISTANT", "right_bubble": "USER"}
        for chat in history:
            position = chat.get('position')
            role = MessageRole[roles.get(position, "USER")]
            content = chat.get('message', '')
            custom_chat_history.append(ChatMessage(role=role, content=content))
        return custom_chat_history
    except Exception as e:
        raise ValueError(f"Invalid chat history format: {e}")


def query_index():
    try:
        if not os.path.exists(INDEX_DIR) or not os.listdir(INDEX_DIR):
            return jsonify({'error': f"Index directory '{INDEX_DIR}' does not exist or is empty."}), 400

        data = request.get_json()
        prompt = data.get('prompt')
        chat_history = data.get('chatHistory', '[]')

        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context)

        query_engine = index.as_query_engine()
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=get_custom_prompt(),
            chat_history=get_chat_history(chat_history),
            verbose=True
        )

        response_node = chat_engine.chat(prompt)
        return jsonify({'result': response_node.response})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500


@app.route('/ask_ai', methods=['POST'])
def query_endpoint():
    return query_index()


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    return create_llama_index()


if __name__ == '__main__':
    app.run(debug=True)
