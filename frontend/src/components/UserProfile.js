import { useState } from "react";

const UserProfile = ({ currentUser, updateProfile, onClose }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(currentUser.name);
  const [email, setEmail] = useState(currentUser.email);
  const [avatar, setAvatar] = useState(currentUser.avatar);

  const handleSave = () => {
    updateProfile({ name, email, avatar });
    setIsEditing(false);
  };

  return (
    <div className="user-profile">
      <h3>User Profile</h3>
      <button className="close-button" onClick={onClose}>
        &times;
      </button>
      {isEditing ? (
        <div className="edit-profile">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Name"
          />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
          />
          <input
            type="text"
            value={avatar}
            onChange={(e) => setAvatar(e.target.value)}
            placeholder="Avatar URL"
          />
          <button onClick={handleSave}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </div>
      ) : (
        <div className="profile-details">
          <img src={currentUser.avatar} alt="Profile" className="profile-avatar" />
          <p><strong>Name:</strong> {currentUser.name}</p>
          <p><strong>Email:</strong> {currentUser.email}</p>
          <button onClick={() => setIsEditing(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
};

export default UserProfile;