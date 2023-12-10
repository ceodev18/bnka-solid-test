import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CreateUser() {
  const navigate = useNavigate();


  const [formData, setFormData] = useState({
    username: '',
    email: '',
  });

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();

    try {
      const form = new FormData();
      form.append('username', formData.username);
      form.append('email', formData.email);
      await axios.post(`${process.env.REACT_APP_BACKEND_API}/create_user`, form);
      navigate('/get_all_users');

    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  return (
    <div>
      <h2>Create User</h2>
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
      <button onClick={handleCreateUser}>Create User</button>
    </div>
  );
}

export default CreateUser;
