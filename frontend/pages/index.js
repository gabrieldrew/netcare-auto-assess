import { useState } from 'react';

export default function Home() {
  const [medical, setMedical] = useState(null);
  const [provider, setProvider] = useState(null);
  const [claim, setClaim] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!medical || !provider || !claim) return;
    const formData = new FormData();
    formData.append('medical', medical);
    formData.append('provider', provider);
    formData.append('claim', claim);

    setLoading(true);
    const res = await fetch('http://localhost:8000/assess', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>GapCare Claim Assessment</h1>
      <div>
        <label>Medical Scheme Statement</label>
        <input type="file" accept="application/pdf" onChange={e => setMedical(e.target.files[0])} />
      </div>
      <div>
        <label>Provider Invoice</label>
        <input type="file" accept="application/pdf" onChange={e => setProvider(e.target.files[0])} />
      </div>
      <div>
        <label>Claim Form</label>
        <input type="file" accept="application/pdf" onChange={e => setClaim(e.target.files[0])} />
      </div>
      <button onClick={handleSubmit} disabled={loading} style={{ marginTop: '1rem' }}>
        {loading ? 'Processing...' : 'Run Pre-Assessment'}
      </button>
      {result && (
        <pre style={{ whiteSpace: 'pre-wrap', marginTop: '1rem' }}>
          {JSON.stringify(result.result, null, 2)}
        </pre>
      )}
      {result?.pdf && (
        <a href={`data:application/pdf;base64,${result.pdf}`} download="assessment.pdf">
          Download PDF Report
        </a>
      )}
    </main>
  );
}
