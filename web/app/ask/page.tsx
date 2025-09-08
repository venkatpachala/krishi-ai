'use client';
import { useState } from 'react';
import VoiceRecorder from '../../components/VoiceRecorder';

export default function AskPage() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState<any>(null);

  const submit = async () => {
    const resp = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({query})
    });
    const data = await resp.json();
    setAnswer(data);
  };

  return (
    <main className="p-4">
      <h1>ప్రశ్న అడగండి</h1>
      <div className="flex items-center space-x-2">
        <textarea value={query} onChange={e=>setQuery(e.target.value)} className="border w-full"/>
        <VoiceRecorder />
      </div>
      <button onClick={submit} className="bg-green-500 text-white px-4 py-2 mt-2">పంపండి</button>
      {answer && (
        <pre className="bg-gray-100 p-2 mt-2">{JSON.stringify(answer, null, 2)}</pre>
      )}
    </main>
  );
}
