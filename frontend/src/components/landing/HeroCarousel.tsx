import { useState, useEffect, useCallback } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import './HeroCarousel.css'

interface CarouselItem {
  id: number
  name: string
  description: string
  price: string
  image: string
}

const carouselItems: CarouselItem[] = [
  {
    id: 1,
    name: 'Sony WH-1000XM5',
    description: 'Premium Sound, Ultimate Comfort. Industry-leading noise cancellation meets exceptional audio quality.',
    price: '$398.00',
    image: 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=800&q=80'
  },
  {
    id: 2,
    name: 'Sennheiser HD 660S2',
    description: 'Pure Audiophile Experience. Open-back design delivers natural, balanced sound for critical listening.',
    price: '$499.00',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'
  },
  {
    id: 3,
    name: 'Audio-Technica ATH-M50x',
    description: 'Studio Quality Everywhere. Professional-grade monitoring headphones trusted by audio engineers worldwide.',
    price: '$149.00',
    image: 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&q=80'
  }
]

export default function HeroCarousel() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [isPaused, setIsPaused] = useState(false)

  const nextSlide = useCallback(() => {
    setCurrentSlide((prev) => (prev + 1) % carouselItems.length)
  }, [])

  const prevSlide = useCallback(() => {
    setCurrentSlide((prev) => (prev - 1 + carouselItems.length) % carouselItems.length)
  }, [])

  const goToSlide = (index: number) => {
    setCurrentSlide(index)
  }

  useEffect(() => {
    if (isPaused) return
    
    const interval = setInterval(() => {
      nextSlide()
    }, 5000)

    return () => clearInterval(interval)
  }, [isPaused, nextSlide])

  return (
    <section 
      className="hero-carousel"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      <div className="carousel-container">
        {carouselItems.map((item, index) => (
          <div
            key={item.id}
            className={`carousel-slide ${index === currentSlide ? 'active' : ''}`}
          >
            <div className="carousel-content">
              <div className="carousel-text">
                <span className="carousel-badge">Featured</span>
                <h2 className="carousel-title">{item.name}</h2>
                <p className="carousel-description">{item.description}</p>
                <div className="carousel-price">{item.price}</div>
                <button className="carousel-cta">Shop Now</button>
              </div>
              <div className="carousel-image-container">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="carousel-image"
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <button 
        className="carousel-nav carousel-nav-prev"
        onClick={prevSlide}
        aria-label="Previous slide"
      >
        <ChevronLeft size={24} />
      </button>

      <button 
        className="carousel-nav carousel-nav-next"
        onClick={nextSlide}
        aria-label="Next slide"
      >
        <ChevronRight size={24} />
      </button>

      <div className="carousel-dots">
        {carouselItems.map((_, index) => (
          <button
            key={index}
            className={`carousel-dot ${index === currentSlide ? 'active' : ''}`}
            onClick={() => goToSlide(index)}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </section>
  )
}
