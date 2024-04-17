import React, { useState } from 'react';
import Image from "../public/assets/image.jpeg";

function Project() {
    const [scale, setScale] = useState(1); // Fator de zoom inicial

    const handleScroll = (event) => {
        const delta = event.deltaY / 1000; // Obter a quantidade de rolagem
        const newScale = Math.max(1, Math.min(5, scale + delta)); // Limitar o zoom entre 0.5 e 2
        setScale(newScale);
    };

    return (
        <>
            <div class="grid h-screen bg-black justify-center items-center">
                <div class="overflow-hidden object-cover h-auto w-auto rounded-lg shadow-lg shadow-gray-500" id="image-container" onWheel={handleScroll}>
                    <img src={Image} style={{ transform: `scale(${scale})` }} />
                </div>
                <div class="inline-flex items-center justify-center w-auto">
                    <div className="relative hidden md:inline-flex">
                        <div className="absolute transition-all duration-200 rounded-full -inset-px bg-gradient-to-r from-cyan-500 to-purple-500 group-hover:shadow-lg group-hover:shadow-cyan-500/50 hover:bg-cyan-600 justify-center"></div>
                        <a href="#" title="" className="relative inline-flex items-center justify-center px-10 py-1 text-base font-normal text-white bg-black border border-transparent rounded-full hover:bg-blue-500 " role="button">Back</a>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Project;

