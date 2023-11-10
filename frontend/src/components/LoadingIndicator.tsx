import React from 'react';
import '../LoadingIndicator.css'; // Assume you will create a separate CSS file for styles

const LoadingIndicator: React.FC = () => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p>Loading...</p>
    </div>
  );
};

export default LoadingIndicator;
