import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(""); // Reset error on input change
  };

  const handleRegister = async () => {
    const { username, email, password, confirm_password } = formData;

    if (!username || !email || !password || !confirm_password) {
      setError("Please fill in all fields.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirm_password) {
      setError("Passwords do not match.");
      return;
    }
    try {
      // Send registration data to the backend using fetch
      const response = await fetch("http://localhost:8000/auth/user/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password, confirm_password }),
      });

      // Parse the JSON response
      const data = await response.json();

      // Handle backend errors
      if (!response.ok) {
        throw new Error(data.detail || "Registration failed. Please try again.");
      }

      // If registration is successful, navigate to the login page
      console.log("User Registered:", data);
      navigate("/login");
    } catch (error) {
      // Handle errors
      setError(error.message || "Registration failed. Please try again.");
      console.log(error.message)
    }
    // console.log("User Registered:", formData);
    // navigate("/login");
  };

  return (
    <div className="register-container">
      <h2>Sign Up</h2>
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
        name="confirm_password"
        placeholder="Confirm Password"
        value={formData.confirm_password}
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
