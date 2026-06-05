# Agent Guide

This repository is the source for Prov1dence's photography portfolio at
https://photography.prov1dence.top. It is maintained by agents on request from
the content owner.

## Add-Photo Workflow

Use this workflow whenever the owner asks to add photos:

1. Inspect the candidate image visually before adding it.
2. If the owner asks for screening, recommendation, or review, stop after
   presenting recommended filenames and thumbnails. Do not copy, compress, or
   add candidate photos until the owner explicitly approves the exact filenames.
3. Choose the album from the subject matter:
   - `Animals`: wildlife and pets
   - `Astro`: night sky and astrophotography
   - `Cities`: urban, architecture, and street
   - `Fireworks`: fireworks
   - `Nature`: landscapes, flora, desert, mountains, and outdoors
   - `Portrait`: people and portraits
4. Copy candidate files into a temporary directory.
5. Run `python3 scripts/compress_web_images.py <temp-dir> --max-width 2048 --quality 3`.
6. Copy the compressed JPEGs into `content/<Album>/`.
7. Add each filename to `content/<Album>/index.md` under `resources`.
8. Run `hugo --minify` and inspect the local page or generated HTML.
9. Commit only source changes on `main`. Do not commit `public/`, `resources/_gen/`,
   or `.hugo_build.lock`.

## Photo Selection Bar

Only add photos that feel portfolio-worthy. Prefer:

- Strong composition with a clear subject or visual rhythm.
- Good light, color, atmosphere, or a distinctive moment.
- Technical quality good enough for full-screen viewing after 2048px compression.
- Images that add variety to an album instead of duplicating a stronger existing frame.

Reject or hold back images with unclear subject, obvious blur, distracting dust spots,
awkward crop, blown highlights, or near-duplicates of a stronger frame.

## Verification

For photo additions, verify with:

```bash
python3 -m unittest discover tests
hugo --minify
```

When a local preview is useful:

```bash
hugo server --bind 127.0.0.1 --port 1313
```

## Deployment

Deployment is automated by GitHub Actions. Push source changes to `main`; CI builds
the site and publishes `gh-pages`. Never deploy by editing `gh-pages` manually.
