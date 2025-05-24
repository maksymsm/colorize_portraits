import React from 'react';
import { buttonStyles } from '../styles/components';

const ImageUploader = ({ 
  onColoredFileChange, 
  onGrayscaleFileChange, 
  onSubmit, 
  coloredFile,
  grayscaleFile,
  loading 
}) => {
  return (
    <form onSubmit={onSubmit}>
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '10px' }}>
          Original Colored Image:
          <input 
            type="file" 
            accept="image/*" 
            onChange={onColoredFileChange}
            style={{ marginLeft: '10px' }}
          />
        </label>
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '10px' }}>
          Grayscale Image:
          <input 
            type="file" 
            accept="image/*" 
            onChange={onGrayscaleFileChange}
            style={{ marginLeft: '10px' }}
          />
        </label>
      </div>

      <button 
        type="submit" 
        disabled={!coloredFile || !grayscaleFile || loading}
        style={{
          ...buttonStyles.primary,
          ...(!coloredFile || !grayscaleFile || loading ? buttonStyles.disabled : {})
        }}
      >
        {loading ? 'Processing...' : 'Upload & Colorize'}
      </button>
    </form>
  );
};

export default ImageUploader; 