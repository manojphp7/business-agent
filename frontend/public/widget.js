(function () {
  const script = document.currentScript;
  const agentKey = script?.getAttribute("data-agent-key");

  if (!agentKey) {
    console.error("AI Agent: data-agent-key is missing");
    return;
  }

  // =========================
  // Conversation State
  // =========================

  let currentOrderId = null;

  // =========================
  // Typing Animation CSS
  // =========================

  const style = document.createElement("style");

  style.textContent = `
    .ai-typing {
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 2px 3px;
    }

    .ai-typing span {
      width: 6px;
      height: 6px;
      background: #6b7280;
      border-radius: 50%;
      display: inline-block;
      animation: aiTyping 1.4s infinite ease-in-out;
    }

    .ai-typing span:nth-child(1) {
      animation-delay: 0s;
    }

    .ai-typing span:nth-child(2) {
      animation-delay: 0.2s;
    }

    .ai-typing span:nth-child(3) {
      animation-delay: 0.4s;
    }

    @keyframes aiTyping {
      0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
      }

      30% {
        transform: translateY(-4px);
        opacity: 1;
      }
    }
  `;

  document.head.appendChild(style);

  // =========================
  // Chat Button
  // =========================

  const button = document.createElement("button");

  button.innerHTML = "💬";

  button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    background: #111827;
    color: white;
    font-size: 24px;
    cursor: pointer;
    z-index: 999999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  `;

  document.body.appendChild(button);

  // =========================
  // Chat Window
  // =========================

  const chat = document.createElement("div");

  chat.style.cssText = `
    position: fixed;
    bottom: 10px;
    right: 20px;
    width: 350px;
    height: 500px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.2);
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 999998;
    font-family: Arial, sans-serif;
  `;

  chat.innerHTML = `
    <div style="
      background:#111827;
      color:white;
      padding:15px;
      font-size:16px;
      font-weight:bold;
      display:flex;
      justify-content:space-between;
      align-items:center;
    ">
      <span>AI Assistant</span>

      <button
        id="ai-chat-close"
        style="
          background:none;
          border:none;
          color:white;
          font-size:22px;
          cursor:pointer;
        "
      >
        ×
      </button>
    </div>

    <div id="ai-chat-messages" style="
      flex:1;
      padding:15px;
      overflow-y:auto;
      background:#f9fafb;
    ">
      <div style="
        background:#e5e7eb;
        color:#111827;
        padding:10px;
        border-radius:8px;
        margin-bottom:10px;
        width:fit-content;
        max-width:80%;
      ">
        Hi! How can I help you?
      </div>
    </div>

    <div style="
      display:flex;
      border-top:1px solid #ddd;
      padding:10px;
    ">
      <input
        id="ai-chat-input"
        type="text"
        placeholder="Type your message..."
        style="
          flex:1;
          padding:10px;
          border:1px solid #ddd;
          border-radius:6px;
          outline:none;
        "
      />

      <button
        id="ai-chat-send"
        style="
          margin-left:8px;
          padding:10px 15px;
          background:#111827;
          color:white;
          border:none;
          border-radius:6px;
          cursor:pointer;
        "
      >
        Send
      </button>
    </div>
  `;

  document.body.appendChild(chat);

  // =========================
  // Elements
  // =========================

  const input = chat.querySelector("#ai-chat-input");
  const sendButton = chat.querySelector("#ai-chat-send");
  const messages = chat.querySelector("#ai-chat-messages");
  const closeButton = chat.querySelector("#ai-chat-close");

  // =========================
  // Open / Close
  // =========================

  button.addEventListener("click", function () {
    chat.style.display = "flex";
    button.style.display = "none";

    input.focus();
  });

  closeButton.addEventListener("click", function () {
    chat.style.display = "none";
    button.style.display = "block";
  });

  // =========================
  // Detect Order ID
  // =========================

  function extractOrderId(message) {
  // 10-digit number is a phone number, not an order ID
  const match = message.match(/\b\d{3,9}\b/);

  if (match) {
    return Number(match[0]);
  }

  return null;
    }
  // =========================
  // Detect Phone Number
  // =========================

  function extractPhone(message) {
    const match = message.match(/\b\d{10}\b/);

    if (match) {
      return match[0];
    }

    return null;
  }

  // =========================
  // Add Typing Indicator
  // =========================

  function createTypingMessage() {
    const typingMessage = document.createElement("div");

    typingMessage.style.cssText = `
      background:#e5e7eb;
      color:#111827;
      padding:10px 14px;
      border-radius:8px;
      margin-bottom:10px;
      width:fit-content;
    `;

    typingMessage.innerHTML = `
      <div class="ai-typing">
        <span></span>
        <span></span>
        <span></span>
      </div>
    `;

    messages.appendChild(typingMessage);

    messages.scrollTop = messages.scrollHeight;

    return typingMessage;
  }

  // =========================
  // Send Message
  // =========================

  async function sendMessage() {
    const message = input.value.trim();

    if (!message || sendButton.disabled) {
      return;
    }

    // =========================
    // Detect Order ID
    // =========================

    const detectedOrderId = extractOrderId(message);

    if (detectedOrderId) {
      currentOrderId = detectedOrderId;
    }

    // =========================
    // Detect Phone
    // =========================

    const detectedPhone = extractPhone(message);

    // =========================
    // Disable Input
    // =========================

    input.disabled = true;
    sendButton.disabled = true;

    sendButton.textContent = "•••";
    sendButton.style.opacity = "0.6";
    sendButton.style.cursor = "not-allowed";

    // =========================
    // User Message
    // =========================

    const userMessage = document.createElement("div");

    userMessage.style.cssText = `
      background:#111827;
      color:white;
      padding:10px;
      border-radius:8px;
      margin-bottom:10px;
      margin-left:auto;
      width:fit-content;
      max-width:80%;
      white-space:pre-wrap;
      word-break:break-word;
    `;

    userMessage.textContent = message;

    messages.appendChild(userMessage);

    input.value = "";

    messages.scrollTop = messages.scrollHeight;

    // =========================
    // Typing Indicator
    // =========================

    const typingMessage = createTypingMessage();

    try {
      // =========================
      // API Request
      // =========================

      const response = await fetch(
        "http://127.0.0.1:8000/widget/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            agent_key: agentKey,
            query: message,
            order_id: currentOrderId,
            phone: detectedPhone
          })
        }
      );

      // =========================
      // Error Handling
      // =========================

      if (!response.ok) {
        let errorMessage = "Something went wrong";

        try {
          const errorData = await response.json();

          errorMessage =
            errorData.detail || errorMessage;

        } catch {}

        throw new Error(errorMessage);
      }

      // =========================
      // AI Message Bubble
      // =========================

      const aiMessage =
        document.createElement("div");

      aiMessage.style.cssText = `
        background:#e5e7eb;
        color:#111827;
        padding:10px;
        border-radius:8px;
        margin-bottom:10px;
        width:fit-content;
        max-width:80%;
        white-space:pre-wrap;
        word-break:break-word;
        display:none;
      `;

      messages.appendChild(aiMessage);

      // =========================
      // Read Streaming Response
      // =========================

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let answer = "";

      let firstChunk = true;

      while (true) {
        const { value, done } =
          await reader.read();

        if (done) {
          break;
        }

        const chunk =
          decoder.decode(value, {
            stream: true
          });

        // First response
        if (firstChunk) {
          firstChunk = false;

          typingMessage.remove();

          aiMessage.style.display = "block";
        }

        answer += chunk;

        aiMessage.textContent = answer;

        messages.scrollTop =
          messages.scrollHeight;
      }

      // Remaining bytes
      answer += decoder.decode();

      aiMessage.textContent = answer;

      messages.scrollTop =
        messages.scrollHeight;

      // =========================
      // Clear Order ID
      // =========================

      if (
        currentOrderId &&
        detectedPhone
      ) {
        currentOrderId = null;
      }

    } catch (error) {
      console.error(error);

      typingMessage.remove();

      const errorMessage =
        document.createElement("div");

      errorMessage.style.cssText = `
        color:#dc2626;
        padding:10px;
        margin-bottom:10px;
      `;

      errorMessage.textContent =
        "Unable to connect to AI agent.";

      messages.appendChild(errorMessage);

    } finally {
      // =========================
      // Enable Again
      // =========================

      input.disabled = false;
      sendButton.disabled = false;

      sendButton.textContent = "Send";
      sendButton.style.opacity = "1";
      sendButton.style.cursor = "pointer";

      input.focus();
    }
  }

  // =========================
  // Events
  // =========================

  sendButton.addEventListener(
    "click",
    sendMessage
  );

  input.addEventListener(
    "keydown",
    function (event) {
      if (event.key === "Enter") {
        sendMessage();
      }
    }
  );

})();