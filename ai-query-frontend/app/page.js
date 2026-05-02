// app/page.js

// "use client" tells Next.js this component runs in the browser (not on the server).
// We need this because we will use React hooks like useState, which only work client-side.
"use client";

export default function Home() {
  return (
    // The outer container fills the full screen height and uses a flex column layout
    <div className="flex flex-col h-screen bg-gray-50">

      {/* Header bar at the top */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl font-semibold text-gray-800">AI Query Chat</h1>
        <p className="text-sm text-gray-500">Powered by your FastAPI backend</p>
      </header>

      {/* Message area — takes up all remaining space */}
      <main className="flex-1 overflow-y-auto px-6 py-4">
        {/* We will put messages here in a later milestone */}
        <p className="text-gray-400 text-center mt-8">
          No messages yet. Type something below to start.
        </p>
      </main>

      {/* Input area pinned to the bottom */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3 max-w-3xl mx-auto">
          <input
            type="text"
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