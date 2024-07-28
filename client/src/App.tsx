import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Upload from './pages/Upload';
import Chat from './pages/Chat';
import NavBar from './components/NavBar';


function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
