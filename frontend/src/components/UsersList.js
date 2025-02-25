const UsersList = ({ users }) => {
    return (
      <div className="users-list">
        <h3>Online Users</h3>
        <ul>
          {users.map((user) => (
            <li key={user.id} className={user.online ? "online" : "offline"}>
              {user.name}
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default UsersList;