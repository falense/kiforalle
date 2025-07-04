# Kiforalle.no

En nettside som oppsummerer utvalgt AI-forskning på tre nivåer: for barn, for videregåendeelever og for universitets-/høyskolenivå.

## Slik legger du til en ny artikkel

1. Legg til en PDF-fil av forskningsartikkelen i `_papers`-mappen.
2. En GitHub Action vil automatisk opprette et utkast til de tre oppsummeringene og en pull request.
3. Gjennomgå og rediger de tre oppsummeringene i den nye filen i pull requesten.
4. Når du er fornøyd, godkjenner du pull requesten for å publisere oppsummeringene.

## TODO

- [x] Sett opp Jekyll-tema og grunnleggende sidestruktur.
- [x] Lag en innholdsstruktur for de tre nivåene av oppsummeringer.
- [x] Implementer et skjelett for `summarize.py`-scriptet.
- [ ] Skriv den første oppsummeringen på tre nivåer.
- [ ] Oversett siden til norsk.
- [ ] Sett opp tilpasset domene `kiforalle.no`.

## Forslag til forbedringer

*   **Implementer faktisk oppsummering i `summarize.py`:** Utvid skriptet til å bruke en språkmodell for å generere faktiske oppsummeringer av PDF-filene.
*   **Forbedre `tabbed_post.html`-layouten:** Gjør layouten mer mobilvennlig og visuelt tiltalende.
*   **Legg til en "Om oss"-side:** Introduser prosjektet og forfatterne.
*   **Sett opp et system for å håndtere bilder:** Legg til funksjonalitet for å inkludere bilder i oppsummeringene.
*   **Skriv enhetstester for `summarize.py`:** Sikre at skriptet fungerer som forventet.
*   **Legg til en søkefunksjon:** Gjør det enklere for brukere å finne spesifikke artikler.
