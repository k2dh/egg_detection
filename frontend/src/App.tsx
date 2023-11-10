import React, { useState } from 'react';
import ImageUpload from "./components/ImageUpload";
import NavigationBar from "./components/NavigationBar";
import axios from 'axios';
import LoadingIndicator from "./components/LoadingIndicator";
import AnalysisResult from './components/AnalysisResult';
import './App.css';

function App() {
  const State = {
    Initial: 0,
    Loading: 1,
    Result: 2,
  }

  const backendAddress = 'http://localhost:33333/api/eggs/'
  const [appState, setAppState] = useState(State.Initial);
  const [imageUrl, SetImageUrl] = useState<string>('');
  
  const startLoading = () => {
    setAppState(State.Loading);
  }

  const getResult = async () => {
    try {
      const response = await axios.get(backendAddress);
      let imagelist = new Array();
      imagelist = response.data;
      SetImageUrl(imagelist.at(-1).image);
      setAppState(State.Result);
    } catch (error) {
      console.error('Error getting result', error);
    }
  };

  const handleBackClick = () => {
    setAppState(State.Initial); // Set the state back to Initial when the button is clicked
  };

  return (
    <div className="background-image">
      <NavigationBar className="navigation-bar"/>
      <div className="main-content">
        {appState==State.Loading && <LoadingIndicator />}
        {appState==State.Initial && <ImageUpload onUploadStart={startLoading} onGettingResult={getResult}/>}
        {appState === State.Result && <AnalysisResult imageUrl={imageUrl} onBackClick={handleBackClick} />}
      </div>
    </div>
  );
}

export default App;