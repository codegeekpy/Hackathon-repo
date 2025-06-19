import { Link } from 'react-router-dom';
import '../styles/ServicePage.css';

export default function UploadPDF() {
  return (
    <div className="service-page">
      <Link to="/" className="home-btn">🏠 Home</Link>
      <h2>Upload PDF</h2>
      <p>Select a PDF file to upload and process.</p>
      <form className="service-form">
        <input type="file" accept="application/pdf" className="service-file" />
        <button type="submit" className="service-btn">
          Upload
        </button>
      </form>
    </div>
  );
}