import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Upload from './pages/Upload';
import Chat from './pages/Chat';
import NavBar from './components/NavBar';
import { ToastContainer, } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <ToastContainer />
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
