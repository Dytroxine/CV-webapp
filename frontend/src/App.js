import React, { useState, useEffect } from 'react';
import Login from './Login';
import ResumeList from './ResumeList';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>CV WebApp</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>
      <main>
        <ResumeList />
      </main>
    </div>
  );
}

export default App;