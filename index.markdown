---
layout: home
---

Velkommen til Kiforalle.no!

Her finner du oppsummeringer av AI-forskning, tilpasset tre ulike nivåer.

<ul>
  {% for post in site.posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

