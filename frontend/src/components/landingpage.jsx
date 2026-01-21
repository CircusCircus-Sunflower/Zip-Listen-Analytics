import { useNavigate } from 'react-router-dom';
import './landingpage.css';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <nav className="landing-nav">
        <div className="nav-logo">🌻</div>
        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#pricing">Pricing</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </div>
        <button className="sign-in-btn">Sign In</button>
      </nav>

      <div className="hero-section">
        <h1 className="hero-title">Sunflower Analytics</h1>
        <p className="hero-subtitle">
          Meet Sol.. Your friendly AI assistant for smarter analytics 🌻
        </p>

        <div className="sol-logo-container">
          <img src="/sol-logo.png" alt="Sol - Sunflower Analytics Mascot" className="sol-logo" />
        </div>

        <div className="chat-input-container">
          <input 
            type="text" 
            placeholder="Hi there! I'm Sol... how can I assist you today?"
            className="landing-chat-input"
            onFocus={() => navigate('/chat')}
          />
          <button className="send-btn-landing" onClick={() => navigate('/chat')}>
            Send
          </button>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3>Instant Insights</h3>
            <p>Ask questions in plain English and get fast answers.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Powerful Analytics</h3>
            <p>Built for streaming metrics: artists, genres, growth, retention.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Keep data protected with simple, safe backend patterns.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;