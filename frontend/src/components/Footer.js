import React from "react";
import TailLogo from "../public/assets/TailLogo.svg";

const Footer = () => {
    return (
        <footer className=" bg-black py-8 w-full">
            <div className="px-auto mx-auto sm:px-6 lg:px-8 max-w-7xl ">
                <div className="flex flex-row-reverse mb-10" style={{position:"relative", bottom:"160px"}}>
                    <img className="w-auto mt-[-50px]" src={TailLogo} alt="" draggable="false"/>
                </div>
            </div>
        </footer>
    );
};

export default Footer;