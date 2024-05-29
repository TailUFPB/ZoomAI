import { Pagination, Navigation } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

import { RxArrowTopRight } from "react-icons/rx";
import { GiClick } from "react-icons/gi";

import { ServiceData } from "./Constants/constants";
import { Link, useNavigate } from 'react-router-dom';
import ReactLoading from 'react-loading';
import { useState } from 'react';

const AllProjects = () => {
  const navigate = useNavigate();

  const gotoZoom = (project) => {
    navigate(`/zoom`, {state: {project}});
  }

  return (
    <div className='flex flex-col h-screen bg-black m:pb-16 lg:pb-20 xl:pb-24' style={{minHeight: "700px"}}>

      <div className='flex items-center justify-center flex-col gap-6 m-5 p-12 ' style={{marginTop: "40px", marginBottom:"100px"}}>
        <h1 className='text-4xl text-white font-bold'>See your ZoomAI projects</h1>
        <p className='tmt-4 text-lg font-normal text-gray-400 sm:mt-8'>Clarity gives you the blocks & components you need to create a truly professional website, landing page or admin panel for your SaaS.</p>
      </div>

      <div className='flex items-center justify-center gap-6 flex-grow' style={{padding: "30px", paddingInlineEnd: "60px", paddingInlineStart: "60px",  position: "relative",bottom: "100px", userSelect: "none"}}>
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
          className="max-w-[90%] lg:max-w-[80%]"
        >
          {ServiceData.map((item) => (
          <SwiperSlide key={item.title}>
            
            <div className=" flex flex-col gap-6 mb-20 group relative shadow-lg text-white rounded-xl px-6 py-8 h-[250px] w-[215px] lg:h-[400px] lg:w-[350px] overflow-hidden cursor-pointer">
              
            <div className="absolute inset-0 bg-coevr bg-center"/>

            <div className="absolute inset-0 bg-black opacity-10 group-hover:opacity-50"/>
            <div className=" relative flex flex-col gap-3 p-10">
              <img src={item.backgroundImage} alt={item.title} className="object-cover project-image" onClick={()=>{gotoZoom(item.id)}}/>
              <div className="absolute left-0 p-4 z-20 flex items-start justify-between w-full h-full " style={{bottom: "0px", left: "0px", fontSize: "18px"}}>
                <h1 className="text-2xl font-bold">{item.title}</h1>
                {/* <GiClick  className="redirect-to-project" size={20} /> */}
                <ReactLoading type='spin' height={"30px"} width={"30px"}/>
              </div>
            </div>
            
          </div>
            
          </SwiperSlide>
          ))}
        </Swiper>
      </div>

      <div className="flex justify-center mt-6" style={{userSelect: 'none', position: 'fixed', bottom: 50, width: '100%'}}>
        <div className="relative inline-flex items-center justify-center group">
          <div className="absolute transition-all duration-200 rounded-full -inset-px bg-gradient-to-r from-cyan-500 to-purple-500 group-hover:shadow-lg group-hover:shadow-cyan-500/50"></div>
          <Link to="/" className="relative inline-flex items-center justify-center px-6 py-2 text-base font-normal text-white bg-black border border-transparent rounded-full" role="button"> New Project
          </Link>
        </div>
      </div>

    </div>
  );
};

export default AllProjects;
