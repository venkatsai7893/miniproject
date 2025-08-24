import React, { useState } from 'react';
import './UploadForm.css';

function UploadForm() {
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = e.target.image.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    setLoading(true);
    setResultImage(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Detection failed');

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setResultImage(imageUrl);
    } catch (err) {
      alert('❌ Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🕵️‍♂️ Image Forgery Detection</h1>
        <p>Upload an image to detect copy-move forgery.</p>
      </header>

      <form onSubmit={handleSubmit}>
        <input type="file" name="image" accept="image/*" required />

        <button type="submit">🧠 Detect Forgery</button>
      </form>

      {loading && <div className="loader"></div>}

      {resultImage && (
        <div id="resultContainer">
          <h2>🔍 Detection Result</h2>
          <img src={resultImage} alt="Detection result" />
        </div>
      )}
    </div>
  );
}

export default UploadForm;
