import React, { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import ImageDisplay from './components/ImageDisplay';
import { colorizeImage } from './services/api';

function App() {
  const [coloredFile, setColoredFile] = useState(null);
  const [grayscaleFile, setGrayscaleFile] = useState(null);
  const [coloredUrl, setColoredUrl] = useState(null);
  const [grayscaleUrl, setGrayscaleUrl] = useState(null);
  const [colorizedUrl, setColorizedUrl] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleColoredFileChange = (e) => {
    const file = e.target.files[0];
    console.log('Colored file selected:', file);
    setColoredFile(file);
    setColorizedUrl(null);
    setMetrics(null);
    setError('');
    if (file) {
      setColoredUrl(URL.createObjectURL(file));
    } else {
      setColoredUrl(null);
    }
  };

  const handleGrayscaleFileChange = (e) => {
    const file = e.target.files[0];
    console.log('Grayscale file selected:', file);
    setGrayscaleFile(file);
    setColorizedUrl(null);
    setMetrics(null);
    setError('');
    if (file) {
      setGrayscaleUrl(URL.createObjectURL(file));
    } else {
      setGrayscaleUrl(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!coloredFile || !grayscaleFile) return;
    
    console.log('Submitting files:', {
      colored: coloredFile,
      grayscale: grayscaleFile
    });
    
    setLoading(true);
    setError('');
    setColorizedUrl(null);
    setMetrics(null);

    try {
      const result = await colorizeImage(coloredFile, grayscaleFile);
      console.log('API response:', result);
      setColorizedUrl(result.colorizedImageUrl);
      setMetrics(result.metrics);
    } catch (err) {
      console.error('Error details:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 1200, margin: '40px auto', textAlign: 'center' }}>
      <h1>Portrait Colorizer</h1>
      
      <ImageUploader
        onColoredFileChange={handleColoredFileChange}
        onGrayscaleFileChange={handleGrayscaleFileChange}
        onSubmit={handleSubmit}
        coloredFile={coloredFile}
        grayscaleFile={grayscaleFile}
        loading={loading}
      />

      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {(coloredUrl || grayscaleUrl || colorizedUrl) && (
        <ImageDisplay
          coloredUrl={coloredUrl}
          grayscaleUrl={grayscaleUrl}
          colorizedUrl={colorizedUrl}
          metrics={metrics}
        />
      )}
    </div>
  );
}

export default App;
