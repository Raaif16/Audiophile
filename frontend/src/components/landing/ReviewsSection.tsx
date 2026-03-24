import { Star, Quote } from 'lucide-react'
import './ReviewsSection.css'

interface Review {
  id: number
  name: string
  initials: string
  rating: number
  date: string
  review: string
}

const reviews: Review[] = [
  {
    id: 1,
    name: 'Sarah M.',
    initials: 'SM',
    rating: 5,
    date: '2 weeks ago',
    review: 'The Sony XM5s exceeded all my expectations. The noise cancellation is incredible for my daily commute. Audiophile\'s customer service was also fantastic - helped me choose the right model!'
  },
  {
    id: 2,
    name: 'James K.',
    initials: 'JK',
    rating: 5,
    date: '1 month ago',
    review: 'Finally found headphones that match my HiFi setup. The Sennheiser HD 660S2 delivers pure audio bliss. Fast shipping and well-packaged. Will definitely be a returning customer.'
  },
  {
    id: 3,
    name: 'Emily R.',
    initials: 'ER',
    rating: 5,
    date: '3 weeks ago',
    review: 'Bought the ATH-M50x for my home studio. The sound quality is pristine and the build quality is solid. Great value for money. Love the warm aesthetic of this website too!'
  }
]

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="review-stars">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          size={18}
          className={`review-star ${star <= rating ? 'filled' : ''}`}
          fill={star <= rating ? '#b8860b' : 'none'}
        />
      ))}
    </div>
  )
}

export default function ReviewsSection() {
  return (
    <section className="reviews-section">
      <div className="reviews-container">
        <div className="section-header">
          <span className="section-label">Testimonials</span>
          <h2 className="section-title">What Our Customers Say</h2>
          <p className="section-description">
            Real feedback from our community of audio enthusiasts
          </p>
        </div>
        
        <div className="reviews-grid">
          {reviews.map((review) => (
            <div key={review.id} className="review-card">
              <div className="review-quote-icon">
                <Quote size={40} />
              </div>
              
              <StarRating rating={review.rating} />
              
              <p className="review-text">{review.review}</p>
              
              <div className="reviewer-info">
                <div className="reviewer-avatar">
                  {review.initials}
                </div>
                <div className="reviewer-details">
                  <div className="reviewer-name">{review.name}</div>
                  <div className="review-date">{review.date}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
