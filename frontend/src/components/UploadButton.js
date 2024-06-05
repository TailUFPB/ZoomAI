import React from 'react';
import { BsCloudUploadFill } from "react-icons/bs";

const UploadButton = ({request}) => {
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file){
      const formData = new FormData();
      formData.append('file', file);  
      formData.append('prompt', '');
      console.log("Form data", formData);
      request(formData);
    }
  }

    return (
      <div className="relative mt-8 rounded-full sm:mt-12 transition-all duration-200 bg-white sm:w-auto hover:opacity-90">
        <label htmlFor="file-upload" className="relative cursor-pointer">
          <div className="absolute inset-0 bg-white rounded-full"></div>
          <div className="flex items-center justify-center w-full h-full"  role="button">
            <div className="upload-button inline-flex items-center justify-center w-full px-5 py-5 text-sm font-semibold tracking-widest text-black uppercase ">
              <BsCloudUploadFill className="h-6 w-6" aria-hidden="true" size={30} style={{position: "relative", top: "4px", marginRight: "20px"}}/>
              <span>Upload Image</span>
            </div>
            
          </div>
          <input id="file-upload" name="file-upload" type="file" className="sr-only"  accept="image/png, image/jpeg" onChange={handleFileUpload} />
        </label>
      </div>
    );
  };
export default UploadButton;