import React, { useState } from 'react';

const AuditorDashboard = ({ selectedNode, token }) => {
  const [patientQuery, setPatientQuery] = useState('');
  const [auditorQuery, setAuditorQuery] = useState('');
  const [patientResults, setPatientResults] = useState([]);
  const [auditorResults, setAuditorResults] = useState([]);
  const [loadingPatient, setLoadingPatient] = useState(false);
  const [loadingAuditor, setLoadingAuditor] = useState(false);
  const [verifyStatus, setVerifyStatus] = useState('');
  const [loadingVerify, setLoadingVerify] = useState(false);

  const fetchPatientRecords = async () => {
    try {
      setLoadingPatient(true);
      const body = {
        patient_id: patientQuery.trim()
      };

      const response = await fetch(`${selectedNode}/audit/patient-records`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });

      const data = await response.json();
      setPatientResults(data.records || []);
    } catch (error) {
      console.error('Error fetching patient records:', error);
      alert('Failed to fetch patient audit records.');
    } finally {
      setLoadingPatient(false);
    }
  };

  const fetchAuditorRecords = async () => {
    try {
      setLoadingAuditor(true);
      const body = {
        auditor_id: auditorQuery.trim()
      };

      const response = await fetch(`${selectedNode}/audit/auditor-records`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });

      const data = await response.json();
      setAuditorResults(data.records || []);
    } catch (error) {
      console.error('Error fetching auditor records:', error);
      alert('Failed to fetch auditor audit records.');
    } finally {
      setLoadingAuditor(false);
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
              <h5 className="card-title">Query Patient Audit Records</h5>
              <div className="mb-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Enter Patient ID or *"
                  value={patientQuery}
                  onChange={(e) => setPatientQuery(e.target.value)}
                />
              </div>
              <div className="d-grid">
                <button className="btn btn-primary" onClick={fetchPatientRecords} disabled={loadingPatient}>
                  {loadingPatient ? 'Loading...' : 'Query Patient Records'}
                </button>
              </div>

              <div className="mt-4 overflow-auto" style={{ maxHeight: '300px' }}>
                {patientResults.length > 0 ? (
                  patientResults.map((record, idx) => (
                    <div key={idx} className="border rounded p-2 mb-2">
                      <strong>Action:</strong> {record.action} <br />
                      <strong>Actor Role:</strong> {record.actor_role} <br />
                      <strong>Actor User ID:</strong> {record.actor_user_id} <br />
                      <strong>Actor Username:</strong> {record.actor_username} <br />
                      <strong>Target User ID:</strong> {record.target_user_id}
                    </div>
                  ))
                ) : !loadingPatient ? (
                  <p className="text-muted">No matching patient records found.</p>
                ) : null}
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4 d-flex">
          <div className="card shadow w-100">
            <div className="card-body d-flex flex-column">
              <h5 className="card-title">Query Auditor Audit Records</h5>
              <div className="mb-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Enter Auditor ID or *"
                  value={auditorQuery}
                  onChange={(e) => setAuditorQuery(e.target.value)}
                />
              </div>
              <div className="d-grid">
                <button className="btn btn-primary" onClick={fetchAuditorRecords} disabled={loadingAuditor}>
                  {loadingAuditor ? 'Loading...' : 'Query Auditor Records'}
                </button>
              </div>

              <div className="mt-4 overflow-auto" style={{ maxHeight: '300px' }}>
                {auditorResults.length > 0 ? (
                  auditorResults.map((record, idx) => (
                    <div key={idx} className="border rounded p-2 mb-2">
                      <strong>Action:</strong> {record.action} <br />
                      <strong>Actor Role:</strong> {record.actor_role} <br />
                      <strong>Actor User ID:</strong> {record.actor_user_id} <br />
                      <strong>Actor Username:</strong> {record.actor_username} <br />
                      <strong>Target User ID:</strong> {record.target_user_id}
                    </div>
                  ))
                ) : !loadingAuditor ? (
                  <p className="text-muted">No matching auditor records found.</p>
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-12 d-flex">
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