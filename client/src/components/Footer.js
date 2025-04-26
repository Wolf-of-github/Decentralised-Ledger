import React from 'react';

const Footer = ({ logout, token }) => {
  return (
    <footer className="bg-light py-3 mt-auto">
      <div className="container d-flex justify-content-center">
        {token ? (
          <button className="btn btn-danger" onClick={logout}>
            Logout
          </button>
        ) : (
          <span className="text-muted small">© 2025 Decentralized Audit System</span>
        )}
      </div>
    </footer>
  );
};

export default Footer;