import { useEffect, useRef, useState } from "react";
import AdminUpload from "./AdminUpload";
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
    <>
      <AdminUpload />
    </>
  );
}

export default App;