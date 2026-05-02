// app/page.js
"use client";

import { useState } from "react";

// The URL of your FastAPI backend endpoint
const API_URL = "http://localhost:8000/query";

export default function Home() {

  // Start with an empty conversation (remove the sample messages)
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");

  // --- SEND MESSAGE FUNCTION ---
  // This function runs when the user clicks Send or presses Enter
  async function sendMessage() {

    // 1. Do nothing if the input is empty or just whitespace
    const trimmedInput = inputText.trim();
    if (!trimmedInput) return;

    // 2. Add the user's message to the conversation immediately
    //    We use the functional form of setMessages to always work with the latest state
    const userMessage = { role: "user", content: trimmedInput };
    setMessages((prev) => [...prev, userMessage]);

    // 3. Clear the input box
    setInputText("");

    // 4. Call the FastAPI backend
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: trimmedInput }),
      });

      // 5. Parse the JSON response
      const data = await response.json();

      // 6. Add the AI's response to the conversation
      const assistantMessage = { role: "assistant", content: data.message };
      setMessages((prev) => [...prev, assistantMessage]);

    } catch (error) {
      // 7. If something went wrong, add an error message to the chat
      console.error("Error calling backend:", error);
      const errorMessage = {
        role: "assistant",
        content: "Sorry, I could not reach the backend. Please check that your FastAPI server is running.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  }

  // Allow sending with the Enter key
  function handleKeyDown(e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">

      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl font-semibold text-gray-800">AI Query Chat</h1>
        <p className="text-sm text-gray-500">Powered by your FastAPI backend</p>
      </header>

      <main className="flex-1 overflow-y-auto px-6 py-4">
        <div className="max-w-3xl mx-auto space-y-4">

          {messages.length === 0 && (
            <p className="text-gray-400 text-center mt-8">
              No messages yet. Type something below to start.
            </p>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  message.role === "user"
                    ? "bg-blue-600 text-white rounded-br-sm"
                    : "bg-white text-gray-800 border border-gray-200 rounded-bl-sm"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}

        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3 max-w-3xl mx-auto">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Send
          </button>
        </div>
      </footer>

    </div>
  );
}