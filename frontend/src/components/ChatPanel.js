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


//   // Auto-scroll to the latest message
//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages]);

//   // Function to format time (HH:mm am/pm)
//   const formatTime = (date) => {
//     return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true });
//   };

//   // Function to send user message and generate bot response
//   const sendMessage = () => {
//     if (!newMessage.trim()) return;

//     setMessages((prev) => {
//       const userMessage = {
//         id: prev.length + 1,
//         text: newMessage,
//         sender: "You",
//         time: formatTime(new Date()),
//       };

//       return [...prev, userMessage];
//     });

//     setNewMessage("");

//     // Bot Response after 1.5 seconds
//     setTimeout(() => {
//       setMessages((prev) => {
//         const botReplies = [
//           "Hello! How can I help you?",
//           "That's interesting!",
//           "Tell me more about it.",
//           "I'm here to chat!",
//           "Keep going, I'm listening!",
//           "Let's talk more about this!"
//         ];

//         const botMessage = {
//           id: prev.length + 1, // Fixes ID issue
//           text: botReplies[Math.floor(Math.random() * botReplies.length)],
//           sender: "Bot",
//           time: formatTime(new Date()),
//         };

//         return [...prev, botMessage];
//       });
//     }, 1500);
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-header">Chat Panel</div>

//       <MessageList messages={messages} />
//       <div ref={chatEndRef}></div>

//       <div className="chat-input">
//         <input
//           type="text"
//           placeholder="Type a message..."
//           value={newMessage}
//           onChange={(e) => setNewMessage(e.target.value)}
//           onKeyDown={(e) => e.key === "Enter" && sendMessage()}
//         />
//         <button onClick={sendMessage}>Send</button>
//       </div>
//     </div>
//   );
// };

// export default ChatPanel;
