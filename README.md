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
- [ ] Implementer summarization-scriptet i `.github/scripts/summarize.py`.
- [x] Skriv den første oppsummeringen på tre nivåer.
- [ ] Oversett siden til norsk.
- [ ] Sett opp tilpasset domene `kiforalle.no`.
