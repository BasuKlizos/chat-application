const MessageItem = ({ msg }) => {
  return (
    <div className={`message ${msg.sender === "You" ? "my-message" : "other-message"}`}>
      <div className="message-content">
        <span className="message-text">{msg.text}</span>
        <span className="timestamp">{msg.time}</span>
      </div>
    </div>
  );
};

export default MessageItem;
