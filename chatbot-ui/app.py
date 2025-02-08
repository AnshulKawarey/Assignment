from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import WebBaseLoader
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (React frontend)

# Set USER_AGENT (Fixes LangChain warning)
os.environ["USER_AGENT"] = "MyChatbot/1.0"

# Step 1: Load data from the given URL
url = "https://brainlox.com/courses/category/technical"
loader = WebBaseLoader(url)
documents = loader.load()

# Step 2: Split text for better embedding representation
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

# Step 3: Create embeddings and store in a vector database
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Explicit model
vector_store = FAISS.from_documents(split_docs, embeddings)
retriever = vector_store.as_retriever()

# Step 4: Create a Langchain QA Chain
llm = ChatGroq(temperature=0, model_name="mixtral-8x7b")  # Explicit model
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "Query parameter is missing"}), 400

    response = qa_chain.run(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Ensure Flask runs on port 5000
