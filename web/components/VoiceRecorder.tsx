'use client';
export default function VoiceRecorder(){
  const record = () => alert('voice recording stub');
  return <button onClick={record} className="bg-gray-200 px-2">🎤</button>;
}
