import { Routes, Route } from "react-router-dom";
import ChatRoom from "./pages/ChatRoom";

function App() {
  return (
    <Routes>
      {/* <Route path="/" element={<Home />} /> */}
      {/* <Route path="/login" element={<Login />} /> */}
      {/* <Route path="/register" element={<Register />} /> */}
      <Route path="/chat" element={<ChatRoom />} />
      {/* <Route path="/video" element={<VideoChat />} /> */}
    </Routes>
  );
}

export default App;
