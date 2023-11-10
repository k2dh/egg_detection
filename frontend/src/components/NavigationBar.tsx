import React from 'react';

interface NavigationBarProps {
  className?: string;
}

const NavigationBar:React.FC<NavigationBarProps> = ({className}) => {
  return (
    <nav className={`navbar navbar-expand-lg bg-body-tertiary ${className}`} style={{backgroundColor: "#e3f2fd"}}>
        <div className="container-fluid">
            <a className="navbar-brand" href="#">
                <img src="/images/icon.png" alt="Bootstrap" width="30" height="24" />
            </a>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse d-flex justify-content-end" id="navbarNav">
            <ul className="navbar-nav">
                <li className="nav-item">
                <a className="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li className="nav-item">
                <a className="nav-link" href="#">Nav1</a>
                </li>
                <li className="nav-item">
                <a className="nav-link" href="#">Nav2</a>
                </li>
            </ul>
            </div>
        </div>
    </nav>
  );
};

export default NavigationBar;