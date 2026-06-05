# Prov1dence Photography

Static Hugo photography portfolio for https://photography.prov1dence.top.

## Quick Start

```bash
hugo server
```

Open http://localhost:1313.

## Common Agent Tasks

- Add photos: follow [docs/sop-add-photo.md](docs/sop-add-photo.md).
- Edit non-photo site content: follow [docs/sop-site-edit.md](docs/sop-site-edit.md).
- Understand the stack: read [docs/tech-stack.md](docs/tech-stack.md).
- Maintain the site: read [docs/maintenance.md](docs/maintenance.md).

## Photo Source Rules

Gallery source images live in `content/<Album>/` and should be compressed before
commit:

```bash
python3 scripts/compress_web_images.py /path/to/temp/photos --max-width 2048 --quality 3
```

Each displayed image must also be listed in that album's `index.md` `resources`
section.
