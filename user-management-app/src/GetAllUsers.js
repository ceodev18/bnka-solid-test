import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function GetAllUsers() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchAllUsers = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_API}/get_all_users`);
        setUsers(response.data.users);
      } catch (error) { 
        console.error('Error fetching all users:', error);
      }
    };

    fetchAllUsers();
  }, []);

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`${process.env.REACT_APP_BACKEND_API}/delete_user/${userId}`);
      setUsers((prevUsers) => prevUsers.filter((user) => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <div>
      <h2>All Users</h2>
      <Link to="/create_user">
        <button>Add User</button>
      </Link>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>
                <Link to={`/edit_user/${user.id}`}>
                  <button>Edit</button>
                </Link>
                <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GetAllUsers;
