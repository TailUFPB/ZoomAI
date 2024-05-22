// import dependencies
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/free-mode';

import { FreeMode, Pagination } from 'swiper/modules';

import { RxArrowTopRight } from "react-icons/rx";

import { ServiceData } from "../Constants/index.js";
import { Link } from 'react-router-dom';


const MyProjects = () => {
  return (
    <div className='flex flex-col h-screen bg-black m:pb-16 lg:pb-20 xl:pb-24'>
      <div className='flex items-center justify-center flex-col gap-6 m-5 mt-10 p-12'>
        <h1 className='text-4xl text-white font-bold'>See your ZoomAI projects</h1>
        <p className='tmt-4 text-lg font-normal text-gray-400 sm:mt-8'>Clarity gives you the blocks & components you need to create a truly professional website, landing page or admin panel for your SaaS.</p>
      </div>

      <div className='flex items-center justify-center gap-6 flex-grow'>
        <Swiper
          breakpoints={{
            340: {
              slidesPerView: 2,
              spaceBetween: 15
            },
            700: {
              slidesPerView: 3,
              spaceBetween: 15
            }
          }}

          freeMode={false}
          pagination={{
            clickable: true
          }}

          modules={[FreeMode, Pagination]}
          className='max-w-[90%] lg:max-w-[80%]'
        >
          {ServiceData.map((item) => (
          <SwiperSlide key={item.title}>
            <div className="flex flex-col gap-6 mb-20 group relative shadow-lg text-white rounded-xl overflow-hidden cursor-pointer">
              <div className="relative h-[250px] lg:h-[350px]">
                <img
                  src={item.backgroundImage}
                  alt={item.title}
                  className="absolute inset-0 w-full h-full max-h-64 lg:max-h-96 object-cover"
                  style={{ maxHeight: '400px' }} 
                />
                <div className="absolute inset-0 bg-black opacity-10 group-hover:opacity-50" />
                <div className="relative flex flex-col gap-3 p-6 lg:p-8">
                </div>
                <div className="absolute bottom-5 w-full flex justify-between px-5">
                  <h1 className="text-xl lg:text-2xl ">{item.title}</h1>
                  <RxArrowTopRight className="w-[35px] h-[35px] text-white group-hover:rotate-45 duration-100" />
                </div>
              </div>
            </div>
          </SwiperSlide>
          ))}
        </Swiper>
      </div>
      <div className="flex justify-center mt-8">
        <div className="relative inline-flex items-center justify-center group">
          <div className="absolute transition-all duration-200 rounded-full -inset-px bg-gradient-to-r from-cyan-500 to-purple-500 group-hover:shadow-lg group-hover:shadow-cyan-500/50"></div>
          <Link to="/" className="relative inline-flex items-center justify-center px-6 py-2 text-base font-normal text-white bg-black border border-transparent rounded-full" role="button"> New Project
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MyProjects;
