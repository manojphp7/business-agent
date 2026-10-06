import { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";
const AGENT_KEY = "abc_7f82k9_agent";

type Document = {
  filename: string;
  size: number;
  modified_at: number;
};

function AdminUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  // Load uploaded documents
  const loadDocuments = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/documents/?agent_key=${encodeURIComponent(AGENT_KEY)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load documents");
      }

      setDocuments(data.documents || []);
    } catch (error) {
      console.error("Documents error:", error);
      setMessage("Unable to load documents.");
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleDelete = async (filename: string) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${filename}"?`
    );

    if (!confirmed) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/documents/${encodeURIComponent(
          filename
        )}?agent_key=${encodeURIComponent(AGENT_KEY)}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Delete failed");
      }

      setMessage(`${filename} deleted successfully.`);

      await loadDocuments();
    } catch (error) {
      console.error("Delete error:", error);

      setMessage(
        error instanceof Error ? error.message : "Unable to delete document."
      );
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF file.");
      return;
    }

    if (file.type !== "application/pdf") {
      setMessage("Only PDF files are allowed.");
      return;
    }

    setUploading(true);
    setMessage("");

    const formData = new FormData();

    formData.append("file", file);
    formData.append("agent_key", AGENT_KEY);

    try {
      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setMessage(`Upload successful. ${data.total_chunks} chunks created.`);

      setFile(null);

      // Refresh document list
      await loadDocuments();
    } catch (error) {
      console.error("Upload error:", error);

      setMessage(
        error instanceof Error ? error.message : "Unable to upload document."
      );
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "50px auto",
        fontFamily: "Arial",
      }}
    >
      {/* Upload Section */}

      <div
        style={{
          padding: "30px",
          borderRadius: "12px",
          boxShadow: "0 5px 20px rgba(0,0,0,0.15)",
        }}
      >
        <h2>Admin Document Upload</h2>

        <p>Upload company policy or knowledge-base PDF.</p>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            setFile(e.target.files?.[0] || null);
            setMessage("");
          }}
        />

        {file && (
          <p>
            Selected: <strong>{file.name}</strong>
          </p>
        )}

        <button
          onClick={handleUpload}
          disabled={uploading || !file}
          style={{
            marginTop: "15px",
            padding: "10px 20px",
            border: "none",
            borderRadius: "6px",
            background: "#111827",
            color: "white",
            cursor: uploading || !file ? "not-allowed" : "pointer",
            opacity: uploading || !file ? 0.6 : 1,
          }}
        >
          {uploading ? "Uploading..." : "Upload PDF"}
        </button>

        {message && <p style={{ marginTop: "15px" }}>{message}</p>}
      </div>

      {/* Documents List */}

      <div
        style={{
          marginTop: "30px",
          padding: "25px",
          borderRadius: "12px",
          boxShadow: "0 5px 20px rgba(0,0,0,0.12)",
        }}
      >
        <h2>Uploaded Documents</h2>

        {documents.length === 0 ? (
          <p>No documents uploaded yet.</p>
        ) : (
          <div>
            {documents.map((document) => (
              <div
                key={document.filename}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: "20px",
                  padding: "15px",
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                {/* File Information */}
                <div
                  style={{
                    flex: 1,
                    minWidth: 0,
                  }}
                >
                  <strong
                    style={{
                      display: "block",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                    title={document.filename}
                  >
                    📄 {document.filename}
                  </strong>

                  <div
                    style={{
                      fontSize: "13px",
                      color: "#6b7280",
                      marginTop: "5px",
                    }}
                  >
                    {formatFileSize(document.size)}
                  </div>
                </div>

                {/* Actions */}
                <div
                  style={{
                    display: "flex",
                    gap: "8px",
                    flexShrink: 0,
                  }}
                >
                  <button
                    style={{
                      padding: "7px 14px",
                      border: "1px solid #d1d5db",
                      borderRadius: "6px",
                      background: "white",
                      cursor: "pointer",
                    }}
                  >
                    Download
                  </button>

                  <button
                    onClick={() => handleDelete(document.filename)}
                    style={{
                      padding: "7px 14px",
                      border: "none",
                      borderRadius: "6px",
                      background: "#dc2626",
                      color: "white",
                      cursor: "pointer",
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminUpload;
