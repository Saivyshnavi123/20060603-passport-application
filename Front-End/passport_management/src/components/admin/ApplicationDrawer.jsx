import { useState, useEffect } from 'react';
import api from '../../services/api';
import './ApplicationDrawer.css';

const ApplicationDrawer = ({ application, onClose, onRefresh }) => {
  const [message, setMessage] = useState('');

  // Reset message when application changes
  useEffect(() => {
    setMessage('');
  }, [application]);

  if (!application) return null;

  const handleApprove = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      await api.patch(`/admin/application/${application.id}/status`, {
        status: 'approved',
        user_id: parseInt(userId)
      });
      setMessage('Application approved successfully');
      setTimeout(() => {
        onRefresh();
        onClose();
      }, 2000);
    } catch (error) {
      setMessage('Failed to approve application');
      console.error(error);
    }
  };

  const handleReject = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      await api.patch(`/admin/application/${application.id}/status`, {
        status: 'rejected',
        user_id: parseInt(userId)
      });
      setMessage('Application rejected successfully');
      setTimeout(() => {
        onRefresh();
        onClose();
      }, 2000);
    } catch (error) {
      setMessage('Failed to reject application');
      console.error(error);
    }
  };

  return (
    <>
      <div className="drawer-overlay" onClick={onClose}></div>
      <div className="drawer">
        <div className="drawer-header">
          <h2>Application Details</h2>
        </div>

        {message && (
          <div className="message">
            {message}
          </div>
        )}

        <div className="drawer-content">
          <div className="detail-row">
            <strong>Application ID:</strong>
            <span>{application.id}</span>
          </div>
          <div className="detail-row">
            <strong>Full Name:</strong>
            <span>{application.full_name}</span>
          </div>
          <div className="detail-row">
            <strong>Passport Number:</strong>
            <span>{application.passport_number}</span>
          </div>
          <div className="detail-row">
            <strong>Date of Birth:</strong>
            <span>{application.dob}</span>
          </div>
          <div className="detail-row">
            <strong>Gender:</strong>
            <span>{application.gender}</span>
          </div>
          <div className="detail-row">
            <strong>Nationality:</strong>
            <span>{application.nationality}</span>
          </div>
          <div className="detail-row">
            <strong>Place of Birth:</strong>
            <span>{application.place_of_birth}</span>
          </div>
          <div className="detail-row">
            <strong>Appointment Date:</strong>
            <span>{application.appointment_date}</span>
          </div>
          <div className="detail-row">
            <strong>Status:</strong>
            <span><strong>{application.status.charAt(0).toUpperCase() + application.status.slice(1)}</strong></span>
          </div>
          <div className="detail-row">
            <strong>User ID:</strong>
            <span>{application.user_id}</span>
          </div>
        </div>

        {application.status === 'pending' && (
          <div className="drawer-footer">
            <button className="approve-btn" onClick={handleApprove}>
              Approve
            </button>
            <button className="reject-btn" onClick={handleReject}>
              Reject
            </button>
          </div>
        )}
      </div>
    </>
  );
};

export default ApplicationDrawer;
