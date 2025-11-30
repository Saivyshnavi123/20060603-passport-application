import { useState } from 'react';
import api from '../../services/api';
import './PassportApplicationForm.css';

const PassportApplicationForm = ({ onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    full_name: '',
    dob: '',
    gender: '',
    nationality: '',
    place_of_birth: '',
    appointment_date: ''
  });
  const [slotInfo, setSlotInfo] = useState(null);
  const [showSlotDialog, setShowSlotDialog] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    
    setFormData({
      ...formData,
      [name]: value
    });

    if (name === 'appointment_date' && value) {
      checkSlots(value);
    }
  };

  const checkSlots = async (date) => {
    try {
      const response = await api.get(`/slots?date=${date}`);
      setSlotInfo(response);
      setShowSlotDialog(true);
      setMessage('');
    } catch (error) {
      setMessage('Failed to check slot availability');
    }
  };

  const closeDialog = () => {
    setShowSlotDialog(false);
  };

  const changeDate = () => {
    setFormData({
      ...formData,
      appointment_date: ''
    });
    setShowSlotDialog(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const userId = localStorage.getItem('user_id');
      const response = await api.post('/passport/apply', {
        full_name: formData.full_name,
        dob: formData.dob,
        gender: formData.gender,
        nationality: formData.nationality,
        place_of_birth: formData.place_of_birth,
        appointment_date: formData.appointment_date,
        user_id: parseInt(userId)
      });
      
      const successMessage = response.message || 'Application submitted successfully';
      setMessage(successMessage);
      
      setTimeout(() => {
        onClose();
        onSuccess();
      }, 2000);
    } catch (error) {
      let errorMessage = 'Failed to submit application';
      if (error.data && error.data.message) {
        errorMessage = error.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }
      setMessage(errorMessage);
    }
  };

  const getTomorrowDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const year = tomorrow.getFullYear();
    const month = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const day = String(tomorrow.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  return (
    <>
      <div className="drawer-overlay" onClick={onClose}></div>
      <div className="drawer">
        <div className="drawer-header">
          <h2>Apply for Passport</h2>
        </div>
        
        {message && (
          <div className="message">
            {message}
          </div>
        )}
        
        <div className="drawer-content">
          <form onSubmit={handleSubmit} id="passport-form">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="Enter your full name"
                required
              />
            </div>

            <div className="form-group">
              <label>Date of Birth</label>
              <input
                type="date"
                name="dob"
                value={formData.dob}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Gender</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label>Nationality</label>
              <input
                type="text"
                name="nationality"
                value={formData.nationality}
                onChange={handleChange}
                placeholder="Enter your nationality"
                required
              />
            </div>

            <div className="form-group">
              <label>Place of Birth</label>
              <input
                type="text"
                name="place_of_birth"
                value={formData.place_of_birth}
                onChange={handleChange}
                placeholder="Enter your place of birth"
                required
              />
            </div>

            <div className="form-group">
              <label>Appointment Date</label>
              <input
                type="date"
                name="appointment_date"
                value={formData.appointment_date}
                onChange={handleChange}
                min={getTomorrowDate()}
                required
              />
            </div>
          </form>
        </div>

        <div className="form-footer">
          <button type="button" className="cancel-btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" form="passport-form" className="submit-btn">
            Apply
          </button>
        </div>
      </div>

      {showSlotDialog && slotInfo && (
        <>
          <div className="dialog-overlay" onClick={closeDialog}></div>
          <div className="dialog">
            <div className="dialog-header">
              <h3>Slot Information</h3>
            </div>
            <div className="dialog-content">
              <p><strong>Selected Date:</strong> {slotInfo.date}</p>
              <p><strong>Already Booked:</strong> {slotInfo.booked_count}</p>
              <p><strong>Available Slots:</strong> <span className={slotInfo.remaining_slots > 0 ? 'available' : 'unavailable'}>{slotInfo.remaining_slots}</span></p>
              
              {slotInfo.remaining_slots === 0 && (
                <p className="warning-message">Sorry! No slots available for this date. Please select another date.</p>
              )}
              
              {slotInfo.remaining_slots > 0 && (
                <p className="success-message">Great! Slots are available. You can proceed with your application.</p>
              )}
            </div>
            <div className="dialog-footer">
              {slotInfo.remaining_slots === 0 ? (
                <button className="dialog-btn change-btn" onClick={changeDate}>
                  Change Date
                </button>
              ) : (
                <button className="dialog-btn ok-btn" onClick={closeDialog}>
                  OK
                </button>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default PassportApplicationForm;
