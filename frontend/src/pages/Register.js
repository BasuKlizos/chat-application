import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleRegister = () => {
    console.log("User Registered:", username);
    navigate("/login");
  };

  return (
    <div>
      <h2>Register</h2>
      <input 
        type="text" 
        placeholder="Choose Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default Register;
