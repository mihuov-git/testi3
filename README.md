# Turun lounaat

Tama repo kokoaa yhteen kolmen ravintolan lounaat:
- Aitiopaikka
- Viides Nayttamo
- Grill it! Marina

## Tiedostot
- `index.html` nayttaa sivun
- `scripts/fetch_lunches.py` hakee lounaat
- `data/lunches.json` sisaltaa viimeisimman datan
- `.github/workflows/pages.yml` paivittaa datan ja julkaisee GitHub Pagesiin

## Kayttoonotto GitHubin webissa
1. Luo uusi public-repo.
2. Uploadaa kaikki muut tiedostot paitsi `.github`.
3. Luo tiedosto `.github/workflows/pages.yml` GitHubissa kasin ja liita workflow.
4. Aseta `Settings -> Pages -> Source` arvoon `GitHub Actions`.
5. Kaynnista workflow Actions-valilehdelta.
