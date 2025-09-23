import React from 'react'
import { useState } from 'react'
import { useNavigate } from "react-router-dom"; // If using react-router



export default function Login() {
    const navigate = useNavigate();

    const [role, setRole] = useState("party"); // Default active tab = party
    const [id, setId] = useState("");
    const [password, setPassword] = useState("");
  
    const handleSubmit = (e) => {
      e.preventDefault();
      localStorage.setItem('user',JSON.stringify({ role, id, password }))
      navigate('/dashboard')
      console.log({ role, id, password });
    };
  
    return (
      <div className="flex items-center justify-center min-h-screen bg-black text-white">
        <div className="w-full max-w-md p-8 rounded-2xl shadow-lg bg-zinc-900">
          <h1 className="text-2xl font-semibold mb-6 text-center">Sign Up</h1>
  
          {/* Tab Bar */}
          <div className="flex border-b border-zinc-700 mb-6">
            <button
              onClick={() => setRole("admin")}
              className={`flex-1 py-2 text-center font-medium transition ${
                role === "admin"
                  ? "border-b-2 border-white text-white"
                  : "text-zinc-400 hover:text-white"
              }`}
            >
              Admin
            </button>
            <button
              onClick={() => setRole("party")}
              className={`flex-1 py-2 text-center font-medium transition ${
                role === "party"
                  ? "border-b-2 border-white text-white"
                  : "text-zinc-400 hover:text-white"
              }`}
            >
              Party
            </button>
          </div>
  
          {/* Form */}
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block mb-2 text-sm font-medium">ID</label>
              <input
                type="text"
                value={id}
                onChange={(e) => setId(e.target.value)}
                placeholder="Enter your ID"
                className="w-full p-3 rounded-lg bg-black border border-zinc-700 placeholder-gray-400 focus:border-white focus:outline-none"
              />
            </div>
  
            <div className="mb-6">
              <label className="block mb-2 text-sm font-medium">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="w-full p-3 rounded-lg bg-black border border-zinc-700 placeholder-gray-400 focus:border-white focus:outline-none"
              />
            </div>
  
            <button
              type="submit"
              className="w-full p-3 rounded-lg bg-white text-black font-semibold hover:bg-zinc-200 transition"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    );
}
