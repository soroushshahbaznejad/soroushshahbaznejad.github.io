# Soroush Shahbaznejad — Academic website

A lightweight, accessible static website hosted free at https://soroushshahbaznejad.github.io/. HTML/CSS with a Python standard-library build; no JavaScript, package dependencies, API keys, or paid services.

## Preview and validate

Requires Python 3.10 or newer:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m http.server 8000 --directory _site
```

Visit http://localhost:8000. Rebuild after editing. `_site/` is generated and ignored by Git; edit sources instead. All site copy is escaped during rendering.

## Maintain content

- **Biography and academic details:** edit `data/profile.json`. Its `bio`, `themes`, `education`, `experience`, `service`, and `skills` arrays hold the corresponding text.
- **Profile photograph:** add your own photo to `assets/images/`, then change `photo` in `data/profile.json` from `null` to its repository-relative path, e.g. `assets/images/profile.jpg`. Use a roughly 6:7 crop. The current monogram is explicitly labeled as a photograph placeholder.
- **Publications:** add an object to `data/publications.json`, with a unique `id`, `category`, exact `title`, ordered `authors`, and `venue`. Add `year` only for published work; use `status` for forthcoming or unpublished work. `doi` is optional and contains only the DOI, without the URL prefix. Author names matching `Shahbaznejad, S.` are bolded. Categories appear in their first-occurrence order. No publication PDFs or code repositories have been supplied or verified; add links only when available, extending the publication renderer in `scripts/build.py` as needed.
- **Projects:** add an object to `data/projects.json` with `title`, `summary`, `methods`, optional `detail`, and a `publications` array of publication IDs.
- **CV:** replace `assets/cv/Shahbaznejad_CV.pdf` with your new original PDF. The build copies it byte-for-byte. **The current PDF contains a personal phone number and is publicly downloadable.** This was flagged before publication as requested; the phone is excluded from the HTML. To remove it from the PDF, supply a redacted original or explicitly authorize modification.
- **Navigation:** edit `navigation` in `data/profile.json`. Each pair contains a label and anchor. New sections need matching IDs in `templates/index.html`.
- **Layout and styles:** edit `templates/index.html` and `assets/css/style.css`. Inline SVG link icons and the favicon are original vector assets. No third-party fonts, tracking, portrait generation, or reused research imagery.

## Deployment

The public repository uses GitHub Pages with GitHub Actions. `.github/workflows/pages.yml` builds and validates on pull requests; pushes to `main` also deploy `_site/` using GitHub's Pages artifact and deployment actions. Set repository Settings → Pages → Source to **GitHub Actions**. Development belongs on a branch such as `codex/academic-website`, then merge into `main`. GitHub provides HTTPS and the free `github.io` domain.

The root URL, canonical, Open Graph URL, sitemap, and Person structured data derive from `data/profile.json`. A minimal 404 page, robots.txt, sitemap.xml, and `.nojekyll` are generated at build time.

## Content provenance and outstanding assets

Academic content was transcribed from the original `Shahbaznejad_CV.pdf` supplied on October 23, 2026, with the user's brief guiding the introduction and structure. Published titles, supplied author order, venues, years, and DOIs are preserved. No fabricated PDF/code links, citations, experimental figures, or conclusions.

- No professional photograph was supplied; replace the labeled placeholder when ready.
- The full author list for “Frozen Pretrained Vision Representations and Human Judgments of Material Appearance in Natural Photographs” is abbreviated as `Shahbaznejad, S., et al.` in the CV. It remains abbreviated pending an authoritative full list.
- Google Scholar URL was extracted directly from the CV's hyperlink. Automated inspection may be blocked by Scholar. LinkedIn may likewise restrict unauthenticated inspection.
- CVCS and Electronic Imaging conference records have no DOIs in the supplied CV; none are guessed.
- “Do Pretrained Vision Models Reflect Human Material Judgments?” is labeled to be presented at Electronic Imaging 2027. The other manuscript is complete with submission planned for November 2026; neither is described as published.

## Organization

`data/`: content · `templates/`: layout · `assets/css/`: styles · `assets/images/`: profile and icons · `assets/cv/`: original CV · `scripts/`: build and validation · `.github/workflows/`: deployment.
