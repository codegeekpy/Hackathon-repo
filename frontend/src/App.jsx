import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import UploadPDF from './components/UploadPDF';
import GenerateQuestions from './components/GenerateQuestions';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadPDF />} />
        <Route path="/generate" element={<GenerateQuestions />} />
        <Route path="/chat" element={<ChatBox />} />
      </Routes>
    </>
  );
}

export default App;
