import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../../services/authService';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const menuRef = useRef(null);
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('');
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    const user = localStorage.getItem('username');
    const userRole = localStorage.getItem('role');
    setUsername(user || 'User');
    setRole(userRole || '');
  }, []);

  useEffect(() => {
    const handleClick = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    if (showMenu) {
      document.addEventListener('mousedown', handleClick);
    }

    return () => {
      document.removeEventListener('mousedown', handleClick);
    };
  }, [showMenu]);

  const handleLogout = () => {
    authService.logout();
    navigate('/');
    setShowMenu(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <span className="welcome-icon">👋</span>
          <h3>Welcome, {username}!</h3>
        </div>

        <div className="navbar-right" ref={menuRef}>
          <div className="user-icon" onClick={() => setShowMenu(!showMenu)}>
            {username.charAt(0).toUpperCase()}
          </div>
          
          {showMenu && (
            <div className="dropdown-menu">
              <p><strong>Username:</strong> {username}</p>
              <p><strong>Role:</strong> {role}</p>
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
