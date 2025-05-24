import React from 'react';
import MetricsDisplay from './MetricsDisplay';
import { imageStyles, buttonStyles } from '../styles/components';

const ImageDisplay = ({ originalUrl, colorizedUrl, metrics }) => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: '40px', marginTop: '30px', flexWrap: 'wrap' }}>
      {originalUrl && (
        <div>
          <h3>Original Image</h3>
          <img src={originalUrl} alt="Original" style={imageStyles} />
        </div>
      )}
      {colorizedUrl && (
        <div>
          <h3>Colorized Image</h3>
          <img src={colorizedUrl} alt="Colorized" style={imageStyles} />
          <br />
          <a 
            href={colorizedUrl} 
            download="colorized.png"
            style={buttonStyles.download}
          >
            Download
          </a>
          {metrics && <MetricsDisplay metrics={metrics} />}
        </div>
      )}
    </div>
  );
};

export default ImageDisplay; 