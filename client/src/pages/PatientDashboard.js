import React, { useState } from 'react';

const PatientDashboard = ({ selectedNode, token }) => {
  const [ehrData, setEhrData] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loadingEHR, setLoadingEHR] = useState(false);
  const [loadingAudit, setLoadingAudit] = useState(false);

  const fetchEHR = async () => {
    try {
      setLoadingEHR(true);
      const response = await fetch(`${selectedNode}/my-ehr`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const data = await response.json();
      setEhrData(data);
    } catch (error) {
      console.error('Error fetching EHR:', error);
      alert('Failed to fetch EHR data.');
    } finally {
      setLoadingEHR(false);
    }
  };

  const fetchAuditLogs = async () => {
    try {
      setLoadingAudit(true);
      const response = await fetch(`${selectedNode}/audit/my-access`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const data = await response.json();
      console.log(data)
      setAuditLogs(data.records || []);
    } catch (error) {
      console.error('Error fetching audit logs:', error);
      alert('Failed to fetch audit logs.');
    } finally {
      setLoadingAudit(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Welcome to Patient Dashboard</h2>

      <div className="row">
        <div className="col-md-6 mb-4 d-flex">
          <div className="card shadow w-100">
            <div className="card-body d-flex flex-column">
              <h5 className="card-title">View My EHR Data</h5>
              <div className="d-grid mt-3">
                <button className="btn btn-primary" onClick={fetchEHR} disabled={loadingEHR}>
                  {loadingEHR ? 'Loading...' : 'Fetch EHR'}
                </button>
              </div>

              <div className="mt-4 overflow-auto" style={{ maxHeight: '300px' }}>
                {ehrData && ehrData.records && ehrData.records.length > 0 ? (
                  ehrData.records.map((record, idx) => (
                    <div key={idx} className="border rounded p-3 mb-2">
                      <p><strong>Name:</strong> {record.first_name} {record.last_name}</p>
                      <p><strong>Date of Birth:</strong> {record.date_of_birth}</p>
                      <p><strong>Gender:</strong> {record.gender}</p>
                      <p><strong>Condition:</strong> {record.conditions}</p>
                      <p><strong>Consulting Doctor:</strong> {record.consulting_docter}</p>
                      <p><strong>Last Visit:</strong> {record.last_visit_date} ({record.last_visit_duration} mins)</p>
                    </div>
                  ))
                ) : ehrData ? (
                  <p className="text-muted">No records found.</p>
                ) : null}
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4 d-flex">
          <div className="card shadow w-100">
            <div className="card-body d-flex flex-column">
              <h5 className="card-title">View Who Accessed My Records</h5>
              <div className="d-grid mt-3">
                <button className="btn btn-success" onClick={fetchAuditLogs} disabled={loadingAudit}>
                  {loadingAudit ? 'Loading...' : 'Fetch Access Logs'}
                </button>
              </div>

              <div className="mt-4 overflow-auto" style={{ maxHeight: '300px' }}>
                {auditLogs.length > 0 ? (
                  auditLogs.map((log, idx) => (
                    <div key={idx} className="border rounded p-2 mb-2">
                      <p><strong>Action:</strong> {log.action}</p>
                      <p><strong>Actor Role:</strong> {log.actor_role}</p>
                      <p><strong>Actor User ID:</strong> {log.actor_user_id}</p>
                      <p><strong>Actor Username:</strong> {log.actor_username}</p>
                      <p><strong>Target User ID:</strong> {log.target_user_id}</p>
                      <p><strong>Target User ID:</strong> {log.timestamp}</p>
                    </div>
                  ))
                ) : auditLogs.length === 0 && !loadingAudit ? (
                  <p className="text-muted">No access logs found.</p> 
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;