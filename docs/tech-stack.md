# Tech Stack

## Overview

Static photography portfolio site hosted on GitHub Pages, built with Hugo. No backend, no database, no runtime dependencies — all content is compiled at deploy time.

**Live URL:** https://photography.prov1dence.top  
**Repository:** https://github.com/chr1sc2y/photography  
**Maintained by:** Claude (AI) on behalf of Prov1dence

---

## Stack

### Site Generator

| Component | Details |
|-----------|---------|
| **Hugo** | v0.143.1 extended |
| **Theme** | [hugo-theme-gallery v4](https://github.com/nicokaiser/hugo-theme-gallery) (git submodule) |
| **Go modules** | `github.com/nicokaiser/hugo-theme-gallery/v4 v4.6.6` |

Hugo compiles `content/` into a static site. The gallery theme handles image resizing (thumbnails), lightbox, and responsive layouts at build time using Hugo's built-in image processing pipeline.

### Hosting & Deployment

| Component | Details |
|-----------|---------|
| **Host** | GitHub Pages |
| **Deploy branch** | `gh-pages` (auto-managed by Actions) |
| **CI/CD** | GitHub Actions (`.github/workflows/deploy.yml`) |
| **Trigger** | Every push to `main` |
| **Custom domain** | `photography.prov1dence.top` |
| **DNS** | CNAME: `photography.prov1dence.top → chr1sc2y.github.io` |
| **TLS** | Auto-provisioned by GitHub Pages |

Workflow: push to `main` → Actions builds Hugo → pushes compiled HTML/assets to `gh-pages` → GitHub Pages serves it.

### Content Structure

```
content/
├── _index.md          # Home page config
├── Animals/           # Album: animals photography
│   ├── index.md       # Album metadata + image manifest
│   └── *.jpg / *.jpeg # Source images (2048px wide, JPEG q85)
├── Astro/             # Album: astrophotography
├── Cities/            # Album: urban photography
├── Fireworks/         # Album: fireworks
├── Nature/            # Album: nature photography
├── Portrait/          # Album: portrait photography
└── featured-album/    # Featured picks (cross-album)
```

Each album is a Hugo page bundle. The `index.md` contains album metadata and an explicit `resources` list that controls which images appear and in what order.

### Image Pipeline

Source images are stored directly in `content/` at web-optimised resolution. Hugo generates thumbnails and responsive variants at build time into `resources/_gen/` (gitignored).

**Source image spec:** max 2048px wide, JPEG quality ~85% (`-q:v 3` via FFmpeg)  
**Compression tool:** `media-workflow/scripts/compress_web_images.py`  
**Build-time processing:** Hugo CatmullRom resampling, quality 75 (for generated thumbnails)

### Config

Hugo config lives in `config/_default/params.toml`. Key settings:

- `defaultTheme: dark`
- `imaging.quality: 75` (Hugo-generated thumbnails)
- `imaging.resampleFilter: CatmullRom`
- EXIF: date preserved, GPS stripped (`disableLatLong: true`)

---

## Dependencies

| Dependency | Version | Purpose | Update policy |
|------------|---------|---------|--------------|
| Hugo | 0.143.1 | Site generator | Pin; update when theme requires it |
| hugo-theme-gallery | v4.6.6 | Gallery theme | Pin via go.sum; update manually |
| peaceiris/actions-hugo | v3 | CI Hugo setup | Auto minor |
| peaceiris/actions-gh-pages | v4 | CI deploy | Auto minor |

---

## Local Development

Requirements: Hugo extended (≥ 0.121.2), Go, Git.

```bash
git clone --recurse-submodules git@github-chr1sc2y:chr1sc2y/photography.git
cd photography
hugo server
```

Site available at `http://localhost:1313`.
