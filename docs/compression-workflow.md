# Image Compression Workflow

All source images must be compressed before being committed to the repository. This keeps the repo size manageable and ensures fast page loads.

---

## Why we compress

- Original camera exports are 10–25MB per file (7000–9000px wide)
- Web display never exceeds 2048px on any device at 2× DPI
- Git stores binary files inefficiently — large images balloon repo size permanently
- GitHub Pages has a 1GB soft limit; uncompressed originals would exhaust it quickly

**Current repo content size:** ~15MB for 32 images (originals were ~123MB)

---

## Tool

Script: `scripts/compress_web_images.py`  
Dependency: FFmpeg (`brew install ffmpeg`)

### What it does

1. Scans a directory recursively for `.jpg` / `.jpeg` files (case-insensitive)
2. Reads each image's pixel width via `ffprobe`
3. Skips files already <= `--max-width` (default 2048px)
4. For files wider than the limit: resizes using FFmpeg `scale` filter, sets JPEG quality via `-q:v` (default 3 ≈ 85%)
5. Replaces the original file in-place
6. Reports original → compressed size for each file

### Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--max-width` | 2048 | Max output width in pixels |
| `--quality` | 3 | FFmpeg JPEG quality scale (1=best, 31=worst; 3≈85%, 5≈80%) |

---

## Usage

### Compress a single directory

```bash
python3 scripts/compress_web_images.py /path/to/dir/ --max-width 2048 --quality 3
```

### Compress a single file via temp directory

```bash
mkdir /tmp/compress && cp /path/to/photo.jpg /tmp/compress/
python3 scripts/compress_web_images.py /tmp/compress/ --max-width 2048 --quality 3
cp /tmp/compress/photo.jpg content/<Album>/
```

### Compress all existing content images

```bash
python3 scripts/compress_web_images.py content/ --max-width 2048 --quality 3
```

Already-compressed files (≤ 2048px) will be skipped automatically.

---

## Output interpretation

```
compressed content/Animals/EUR03920-Signed.jpg 8698x5799 -> 2048x1366, 13400000 -> 400000
skip content/Astro/DSC02762.jpeg width=2048
```

---

## Quality tradeoffs

| Setting | Quality | Typical size | Use case |
|---------|---------|-------------|---------|
| `--quality 2` | ~95% | 2–4MB | Archival web copies |
| `--quality 3` | ~85% | 0.3–1.5MB | **Default — gallery use** |
| `--quality 5` | ~80% | 0.2–1.0MB | Aggressive size reduction |

At 2048px wide and quality 3, images are visually indistinguishable from the original at normal viewing distances and browser zoom levels.

---

## EXIF preservation

The script passes `-map_metadata 0` to FFmpeg, which preserves all EXIF data (camera model, lens, shutter speed, aperture, ISO, date). GPS coordinates are stripped at **Hugo build time** by the site config (`imaging.exif.disableLatLong: true`), not during compression.

---

## Re-running on committed images

It is safe to re-run the script on `content/` at any time. Images already at or below 2048px will be skipped. This is useful after updating `--quality` or `--max-width` parameters for a new standard.

After re-running, commit the changed files:

```bash
git add content/
git commit -m "Re-compress images: <reason>"
git push origin main
```

---

## Git history and large files

Once a large file is committed to git, it persists in history even after deletion or replacement. To clean historical blobs, use:

```bash
git filter-repo --force --strip-blobs-bigger-than 1500K
git remote add origin git@github-chr1sc2y:chr1sc2y/photography.git
git push --force origin main
```

Run this only after compressing and committing the current images, so that HEAD contains only small files before the strip runs.
