'use client';
import { useState } from 'react';

export default function EscalatePage(){
  const [qid, setQid] = useState('');
  const [officers, setOfficers] = useState<any[]>([]);

  const submit = async () => {
    const resp = await fetch('/api/escalate', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({query_id: Number(qid)})
    });
    setOfficers(await resp.json());
  };

  return (
    <main className="p-4">
      <h1>ఎస్కలేషన్ డ్యాష్‌బోర్డ్</h1>
      <input value={qid} onChange={e=>setQid(e.target.value)} className="border" placeholder="Query ID"/>
      <button onClick={submit} className="bg-blue-500 text-white px-4 py-2 ml-2">పొందండి</button>
      <ul>
        {officers.map((o,i)=>(
          <li key={i}>{o.name} - {o.phone} ({o.distance_km.toFixed(1)} km)</li>
        ))}
      </ul>
    </main>
  );
}
