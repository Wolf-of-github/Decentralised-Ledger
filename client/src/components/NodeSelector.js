import React from 'react';

const NodeSelector = ({ selectedNode, setSelectedNode, nodes, logout }) => {
  
  const handleChange = (e) => {
    const newNode = e.target.value;
    if (newNode !== selectedNode) {
      logout();  // logout automatically if switching node
      setSelectedNode(newNode);
    }
  };

  return (
    <div className="d-flex align-items-center">
      <select
        className="form-select"
        style={{ width: '200px' }}
        value={selectedNode}
        onChange={handleChange}
      >
        {nodes.map((node) => (
          <option key={node.url} value={node.url}>
            {node.isAlive ? '🟢' : '🔴'} {node.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default NodeSelector;