import { useEffect, useState, useRef } from "react";
import "./App.css";

function App() {
  const chatBodyRef = useRef<HTMLDivElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<string[]>([]);

  const [activeTab, setActiveTab] = useState<"documents" | "chat">("chat");

  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/documents/");

      const data = await response.json();

      setDocuments(data.documents);
    } catch (error) {
      console.error("Failed to fetch documents:", error);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a document first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      console.log("Upload successful:", data);
      await fetchDocuments();
      alert(`Uploaded: ${data.filename}`);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Document upload failed.");
    }
  };

  const handleAsk = async () => {
  if (!query.trim()) {
    return;
  }

  const userQuery = query;

  setLoading(true);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/orders/agent?query=${encodeURIComponent(userQuery)}`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuery,
      },
      {
        role: "assistant",
        content: data.answer,
      },
    ]);

    setQuery("");
  } catch (error) {
    console.error("Ask error:", error);
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AI Business Agent</h1>
          <p>Business Knowledge & Support</p>
        </div>

        <nav>
          <button
            className={`nav-btn ${activeTab === "documents" ? "active" : ""}`}
            onClick={() => setActiveTab("documents")}
          >
            Documents
          </button>

          <button
            className={`nav-btn ${activeTab === "chat" ? "active" : ""}`}
            onClick={() => setActiveTab("chat")}
          >
            Chat
          </button>
        </nav>
      </header>

      <main className="container">
        {activeTab === "documents" ? (
          <>
            <section className="page-heading">
              <h2>Knowledge Base</h2>
              <p>
                Upload company documents to give your AI agent business
                knowledge.
              </p>
            </section>

            <section className="upload-card">
              <div className="upload-icon">↑</div>

              <h3>Upload a company document</h3>

              <p>
                Upload PDF, TXT or DOCX files containing your company's
                information, policies or FAQs.
              </p>

              <label className="file-input">
                <span>Choose File</span>
                <input
                  type="file"
                  accept=".pdf,.txt,.docx"
                  onChange={(e) => {
                    const file = e.target.files?.[0] || null;
                    setSelectedFile(file);
                  }}
                />
              </label>

              {selectedFile && (
                <p className="selected-file">Selected: {selectedFile.name}</p>
              )}

              <button className="upload-btn" onClick={handleUpload}>
                Upload Document
              </button>
            </section>

            <section className="documents-card">
              <div className="section-header">
                <div>
                  <h3>Uploaded Documents</h3>
                  <p>Your company's knowledge base</p>
                </div>

                <span className="document-count">
                  {documents.length} Documents
                </span>
              </div>

              {documents.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">📄</div>
                  <h3>No documents yet</h3>
                  <p>
                    Upload your first company document to start building the
                    knowledge base.
                  </p>
                </div>
              ) : (
                <div>
                  {documents.map((document) => (
                    <div key={document} className="document-item">
                      📄 {document}
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        ) : (
          <>
            <div className="chat-card">
              {/* <div className="chat-header">
    <h2>Business Support Agent</h2>
    <p>Ask questions about your company's knowledge base.</p>
  </div> */}

              <div className="chat-body" ref={chatBodyRef}>
                {messages.length === 0 ? (
                  <div className="chat-empty">
                    <div className="empty-icon">💬</div>
                    <h3>Ask your business question</h3>
                    <p>
                      Your AI agent will search the company knowledge base and
                      answer your question.
                    </p>
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
                        {/* 0000000 */}

                        <div className="message-text">{message.content}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="chat-input-area">
                <input
                  type="text"
                  placeholder="Ask a question..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleAsk();
                    }
                  }}
                />

                <button onClick={handleAsk} disabled={loading}>
                  {loading ? "Thinking..." : "Ask"}
                </button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
