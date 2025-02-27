import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import ChatPanel from "../components/ChatPanel";
import UsersList from "../components/UsersList";
import UserAuth from "../components/UserAuth";
import UserProfile from "../components/UserProfile"; 
import "../styles.css";

const ChatRoom = () => {
  const location = useLocation();
  const [currentUser, setCurrentUser] = useState(() => {
    const storedUser = JSON.parse(localStorage.getItem("currentUser"));
    return storedUser || { username: "", user_id: null, online: false, avatar: "/boy.png" };
  });

  // const [users, setUsers] = useState([
  //   { id: 1, name: "Alice", online: true },
  //   { id: 2, name: "Bob", online: false },
  //   { id: 3, name: "Charlie", online: true },
  // ]);

  const [selectedUser, setSelectedUser] = useState(null);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  useEffect(() => {
    if (location.state?.username && location.state?.user_id) {
      const userData = {
        username: location.state.username,
        user_id: location.state.user_id,
        online: true,
        avatar: "/boy.png",
      };
      setCurrentUser(userData);
      localStorage.setItem("currentUser", JSON.stringify(userData));
    }
  }, [location.state]);

  const updateProfile = (updatedProfile) => {
    setCurrentUser((prev) => ({ ...prev, ...updatedProfile }));
  };

  return (
    <div className="chat-room">
      <div className="sidebar">
        <UserAuth currentUser={currentUser} />
        <UsersList currentUser={currentUser} setSelectedUser={setSelectedUser}/>
        <div className="profile-section" onClick={() => setIsProfileOpen(true)}>
          <img src={currentUser.avatar} alt="Profile" className="profile-avatar" />
          <span>{currentUser.username || "Unknown User"}</span>
        </div>
      </div>
      <div className="chat-section">
        <ChatPanel currentUser={currentUser} selectedUser={selectedUser}/>
      </div>

      {isProfileOpen && (
        <div className="profile-overlay">
          <div className="profile-modal">
            <UserProfile currentUser={currentUser} updateProfile={updateProfile} onClose={() => setIsProfileOpen(false)} />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatRoom;
