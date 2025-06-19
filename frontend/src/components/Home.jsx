import { Link } from 'react-router-dom';
import '../styles/Home.css';

export default function Home() {
  return (
    <div className="home-container">
      <div style={{ textAlign: 'right', marginBottom: '1rem' }}>
        <button className="sign-in-btn">Sign In</button>
      </div>
      <h1 className="site-title">AI Question Generator</h1>
      <p className="site-tagline">Smart tools for educators and learners</p>
      <div className="services">
        <Link to="/upload" className="service-card">
          <h2>Upload PDF</h2>
          <p>Upload your study material in PDF format.</p>
        </Link>
        <Link to="/generate" className="service-card">
          <h2>Generate Questions</h2>
          <p>Automatically generate questions from your content.</p>
        </Link>
        <Link to="/chat" className="service-card">
          <h2>Chat</h2>
          <p>Interact with our AI assistant for help.</p>
        </Link>
      </div>
    </div>
  );
}