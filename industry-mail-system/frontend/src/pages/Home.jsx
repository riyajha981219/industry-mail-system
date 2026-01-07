import { Link } from 'react-router-dom'
import './Home.css'

const Home = () => {
    return (
        <div className="container">
            <div className="hero">
                <h1>Welcome to Industry Mailer System</h1>
                <p className="hero-subtitle">
                    Stay updated with the latest news from your favorite industries
                </p>
                <p className="hero-description">
                    Subscribe to industry topics and receive curated newsletters with the top 10 news articles
                    delivered directly to your inbox. Choose your preferred frequency: daily, weekly, or monthly.
                </p>
                <div className="hero-actions">
                    <Link to="/subscribe" className="btn btn-primary btn-large">
                        Get Started →
                    </Link>
                    <Link to="/dashboard" className="btn btn-secondary btn-large">
                        View Dashboard
                    </Link>
                </div>
            </div>

            <div className="features">
                <h2>How It Works</h2>
                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon">🎯</div>
                        <h3>Select Topics</h3>
                        <p>Choose from various industry topics that interest you</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">📅</div>
                        <h3>Set Frequency</h3>
                        <p>Decide how often you want to receive updates: 1, 7, or 30 days</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">📰</div>
                        <h3>Get News</h3>
                        <p>Receive top 10 curated articles from trusted sources</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">📧</div>
                        <h3>Email Delivery</h3>
                        <p>Get beautifully formatted newsletters in your inbox</p>
                    </div>
                </div>
            </div>

            <div className="cta-section">
                <h2>Ready to stay informed?</h2>
                <p>Join thousands of professionals who trust Industry Mailer for their news</p>
                <Link to="/subscribe" className="btn btn-primary btn-large">
                    Subscribe Now
                </Link>
            </div>
        </div>
    )
}

export default Home
