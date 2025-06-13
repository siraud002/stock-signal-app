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
  const [mode, setMode] = React.useState('screen');  // track which screener is being used

  const handleScreenSubmit = async (e) => {
    e.preventDefault();
    if (!symbols) return;

    setLoading(true);
    setError('');
    setResults([]);
    setMode('screen');

    try {
      const res = await axios.get('http://localhost:8000/screen', {
        params: { symbols, short_ma: shortMA, long_ma: longMA },
      });
      setResults(res.data);
    } catch (err) {
      setError('Server error while running custom screener.');
    } finally {
      setLoading(false);
    }
  };

  const handleCompressionScreen = async () => {
    setLoading(true);
    setError('');
    setResults([]);
    setMode('compression');

    try {
      const res = await axios.get('http://localhost:8000/compression_screen');
      setResults(res.data);
    } catch (err) {
      setError('Server error while running compression screener.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', width: '100%' }}>
      <h1>Stock Screener App</h1>

      <form onSubmit={handleScreenSubmit} style={{ marginBottom: '20px' }}>
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
        <button type="submit">Run Custom Screener</button>
      </form>

      <button onClick={handleCompressionScreen} style={{ marginBottom: '20px' }}>
        Run Compression Screener
      </button>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <div className="card" style={{ marginTop: '20px' }}>
          <table style={{ width: '80%', margin: '0 auto', borderCollapse: 'collapse', border: '1px solid #ddd' }}>
            <thead>
              <tr style={{ backgroundColor: '#f2f2f2' }}>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>Symbol</th>
                <th style={{ border: '1px solid #ddd', padding: '10px' }}>Price</th>
                {mode === 'screen' ? (
                  <>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA Short</th>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA Long</th>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>Signal</th>
                  </>
                ) : (
                  <>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA20</th>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA35</th>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>SMA50</th>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>Delta1</th>
                    <th style={{ border: '1px solid #ddd', padding: '10px' }}>Delta2</th>
                  </>
                )}
              </tr>
            </thead>
            <tbody>
              {results.map((item, index) => (
                <tr key={item.symbol} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f9f9f9' }}>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.symbol}</td>
                  <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.price}</td>

                  {mode === 'screen' ? (
                    <>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.sma_short}</td>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.sma_long}</td>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.signal}</td>
                    </>
                  ) : (
                    <>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.SMA20}</td>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.SMA35}</td>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.SMA50}</td>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.delta1}</td>
                      <td style={{ border: '1px solid #ddd', padding: '10px' }}>{item.delta2}</td>
                    </>
                  )}
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

