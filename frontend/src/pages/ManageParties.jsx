
import React, { useState } from "react";
import axios from "axios";

export default function ManageParties() {
  const [parties, setParties] = useState([{party_id:"", party_name: "", split_rule: "" }]);
  const [error, setError] = useState("");
  const [apiData, setApiData] = useState([]);

  function generateRandomId() {
    const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
    let id = "";
    for (let i = 0; i < 6; i++) {
      id += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return id;
  }

  // Calculate total party share
  const totalPartyPercentage = parties.reduce(
    (sum, p) => sum + (parseFloat(p.split_rule) || 0),
    0
  );

  // Admin share = 100 - sum of party %
  const adminShare = 100 - totalPartyPercentage;

  // Add new party row
  const addParty = () => {
    setParties([...parties, {party_id:"", party_name: "", split_rule: "" }]);
  };

  // Handle input change
  const updateParty = (index, field, value) => {
    const updated = [...parties];
    updated[index][field] = value;
    setParties(updated);
  };

  //  Submit logic (modified with "%" suffix)
  const handleSubmit = async () => {
    if (totalPartyPercentage > 100) {
      setError("Total percentage cannot exceed 100%");
      return;
    }
    setError("");

    // Prepare final data with admin included and add "%" to each percentage
    const finalSplit = [
      ...parties.map((p) => ({
        party_id: generateRandomId(),
        party_name: p.party_name,
        split_rule: `${p.split_rule}%`,
      })),
      {party_id:"admin13wb3e", party_name: "Admin", split_rule: `${adminShare < 0 ? 0 : adminShare}%` },
    ];

    const data  = await(await axios.post('http://localhost:8003/parties/bulk', finalSplit)).data;

    console.log("Final Split:", data);
    if(data){

      alert("Split created!");
      setApiData(data);
    }
    else{
      alert("Something Went Wrong");

    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header */}
      <header className="p-6 border-b border-zinc-800">
        <h1 className="text-2xl font-bold">Manage Parties</h1>
      </header>

      {/* Content */}
      <main className="flex-1 p-6 space-y-6">
        {/* Admin Share */}
        <div className="p-4 rounded-xl bg-zinc-900 border border-zinc-700">
          <h2 className="text-lg font-semibold mb-1">Admin Share</h2>
          <p
            className={`text-3xl font-bold ${
              adminShare < 0 ? "text-red-400" : "text-green-400"
            }`}
          >
            {adminShare < 0 ? "0" : adminShare}%
          </p>
        </div>

        {/* Parties */}
        <div className="space-y-4">
          {parties.map((party, index) => (
            <div
              key={index}
              className="flex items-center gap-4 p-4 rounded-xl bg-zinc-900 border border-zinc-700"
            >
              {/* Party Name */}
              <input
                type="text"
                value={party.name}
                onChange={(e) => updateParty(index, "party_name", e.target.value)}
                placeholder="Party Name"
                className="flex-1 p-3 rounded-lg bg-black border border-zinc-700 placeholder-gray-400 focus:border-white focus:outline-none"
              />

              {/* Percentage */}
              <input
                type="number"
                min="0"
                max="100"
                value={party.percentage}
                onChange={(e) =>
                  updateParty(index, "split_rule", e.target.value)
                }
                placeholder="%"
                className="w-28 p-3 rounded-lg bg-black border border-zinc-700 placeholder-gray-400 focus:border-white focus:outline-none"
              />
            </div>
          ))}

          {/* Add More Party */}
          <button
            onClick={addParty}
            className="w-full p-3 rounded-lg bg-zinc-800 text-white font-medium hover:bg-zinc-700 transition"
          >
            + Add More Party
          </button>
        </div>

        {/* Error */}
        {error && <p className="text-red-400 font-medium">{error}</p>}

        {/* Submit */}
        {apiData.length === 0?
         <button
         onClick={handleSubmit}
         className="w-full p-3 rounded-lg bg-white text-black font-semibold hover:bg-zinc-200 transition"
       >
         Create Split
       </button>:
           <div className="w-full min-h-[40px] p-3 bg-white rounded-lg flex items-center justify-center flex-col">
          {apiData.map((party)=>(

           <div className="text-black font-bold">{party.party_name} - {party.party_id} - {party.split_rule}</div>
          ))}
           
         </div>
        }
       

       
      </main>

     
    </div>
  );
}
