import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import ImageUpload from "./components/ImageUpload";
import NavigationBar from "./components/NavigationBar";
import axios from 'axios';
import LoadingIndicator from "./components/LoadingIndicator";
import AnalysisResult from './components/AnalysisResult';
import Login from './components/Login';
import SignUp from './components/SignUp';
import './App.css';

function App() {
  const State = {
    Initial: 0,
    Loading: 1,
    Result: 2,
  }

  const backendAddress = 'http://localhost:33333/api/eggs/';
  const [appState, setAppState] = useState(State.Initial);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [token, setToken] = useState<string | null>(null);
  const [loginError, setLoginError] = useState<string | null>(null);

  const startLoading = () => {
    setAppState(State.Loading);
  }

  const getResult = async () => {
    try {
      const response = await axios.get(backendAddress);
      let imagelist = response.data;
      setImageUrl(imagelist.at(-1).image);
      setAppState(State.Result);
    } catch (error) {
      console.error('Error getting result', error);
    }
  };

  const handleBackClick = () => {
    setAppState(State.Initial);
  };

  const handleLogin = async (username: string, password: string, navigate: Function) => {
    try {
      const response = await axios.post('http://localhost:8000/api/token/', {
        username,
        password,
      });
      setToken(response.data.access);
      setAppState(State.Initial);
      navigate('/'); // Navigate to home page
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        // Handle known error response
        setLoginError(error.response.data.detail);
      } else {
        // Handle unknown errors
        setLoginError('An unexpected error occurred. Please try again.');
      }
    }
  };

  const handleSignUp = (username: string, email: string, password: string) => {
    // Implement your signup logic here
    console.log(`Signing up with username: ${username}, email: ${email}, and password: ${password}`);
    // For demo purposes, set app state to Result after signup
    setAppState(State.Initial);
  };

  return (
    <Router>
      <div className="background-image">
        <NavigationBar className="navigation-bar" />
        <div className="main-content">
          {appState === State.Loading && <LoadingIndicator />}
          <Routes>
            <Route path="/" element={<>
              {appState === State.Initial && <ImageUpload onUploadStart={startLoading} onGettingResult={getResult} />}
              {appState === State.Result && <AnalysisResult imageUrl={imageUrl} onBackClick={handleBackClick} />}
            </>} />
            <Route path="/login" element={<Login onLogin={handleLogin} loginError={loginError} />} />
            <Route path="/signup" element={<SignUp onSignUp={handleSignUp} />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
