from flask import Flask, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from flask_cors import CORS
import re

load_dotenv()
os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "MyChatbot/1.0")

app = Flask(__name__)
CORS(app)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

#Loading data from the URL
url = "https://brainlox.com/courses/category/technical"
loader = WebBaseLoader(url)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(split_docs, embeddings)
retriever = vector_store.as_retriever()

#Selecting the model
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0.4)
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

#Chat endpoint api call
# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("query")
#     if not user_input:
#         return jsonify({"error": "Query parameter is missing"}), 400
    
#     response = qa_chain.run(user_input)
#     return jsonify({"response": response})

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "Query parameter is missing"}), 400

    response = qa_chain.invoke(user_input)

    # Process the response line by line for better formatting
    lines = response.splitlines()
    formatted_lines = []
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # If line already starts with bold markers, leave it
        if line.strip().startswith("**"):
            formatted_lines.append(line)
            continue

        # Try to find a delimiter (either " (" or " -")
        # This regex captures text until either " (" or " -"
        m = re.search(r"^(.*?)(\s*(\(|-))", line)
        if m:
            title = m.group(1).strip()
            rest = line[len(title):]
            # Wrap the title in bold markers
            formatted_line = f"**{title}**{rest}"
            formatted_lines.append(formatted_line)
        else:
            formatted_lines.append(line)

    formatted_response = "\n\n".join(formatted_lines)
    return jsonify({"response": formatted_response})

if __name__ == "__main__":
    app.run(debug=True)
