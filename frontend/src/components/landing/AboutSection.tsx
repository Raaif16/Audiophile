import { Users, Headphones, RefreshCw, Truck } from 'lucide-react'
import './AboutSection.css'

const stats = [
  { icon: Users, value: '10,000+', label: 'Happy Customers' },
  { icon: Headphones, value: '50+', label: 'Premium Brands' },
  { icon: RefreshCw, value: '14-Day', label: 'Easy Returns' },
  { icon: Truck, value: 'Free', label: 'Shipping $50+' }
]

export default function AboutSection() {
  return (
    <section className="about-section">
      <div className="about-container">
        <div className="about-image">
          <img 
            src="https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80" 
            alt="Premium headphones on wooden surface"
          />
        </div>
        
        <div className="about-content">
          <span className="about-label">About Us</span>
          <h2 className="about-title">Crafting Perfect Sound Since 2010</h2>
          
          <div className="about-text">
            <p>
              At Audiophile, we believe that great sound should be accessible to everyone. 
              Founded by audio enthusiasts who were tired of compromising on quality, we've 
              spent over a decade curating the finest headphones from around the world.
            </p>
            <p>
              Every product in our collection is hand-selected and tested by our team of 
              audio engineers. We don't just sell headphones - we help you discover your 
              perfect sound.
            </p>
          </div>
          
          <div className="about-stats">
            {stats.map((stat, index) => (
              <div key={index} className="stat-item">
                <stat.icon className="stat-icon" size={32} />
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
