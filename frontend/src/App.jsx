import { useState } from 'react'
import { Routes, Route, Navigate } from "react-router-dom";
import './App.css'
import 'tailwindcss'
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Home from "./pages/Home";
import ProtectedRoute from './routes/ProtectedRoute';
function App() {

  return (
    <Routes>
      <Route path='/login' element={<Login />}/>
      <Route path='/signup' element={<Signup />}/>
      <Route path='/' element={
        <ProtectedRoute>
          <Home />
        </ProtectedRoute>
      }/>
      <Route path='*' element={<Navigate to='/'/>}/> 
    </Routes>
  )
}

export default App
