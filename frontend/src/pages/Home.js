import { Link } from "react-router-dom";
import "../styles.css";

const Home = () => {
  return (
    <main className="home-container">
      <div className="home-content">
        <h1>Welcome to Chat App</h1>
        <p className="home-description">
          Connect with your friends and family in real-time. Join now to start chatting!
        </p>
        <nav className="home-buttons">
          <Link to="/login" className="btn btn-primary">Login</Link>
          <Link to="/register" className="btn btn-secondary">Register</Link>
        </nav>
      </div>
    </main>
  );
};

export default Home;