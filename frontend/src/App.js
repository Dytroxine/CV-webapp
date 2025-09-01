import React, { useState, useEffect } from 'react';
import Login from './Login';
import ResumeList from './ResumeList';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentView, setCurrentView] = useState('list');
  const [selectedResume, setSelectedResume] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setCurrentView('list');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
      <ResumeList />
    </div>
  );
}

export default App;