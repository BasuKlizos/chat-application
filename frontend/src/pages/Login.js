import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!username || !password) {
      setError("Please fill in all fields.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    console.log("User Logged In:", username);
    navigate("/chat");
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <input
        className="input-box"
        type="text"
        placeholder="Enter Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="input-box"
        type="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="btn" onClick={handleLogin}>Login</button>
      <p className="register-link">
        Don't have an account? <span onClick={() => navigate("/register")}>Register here</span>
      </p>
    </div>
  );
};

export default Login;