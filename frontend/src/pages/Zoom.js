import React, { useState, useEffect } from 'react';
import {useNavigate} from 'react-router-dom';
import JSZip from 'jszip';
import axios from 'axios';
import zipFilePath from '../public/assets/frames_800x800.zip';

function Project() {
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const navigate = useNavigate();
    const [images, setImages] = useState([]);

    const goBack = () => {
        navigate("/");
    }

    const handleScroll = (event) => {
        const delta = event.deltaY;
    
        if (delta < 0 && currentImageIndex < images.length - 1) {
            setCurrentImageIndex(Math.min(currentImageIndex + 10, images.length - 1)); // Move para a próxima imagem ou volta para o final
        } else if (delta > 0 && currentImageIndex > 0) {
            setCurrentImageIndex(Math.max(currentImageIndex - 10, 0)); // Move para a imagem anterior ou volta para o início
        }
    };

    useEffect(() => {
        const loadImagesFromZip = async () => {
            try {
                const response = await axios.get(zipFilePath, { responseType: 'arraybuffer' });
                const zip = new JSZip();
                const zipContent = await zip.loadAsync(response.data);

                const files = zip.folder().files;
                const imagePromises = [];

                for (let i = 0; i < 450; i++) {
                    const imageName = `frame_${i}.png`;
                    imagePromises.push(zip.file(imageName).async('blob'));
                    // console.log(imageName);
                }

                const imageBlobs = await Promise.all(imagePromises);
                const extractedImages = imageBlobs.map((blob) => URL.createObjectURL(blob));
                setImages(extractedImages.reverse());

            } catch (error) {
                console.error('Error loading images from ZIP:', error);
            }
        };

        loadImagesFromZip();
    }, []);


    return (
        <>
            <div class="grid h-screen bg-black justify-center items-center">
                <div class="overflow-hidden object-cover size-[35rem] rounded-lg shadow-lg shadow-gray-500" id="image-container" onWheel={handleScroll}>
                    <img
                        src={images[currentImageIndex]}
                    />

                </div>
                <div class="inline-flex items-center justify-center w-auto">
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

