const MessageItem = ({ msg, currentUser }) => {
  const isSentByUser = msg.sender === currentUser.username; // Compare with currentUser.username

  return (
    <div className={`message ${isSentByUser ? "my-message" : "other-message"}`}>
      <div className="message-content">
        <span className="message-text">{msg.text}</span>
        <span className="timestamp">{msg.time}</span>
      </div>
    </div>
  );
};

export default MessageItem;
