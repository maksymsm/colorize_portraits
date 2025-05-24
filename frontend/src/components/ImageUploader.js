import React from 'react';
import { buttonStyles } from '../styles/components';

const ImageUploader = ({ onFileChange, onSubmit, selectedFile, loading }) => {
  return (
    <form onSubmit={onSubmit}>
      <input 
        type="file" 
        accept="image/*" 
        onChange={onFileChange}
      />
      <br /><br />
      <button 
        type="submit" 
        disabled={!selectedFile || loading}
        style={{
          ...buttonStyles.primary,
          ...((!selectedFile || loading) && buttonStyles.disabled)
        }}
      >
        {loading ? 'Colorizing...' : 'Upload & Colorize'}
      </button>
    </form>
  );
};

export default ImageUploader; 