# SOP: Adding a New Photo

This is the standard procedure for adding one or more photos to the gallery. All steps are executed by Claude on instruction from the content owner.

---

## Prerequisites

- Photo file(s) accessible on local disk (original export from Lightroom or camera)
- `media-workflow` repo available at `~/repo/media-workflow/`
- FFmpeg installed (`brew install ffmpeg`)

---

## Step 1: Determine target album

Choose which album the photo belongs to:

| Album | Directory | Subject matter |
|-------|-----------|---------------|
| Animals | `content/Animals/` | Wildlife, pets |
| Astro | `content/Astro/` | Astrophotography, night sky |
| Cities | `content/Cities/` | Urban, architecture, street |
| Fireworks | `content/Fireworks/` | Fireworks |
| Nature | `content/Nature/` | Landscapes, flora, outdoors |
| Portrait | `content/Portrait/` | People, portrait |

To create a new album, see [Creating a New Album](#creating-a-new-album) below.

---

## Step 2: Compress the photo

Run the compression script from the `media-workflow` repo. The script resizes images wider than 2048px and sets JPEG quality to ~85%.

```bash
python3 ~/repo/media-workflow/scripts/compress_web_images.py /path/to/source/directory/
```

Or for a single file, copy it to a temp directory first:

```bash
mkdir /tmp/photo-compress
cp /path/to/DSC05420.jpg /tmp/photo-compress/
python3 ~/repo/media-workflow/scripts/compress_web_images.py /tmp/photo-compress/
```

**Expected output:**
```
✅ DSC05420.jpg: 7952px → 2048px, 24.0MB → 1.2MB
Done: 1 compressed, 0 skipped, 0 failed
```

Files wider than 2048px are resized; files already within limit are skipped.

---

## Step 3: Copy to album directory

```bash
cp /path/to/compressed/DSC05420.jpg content/<Album>/DSC05420.jpg
```

**Naming convention:** Keep the original filename. Do not rename unless the filename is meaningless (e.g., `IMG_0001.jpg` → use a descriptive name).

---

## Step 4: Update the album index.md

Open `content/<Album>/index.md` and add the new file to the `resources` list.

**Example** — adding `DSC05420.jpg` to the Astro album:

```yaml
resources:
  - src: DSC03838-Signed.jpg
  - src: DSC05420.jpg       # ← add here
  - src: 1.jpeg
  - src: DSC02762.jpeg
```

Order in the `resources` list controls display order when `sort_by: Name`. If `sort_by: Date`, Hugo uses EXIF date — order in the list is then used as a fallback for same-date images.

To set the album cover image, update `featured_image`:

```yaml
params:
  featured_image: DSC05420.jpg
```

---

## Step 5: Commit and push

```bash
git add content/<Album>/DSC05420.jpg content/<Album>/index.md
git commit -m "Add DSC05420 to <Album> album"
git push origin main
```

GitHub Actions will automatically build and deploy. Deployment takes ~60 seconds.

---

## Step 6: Verify

Check https://photography.prov1dence.top — the new photo should appear in the album.

---

## Creating a New Album

1. Create a new directory: `content/<AlbumName>/`
2. Add an `index.md` with the following front matter:

```yaml
---
title: <Album Name>
weight: 20          # controls sort order on home page (lower = earlier)
params:
  featured_image: <filename>.jpg
  theme: dark
  sort_order: desc
  sort_by: Date
resources:
  - src: <filename>.jpg
---
```

3. Copy compressed images into the directory
4. Commit and push

---

## Removing a Photo

1. Delete the file from `content/<Album>/`
2. Remove the corresponding `- src: <filename>` line from `index.md`
3. Commit and push

Note: the file blob will remain as a placeholder in git history (this is expected — see maintenance.md).

---

## Checklist

```
[ ] Photo compressed to ≤ 2048px wide (compress_web_images.py)
[ ] File copied to correct content/<Album>/ directory
[ ] resources list in index.md updated
[ ] featured_image updated if this is the new cover
[ ] git commit with descriptive message
[ ] git push to main
[ ] Verified live on photography.prov1dence.top
```
