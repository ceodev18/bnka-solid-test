// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import GetAllUsers from './GetAllUsers';
import CreateUser from './CreateUser';
import UpdateUser from './UpdateUser';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/get_all_users" element={<GetAllUsers />} />
          <Route path="/create_user" element={<CreateUser />} />
          <Route path="/edit_user/:userId" element={<UpdateUser />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
