import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import PatientDashboard from './pages/PatientDashboard';
import AuditorDashboard from './pages/AuditorDashboard';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [selectedNode, setSelectedNode] = useState('http://localhost:5001');
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);
  const [patientId, setPatientId] = useState(null);

  const [nodes, setNodes] = useState([
    { name: "Node 1", url: "http://localhost:5001", isAlive: true },
    { name: "Node 2", url: "http://localhost:5002", isAlive: true },
    { name: "Node 3", url: "http://localhost:5003", isAlive: true }
  ]);

  const logout = () => {
    setToken(null);
    setRole(null);
    setPatientId(null);
  };

  return (
    <div className="App d-flex flex-column min-vh-100">
      <Navbar
        selectedNode={selectedNode}
        setSelectedNode={setSelectedNode}
        nodes={nodes}
        logout={logout}
      />

      <div className="container mt-4 mb-5 flex-grow-1">
        {!token ? (
          <Home
            selectedNode={selectedNode}
            setToken={setToken}
            setRole={setRole}
            setPatientId={setPatientId}
          />
        ) : (
          <>
            {role === 'patient' ? (
              <PatientDashboard selectedNode={selectedNode} token={token} />
            ) : (
              <AuditorDashboard selectedNode={selectedNode} token={token} />
            )}
          </>
        )}
      </div>

      <Footer logout={logout} token={token} />
    </div>
  );
}

export default App;