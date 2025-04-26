import React, { useState } from 'react';
import LoginForm from '../components/LoginForm';

const Home = ({ selectedNode, setToken, setRole, setPatientId }) => {
  const [userType, setUserType] = useState('');

  const handleUserTypeSelect = (type) => {
    setUserType(type);
  };

  return (
    <div className="d-flex flex-column justify-content-center align-items-center" style={{ minHeight: '60vh' }}>
      {!userType ? (
        <div className="text-center">
          <h2 className="mb-4">Login As</h2>
          <div className="d-flex justify-content-center gap-4">
            <button className="btn btn-outline-primary btn-lg" onClick={() => handleUserTypeSelect('patient')}>
              Patient
            </button>
            <button className="btn btn-outline-success btn-lg" onClick={() => handleUserTypeSelect('auditor')}>
              Auditor
            </button>
          </div>
        </div>
      ) : (
        <div style={{ width: '100%', maxWidth: '500px' }}>
          <h3 className="text-center mb-4">
            {userType === 'patient' ? 'Patient Login' : 'Auditor Login'}
          </h3>
          <LoginForm
            selectedNode={selectedNode}
            setToken={setToken}
            setRole={setRole}
            setPatientId={setPatientId}
          />
        </div>
      )}
    </div>
  );
};

export default Home;