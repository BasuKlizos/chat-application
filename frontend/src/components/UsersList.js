import { useState, useEffect } from "react";

const UsersList = ({ currentUser }) => {
  const [users, setUsers] = useState([]);

  // Fetch all users from the backend
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch("http://localhost:8000/user/get-users");
        const data = await response.json();
        setUsers(data.users);
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="users-list">
      <h3>Online Users</h3>
      <ul>
        {users.map((user) => (
          <li
            key={user.username}
            className={user.username === currentUser.username ? "online" : "offline"}
          >
            {user.username} {user.username === currentUser.username && "(You)"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UsersList;



// const UsersList = ({ users }) => {
//     return (
//       <div className="users-list">
//         <h3>Online Users</h3>
//         <ul>
//           {users.map((user) => (
//             <li key={user.id} className={user.online ? "online" : "offline"}>
//               {user.name}
//             </li>
//           ))}
//         </ul>
//       </div>
//     );
//   };
  
//   export default UsersList;