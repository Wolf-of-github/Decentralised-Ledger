import React from 'react';
import NodeSelector from './NodeSelector';

const Navbar = ({ selectedNode, setSelectedNode, nodes, logout }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">Decentralized EHR Audit</a>

        <div className="d-flex">
          <NodeSelector
            selectedNode={selectedNode}
            setSelectedNode={setSelectedNode}
            nodes={nodes}
            logout={logout}
          />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;