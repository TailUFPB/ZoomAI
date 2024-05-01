//import dependencies
import { Swiper, SwiperSlide} from 'swiper/react';

import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/free-mode';

import {FreeMode, Pagination} from 'swiper/modules';


//See your ZoomAI Projects // Clarity gives you the blocks & components you need to creat a truly professional website, landing page or admin panel for you SaaS. //                     New Project

const MyProjects = () => {
    return (
      <div className='flex items-center justify-center flex-col h-screen bg-black'>
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

          freeMode={true}
          pagination= {{
            clickable: true
          }}
          
          modules={[FreeMode, Pagination]}
          className='max-w-[90%] lg:max-w-[80%]'
        >
          {/* ServiceData será a pagina com os projetos feito
                    {ServiceData.map((item) => (
            <SwiperSlide key={item.title}>
              <div className='flex flex-col gap-6 group relative shadow-lg text-white rounded-x1 px-6 py-8 h-[250px] w-[215px] lg:h-[400px] lg:w-[350px]'>
                
              </div>
            </SwiperSlide>
          ))
          }*/}

        </Swiper>

      </div>
    );
  };
  
  export default MyProjects;
  