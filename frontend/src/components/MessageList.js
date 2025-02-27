import MessageItem from "./MessageItem";
import { useEffect, useRef } from "react";

const MessageList = ({ messages, currentUser }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-box">
      {messages.length === 0 ? (
        <p className="no-messages">No messages yet...</p>
      ) : (
        messages.map((msg) => <MessageItem key={msg.id} msg={msg} currentUser={currentUser} />)
      )}
      <div ref={chatEndRef}></div> {/* Auto-scroll target */}
    </div>
  );
};

export default MessageList;
