import {
  HeroCarousel,
  AboutSection,
  BestSellers,
  ReviewsSection,
  Footer
} from '../components/landing'

export default function Home() {
  return (
    <div className="home-page">
      <HeroCarousel />
      <AboutSection />
      <BestSellers />
      <ReviewsSection />
      <Footer />
    </div>
  )
}
