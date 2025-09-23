import React from "react";
import { useNavigate } from "react-router-dom"; // If using react-router
import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [totalAmount, setTotalAmount] = useState(0);
  const [splits, setSplits] = useState([]);
  const [partyName, setPartyName] = useState('');
  const [isExists, setIsExists] = useState(false);
  const [id , setId] = useState('');

  useEffect(()=>{
    let data = JSON.parse(localStorage.getItem('user'));
    setRole(data.role);
    setId(data.id);
  },)

  async function fetchParties(){
    let userdata = JSON.parse(localStorage.getItem('user'));

    const data  = await(await axios.get('http://localhost:8003/parties')).data;
    if(data){
      if(data.length > 0){
        setIsExists(true);
      }
      data.forEach(element => {
        if(element.party_id === userdata.id) {setTotalAmount(element.total_amount); setPartyName(element.party_name)}
      });
      console.log(data)
    }
  }
  async function fetchSplits(){
    const data  = await(await axios.get('http://localhost:8003/splits')).data;
    if(data){
     setSplits(data);
    }
  }

  useEffect(()=>{
    fetchParties()
  },[])

  useEffect(()=>{
    fetchSplits()
  },[])



  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header */}
      <header className="p-6 border-b border-zinc-800 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Welcome - {partyName?partyName: 'User'}</h1>
        <div className="flex items-center justify-center">
        {role === "admin" && isExists === false ?
          <button
            onClick={() => navigate("/admin")}
            className="px-5 py-2 rounded-lg bg-white text-black font-semibold hover:bg-zinc-200 transition"
          >
            Manage Parties
          </button>:<></>
        }
          <button
            onClick={() =>{ localStorage.clear(); navigate("/")}}
            className="px-5 py-2 m-3 rounded-lg bg-white text-black font-semibold hover:bg-zinc-200 transition"
          >
            Log Out
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-6">
        {/* Balance Section */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-2">Wallet Balance</h2>
          <p className="text-5xl font-bold">₹{totalAmount.toLocaleString()}</p>
        </section>

        {/* Transactions */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Transactions</h2>
          <div className="overflow-y-auto max-h-[70vh] space-y-4 pr-2">
            {splits.map((txn) => (
              txn.party_id === id ?
              
              <div
                key={txn.id}
                className="flex justify-between items-center p-4 rounded-xl bg-zinc-900 border border-zinc-700"
              >
                <div>
                  <p className="font-medium">{txn.order_id}</p>
                  <p className="text-sm text-zinc-400">{txn.timestamp}</p>
                </div>
                <p
                  className={`font-semibold text-lg ${
                    txn.amount < 0 ? "text-red-400" : "text-green-400"
                  }`}
                >
                  {txn.amount < 0 ? `- ₹${Math.abs(txn.amount)}` : `+ ₹${txn.amount}`}
                </p>
              </div>: <></>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
