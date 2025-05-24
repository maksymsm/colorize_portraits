import React from 'react';
import MetricsDisplay from './MetricsDisplay';
import { imageStyles, buttonStyles, imageContainerStyles } from '../styles/components';

const ImageDisplay = ({ coloredUrl, grayscaleUrl, colorizedUrl, metrics }) => {
  return (
    <div style={imageContainerStyles}>
      {coloredUrl && (
        <div>
          <h3>Original Colored Image</h3>
          <img src={coloredUrl} alt="Original Colored" style={imageStyles} />
        </div>
      )}
      
      {grayscaleUrl && (
        <div>
          <h3>Grayscale Image</h3>
          <img src={grayscaleUrl} alt="Grayscale" style={imageStyles} />
        </div>
      )}
      
      {colorizedUrl && (
        <div>
          <h3>Colorized Result</h3>
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