# SOP: Editing Site Config or Content (non-photo)

For any change that isn't adding a photo — e.g. renaming the site title, editing menus, deleting pages, tweaking theme params, updating docs.

For photo additions, use [sop-add-photo.md](sop-add-photo.md) instead.

---

## Deploy model — read this first

This site is deployed by **GitHub Actions**, not by hand. There is **one repo** (`chr1sc2y/photography`); the built HTML lives on the `gh-pages` branch and is managed entirely by CI.

- You do **not** run `hugo` locally to deploy.
- You do **not** push to a second repo. (The old `public/` submodule setup was retired in commit `a45f009`.)
- You do **not** touch the `gh-pages` branch by hand.

The only thing you push is your source change on `main`. See [.github/workflows/deploy.yml](../.github/workflows/deploy.yml) and [tech-stack.md](tech-stack.md#hosting--deployment).

---

## Steps

### 1. Make the edit

Edit files under `config/`, `content/`, `docs/`, etc. as needed.

### 2. (Optional) Preview locally

```bash
hugo server
```

Open `http://localhost:1313` to verify. Skip this for trivial edits (typos, docs).

### 3. Commit

```bash
git add <changed files>
git commit -m "<descriptive message>"
```

### 4. Push to main

```bash
git push origin main
```

### 5. Wait for the Action

GitHub Actions runs `hugo --minify` and pushes the build to `gh-pages`. Takes ~60 seconds. Check the Actions tab if you want to watch it.

### 6. Verify

Open https://photography.prov1dence.top in a fresh tab (or hard-refresh) and confirm the change is live.

---

## What if I want to render locally anyway?

You can — `hugo --minify` produces output in `public/` (gitignored). It's useful for previewing, but the output is never committed and never deployed. Only `main` triggers a real deploy.

---

## Checklist

```
[ ] Edit made
[ ] (optional) Previewed with `hugo server`
[ ] git commit with descriptive message
[ ] git push origin main
[ ] GitHub Action succeeded (Actions tab)
[ ] Verified live on photography.prov1dence.top
```
