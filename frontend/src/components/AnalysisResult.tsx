import React from 'react';
import '../AnalysisResult.css'; // Make sure to import your CSS file

interface AnalysisResultProps {
    imageUrl: string;
    onBackClick: () => void;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ imageUrl, onBackClick }) => {
    return (
        <div>
        <div className={`d-flex justify-content-flex-start form-container fixed-container`}>
            <img src={imageUrl} alt="Analysis Result" style={{ width: '100%', height: '100%' }} />
        </div>
        <div className="d-flex justify-content-center">
        <button className="btn btn-primary btn-rounded" onClick={onBackClick}>Back to Initial Page</button>
        </div>
    </div>
    );
}

export default AnalysisResult;
