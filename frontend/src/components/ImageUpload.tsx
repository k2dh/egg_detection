import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

interface ImageUploadProps {
  onUploadStart: () => void;
  onGettingResult: () => void;
}


const ImageUpload: React.FC<ImageUploadProps> = ({ onUploadStart, onGettingResult }) => {
  const [file, setFile] = useState<File | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string>('https://mdbootstrap.com/img/Photos/Others/placeholder.jpg'); // URL of the basic image
  const backendAddress = 'http://localhost:33333/api/eggs/'


  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setFile(file);

      // Create a URL for the file
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append('name',"test");
      formData.append("image", file);
      onUploadStart();
      try {
        const response = await axios.post(backendAddress, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('File uploaded successfully', response.data);
        await onGettingResult();
      } catch (error) {
        console.error('Error uploading file', error);
      };
    }
  };

  return (
    <div className="d-flex justify-content-flex-start form-container">
        <form onSubmit={handleSubmit}>
            <div className="mb-4 d-flex justify-content-center">
                <img id="selectedImage" src={imagePreviewUrl}
                alt="example placeholder" style={{ width: '600px', height: '600px', objectFit: 'cover' }} />
            </div>
            <div className="d-flex justify-content-center">
                <div className="btn btn-primary btn-rounded">
                    <label className="form-label text-white m-1" htmlFor="customFile1">Upload Image</label>
                    <input type="file" className="form-control d-none" id="customFile1" onChange={handleFileChange} />
                </div>
                <button className="btn btn-primary btn-rounded" type="submit">View Result</button>
            </div>
        </form>
    </div>

  );
};
export default ImageUpload;