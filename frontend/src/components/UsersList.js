import { useState, useEffect } from "react";
import "../UsersList.module.css";

const UsersList = ({ currentUser, setSelectedUser }) => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:8000/user/get-users", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.status) {
          setUsers(data.users);
        }
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="users-list">
      <h3>Users</h3>
      <ul>
        {users.map((user) => (
          <li
            key={user.user_id}
            className={user.is_online ? "online" : "offline"}
            onClick={() => setSelectedUser(user)} // Set clicked user
            style={{ cursor: "pointer" }}
          >
            {user.username} {user.username === currentUser.username && "(You)"}
            {user.is_online ? " 🟢" : " ⚪"}
          </li>
        ))}
      </ul>
    </div>
  );
};
export default UsersList;
