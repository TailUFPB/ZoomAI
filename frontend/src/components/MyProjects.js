import { Pagination, Navigation } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

import CoverDefault from '../public/assets/cover_default.jpg';

import { IoPlay } from "react-icons/io5";


import { Link, useNavigate } from 'react-router-dom';
import ReactLoading from 'react-loading';
import React, { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';

import axios from 'axios';

import { enviroment } from '../common/enviroment';

const getProjects = async () => {
  try {
    const response = await axios.get(`${enviroment}/get_projects`);
    const projectsData = Object.values(response.data)
    return projectsData.map(project => ({
      ...project,
      cover: project.cover ? `data:image/png;base64,${project.cover}` : null,
    }));
  } catch (error) {
    console.error(error);
    return [];
  }
}

const AllProjects = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProjects = async () => {
      const projects = await getProjects();
      setProjects(projects);
      setLoading(false);
    };

    fetchProjects();
  }, []);
  
  const gotoZoom = (project) => {
    if(project.ready){
      sessionStorage.setItem('projectId', project.id);
      navigate('/zoom', { state: { projectId: project.id } });
    }
    else {
      toast.info("This project is not ready yet");
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
    <div className='flex flex-col h-screen bg-black m:pb-16 lg:pb-20 xl:pb-24' style={{minHeight: "700px"}}>

      <div className='flex items-center justify-center flex-col' style={{marginTop: "40px", marginBottom:"100px"}}>
        <h1 className='text-4xl text-white font-bold'>See your ZoomAI projects</h1>
        <p className='tmt-4 text-lg font-normal text-gray-400 sm:mt-8'>Clarity gives you the blocks & components you need to create a truly professional website, landing page or admin panel for your SaaS.</p>
      </div>

      <div className='flex items-center justify-center' style={{ position: "relative",bottom: "50px", userSelect: "none"}}>
      {loading ? (
        <ReactLoading type='spin' color='#fff' height={50} width={50} />
      ) : (
        <Swiper
          style={{
            '--swiper-navigation-color': '#fff',
            '--swiper-pagination-color': '#fff',
            padding: "30px",
          }}
          breakpoints={
            {
              340: {
                slidesPerView: 2,
                spaceBetween: 20,
              },
              700: {
                slidesPerView: 3,
                spaceBetween: 50,
              },
            }
          }          
          freeMode={true}
          pagination={{
            clickable: true,

          }}
          modules={[Pagination, Navigation]}
          navigation={true}
          className=""
        >
          {projects.map((project) => (
          <SwiperSlide key={project.id}>
            
            <div className=" flex flex-col mb-20 group relative text-white px-6 py-8 h-[250px] w-[215px] lg:h-[400px] lg:w-[350px] overflow-hidden cursor-pointer"> 
            <div className="absolute bg-cover bg-center"  
              style={{ 
                backgroundImage: project.cover && project.cover !== '0' ? `url(${project.cover})` : `url(${CoverDefault})`, 
                filter: project.cover === '0' ? 'blur(5px)' : 'none' 
              }}/>
            <div className="absolute bg-black opacity-10 group-hover:opacity-50"/>
            <div className="relative flex flex-col p-10">
            <img src={project.cover && project.cover !== '0' ? project.cover : CoverDefault} 
                alt={project.name} 
                className="project-image" 
                onClick={() => { gotoZoom(project) }} 
                style={{ filter: project.cover === '0' ? 'blur(5px)' : 'none' }}/>
              <div className="absolute left-0 p-4 flex justify-between w-full" style={{bottom: "0px", left: "0px", fontSize: "18px"}}>
                <h1 className="font-bold">{project.name}</h1>
                {/* <GiClick  className="redirect-to-project" size={20} /> */}
                {project.ready === 1 ?  <IoPlay size={35}  /> : <ReactLoading type='spin' height={"30px"} width={"30px"} />}
              </div>
            </div>
          </div>
            
          </SwiperSlide>
          )).reverse()}
        </Swiper>
        )}
      </div>

      <div className="flex justify-center" style={{userSelect: 'none', position: 'fixed', bottom: 50, width: '100%'}}>
        <div className="relative inline-flex items-center justify-center group">
          <div className="absolute transition-all duration-200 rounded-full -inset-px bg-gradient-to-r from-cyan-500 to-purple-500 group-hover:shadow-cyan-500/50"></div>
          <Link to="/" className="relative inline-flex items-center justify-center px-6 py-2 text-base font-normal text-white bg-black border border-transparent rounded-full" role="button"> New Project
          </Link>
        </div>
      </div>

    </div>
    </>
  );
};

export default AllProjects;
