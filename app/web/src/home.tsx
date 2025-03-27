
import "./home.css";


function Home() {
  return (
    <div className="home">
        <h1 className="m-0 font-bold drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
          Wild West Dent Repair
        </h1>
        <h2 className="lg:text-2xl drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)] text-white grow p-5">Delivering precision, quality, and the best in customer care. <b>One dent at a time.</b></h2>
        
        {/* <div className="image-gallery-container">
          <ImageGallery slideDuration={3000} showNav={false} showThumbnails={false} items={images} autoPlay={true} showPlayButton={false} showFullscreenButton={false}></ImageGallery>
        </div> */}

        {/* <p className="welcome rounded overflow-hidden shadow-lg bg-white">
          Welcome to Wild West Dent Repair, your trusted vehicle restoration partner. 
          Locally owned and opperated in Golden, CO we specialize in expert dent repair. 
          Our mission is to provide the best dent repair services that not only bring your vehicle 
          back to pristine condition, but also to ensure a seamless and hassle-free experience for 
          our cutomers. 
        </p> */}
    </div>
  )
}

export default Home