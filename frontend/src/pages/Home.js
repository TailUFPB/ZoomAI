import Chaos from "../public/assets/ccchaos.svg";
import React from 'react';

import axios from 'axios';
import {enviroment}  from '../common/enviroment'

import UploadButton from '../components/UploadButton.js'
import PromptInput from '../components/PromptInput.js'
import { STATUS_ENUM, STATUS_MESSAGE } from "../common/status_enum.js";

import { ToastContainer, toast } from 'react-toastify';
import { ViewsContext } from "../contexts/ViewsContext.js";

const TextOnly = () => {
  const [prompt, setPrompt] = React.useState("");
  const { viewIndex } = React.useContext(ViewsContext);   

  const notify = (messageType) => {
    console.log("Message type", messageType)
    if(messageType === STATUS_ENUM.STARTED){
      toast.success(STATUS_MESSAGE.STARTED);
    } else if (messageType === STATUS_ENUM.RUNNING){
      toast.info(STATUS_MESSAGE.RUNNING);
    }
    else if (messageType === STATUS_ENUM.ERROR){
      toast.error(STATUS_MESSAGE.ERROR);
    }
    else if (messageType === STATUS_ENUM.INVALID){
      toast.warn(STATUS_MESSAGE.INVALID);
    }

  }

  const verifyMessage = (message) => {
    if (message === STATUS_ENUM.STARTED) {
      return STATUS_ENUM.STARTED;
    } else if (message === STATUS_ENUM.RUNNING) {
      return STATUS_ENUM.RUNNING;
    }
    else if (message === STATUS_ENUM.INVALID) {
      return STATUS_ENUM.INVALID;
    }
    else {
      return STATUS_ENUM.ERROR;
    }
  }

  const createFileUploadRequest = async (formData) => {
    let messageType = STATUS_ENUM.ERROR;
    try {
      const response = await axios.post(`${enviroment}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
        });
      console.log("Response", response.data)
      messageType = verifyMessage(response.data);
    } catch (error) {
      console.error('Error creating project:', error);
      messageType = STATUS_ENUM.ERROR;
    }
    finally {

      notify(messageType);
    }
  }


  const creteProjectRequest = async () => {

    let messageType = STATUS_ENUM.ERROR;

    try {
      if (prompt === "") {
        messageType = STATUS_ENUM.INVALID;
        return;
      }
      const response = await axios.post(`${enviroment}/create/${prompt}`);
      console.log("Response", response.data)
      
      messageType = verifyMessage(response.data);

    } catch (error) {
      console.error('Error creating project:', error);
      messageType = STATUS_ENUM.ERROR;
    }
    finally {
      notify(messageType);
      setPrompt("");
    } 
  }

    return (
      <>

      <ToastContainer
        position="bottom-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        limit={3}
        draggable
        theme="dark"
      />
      
      <section className="relative overflow-hidden bg-black sm:pb-16 lg:pb-20 xl:pb-24 ">
        
        <div className="px-4 mx-auto relativea sm:px-6 lg:px-8 max-w-7xl ">
          <div className="grid items-center grid-cols-1 gap-y-12 lg:grid-cols-2 gap-x-16" style={{position: "relative", bottom: "50px", left: "50px"}}>
            <div>
              <h1 className="text-4xl font-bold text-white sm:text-5xl lg:text-6xl xl:text-7xl">
                ZoomAI
              </h1>
              <p className="mt-4 text-md font-normal text-gray-400 sm:mt-8">
                Discover the creative power of artificial intelligence with ZoomAI. 
                Explore the infinity of possibilities with infinite zoom technology 
                and let yourself be carried away by a visual experience that challenges the limits of imagination.
              </p>
              {viewIndex === 0 ? 
                <PromptInput request={creteProjectRequest} prompt={prompt} setPrompt={setPrompt}/>
                :
                <UploadButton request={createFileUploadRequest}/> 
              }
            </div>
  
            <div className="relative lg:col-start-2">
              <div className="" style={{userSelect: 'none'}}>
                {/**Gradiente aqui */}
                <img  src={Chaos} alt="" className="rotate" draggable="false"/>
              </div>
            </div>

          </div>
        </div>
      </section>
      </>
    );
  };
  
  export default TextOnly;
  