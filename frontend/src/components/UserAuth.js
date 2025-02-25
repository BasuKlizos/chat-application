const UserAuth = ({ currentUser }) => {
    return (
      <div className="user-auth">
        <h3>Logged in as:</h3>
        <div className="user-details">
          <span className="username">{currentUser.name}</span>
          <span className={`status ${currentUser.online ? "online" : "offline"}`}>
            {currentUser.online ? "Online" : "Offline"}
          </span>
        </div>
      </div>
    );
  };
  
  export default UserAuth;