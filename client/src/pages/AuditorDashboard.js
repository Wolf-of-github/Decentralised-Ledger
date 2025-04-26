import React, { useState } from 'react';

const AuditorDashboard = ({ selectedNode, token }) => {
  const [queryResults, setQueryResults] = useState([]);
  const [verifyStatus, setVerifyStatus] = useState('');
  const [loadingQuery, setLoadingQuery] = useState(false);
  const [loadingVerify, setLoadingVerify] = useState(false);
  const [patientIds, setPatientIds] = useState('');
  const [auditorIds, setAuditorIds] = useState('');

  const fetchAuditChain = async () => {
    try {
      setLoadingQuery(true);
      const body = {
        patients: patientIds ? patientIds.split(',').map(p => p.trim()) : [],
        auditors: auditorIds ? auditorIds.split(',').map(a => a.trim()) : [],
      };

      const response = await fetch(`${selectedNode}/audit/chain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });

      const data = await response.json();
      setQueryResults(data.records || []);
    } catch (error) {
      console.error('Error fetching audit chain:', error);
      alert('Failed to fetch audit records.');
    } finally {
      setLoadingQuery(false);
    }
  };

  const verifyLedger = async () => {
    try {
      setLoadingVerify(true);
      const response = await fetch(`${selectedNode}/audit/verify`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await response.json();
      if (data.valid) {
        setVerifyStatus('✅ Ledger is valid.');
      } else {
        setVerifyStatus('❌ Ledger has been tampered!');
      }
    } catch (error) {
      console.error('Error verifying ledger:', error);
      setVerifyStatus('Error verifying ledger.');
    } finally {
      setLoadingVerify(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Welcome to Auditor Dashboard</h2>

      <div className="row">
        <div className="col-md-6 mb-4 d-flex">
          <div className="card shadow w-100">
            <div className="card-body d-flex flex-column">
              <h5 className="card-title">Query Audit Records</h5>
              <div className="mb-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Patient IDs (comma-separated)"
                  value={patientIds}
                  onChange={(e) => setPatientIds(e.target.value)}
                />
              </div>
              <div className="mb-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Auditor IDs (comma-separated)"
                  value={auditorIds}
                  onChange={(e) => setAuditorIds(e.target.value)}
                />
              </div>
              <div className="d-grid">
                <button className="btn btn-primary" onClick={fetchAuditChain} disabled={loadingQuery}>
                  {loadingQuery ? 'Loading...' : 'Query Audit Logs'}
                </button>
              </div>

              <div className="mt-4 overflow-auto" style={{ maxHeight: '300px' }}>
                {queryResults.length > 0 ? (
                  queryResults.map((record, idx) => (
                    <div key={idx} className="border rounded p-2 mb-2">
                      <strong>Action:</strong> {record.action} <br />
                      <strong>User:</strong> {record.user_id} <br />
                      <strong>Patient ID:</strong> {record.patient_id}
                    </div>
                  ))
                ) : !loadingQuery ? (
                  <p className="text-muted">No matching records found.</p>
                ) : null}
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4 d-flex">
          <div className="card shadow w-100">
            <div className="card-body d-flex flex-column">
              <h5 className="card-title">Verify Ledger Integrity</h5>
              <div className="d-grid mb-3">
                <button className="btn btn-success" onClick={verifyLedger} disabled={loadingVerify}>
                  {loadingVerify ? 'Verifying...' : 'Verify Ledger'}
                </button>
              </div>

              {verifyStatus && (
                <div className="alert alert-info text-center">
                  {verifyStatus}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuditorDashboard;