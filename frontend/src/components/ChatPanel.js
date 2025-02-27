import { useState, useEffect, useRef } from "react";
import MessageList from "./MessageList";
import "../styles.css";

const ChatPanel = ({ currentUser, selectedUser }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const chatEndRef = useRef(null);
  const ws = useRef(null);

  useEffect(() => {
    if (!selectedUser) return;
    ws.current = new WebSocket("ws://localhost:8000/ws"); // Connect to FastAPI WebSocket

    ws.current.onmessage = (event) => {
      const receivedMessage = {
        id: messages.length + 1,
        text: event.data,
        sender: selectedUser.username,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
      };
      setMessages((prev) => [...prev, receivedMessage]);
    };

    return () => ws.current.close(); // Cleanup on unmount
  }, [selectedUser, messages.length]);

  const sendMessage = () => {
    if (!newMessage.trim() || !selectedUser) return;

    const userMessage = {
      id: messages.length + 1,
      text: newMessage,
      sender: currentUser.username,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
    };

    setMessages((prev) => [...prev, userMessage]);
    // ws.current.send(`${currentUser.username}: ${newMessage}`);  // Send message through WebSocket
    ws.current.send(newMessage);  // Send message through WebSocket
    setNewMessage("");
  };

  return (
    <div className="chat-container">
      <div className="chat-header">{selectedUser ? `Chat with ${selectedUser.username}` : "Select a user to start chatting"}</div>
      <MessageList messages={messages} currentUser={currentUser}/>
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