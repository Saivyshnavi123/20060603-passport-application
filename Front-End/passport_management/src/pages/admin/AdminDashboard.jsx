import { useState, useEffect } from 'react';
import Navbar from '../../components/common/Navbar';
import ApplicationDrawer from '../../components/admin/ApplicationDrawer';
import api from '../../services/api';
import './Dashboard.css';

const AdminDashboard = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedApplication, setSelectedApplication] = useState(null);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      const userId = localStorage.getItem('user_id');
      const response = await api.get(`/admin/applications?user_id=${userId}`);
      setApplications(response);
      setLoading(false);
    } catch (err) {
      setError(err.message || 'Failed to fetch applications');
      setLoading(false);
    }
  };

  const handleRowClick = (app) => {
    setSelectedApplication(app);
  };

  const handleCloseDrawer = () => {
    setSelectedApplication(null);
  };

  const handleRefresh = () => {
    fetchApplications();
  };

  return (
    <div className="dashboard-wrapper">
      <Navbar />
      <div className="dashboard-content">
        <div className="dashboard-container">
          <h1 className="dashboard-title">Admin Dashboard</h1>
          <p className="dashboard-subtitle">Manage passport applications</p>

          <div className="dashboard-cards">
            <div className="dashboard-card">
              <h3>Total Applications</h3>
              <p className="card-number">{applications.length}</p>
            </div>

            <div className="dashboard-card">
              <h3>Approved</h3>
              <p className="card-number">{applications.filter(app => app.status === 'approved').length}</p>
            </div>

            <div className="dashboard-card">
              <h3>Pending</h3>
              <p className="card-number">{applications.filter(app => app.status === 'pending').length}</p>
            </div>

            <div className="dashboard-card">
              <h3>Rejected</h3>
              <p className="card-number">{applications.filter(app => app.status === 'rejected').length}</p>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading">Loading applications...</div>
          ) : (
            <div className="applications-list">
              <h2>Applications List</h2>
              <table className="applications-table">
                <thead>
                  <tr>
                    <th>Application ID</th>
                    <th>Full Name</th>
                    <th>Passport Number</th>
                    <th>DOB</th>
                    <th>Gender</th>
                    <th>Nationality</th>
                    <th>Place of Birth</th>
                    <th>Appointment Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {applications.map((app) => (
                    <tr key={app.id} onClick={() => handleRowClick(app)}>
                      <td>{app.id}</td>
                      <td>{app.full_name}</td>
                      <td>{app.passport_number}</td>
                      <td>{app.dob}</td>
                      <td>{app.gender}</td>
                      <td>{app.nationality}</td>
                      <td>{app.place_of_birth}</td>
                      <td>{app.appointment_date}</td>
                      <td>
                        <strong>{app.status.charAt(0).toUpperCase() + app.status.slice(1)}</strong>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {applications.length === 0 && (
                <p className="no-data">No applications found</p>
              )}
            </div>
          )}
        </div>
      </div>

      <ApplicationDrawer
        application={selectedApplication}
        onClose={handleCloseDrawer}
        onRefresh={handleRefresh}
      />
    </div>
  );
};

export default AdminDashboard;
