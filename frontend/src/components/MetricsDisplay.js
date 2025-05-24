import React from 'react';
import { metricsStyles } from '../styles/components';

const MetricsDisplay = ({ metrics }) => (
  <div style={metricsStyles.container}>
    <h3 style={metricsStyles.heading}>Quality Metrics:</h3>
    <p><strong>PSNR:</strong> {metrics.psnr.toFixed(2)} dB</p>
    <p><strong>SSIM:</strong> {metrics.ssim.toFixed(4)}</p>
    <p style={metricsStyles.description}>
      Higher values indicate better quality:
      <br />- PSNR {'>'}30dB is considered good
      <br />- SSIM closer to 1.0 is better
    </p>
  </div>
);

export default MetricsDisplay; 