import React, { useState, useEffect } from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import JSZip, { file } from 'jszip';
import axios from 'axios';
import zipFilePath from '../public/assets/frames_800x800_tentoten.zip';

import ReactLoading from 'react-loading';

import {enviroment} from '../common/enviroment';



function Project() {
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const navigate = useNavigate();
    const location = useLocation();
    const [images, setImages] = useState([]);
    const [isMedium, setIsMedium] = useState(window.matchMedia("(min-width: 1600px)").matches);
    const [isLoading, setIsLoading] = useState(true);
    const [donwloading, setDownloading] = useState(false);

    const project_id = location.state.project;

    const goBack = () => {
        // back to the previous page
        navigate(-1);
    }

    const handleScroll = (event) => {
        const delta = event.deltaY;
    
        if (delta < 0 && currentImageIndex < images.length - 1) {
            setCurrentImageIndex(Math.min(currentImageIndex + 1, images.length - 1)); // Move para a próxima imagem ou volta para o final
        } else if (delta > 0 && currentImageIndex > 0) {
            setCurrentImageIndex(Math.max(currentImageIndex - 1, 0)); // Move para a imagem anterior ou volta para o início
        }
    };

    useEffect(() => {
        const handleResize = () => {
            setIsMedium(window.matchMedia("(min-width: 1600px)").matches);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    useEffect(() => {
        if (!location.state || !location.state.project) {
            navigate("/");
        } else {
            
            console.log("project_id", project_id)
            const loadImages = async () => {
                if(donwloading) return;
                try {
                    const imagesFromLocalStorage = localStorage.getItem(`project_${project_id}`);
                    if (imagesFromLocalStorage) {
                        setImages(JSON.parse(imagesFromLocalStorage));
                    }
                    else {
                        const response = await axios.get(`${enviroment}/get_images/${project_id}`, {
                            headers: { "ngrok-skip-browser-warning": "true" }
                          });

                        setDownloading(true);
                        console.log("downloading images");

                        const images_base64 = response.data.images;

                        const blobs = [];

                        for(let i = 0; i < images_base64.length; i++) {
                            const image = images_base64[i];
                            const imageBlob = await fetch(`data:image/png;base64,${image}`).then(res => res.blob());
                            blobs.push(imageBlob);
                        }

                        localStorage.setItem(`project_${project_id}`, JSON.stringify(blobs.map(blob => URL.createObjectURL(blob))));
                        setImages(blobs.map(blob => URL.createObjectURL(blob)));

                    }

                } catch (error) {
                    console.error('Error loading images from ZIP:', error);
                } finally {
                    setDownloading(false);           
                    setIsLoading(false);
                }

            };

            loadImages();
        }
    }, [project_id]);


    return (
        <>
            <div className="grid h-screen bg-black justify-center items-center">
                <div className={`overflow-hidden rounded-lg object-cover relative ${isMedium ? 'size-[80rem]' : 'size-[35rem]'}`} id="image-container" onWheel={handleScroll} >
                    {isLoading && 
                        <div className="flex items-center justify-center " style={{marginTop: "50%", marginBottom: "50%"}}>
                            <ReactLoading type='bars' />
                        </div>
                    }
                    {images.length === 0 && !isLoading && 
                    <div className="absolute flex items-center justify-center w-full h-full bg-black bg-opacity-50">
                        <div className="text-white">No images found</div>
                    </div>}
                    {images.length > 0 && !isLoading &&
                    <img
                        src={images[currentImageIndex]}
                    />
                    }
                </div>
                <div className="inline-flex items-center justify-center w-auto">
                    <div className="relative hidden md:inline-flex">
                        <div className="absolute transition-all duration-200 rounded-full -inset-px bg-gradient-to-r from-cyan-500 to-purple-500 group-hover:shadow-lg group-hover:shadow-cyan-500/50 hover:bg-cyan-600 justify-center"></div>
                        <a onClick={goBack} href="#" title="" className="relative inline-flex items-center justify-center px-10 py-1 text-base font-normal text-white bg-black border border-transparent rounded-full hover:bg-blue-500 " role="button">Back</a>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Project;

