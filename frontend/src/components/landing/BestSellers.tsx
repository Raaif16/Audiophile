import { Star, ShoppingCart, ArrowRight } from 'lucide-react'
import './BestSellers.css'

interface Product {
  id: number
  name: string
  price: number
  rating: number
  reviews: number
  image: string
}

const products: Product[] = [
  {
    id: 1,
    name: 'Sony WH-1000XM5',
    price: 398.00,
    rating: 5,
    reviews: 245,
    image: 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400&q=80'
  },
  {
    id: 2,
    name: 'Bose QuietComfort 45',
    price: 329.00,
    rating: 5,
    reviews: 189,
    image: 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&q=80'
  },
  {
    id: 3,
    name: 'Sennheiser HD 660S2',
    price: 499.00,
    rating: 5,
    reviews: 156,
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80'
  },
  {
    id: 4,
    name: 'Audio-Technica ATH-M50x',
    price: 149.00,
    rating: 5,
    reviews: 312,
    image: 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&q=80'
  },
  {
    id: 5,
    name: 'Apple AirPods Max',
    price: 549.00,
    rating: 4.5,
    reviews: 423,
    image: 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400&q=80'
  },
  {
    id: 6,
    name: 'Beyerdynamic DT 990 Pro',
    price: 169.00,
    rating: 5,
    reviews: 278,
    image: 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&q=80'
  }
]

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="star-rating">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          size={16}
          className={`star ${star <= rating ? 'filled' : star - 0.5 <= rating ? 'half' : ''}`}
          fill={star <= rating ? '#b8860b' : star - 0.5 <= rating ? 'url(#half)' : 'none'}
        />
      ))}
    </div>
  )
}

export default function BestSellers() {
  return (
    <section className="best-sellers-section">
      <div className="best-sellers-container">
        <div className="section-header">
          <span className="section-label">Our Collection</span>
          <h2 className="section-title">Customer Favorites</h2>
          <p className="section-description">
            Discover our most loved headphones, chosen by thousands of satisfied customers
          </p>
        </div>
        
        <div className="products-grid">
          {products.map((product) => (
            <div key={product.id} className="product-card">
              <div className="product-image-container">
                <img 
                  src={product.image} 
                  alt={product.name}
                  className="product-image"
                />
                <button className="add-to-cart-btn" aria-label="Add to cart">
                  <ShoppingCart size={20} />
                </button>
              </div>
              
              <div className="product-info">
                <h3 className="product-name">{product.name}</h3>
                
                <div className="product-rating">
                  <StarRating rating={product.rating} />
                  <span className="reviews-count">({product.reviews} reviews)</span>
                </div>
                
                <div className="product-price">${product.price.toFixed(2)}</div>
              </div>
            </div>
          ))}
        </div>
        
        <button className="view-all-btn">
          Explore All Products
          <ArrowRight size={20} />
        </button>
      </div>
    </section>
  )
}
