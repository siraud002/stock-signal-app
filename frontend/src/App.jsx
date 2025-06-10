function App() {
  const [symbols, setSymbols] = React.useState('');
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
      const res = await axios.get('http://localhost:8000/fetch_stocks', { params: { symbols } });
      setResults(res.data);
    } catch (err) {
      setError('Invalid symbol(s) or server error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', width: '100%' }}>
      <h1>Stock Signal</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={symbols}
          onChange={(e) => setSymbols(e.target.value)}
          placeholder="Enter symbols, comma separated"
        />
        <button type="submit">Fetch</button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      {results.length > 0 && !loading && (
        <div className="card">
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ borderBottom: '1px solid #ddd', padding: '8px' }}>Symbol</th>
                <th style={{ borderBottom: '1px solid #ddd', padding: '8px' }}>Price</th>
                <th style={{ borderBottom: '1px solid #ddd', padding: '8px' }}>Moving Avg</th>
                <th style={{ borderBottom: '1px solid #ddd', padding: '8px' }}>Signal</th>
              </tr>
            </thead>
            <tbody>
              {results.map((item) => (
                <tr key={item.symbol}>
                  <td style={{ borderBottom: '1px solid #eee', padding: '8px' }}>{item.symbol}</td>
                  <td style={{ borderBottom: '1px solid #eee', padding: '8px' }}>{item.price}</td>
                  <td style={{ borderBottom: '1px solid #eee', padding: '8px' }}>{item.moving_average}</td>
                  <td style={{ borderBottom: '1px solid #eee', padding: '8px' }}>{item.signal}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
