---
layout: home
---

<div class="hero-section">
  <div class="hero-content">
    <h1 class="hero-title">🔬 AI-forskning for alle</h1>
    <p class="hero-subtitle">Kompleks teknologi, enkelt forklart</p>
    <div class="hero-stats">
      <div class="stat-item">
        <span class="stat-number">{{ site.posts.size }}</span>
        <span class="stat-label">forskningsartikler</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">3</span>
        <span class="stat-label">nivåer</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">100%</span>
        <span class="stat-label">norsk</span>
      </div>
    </div>
  </div>
</div>

<section class="mission-section">
  <div class="container">
    <h2>🎯 Vår misjon</h2>
    <p class="mission-text">
      Vi oversetter banebrytende AI-forskning til forståelig norsk for alle aldersgrupper. 
      Fra 8-åringer til universitetsunderviser – alle fortjener å forstå teknologien som former fremtiden.
    </p>
  </div>
</section>

<section class="levels-section">
  <div class="container">
    <h2>📚 Tre nivåer av forståelse</h2>
    <div class="levels-grid">
      <div class="level-card level-child">
        <div class="level-icon">🧒</div>
        <h3>For barn</h3>
        <p class="level-age">8-12 år</p>
        <p>Enkle forklaringer med hverdagslige analogier som gjør kompleks teknologi lett å forstå.</p>
      </div>
      <div class="level-card level-teen">
        <div class="level-icon">🎓</div>
        <h3>For ungdom</h3>
        <p class="level-age">16-18 år</p>
        <p>Dyptgående forklaringer med teknisk kontekst som bygger på kunnskap fra videregående skole.</p>
      </div>
      <div class="level-card level-adult">
        <div class="level-icon">🏛️</div>
        <h3>For voksne</h3>
        <p class="level-age">Universitets-/høyskolenivå</p>
        <p>Fullstendige akademiske oppsummeringer med tekniske detaljer og forskningskontext.</p>
      </div>
    </div>
  </div>
</section>

<section class="process-section">
  <div class="container">
    <h2>⚙️ Slik fungerer det</h2>
    <div class="process-steps">
      <div class="step">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>📄 PDF-opplasting</h3>
          <p>Forskningsartikler lastes opp til GitHub</p>
        </div>
      </div>
      <div class="step">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>🤖 AI-analyse</h3>
          <p>Google Gemini API ekstraherer og analyserer innhold</p>
        </div>
      </div>
      <div class="step">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>🇳🇴 Oversettelse</h3>
          <p>Automatisk oversettelse til norsk på tre nivåer</p>
        </div>
      </div>
      <div class="step">
        <div class="step-number">4</div>
        <div class="step-content">
          <h3>✅ Kvalitetskontroll</h3>
          <p>Automatisk validering og menneskelig gjennomgang</p>
        </div>
      </div>
      <div class="step">
        <div class="step-number">5</div>
        <div class="step-content">
          <h3>📱 Publisering</h3>
          <p>Responsiv Jekyll-publisering med interaktiv design</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="latest-section">
  <div class="container">
    <h2>📖 Nyeste forskningsartikler</h2>
    <div class="articles-grid">
      {% for post in site.posts limit: 3 %}
        <article class="article-card">
          <div class="article-content">
            <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
            <p class="article-authors">{{ post.authors }}</p>
            <p class="article-date">{{ post.date | date: "%d. %B %Y" }}</p>
            <div class="article-levels">
              <span class="level-badge">🧒 Barn</span>
              <span class="level-badge">🎓 Ungdom</span>
              <span class="level-badge">🏛️ Voksne</span>
            </div>
          </div>
        </article>
      {% endfor %}
    </div>
    
    {% if site.posts.size > 3 %}
      <div class="view-all">
        <a href="/arkiv/" class="view-all-btn">Se alle artikler →</a>
      </div>
    {% endif %}
  </div>
</section>

<section class="cta-section">
  <div class="container">
    <div class="cta-content">
      <h2>Bli med på reisen!</h2>
      <p>Utforsk fremtidens teknologi sammen med oss</p>
      <div class="cta-buttons">
        <a href="/om-oss/" class="cta-btn primary">Les mer om prosjektet</a>
        <a href="https://github.com/falense/kiforalle" class="cta-btn secondary">Se på GitHub</a>
      </div>
    </div>
  </div>
</section>

<style>
/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #ffd700;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Mission Section */
.mission-section {
  padding: 4rem 0;
  background: #f8f9fa;
}

.mission-text {
  font-size: 1.2rem;
  line-height: 1.6;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

/* Levels Section */
.levels-section {
  padding: 4rem 0;
}

.levels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.level-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.level-card:hover {
  transform: translateY(-5px);
}

.level-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.level-age {
  color: #666;
  font-style: italic;
  margin-bottom: 1rem;
}

.level-child { border-top: 4px solid #4CAF50; }
.level-teen { border-top: 4px solid #2196F3; }
.level-adult { border-top: 4px solid #FF9800; }

/* Process Section */
.process-section {
  padding: 4rem 0;
  background: #f8f9fa;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.step {
  text-align: center;
}

.step-number {
  display: inline-block;
  width: 3rem;
  height: 3rem;
  background: #667eea;
  color: white;
  border-radius: 50%;
  line-height: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* Latest Section */
.latest-section {
  padding: 4rem 0;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.article-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.article-card:hover {
  transform: translateY(-3px);
}

.article-card h3 a {
  color: #333;
  text-decoration: none;
  font-size: 1.3rem;
}

.article-card h3 a:hover {
  color: #667eea;
}

.article-authors {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.article-date {
  color: #999;
  font-size: 0.8rem;
  margin-bottom: 1rem;
}

.article-levels {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.level-badge {
  background: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

.view-all {
  text-align: center;
  margin-top: 2rem;
}

.view-all-btn {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

/* CTA Section */
.cta-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 2rem;
}

.cta-btn {
  padding: 1rem 2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cta-btn.primary {
  background: white;
  color: #667eea;
}

.cta-btn.primary:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.cta-btn.secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.cta-btn.secondary:hover {
  background: white;
  color: #667eea;
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .hero-stats {
    gap: 1rem;
  }
  
  .levels-grid {
    grid-template-columns: 1fr;
  }
  
  .process-steps {
    grid-template-columns: 1fr;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>