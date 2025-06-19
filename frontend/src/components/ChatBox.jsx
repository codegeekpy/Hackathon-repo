import { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/ServicePage.css';

export default function ChatBox() {
  const [messages, setMessages] = useState([
    { from: 'ai', text: 'Hi! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  const sendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages([...messages, { from: 'user', text: input }]);
    setInput('');
    //Backend Work
  };

  return (
    <div className="service-page">
      <Link to="/" className="home-btn">🏠 Home</Link>
      <h2>Chat with AI</h2>
      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-msg ${msg.from === 'user' ? 'user' : 'ai'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <form className="chat-form" onSubmit={sendMessage}>
        <input
          className="chat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button className="service-btn" type="submit">Send</button>
      </form>
    </div>
  );
}