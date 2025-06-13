import React from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [symbols, setSymbols] = React.useState('');
  const [shortMA, setShortMA] = React.useState(20);
  const [longMA, setLongMA] = React.useState(50);
  const [results, setResults] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symbols) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const res = await axios.get('http://localhost:8000/screen', {
        params: {
          symbols,
          short_ma: shortMA,
          long_ma: longMA,
        },
      });
      setResults(res.data);
    } catch (err) {
      setError('Server error while running screener.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', width: '100%' }}>
      <h1>Custom Stock Screener</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <input
            type="text"
            value={symbols}
            onChange={(e) => setSymbols(e.target.value)}
            placeholder="Enter symbols (comma-separated)"
            style={{ width: '300px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Short MA: </label>
          <input
            type="number"
            value={shortMA}
            onChange={(e) => setShortMA(e.target.value)}
            style={{ width: '60px' }}
          />
          &nbsp;&nbsp;
          <label>Long MA: </label>
          <input
            type="number"
            value={longMA}
            onChange={(e) => setLongMA(e.target.value)}
            style={{ width: '60px' }}
          />
        </div>
        <button type="submit">Run Screener</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <div className="card" style={{ marginTop: '20px' }}>
          <table style={{ width: '80%', margin: '0 auto', borderCollapse: 'collapse', border: '1px solid #ddd' }}>
            <thead>
              <tr style={{ backgroundColor: '#f2f2f2' }}>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>Symbol</th>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>Price</th>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA Short</th>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA Long</th>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>Signal</th>
              </tr>
            </thead>
            <tbody>
              {results.map((item, index) => (
                <tr key={item.symbol} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f9f9f9' }}>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.symbol}</td>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.price}</td>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.sma_short}</td>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.sma_long}</td>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.signal}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
