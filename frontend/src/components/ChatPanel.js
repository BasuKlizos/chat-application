import { useState, useEffect, useRef } from "react";
import MessageList from "./MessageList";
import "../styles.css";
import { v4 as uuidv4 } from "uuid"; 

const ChatPanel = ({ currentUser, selectedUser }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const chatEndRef = useRef(null);
  const ws = useRef(null);
  // const reconnectInterval = useRef(null);
  // const reconnectAttempts = useRef(0);

  useEffect(() => {
    if (!selectedUser) return;

    const fetchChatHistory = async () => {
      try {
        const response = await fetch(`http://localhost:8000/chat/get-chats/${currentUser.user_id}/${selectedUser.user_id}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched Data:", data);
        // console.log("Messages:", data.messages);
  
        if (Array.isArray(data.messages)) {
          const formattedMessages = data.messages.map((msg) => ({
            id: msg._id,
            text: msg.message, // Use correct field from backend
            sender: msg.sender_id === currentUser.user_id ? currentUser.username : selectedUser.username, 
            time: new Date(msg.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
          }));
          setMessages(formattedMessages);
        } else {
          console.error("Messages is not an array:", data.messages);
          setMessages([]);
        }
      } catch (error) {
        console.error("Failed to fetch chat history:", error);
        setMessages([]);
      }
    };

    fetchChatHistory();

    ws.current = new WebSocket(`ws://localhost:8000/ws/${currentUser.user_id}`);

    ws.current.onmessage = (event) => {
      // const messageData = JSON.parse(event.data);
      console.log("WebSocket Message:", event.data);
      // console.log("Parsed WebSocket Data:", messageData);
      const messageParts = event.data.split(":");
      // const [senderId, text] = event.data.split(":");
      const senderId = messageParts[0];
      const text = messageParts.slice(1).join(":").trim();
      console.log("Parsed Sender ID:", senderId, "Message:", text);

      if (senderId === selectedUser.user_id) {
        const receivedMessage = {
          id: uuidv4(),
          text: text.trim(),
          sender: selectedUser.username,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
        };
        setMessages((prev) => [...prev, receivedMessage]);
      }
    };

    return () => ws.current?.close();// Cleanup on unmount
  }, [selectedUser]);

  const sendMessage = () => {
    if (!newMessage.trim() || !selectedUser) return;

    const userMessage = {
      id: uuidv4(),
      text: newMessage.trim(),
      sender: currentUser.username,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
    };

    setMessages((prev) => [...prev, userMessage]);
    // ws.current.send(`${currentUser.username}: ${newMessage}`);  
    ws.current.send(`${currentUser.user_id}:${selectedUser.user_id}:${newMessage}`);
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