import { useState } from "react";
import UsersList from "../components/UsersList";
import ChatPanel from "../components/ChatPanel";
import UserAuth from "../components/UserAuth";
import UserProfile from "../components/UserProfile"; // New component for user profile
import "../styles.css";

const ChatRoom = () => {
  const [users, setUsers] = useState([
    { id: 1, name: "Alice", online: true },
    { id: 2, name: "Bob", online: false },
    { id: 3, name: "Charlie", online: true },
  ]);

  const [currentUser, setCurrentUser] = useState({
    id: 1,
    name: "Alice",
    online: true,
    email: "alice@example.com", // Add email for profile
    avatar: "/boy.png", // Add avatar URL
  });

  const [isProfileOpen, setIsProfileOpen] = useState(false); // State to control profile visibility

  // Function to update user profile
  const updateProfile = (updatedProfile) => {
    setCurrentUser((prev) => ({
      ...prev,
      ...updatedProfile,
    }));
  };

  return (
    <div className="chat-room">
      <div className="sidebar">
        <UserAuth currentUser={currentUser} />
        <UsersList users={users} />
        {/* Profile Section in Bottom-Left Corner */}
        <div className="profile-section" onClick={() => setIsProfileOpen(true)}>
          <img src={currentUser.avatar} alt="Profile" className="profile-avatar" />
          <span>{currentUser.name}</span>
        </div>
      </div>
      <div className="chat-section">
        <ChatPanel currentUser={currentUser} />
      </div>

      {/* Profile Overlay */}
      {isProfileOpen && (
        <div className="profile-overlay">
          <div className="profile-modal">
            <UserProfile
              currentUser={currentUser}
              updateProfile={updateProfile}
              onClose={() => setIsProfileOpen(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatRoom;