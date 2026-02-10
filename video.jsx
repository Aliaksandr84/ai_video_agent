import React, { useRef, useCallback } from 'react';
import Webcam from "react-webcam";

const App = () => {
  const webcamRef = useRef(null);

  const capture = useCallback(async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const blob = await (await fetch(imageSrc)).blob();
    const formData = new FormData();
    formData.append('image', blob, 'snapshot.jpg');

    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    alert(JSON.stringify(data));
  }, [webcamRef]);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={350}
      />
      <button onClick={capture}>Capture & Analyze</button>
    </div>
  );
};

export default App;