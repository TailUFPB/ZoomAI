import React, { useState } from 'react';
import Image from "../public/assets/image.jpeg";

function Project() {
    const [scale, setScale] = useState(1); // Fator de zoom inicial

    const handleScroll = (event) => {
        const delta = event.deltaY / 1000; // Obter a quantidade de rolagem
        const newScale = Math.max(0.5, Math.min(5, scale + delta)); // Limitar o zoom entre 0.5 e 2
        setScale(newScale);
    };

    return (
        <>
            <div class="flex h-screen justify-center items-center overflow-hidden bg-black" id="image-container" onWheel={handleScroll}>
                <img src={Image} style={{ transform: `scale(${scale})` }} />
            </div>
        </>
    );
};

export default Project;

