
const Navbar  = () => {
    const navItems = [
        {link: "text Only", path: "textOnly"},
        {link: "Image Only", path: "imageOnly"},
        {link: "Image + Text", path: "imageText"},
    ]
    return (
        <nav className="bg-white p-6 max-w-screen-2x1 mx-auto ">
            <div className="text-lg container mx-auto flex justify-between items-center font-medium">
                <div className="flex space-x-14 items-center">
                    <a href="/" className="text-2x1 font-semibold flex items-center space-x-3"><img src="/" alt="{Logo}" className="w-10 inline-block items-center" /><span>ZoomAI</span></a>

                    {/**showing navitem using map */}
                    <ul className="md:flex space-x-12">
                        {
                            navItems.map(({link, path}) => <a key={link} href="{path}" className="block hover:text-gray-300" >{link}</a>)
                        }
                    </ul>
                </div>

                {/** My projets*/}
                <div className="space-x-12 hiden md:flex items-center">
                    <button className="bg-red py-2 px-4 transition-all duration-300 border border-sky-400 rounded-full hover:text-white hover:bg-indigo-600">My Projets</button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;