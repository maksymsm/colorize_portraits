import React, { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import ImageDisplay from './components/ImageDisplay';
import { colorizeImage } from './services/api';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [originalUrl, setOriginalUrl] = useState(null);
  const [colorizedUrl, setColorizedUrl] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setColorizedUrl(null);
    setMetrics(null);
    setError('');
    if (file) {
      setOriginalUrl(URL.createObjectURL(file));
    } else {
      setOriginalUrl(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    
    setLoading(true);
    setError('');
    setColorizedUrl(null);
    setMetrics(null);

    try {
      const result = await colorizeImage(selectedFile);
      setColorizedUrl(result.imageUrl);
      setMetrics(result.metrics);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', textAlign: 'center' }}>
      <h1>Portrait Colorizer</h1>
      
      <ImageUploader
        onFileChange={handleFileChange}
        onSubmit={handleSubmit}
        selectedFile={selectedFile}
        loading={loading}
      />

      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {(originalUrl || colorizedUrl) && (
        <ImageDisplay
          originalUrl={originalUrl}
          colorizedUrl={colorizedUrl}
          metrics={metrics}
        />
      )}
    </div>
  );
}

export default App;
