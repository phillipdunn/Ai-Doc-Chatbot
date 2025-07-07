import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

app = Flask(__name__)
CORS(app)

def create_llamma_index():
    try:
        index_dir='index'
        os.makedirs(index_dir, exist_ok=True)
    
        # import gpt stuff
        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
        # read and index documents
        documents = SimpleDirectoryReader('uploads').load_data() 
        # create vector store index
        index = VectorStoreIndex(documents) 
        # stores this index in the specified directory
        index.storage_context.persist(persist_dir=index_dir)
        # check if index is empty
        if not os.path.exists(index_dir) or not os.listdir(index_dir):
            return jsonify({'error': 'Index not created'}), 400
    
        return jsonify({'message': 'File indexed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# creates a custom prompt to be used in quering the index
def get_custom_prompt():
    try:
        from llama_index.prompts import Prompt
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
    except Exception as e:
        # If an error occurs during the try block, catch it here
        return jsonify({'error':  f"An error occurred: {e}"})

# creates chat history
def getChatHistory(history='[]'):
    try:
        from llama_index.llms import ChatMessage, MessageRole
        history = json.loads(history)

        # initialize chart history
        custom_chat_history = []
        roles = {"left_bubble": "ASSISTANT", "right_bubble": "USER"}
        for chat in history:
            position = chat['position']
            role = MessageRole[roles[position]]
            content = chat['message']
            custom_chat_history.append(
                ChatMessage(
                    # can be USER or ASSISTANT
                    role=role,
                    content=content
                )
            )
        return custom_chat_history
    except Exception as e:
        # If an error occurs during the try block, catch it here
        return jsonify({'error':  f"An error occurred: {e}"})
    
        
def query_index():
    # retrive open ai key
    try:
        from llama_index.core import StorageContext, load_index_from_storage
        from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
      
        index_dir = 'index'

        if not os.path.exists(index_dir) or not os.listdir(index_dir):
            return jsonify({'error':  f"Index directory '{index_dir}' does not exist or is empty."})
        data = request.get_json()
        prompt = data.get('prompt')
        chatHistory = data.get('chatHistory')
        
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        
        # TODO query engine not working
        query_engine = index.as_query_engine()
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=get_custom_prompt(),
            chat_history=getChatHistory(chatHistory),
            verbose=True
        )
        
        response_node = chat_engine.chat(prompt)  # chat here
        print('res',response_node)
        return jsonify({'result':  response_node.response})
    

    except Exception as e:
        return jsonify({'error':  f"An error occurred: {e}"})
    
@app.route('/ask_ai', methods=['POST'])
def query_endpoint():
    response = query_index()
    return response      
  
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        file.save(os.path.join(upload_dir, file.filename))
        return create_llamma_index()


if __name__ == '__main__':
    app.run(debug=True)
