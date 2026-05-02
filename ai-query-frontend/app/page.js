// app/page.js
"use client";

// Import the useState hook from React
import { useState } from "react";

export default function Home() {

  // --- STATE ---
  // messages: an array of message objects. Each object has:
  //   role: "user" or "assistant"
  //   content: the text of the message
  const [messages, setMessages] = useState([
    // These are example messages so you can see how the UI looks.
    // We will remove them in Milestone 4 when real messages come in.
    { role: "user", content: "What is the capital of France?" },
    { role: "assistant", content: "The capital of France is Paris." },
    { role: "user", content: "Classify this review as Positive or Negative: The food was amazing!" },
    { role: "assistant", content: "Category: Positive" },
  ]);

  // inputText: the current value of the text input
  const [inputText, setInputText] = useState("");

  return (
    <div className="flex flex-col h-screen bg-gray-50">

      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl font-semibold text-gray-800">AI Query Chat</h1>
        <p className="text-sm text-gray-500">Powered by your FastAPI backend</p>
      </header>

      {/* Message area */}
      <main className="flex-1 overflow-y-auto px-6 py-4">
        <div className="max-w-3xl mx-auto space-y-4">

          {/* If there are no messages, show a placeholder */}
          {messages.length === 0 && (
            <p className="text-gray-400 text-center mt-8">
              No messages yet. Type something below to start.
            </p>
          )}

          {/* Loop through each message and render it */}
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

      {/* Input area */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3 max-w-3xl mx-auto">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors">
            Send
          </button>
        </div>
      </footer>

    </div>
  );
}