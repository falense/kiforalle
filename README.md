# Kiforalle.no

En nettside som oppsummerer utvalgt AI-forskning på tre nivåer: for barn, for videregåendeelever og for universitets-/høyskolenivå.

## Funksjoner

- **Automatisk oppsummering**: Bruker Google Gemini API for å generere oppsummeringer av forskningsartikler på tre nivåer
- **Fane-basert visning**: Interaktiv fane-layout som lar brukere bytte mellom de tre nivåene
- **Automatisk publisering**: GitHub Actions automatiserer både oppsummering og publisering
- **Responsivt design**: Basert på Jekyll og Minima-tema for mobilvennlig visning

## Slik legger du til en ny artikkel

1. Legg til en PDF-fil av forskningsartikkelen i `_papers`-mappen.
2. En GitHub Action vil automatisk:
   - Lese PDF-filen med Google Gemini API
   - Generere oppsummeringer på tre nivåer
   - Opprette en pull request med den nye artikkelen
3. Gjennomgå og rediger de tre oppsummeringene i pull requesten.
4. Når du er fornøyd, godkjenner du pull requesten for å publisere oppsummeringene.

## Teknisk arkitektur

### Komponenter
- **Jekyll**: Statisk nettside generator
- **Minima**: Jekyll-tema for grunnleggende styling
- **Google Gemini API**: AI-modell for oppsummering av PDF-er
- **GitHub Actions**: CI/CD for automatisk oppsummering og publisering

### Filstruktur
```
├── _layouts/
│   └── tabbed_post.html     # Layout for fane-baserte artikler
├── _papers/                 # PDF-filer av forskningsartikler
├── _posts/                  # Genererte oppsummeringer
├── .github/
│   ├── scripts/
│   │   └── summarize.py     # Python-script for oppsummering
│   └── workflows/
│       ├── summarize.yml    # Workflow for oppsummering
│       └── jekyll.yml       # Workflow for publisering
└── _config.yml              # Jekyll-konfigurasjon
```

## Utvikling

### Lokalt miljø
```bash
# Installer avhengigheter
bundle install

# Kjør Jekyll lokalt
bundle exec jekyll serve

# Nettstedet er tilgjengelig på http://localhost:4000
```

### Miljøvariabler
- `GEMINI_API_KEY`: Google Gemini API-nøkkel for oppsummering

## Status

- [x] Sett opp Jekyll-tema og grunnleggende sidestruktur
- [x] Lag en innholdsstruktur for de tre nivåene av oppsummeringer
- [x] Implementer komplett `summarize.py`-script med Google Gemini API
- [x] Komplett `tabbed_post.html`-layout med JavaScript-funksjonalitet
- [x] GitHub Actions for automatisk oppsummering og publisering
- [x] Første oppsummering publisert (2505.22954v1.pdf)
- [ ] Oversett siden til norsk (delvis gjort)
- [ ] Sett opp tilpasset domene `kiforalle.no`

## Fremtidige forbedringer

### Høy prioritet
- **Forbedre mobilresponsivt design**: Optimalisere fane-layouten for mobile enheter
- **Legg til feilhåndtering**: Bedre håndtering av API-feil og ugyldig PDF-innhold
- **Implementer caching**: Redusere API-kall ved å cache oppsummeringer
- **Legg til metadata**: Automatisk ekstrahere forfatter, publiseringsdato og journal fra PDF-er

### Mellom prioritet
- **Søkefunksjon**: Implementer søk i titler og innhold
- **Kategorisering**: Legg til emnetagging (maskinlæring, computer vision, NLP, etc.)
- **RSS-feed**: Automatisk RSS-feed for nye oppsummeringer
- **Kommentarfunksjon**: Legg til kommentarfelt for diskusjon

### Lav prioritet
- **Flerspråklig støtte**: Engelsk og norsk versjon av samme artikkel
- **Bildehandtering**: Ekstrahere og vise figurer fra PDF-er
- **Statistikk**: Analysere lesemønstre og populære artikler
- **API-endepunkter**: REST API for ekstern tilgang til oppsummeringer
- **Favorittsystem**: La brukere markere og lagre favorittartikler
- **Sosial deling**: Integrere delingsknapper for sosiale medier

## Bidrag

Bidrag er velkomne! Vennligst opprett en issue eller pull request for forbedringer eller feilrettinger.

## Lisens

Dette prosjektet er lisensiert under MIT-lisensen.
