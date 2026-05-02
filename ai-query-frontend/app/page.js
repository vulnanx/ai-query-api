// app/page.js
"use client";

import { useState, useRef, useEffect } from "react";

const API_URL = "http://localhost:8000/query";

export default function Home() {

  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");

  // isLoading: true while we are waiting for the backend to respond
  const [isLoading, setIsLoading] = useState(false);

  // errorText: stores an error message if something goes wrong
  const [errorText, setErrorText] = useState("");

  // messagesEndRef: a reference to an invisible div at the bottom of the chat
  // We use this to automatically scroll down when new messages arrive
  const messagesEndRef = useRef(null);

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    const trimmedInput = inputText.trim();
    if (!trimmedInput) return;

    // Clear any previous error
    setErrorText("");

    const userMessage = { role: "user", content: trimmedInput };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");

    // Show the loading indicator
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmedInput }),
      });

      // Check if the HTTP status code indicates an error (4xx or 5xx)
      if (!response.ok) {
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const assistantMessage = { role: "assistant", content: data.message };
      setMessages((prev) => [...prev, assistantMessage]);

    } catch (error) {
      console.error("Error calling backend:", error);
      // Show the error to the user
      setErrorText(
        error.message.includes("Failed to fetch")
          ? "Cannot connect to the backend. Is your FastAPI server running on port 8000?"
          : `Error: ${error.message}`
      );
    } finally {
      // Always hide the loading indicator when done (success or error)
      setIsLoading(false);
    }
  }

  function handleKeyDown(e) {
    // Allow Enter to send, but not while loading
    if (e.key === "Enter" && !isLoading) {
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

          {messages.length === 0 && !isLoading && (
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

          {/* Loading indicator — shown while waiting for the backend */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1 items-center">
                  {/* Three bouncing dots */}
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
                </div>
              </div>
            </div>
          )}

          {/* Error message — shown when something goes wrong */}
          {errorText && (
            <div className="flex justify-center">
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm max-w-[90%]">
                ⚠️ {errorText}
              </div>
            </div>
          )}

          {/* Invisible element at the bottom — used for auto-scrolling */}
          <div ref={messagesEndRef} />

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
            // Disable the input while loading
            disabled={isLoading}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2  text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <button
            onClick={sendMessage}
            // Disable the button while loading
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>
      </footer>

    </div>
  );
}