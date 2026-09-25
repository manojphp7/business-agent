import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const handleUpload = async () => {
  if (!selectedFile) {
    alert("Please select a document first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/documents/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Upload failed");
    }

    console.log("Upload successful:", data);
    alert(`Uploaded: ${data.filename}`);
  } catch (error) {
    console.error("Upload error:", error);
    alert("Document upload failed.");
  }
};


  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AI Business Agent</h1>
          <p>Business Knowledge & Support</p>
        </div>

        <nav>
          <button className="nav-btn active">Documents</button>
          <button className="nav-btn">Chat</button>
        </nav>
      </header>

      <main className="container">
        <section className="page-heading">
          <h2>Knowledge Base</h2>
          <p>
            Upload company documents to give your AI agent business knowledge.
          </p>
        </section>

        <section className="upload-card">
          <div className="upload-icon">↑</div>

          <h3>Upload a company document</h3>

          <p>
            Upload PDF, TXT or DOCX files containing your company's information,
            policies or FAQs.
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

            <span className="document-count">0 Documents</span>
          </div>

          <div className="empty-state">
            <div className="empty-icon">📄</div>
            <h3>No documents yet</h3>
            <p>
              Upload your first company document to start building the knowledge
              base.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
