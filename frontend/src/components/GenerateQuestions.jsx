import { Link } from 'react-router-dom';
import '../styles/ServicePage.css';

export default function GenerateQuestions() {
  return (
    <div className="service-page">
      <Link to="/" className="home-btn">🏠 Home</Link>
      <h2>Generate Questions</h2>
      <p>Paste your text or select a PDF to generate questions automatically.</p>
      <form className="service-form">
        <textarea
          placeholder="Paste your study material here..."
          rows={6}
          className="service-textarea"
        />
        <button type="submit" className="service-btn">
          Generate
        </button>
      </form>
    </div>
  );
}