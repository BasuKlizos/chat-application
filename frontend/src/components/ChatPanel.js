import { useState, useEffect, useRef } from "react";
import MessageList from "./MessageList";
import "../styles.css";

const ChatPanel = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const chatEndRef = useRef(null);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws"); // Connect to FastAPI WebSocket

    ws.current.onmessage = (event) => {
      const receivedMessage = {
        id: messages.length + 1,
        text: event.data,
        sender: "Other",
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
      };
      setMessages((prev) => [...prev, receivedMessage]);
    };

    return () => ws.current.close(); // Cleanup on unmount
  }, [messages.length]);

  const sendMessage = () => {
    if (!newMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: newMessage,
      sender: "You",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
    };

    setMessages((prev) => [...prev, userMessage]);
    ws.current.send(newMessage); // Send message through WebSocket
    setNewMessage("");
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Chat Panel</div>
      <MessageList messages={messages} />
      <div ref={chatEndRef}></div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatPanel;