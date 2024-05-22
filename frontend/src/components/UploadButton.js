import React from 'react';
import { BsCloudUploadFill } from "react-icons/bs";

const UploadButton = () => {
    return (
      <div className="relative mt-8 rounded-full sm:mt-12 bg-white">
        <label htmlFor="file-upload" className="relative cursor-pointer">
          <div className="absolute inset-0 bg-white rounded-full"></div>
          <div className="flex items-center justify-center w-full h-full">
            <div className="upload-button inline-flex items-center justify-center w-full px-5 py-5 text-sm font-semibold tracking-widest text-black uppercase transition-all duration-200 bg-white rounded-full sm:w-auto sm:py-3 hover:opacity-90">
              <BsCloudUploadFill className="h-6 w-6" aria-hidden="true" size={30}/>
              <span className='upload-text'>Upload Image</span>
            </div>
            
          </div>
          <input id="file-upload" name="file-upload" type="file" className="sr-only" />
        </label>
      </div>
    );
  };
export default UploadButton;