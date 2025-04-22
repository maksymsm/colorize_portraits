import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [colorizedUrl, setColorizedUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setColorizedUrl(null);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    setLoading(true);
    setError('');
    setColorizedUrl(null);
    const formData = new FormData();
    formData.append('image', selectedFile);
    try {
      const response = await axios.post('http://localhost:5050/colorize', formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const url = URL.createObjectURL(response.data);
      setColorizedUrl(url);
    } catch (err) {
      setError('Failed to colorize image.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', textAlign: 'center' }}>
      <h1>Portrait Colorizer</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <br /><br />
        <button type="submit" disabled={!selectedFile || loading}>
          {loading ? 'Colorizing...' : 'Upload & Colorize'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {colorizedUrl && (
        <div>
          <h3>Colorized Image</h3>
          <img src={colorizedUrl} alt="Colorized" style={{ maxWidth: '100%' }} />
          <br />
          <a href={colorizedUrl} download="colorized.png">Download</a>
        </div>
      )}
    </div>
  );
}

export default App;
