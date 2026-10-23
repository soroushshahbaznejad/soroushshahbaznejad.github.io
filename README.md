# Soroush Shahbaznejad — Academic website

A static academic website hosted free at https://soroushshahbaznejad.github.io/. The design uses a dark background, rounded panels, blue accents, and compact spacing. HTML/CSS is generated with Python's standard library; no client JavaScript, API keys, or paid services.

## Preview and validate

Requires Python 3.10 or newer:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m http.server 8000 --directory _site
```

Visit http://localhost:8000. Rebuild after editing. `_site/` is generated and ignored by Git; edit sources instead.

## Maintain content

- **Biography and academic details:** edit `data/profile.json`. Its `bio`, `themes`, `education`, `experience`, `service`, and `skills` arrays hold the corresponding text.
- **Profile photograph:** add your own photo to `assets/images/`, then set `photo` in `data/profile.json` to its repository-relative path. The current photograph is `assets/images/profile.png`. CSS crops the display without modifying the original image. Set `photo` to `null` to restore a labeled placeholder.
- **Publications:** add an object to `data/publications.json`, with a unique `id`, `category`, exact `title`, ordered `authors`, and `venue`. Add `year` for published work; use `status` for forthcoming or unpublished work. `doi` is optional and contains the DOI without the URL prefix. Author names matching `Shahbaznejad, S.` are bolded. Categories appear in first-occurrence order.
- **Projects:** add an object to `data/projects.json` with `title`, `summary`, `methods`, optional `detail`, and a `publications` array of publication IDs.
- **CV requests:** the CV is available by email request only. Three “Request CV” links open a prefilled email addressed to the `email` value in `data/profile.json`. The visitor sends the request through their own email client; you choose whether and when to reply with the CV. Edit the subject and request body in `scripts/build.py` and the section text in `templates/index.html`. No message is sent automatically, no backend is required, and no CV PDF is included in the deployment. Keep your current CV privately on your computer.
- **Navigation:** edit `navigation` in `data/profile.json`. Each pair contains a label and anchor. The original `CV` navigation entry is replaced by the separate request button. New sections need matching IDs in `templates/index.html`.
- **Layout and styles:** edit `templates/index.html` and `assets/css/style.css`. Section padding is 30px on desktop and 24px on mobile. The design is an original implementation informed by the requested reference, without copying its code or media.

## Deployment

`.github/workflows/pages.yml` builds and validates pull requests. Pushes to `main` also deploy `_site/` using GitHub Pages. Repository Settings → Pages → Source is **GitHub Actions**. Develop on a branch, then merge into `main`. GitHub provides HTTPS and the free `github.io` domain.

The canonical URL, Open Graph URL, sitemap, and Person structured data derive from `data/profile.json`. A 404 page, robots.txt, sitemap.xml, and `.nojekyll` are generated. The build copies only `assets/css/` and `assets/images/` to the public artifact; validation rejects deployed PDFs and CV download links.

## Content and privacy notes

Academic content derives from the supplied CV and user edits. Published titles, author order, venues, years, and DOIs are preserved. Unpublished manuscripts retain their stated status. The full author list for the planned CVIU submission is abbreviated in the supplied CV and has not been invented. No publication PDFs or code repositories have been supplied or linked.

The previously downloadable CV was removed from the current repository and deployment when the user requested email-only access. Historical Git commits still contain previously published PDFs; removing the current download does not erase repository history or third-party cached copies. No history rewriting was performed.

Google Scholar identity and journal DOI records were verified. LinkedIn restricts automated access. The user-supplied photograph is included unchanged. No tracking or third-party fonts are used.

## Organization

`data/`: content · `templates/`: layout · `assets/css/`: styles · `assets/images/`: photo and favicon · `scripts/`: build and validation · `.github/workflows/`: deployment.
