import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

type Message = {
  role: "user" | "assistant";
  content: string;
};

function App() {
  const chatBodyRef = useRef<HTMLDivElement | null>(null);

  const [isOpen, setIsOpen] = useState(true);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async (question?: string) => {
    const userQuery = (question ?? query).trim();

    if (!userQuery || loading) {
      return;
    }

    setLoading(true);

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuery,
      },
    ]);

    setQuery("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/agent/?query=${encodeURIComponent(userQuery)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      console.error("Ask error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't process your request right now.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop =
        chatBodyRef.current.scrollHeight;
    }
  }, [messages, loading]);

  return (
    <div className="app">

      {/* Demo page content */}
      <div className="page-content">
        <h1>ABC Technologies</h1>
        <p>Welcome to our website.</p>
      </div>

      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          className="chat-floating-button"
          onClick={() => setIsOpen(true)}
        >
          💬
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">

          {/* Header */}
          <div className="chat-header">
            <div className="chat-agent-info">
              <div className="agent-avatar">
                AI
              </div>

              <div>
                <h2>Business Support</h2>

                <div className="online-status">
                  <span className="online-dot"></span>
                  Online
                </div>
              </div>
            </div>

            <button
              className="close-button"
              onClick={() => setIsOpen(false)}
            >
              ×
            </button>
          </div>

          {/* Chat Body */}
          <div
            className="chat-body"
            ref={chatBodyRef}
          >
            {messages.length === 0 ? (
              <div className="chat-empty">

                <div className="welcome-icon">
                  ✦
                </div>

                <h3>
                  Hi! How can I help?
                </h3>

                <p>
                  Ask me about policies, products,
                  shipping, refunds or your order.
                </p>

                <div className="suggestions">

                  <button
                    onClick={() =>
                      handleAsk(
                        "What is your refund policy?"
                      )
                    }
                  >
                    Refund policy
                  </button>

                  <button
                    onClick={() =>
                      handleAsk(
                        "What is your shipping policy?"
                      )
                    }
                  >
                    Shipping policy
                  </button>

                  <button
                    onClick={() =>
                      handleAsk(
                        "What is the status of order 1001?"
                      )
                    }
                  >
                    Order status
                  </button>

                </div>
              </div>
            ) : (
              <div className="conversation">

                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`message ${
                      message.role === "user"
                        ? "user-message"
                        : "ai-message"
                    }`}
                  >
                    {message.role === "assistant" && (
                      <div className="message-avatar">
                        AI
                      </div>
                    )}

                    <div className="message-text">
                      {message.content}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="message ai-message">
                    <div className="message-avatar">
                      AI
                    </div>

                    <div className="typing">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                )}

              </div>
            )}
          </div>

          {/* Input */}
          <div className="chat-input-area">

            <input
              type="text"
              placeholder="Ask something..."
              value={query}
              onChange={(e) =>
                setQuery(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleAsk();
                }
              }}
            />

            <button
              onClick={() => handleAsk()}
              disabled={loading || !query.trim()}
            >
              ➤
            </button>

          </div>

        </div>
      )}

    </div>
  );
}

export default App;