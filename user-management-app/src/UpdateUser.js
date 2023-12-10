import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

function UpdateUser() {
  const { userId } = useParams();
  const navigate = useNavigate();

  const [user, setUser] = useState({});
  const [formData, setFormData] = useState({
    username: '',
    email: '',
  });

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_API}/get_user/${userId}`);
        setUser(response.data);
        setFormData({
          username: response.data.username,
          email: response.data.email,
        });
      } catch (error) {
        // Add error handling, e.g., display an error message
        console.error('Error fetching user:', error);
      }
    };

    fetchUser();
  }, [userId]);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdateUser = async () => {
    try {
      const form = new FormData();
      form.append('username', formData.username);
      form.append('email', formData.email);
      await axios.put(`${process.env.REACT_APP_BACKEND_API}/update_user/${userId}`, form);
      navigate('/get_all_users');

    } catch (error) {
      // Add error handling, e.g., display an error message
      console.error('Error updating user:', error);
    }
  };

  return (
    <div>
      <h2>Update User</h2>
      <p>Editing user with ID: {userId}</p>
      <label>
        Username:
        <input type="text" name="username" value={formData.username} onChange={handleInputChange} />
      </label>
      <br />
      <label>
        Email:
        <input type="text" name="email" value={formData.email} onChange={handleInputChange} />
      </label>
      <br />
      <button onClick={handleUpdateUser}>Update User</button>
    </div>
  );
}

export default UpdateUser;
