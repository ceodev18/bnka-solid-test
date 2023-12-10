import React, { useState, useEffect } from 'react';
import axios from 'axios';

function GetUser({ match }) {
  const userId = match.params.userId;
  const [user, setUser] = useState({});

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_API}/get_user/${userId}`);
        setUser(response.data);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    };

    fetchUser();
  }, [userId]);

  return (
    <div>
      <h2>User Details</h2>
      <p>Displaying details for user with ID: {userId}</p>
      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
    </div>
  );
}

export default GetUser;
