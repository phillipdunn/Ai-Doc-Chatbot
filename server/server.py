import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import os


# set = os.environ.get("OPENAI_API_KEY")

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
    
# @app.route('/')   
# def index():
#     return create_llamma_index() 
    
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
