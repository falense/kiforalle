---
layout: home
---

<div class="hero">
  <div class="hero-content">
    <h1>🧠 KI-forskning for alle</h1>
    <p class="lead">Komplekse teknologier forklart på ditt nivå så alle kan forstå</p>
    <div class="hero-badges">
      <span class="badge">{{ site.posts.size }} artikler</span>
      <span class="badge">3 vanskelighetsgrader</span>
      <span class="badge">100% norsk</span>
    </div>
    <div class="hero-description">
      <p>Vi oversetter spennende KI-forskning til norsk og forklarer det på tre forskjellige nivåer – fra 8-åringer til universitetsunderviser. Vi ønsker å gjøre KI forståelig for alle.</p>
      <p style="margin-top: 2rem;"><a href="/om-oss/">Les mer om prosjektet</a></p>
    </div>
  </div>
</div>

<section class="levels">
  <h2>Tre nivåer av forklaring</h2>
  <div class="level-grid">
    <div class="level-item">
      <div class="level-emoji">🧒</div>
      <h3>For barn</h3>
      <p class="level-age">8-12 år</p>
      <p>Enkle forklaringer med analogier fra hverdagen</p>
    </div>
    <div class="level-item">
      <div class="level-emoji">🎓</div>
      <h3>For ungdom</h3>
      <p class="level-age">16-18 år</p>
      <p>Dyptgående forklaringer med teknisk kontekst</p>
    </div>
    <div class="level-item">
      <div class="level-emoji">🏛️</div>
      <h3>For voksne</h3>
      <p class="level-age">Universitets-/høyskolenivå</p>
      <p>Fullstendige akademiske oppsummeringer</p>
    </div>
  </div>
</section>

<section class="how-it-works">
  <h2>Slik fungerer det</h2>
  <div class="steps">
    <div class="step">
      <span class="step-number">1</span>
      <div class="step-content">
        <h3>🔍 Utvelgelse</h3>
        <p>Spennende artikler velges ut av mennesker</p>
      </div>
    </div>
    <div class="step">
      <span class="step-number">2</span>
      <div class="step-content">
        <h3>🤖 KI-analyse</h3>
        <p>Gemini KI lager sammendrag og analyser</p>
      </div>
    </div>
    <div class="step">
      <span class="step-number">3</span>
      <div class="step-content">
        <h3>✅ Kontroll</h3>
        <p>Validering og menneskelig gjennomgang</p>
      </div>
    </div>
    <div class="step">
      <span class="step-number">4</span>
      <div class="step-content">
        <h3>🌐 Publisering</h3>
        <p>Publiseres på kiforalle.no</p>
      </div>
    </div>
  </div>
</section>

<section class="latest-posts">
  <h2>📚 Nyeste KI-forskning</h2>
  <div class="posts-grid">
    {% for post in site.posts limit: 6 %}
      <div class="post-card">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
        <p class="post-meta">{{ post.date | date: "%d. %B %Y" }}</p>
        <p class="post-authors">{{ post.authors }}</p>
      </div>
    {% endfor %}
  </div>
</section>


<style>
/* Reset and base styles */
* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  margin: 0;
  padding: 0;
}

/* Hero section */
.hero {
  padding: 3rem 2rem;
  text-align: center;
}

.hero h1 {
  font-size: 2.5rem;
  margin: 0 0 1rem 0;
  font-weight: 600;
  color: #2c3e50;
}

.hero .lead {
  font-size: 1.2rem;
  margin: 0 0 2rem 0;
  color: #666;
}

.hero-badges {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.hero-description {
  max-width: 800px;
  margin: 0 auto;
}

.hero-description p {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.6;
}

.badge {
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #555;
  border: 1px solid #dee2e6;
}

/* Sections */
section {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

section h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  color: #2c3e50;
}

.intro {
  text-align: center;
}

.intro p {
  font-size: 1.1rem;
  max-width: 800px;
  margin: 0 auto;
  color: #555;
}

/* Levels section */
.levels {
}

.level-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 2rem;
}

.level-item {
  text-align: center;
  padding: 2rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.level-item:hover {
  border-color: #007bff;
}

.level-emoji {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.level-item h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.level-age {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
  margin: 0 0 1rem 0;
}

.level-item p:last-child {
  margin: 0;
  color: #555;
}

/* How it works section */
.how-it-works {
}

.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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
  background: #007bff;
  color: white;
  border-radius: 50%;
  line-height: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.step-content h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.step-content p {
  margin: 0;
  color: #555;
  font-size: 0.9rem;
}

/* Latest posts section */
.latest-posts {
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.post-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  transition: box-shadow 0.3s ease;
}

.post-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.post-card h3 {
  margin: 0 0 0.5rem 0;
}

.post-card h3 a {
  color: #007bff;
  text-decoration: none;
}

.post-card h3 a:hover {
  text-decoration: underline;
}

.post-meta {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
}

.post-authors {
  color: #888;
  font-size: 0.85rem;
  margin: 0 0 1rem 0;
}

.post-levels {
  display: flex;
  gap: 0.5rem;
}

.level-tag {
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  border: 1px solid #dee2e6;
}


/* Responsive design */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .hero .lead {
    font-size: 1.1rem;
  }
  
  .hero-badges {
    flex-direction: column;
    align-items: center;
  }
  
  section {
    padding: 2rem 1rem;
  }
  
  section h2 {
    font-size: 1.5rem;
  }
  
  .level-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .steps {
    grid-template-columns: 1fr;
  }
  
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
}
</style>