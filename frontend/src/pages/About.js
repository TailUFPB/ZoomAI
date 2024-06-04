import foto_allejandro from "../public/assets/allejandro.jpeg";
import foto_fernanda from "../public/assets/fernanda.jpg";
import foto_kaiky from "../public/assets/kaiky.jpeg";
import foto_dantas from "../public/assets/dantas.jpeg";
import foto_puca from "../public/assets/pucavaz.jpeg";

function About() {

    const autors = [
        {
            nome: "Allejandro",
            foto: foto_allejandro,
            cargo: "Back-End Developer",
            linkedin: "https://www.linkedin.com/in/allej-sousa/",
            github: "https://github.com/AllejandroSousa/"
        },
        {
            nome: "Fernanda Azevedo",
            foto: foto_fernanda,
            cargo: "Front-End Developer",
            linkedin: "https://www.linkedin.com/in/fernanda-azevedo-egc/",
            github: "https://github.com/fernandadants"
        },
        {
            nome: "Frankley Kaiky",
            foto: foto_kaiky,
            cargo: "Product Manager",
            linkedin: "https://www.linkedin.com/in/franky03/",
            github: "https://github.com/Franky03"
        },
        {
            nome: "Maria Moura",
            foto: "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&amp;cs=tinysrgb&amp;dpr=3&amp;h=750&amp;w=1260",
            cargo: "Front-End Developer",
            linkedin: "https://www.linkedin.com/in/mariam0ura/",
            github: "https://github.com/MariaM0ura"
        },
        {
            nome: "João Dantas",
            foto: foto_dantas,
            cargo: "Back-End Developer",
            linkedin: "https://www.linkedin.com/in/joao-victor-dantas/",
            github: "https://github.com/theBlueNautilus"
        },
        {
            nome: "Pucavaz",
            foto: foto_puca,
            cargo: "Product Owner",
            linkedin: "https://www.linkedin.com/in/pucavaz/",
            github: "http://github.com/PucaVaz/"
        },
    ]

    let autorsList = [];

    autors.forEach((autor) => {
        autorsList.push(
            <div className="h-40 grid sm:grid-cols-2">
                <div className="relative w-full h-full rounded shadow sm:h-auto">
                    <img
                        className="absolute object-cover w-full h-full rounded"
                        src={autor.foto}
                        alt="Person"
                    /> 
                </div>
                <div className="flex flex-col justify-center mt-5 sm:mt-0 sm:p-5">
                    <p className="text-white text-lg font-normal">{autor.nome}</p>
                    <p className="mb-4 text-xs text-white">{autor.cargo}</p>
                    <div className="flex items-center space-x-3">
                        <a
                            href={autor.linkedin}
                            className="text-white transition-colors duration-300 hover:text-deep-purple-accent-400"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">
                                <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                            </svg>
                        </a>
                        <a
                            href={autor.github}
                            className="text-white transition-colors duration-300 hover:text-deep-purple-accent-400"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8" />
                            </svg>
                        </a>
                    </div>
                </div>
            </div>
        )
    })
    return (
        <>
            <div className="bg-black">
                <section className="">
                    <div className="gap-16 items-center py-8 px-4 mx-auto max-w-screen-xl lg:grid lg:grid-cols-2 lg:py-16 lg:px-6">
                        <div className="font-light text-white sm:text-lg dark:text-gray-400">
                            <p className="mb-4 text-4xl tracking-tight font-normal text-white">Where Art and Technology Converge</p>
                            <p className="mb-4">This project is about rediscovering the inherent beauty of infinity, its deep connection to our past, present and future. It's a celebration of artificial intelligence's ability to transform the ordinary into something extraordinary, finding infinite inspiration in the things that surround us.</p>
                            <p>Here you will discover a world of hidden wonders, a symphony of textures, colors and shapes that dance and intertwine. Each pixel, each brushstroke, reveals a story waiting to be told, a testament to the boundless creativity to be found in the simplest of forms.</p>
                        </div>
                        <div className="grid grid-cols-2 gap-4 mt-8">
                            <img className="w-full rounded-lg " src="https://images.unsplash.com/photo-1541448232224-93f4a582b89d?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="office content 1" />
                            <img className="mt-4 h-full object-cover lg:mt-10 rounded-lg" src="https://images.unsplash.com/photo-1534723328310-e82dad3ee43f?q=80&w=1936&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="office content 2" />
                        </div>
                    </div>
                </section>
                
                <div className="px-4 py-16 mx-auto sm:max-w-xl md:max-w-full lg:max-w-screen-xl md:px-20     lg:px-8 lg:py-20">
                    <div className="mx-auto mb-10 lg:max-w-xl sm:text-center">
                        <p className="mb-4 text-4xl tracking-tight font-bold text-white">
                            Know Our Team
                        </p>
                    </div>
                    <hr class="w-48 h-1 mx-auto my-4 bg-gray-100 border-0 rounded md:my-10"></hr>

                    <div className="grid gap-10 w-max mx-auto lg:grid-cols-3 lg:max-w-screen-lg">
                        {autorsList}
                    </div>
                </div>
            </div>
        </>
    )
}
export default About;