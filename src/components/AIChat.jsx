import React from "react";
import "./AIChat.css";

const AIChat = ({ tabContext }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState("");

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { type: "user", text: input }]);
      setInput("");

      // Simulate API call response
      setTimeout(() => {
        setMessages((prev) => [...prev, { type: "bot", text: "Hello from AI!" }]);
      }, 1000);
    }
  };

  return (
    <div className="ai-chat">
      <button className="chat-toggle" onClick={toggleChat}>
        {isOpen ? "Close Chat" : "Open Chat"}
      </button>
      {isOpen && (
        <div className="chat-box">
          <div className="chat-header">AI Assistant</div>
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIChat;