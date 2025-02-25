import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(""); // Reset error on input change
  };

  const handleRegister = () => {
    const { username, email, password, confirmPassword } = formData;

    if (!username || !email || !password || !confirmPassword) {
      setError("Please fill in all fields.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    console.log("User Registered:", formData);
    navigate("/login");
  };

  return (
    <div className="register-container">
      <h2>Signup</h2>
      {error && <p className="error-message">{error}</p>}
      <input
        className="input-box"
        type="text"
        name="username"
        placeholder="Choose Username"
        value={formData.username}
        onChange={handleChange}
      />
      <input
        className="input-box"
        type="email"
        name="email"
        placeholder="Enter Email"
        value={formData.email}
        onChange={handleChange}
      />
      <input
        className="input-box"
        type="password"
        name="password"
        placeholder="Enter Password"
        value={formData.password}
        onChange={handleChange}
      />
      <input
        className="input-box"
        type="password"
        name="confirmPassword"
        placeholder="Confirm Password"
        value={formData.confirmPassword}
        onChange={handleChange}
      />
      <button className="btn" onClick={handleRegister}>Register</button>
      <p className="login-link">
        Already have an account? <span onClick={() => navigate("/login")}>Login here</span>
      </p>
    </div>
  );
};

export default Register;
