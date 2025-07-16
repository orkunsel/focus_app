import { useState } from 'react';
import './App.css';



export default function App() {
  // State for banned apps and the current input
  const [banned, setBanned] = useState([]);
  const [appInput, setAppInput] = useState('');

  return (
    <div className="p-4">
      <h1 className="text-xl mb-2">🛠️ Lockdown Setup</h1>

      {/* Input + Add button */}
      <div className="flex mb-2">
        <input
          type="text"
          placeholder="App to ban"
          value={appInput}
          onChange={e => setAppInput(e.target.value)}
          className="border p-2 flex-grow mr-2"
        />
        <button
          onClick={() => {
            if (appInput.trim()) {
              setBanned([...banned, appInput.trim().toLowerCase()]);
              setAppInput('');
            }
          }}
          className="px-4 py-2 rounded shadow"
        >
          Add
        </button>
      </div>

      {/* List of banned apps */}
      <ul className="mt-4 list-disc ml-5">
        {banned.map(app => (
          <li key={app}>{app}</li>
        ))}
      </ul>
    </div>
  );
}
