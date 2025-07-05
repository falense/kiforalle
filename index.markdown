---
layout: home
---

# Velkommen til Kiforalle.no! 🧠

**AI-forskning gjort forståelig for alle**

Her finner du oppsummeringer av banebrytende AI-forskning, tilpasset tre ulike nivåer – fra barn til universitetsunderviser. Vi gjør kompleks teknologi tilgjengelig for alle som er nysgjerrige på fremtiden.

## 🎯 Slik fungerer det

<div class="level-explanation">
  <div class="level-card">
    <h3>🧒 For barn (8-12 år)</h3>
    <p>Enkle forklaringer med analogier og eksempler fra hverdagen</p>
  </div>
  
  <div class="level-card">
    <h3>🎓 For videregåendeelever (16-18 år)</h3>
    <p>Mer dyptgående forklaringer med teknisk kontekst</p>
  </div>
  
  <div class="level-card">
    <h3>🏛️ For universitets-/høyskolenivå</h3>
    <p>Fullstendige akademiske oppsummeringer med detaljer</p>
  </div>
</div>

## 📚 Nyeste AI-forskning

<div class="posts-grid">
  {% for post in site.posts limit: 6 %}
    <div class="post-card">
      <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
      <p class="post-meta">{{ post.date | date: "%d. %B %Y" }}</p>
      <p class="post-authors">{{ post.authors }}</p>
    </div>
  {% endfor %}
</div>

<div class="cta-section">
  <a href="/om-oss/" class="cta-button">Les mer om prosjektet</a>
</div>

