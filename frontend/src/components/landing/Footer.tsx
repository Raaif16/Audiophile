import { Headphones, Mail, Phone, MapPin, Facebook, Twitter, Instagram, Youtube, Send } from 'lucide-react'
import './Footer.css'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-main">
          <div className="footer-brand">
            <div className="footer-logo">
              <Headphones size={32} />
              <span>Audiophile</span>
            </div>
            <p className="footer-tagline">
              Your destination for premium audio excellence. Discover your perfect sound with us.
            </p>
            <div className="footer-social">
              <a href="#" aria-label="Facebook"><Facebook size={20} /></a>
              <a href="#" aria-label="Twitter"><Twitter size={20} /></a>
              <a href="#" aria-label="Instagram"><Instagram size={20} /></a>
              <a href="#" aria-label="YouTube"><Youtube size={20} /></a>
            </div>
          </div>
          
          <div className="footer-links">
            <div className="footer-column">
              <h4>Shop</h4>
              <ul>
                <li><a href="#">All Headphones</a></li>
                <li><a href="#">Over-Ear</a></li>
                <li><a href="#">On-Ear</a></li>
                <li><a href="#">In-Ear</a></li>
                <li><a href="#">Wireless</a></li>
                <li><a href="#">Gaming</a></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h4>Support</h4>
              <ul>
                <li><a href="#">Contact Us</a></li>
                <li><a href="#">FAQs</a></li>
                <li><a href="#">Shipping Info</a></li>
                <li><a href="#">Returns</a></li>
                <li><a href="#">Warranty</a></li>
                <li><a href="#">Size Guide</a></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h4>Company</h4>
              <ul>
                <li><a href="#">About Us</a></li>
                <li><a href="#">Careers</a></li>
                <li><a href="#">Press</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Affiliates</a></li>
                <li><a href="#">Sustainability</a></li>
              </ul>
            </div>
          </div>
          
          <div className="footer-contact">
            <h4>Newsletter</h4>
            <p>Subscribe for exclusive offers and audio tips</p>
            <form className="newsletter-form">
              <input 
                type="email" 
                placeholder="Enter your email"
                aria-label="Email address"
              />
              <button type="submit" aria-label="Subscribe">
                <Send size={18} />
              </button>
            </form>
            
            <div className="contact-info">
              <div className="contact-item">
                <Mail size={18} />
                <span>support@audiophile.com</span>
              </div>
              <div className="contact-item">
                <Phone size={18} />
                <span>1-800-AUDIO-PRO</span>
              </div>
              <div className="contact-item">
                <MapPin size={18} />
                <span>123 Sound Street, NY 10001</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>© 2024 Audiophile. All rights reserved.</p>
          <div className="footer-legal">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Cookie Settings</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
