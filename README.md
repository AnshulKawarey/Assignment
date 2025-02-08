# Chatbot Project

This project implements a chatbot that uses a Flask backend powered by LangChain and ChatGroq, and a React frontend that displays a dynamic chat interface with markdown-rendered responses.

## Project Overview

- **Backend:**  
  Uses Flask along with LangChain for retrieval-augmented generation. The backend:
  - Loads data from a technical courses webpage using `WebBaseLoader`.
  - Splits and processes the text with `RecursiveCharacterTextSplitter`.
  - Creates embeddings with `HuggingFaceEmbeddings` and stores them in a FAISS vector store.
  - Sets up a retrieval-based QA chain using `RetrievalQA` with ChatGroq.
  - Formats responses in Markdown for improved readability.
  - Provides a `/chat` endpoint to process chat requests.

- **Frontend:**  
  Uses React to create a modern, responsive chat UI. The frontend:
  - Sends user queries to the Flask backend via axios.
  - Receives responses and renders them using `ReactMarkdown` for proper markdown formatting.
  - Supports dark mode and a dynamic layout with smooth animations using Framer Motion.

## Backend Setup

### Required Libraries

The backend requires the following Python libraries:

- **Flask** – Web framework  
- **Flask-CORS** – Enable CORS for cross-origin requests  
- **python-dotenv** – Load environment variables from a `.env` file  
- **langchain_community.document_loaders** – For loading documents from web URLs  
- **langchain_huggingface** – For HuggingFaceEmbeddings  
- **langchain_community.vectorstores** – For FAISS vector store  
- **langchain.text_splitter** – For splitting documents  
- **langchain.chains** – For RetrievalQA chains  
- **langchain_groq** – For ChatGroq (LLM integration)  
- **re** – For regex formatting  
- **markdown2** – (Optional) For converting markdown if needed  
- **faiss-cpu** – For the FAISS vector store (if not included in langchain dependencies)

#### Installation:

You can install the required libraries using pip. For example, create a `requirements.txt` in the backend folder with the following content:

Flask
flask-cors
python-dotenv
langchain
langchain-huggingface
langchain-groq
markdown2
faiss-cpu

Then run:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the `backend` folder with at least the following variables:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
USER_AGENT=MyChatbot/1.0
```

### Running the Backend

From the `backend` directory, run:

```bash
python app.py
```

The Flask server should start and listen on `http://127.0.0.1:5000`.

## Frontend Setup

### Required Libraries

The frontend requires the following Node/React libraries:

- **axios** – For HTTP requests  
- **framer-motion** – For animations  
- **react-markdown** – For rendering markdown  
- **React** (installed by create-react-app)

#### Installation:

If you haven't created the React app yet, you can do so with Create React App:

```bash
npx create-react-app frontend
cd frontend
npm install axios framer-motion react-markdown
```

### Running the Frontend

From the `frontend` directory, run:

```bash
npm start
```

This will start the React app at `http://localhost:3000`.

## Usage

- **Sending a Message:**  
  Type your message in the input field and press "Enter" or click "Send".  
- **Backend Processing:**  
  The backend `/chat` endpoint processes the query, retrieves relevant data via FAISS and the QA chain, and formats the response in Markdown.
- **Markdown Rendering:**  
  The React frontend uses `ReactMarkdown` to render the formatted markdown (e.g., bold text, bullet lists).


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
(Someone try to fix the formatting of the output as i tried but was getting random * at the start of the lines)
