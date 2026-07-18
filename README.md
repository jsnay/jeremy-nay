# jeremynay.com

Personal resume site for Jeremy Nay, live at [jeremynay.com](https://jeremynay.com). The site is a single self-contained HTML page. Every experience bullet expands in place into a short first-person story, and a Download PDF link in the header serves the traditional resume.

## Repository layout

| File | Role |
|---|---|
| `index.html` | The entire site: markup, embedded CSS, and a small vanilla JS controller. No external dependencies of any kind. |
| `Jeremy Nay - Resume.pdf` | The downloadable resume. Generated outside this repo from the master resume source and committed here as a binary. |
| `og-image.png` | 1200x630 social link preview referenced by the Open Graph and Twitter meta tags. |
| `scripts/generate-og-image.py` | Regenerates `og-image.png` with Pillow. Run it whenever the name, title, or brand colors change. |
| `robots.txt` | Allows all crawlers and advertises the sitemap. |
| `sitemap.xml` | Lists the home page and the PDF for search engines. |

Each source file carries a header comment covering its purpose, upstream dependencies, downstream consumers, and special considerations. Read those first when diving into the code.

## How the pieces connect

Content originates in a master resume source maintained outside this repo. A tailored selection of bullets from that source appears in `index.html`, each paired with an expanded story, and the same selection is used to generate the PDF. The two must change together: master source first, then the site, then the PDF.

At serve time, Netlify hosts `index.html` as the root. Crawlers find the site through `robots.txt` and `sitemap.xml` and read the JSON-LD Person schema and meta tags in the page head. Social scrapers read the Open Graph and Twitter Card tags, which point at `og-image.png`.

Inside `index.html`, an inline head script adds a `js` class to the root element. All collapse and animation styling is gated on that class, so the page degrades cleanly: without JavaScript every story renders expanded. With JavaScript, stories collapse into accordion panels animated through a CSS `grid-template-rows` transition, and a staggered entrance animation with a highlight sweep runs once on load to signal that the bullets are clickable. Reduced-motion preferences disable the animation, and print styles collapse the page back to a plain resume.

## Updating content

1. Change the master resume source first, so the site and PDF stay in sync.
2. Update the bullet text in `index.html`, and update or add the matching story.
3. Regenerate the PDF from the master and replace `Jeremy Nay - Resume.pdf`.
4. Update `lastmod` in `sitemap.xml` for whatever changed.
5. Open a pull request. Netlify builds a deploy preview per PR; merging to `main` deploys production.

## Writing rules

All visible prose follows plain-writing rules: no em dashes anywhere (en dashes are fine in date ranges and titles), no rhetorical filler patterns, plain descriptive headings, and professional prose that leads with substance. Check new copy against these rules before committing.

## Local preview

Open `index.html` directly in a browser, or serve the directory:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`. There is no build step.

## Known issues

Open findings from code review are tracked in [GitHub issues](https://github.com/jsnay/jeremy-nay/issues), including accessibility gaps in the collapsed panels, missing security headers, and the PDF regeneration backlog.
