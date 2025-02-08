import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("darkMode") === "true"
  );
  const chatEndRef = useRef(null);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("darkMode", darkMode);
  }, [darkMode]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages([...messages, userMessage]);
    setInput("");

    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        query: input,
      });

      if (response.status === 200) {
        const botMessage = { sender: "bot", text: response.data.response };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: "⚠️ Server error! Try again." },
      ]);
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      className={`flex flex-col h-screen transition-all ${
        darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-black"
      }`}
    >
      {/* Header */}
      <header className="flex justify-between items-center p-4 shadow-md transition-all bg-blue-600 text-white dark:bg-gray-800">
        <h1 className="text-2xl font-bold">Chatbot</h1>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-full transition-all focus:outline-none"
        >
          {darkMode ? "🌞" : "🌙"}
        </button>
      </header>

      {/* Chat Window */}
      <main className="flex-1 overflow-y-auto p-6 transition-all">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`p-3 w-fit max-w-lg rounded-lg shadow-md transition-all ${
                msg.sender === "user"
                  ? "ml-auto bg-blue-500 text-white"
                  : darkMode
                  ? "mr-auto bg-gray-700 text-white"
                  : "mr-auto bg-gray-300 text-black"
              }`}
            >
              {/* Render markdown using ReactMarkdown */}
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </motion.div>
          ))}
          <div ref={chatEndRef} />
        </div>
      </main>

      {/* Input Field */}
      <footer className="p-4 bg-white dark:bg-gray-800 shadow-md flex items-center space-x-2 border-t border-gray-300 dark:border-gray-600">
        <input
          type="text"
          value={input}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border border-gray-400 p-3 rounded-lg dark:border-gray-600 dark:bg-gray-700 dark:text-white"
          placeholder="Type a message..."
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-all"
        >
          Send
        </button>
      </footer>
    </div>
  );
}

export default App;
