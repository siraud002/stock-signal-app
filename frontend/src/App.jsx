import React from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [symbol, setSymbol] = React.useState('');
  const [data, setData] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symbol) return;
    setLoading(true);
    setError('');
    setData(null);
    try {
      const res = await axios.get(`http://localhost:8000/fetch_stock/${symbol}`);
      setData(res.data);
    } catch (err) {
      setError('Invalid symbol or server error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', width: '100%' }}>
      <h1>Stock Signal</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Enter symbol"
        />
        <button type="submit">Fetch</button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      {data && !loading && (
        <div className="card">
          <h2>{data.symbol}</h2>
          <p>Price: {data.price}</p>
          <p>Moving Average: {data.moving_average}</p>
          <p>Signal: {data.signal}</p>
        </div>
      )}
    </div>
  );
}

export default App;

