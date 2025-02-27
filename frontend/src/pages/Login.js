import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

const Login = () => {
  const [usernameOrEmail, setUsernameOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!usernameOrEmail || !password) {
      setError("Please fill in all fields.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username_or_email: usernameOrEmail,
          password,
        }),
      });

      const data = await response.json();
      // console.log(data, "fron====================")

      if (response.status !== 200) {
        throw new Error(data.detail || "Login failed. Please try again.");
      }

      // console.log("User Logged In:", data);

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("currentUser", JSON.stringify(data.data));

     navigate("/chat", { state: { username: data.data.username, user_id: data.data.id } });
    } catch (error) {
      setError(error.message || "Login failed. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <input
        className="input-box"
        type="text"
        placeholder="Enter Username or Email"
        value={usernameOrEmail}
        onChange={(e) => setUsernameOrEmail(e.target.value)}
      />
      <input
        className="input-box"
        type="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="btn" onClick={handleLogin}>
        Login
      </button>
      <p className="register-link">
        Don't have an account?{" "}
        <span onClick={() => navigate("/register")}>Register here</span>
      </p>
    </div>
  );
};

export default Login;
