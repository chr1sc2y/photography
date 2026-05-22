# Maintenance Status

## Ownership

| Role | Owner |
|------|-------|
| **Content owner** | Prov1dence (chr1sc2y) |
| **Technical maintainer** | Claude (AI) via Claude Code |
| **Hosting account** | chr1sc2y (GitHub) |

This repository is **AI-maintained**. All infrastructure changes, dependency updates, content additions, and operational tasks are performed by Claude on instruction from the content owner. The owner provides photos and editorial decisions; Claude handles all technical execution.

---

## Status

**Site status:** Active  
**Deployment:** Automated (push-to-deploy on `main`)  
**Last infrastructure migration:** 2026-05-22 (migrated from `chr1sc2y-photography` sub-account to `chr1sc2y`)

---

## Operational Health

### What's automated

- Build and deploy on every push to `main` (GitHub Actions)
- TLS certificate renewal (GitHub Pages)
- Hugo thumbnail generation at build time

### What requires manual action

| Task | Trigger | Owner |
|------|---------|-------|
| Add new photos | Content owner decision | Claude (on instruction) |
| Update Hugo version | Theme release or security note | Claude |
| Update theme submodule | Theme release | Claude |
| DNS changes | Domain renewal or provider change | Content owner |
| GitHub Pages config | Domain change | Content owner (browser) |

### Maintenance windows

No scheduled maintenance windows required. GitHub Pages has no downtime for static sites. Deployments take ~60 seconds and are zero-downtime (GitHub swaps the `gh-pages` branch atomically).

---

## Known Constraints

- **GitHub Pages free tier:** 1GB storage soft limit, 100GB/month bandwidth. Current repo is well within limits (~15MB content).
- **No server-side logic:** All filtering, search, and navigation is client-side or compile-time. Adding dynamic features (comments, auth) would require a different architecture.
- **Image history:** Git history retains placeholder stubs for images removed or replaced. This is expected behaviour from `git filter-repo --strip-blobs-bigger-than`.

---

## Dependency Update Policy

| Dependency | Policy |
|------------|--------|
| Hugo | Manual pin. Check release notes before upgrading — theme compatibility must be verified. |
| hugo-theme-gallery | Manual. Run `git submodule update --remote themes/gallery` and test locally before committing. |
| GitHub Actions | Actions use `@v3`/`@v4` floating tags. Monitor for breaking changes in major version bumps. |

---

## Incident Response

**Site down (DNS/Pages issue):**
1. Check `https://www.githubstatus.com/`
2. Verify DNS: `dig photography.prov1dence.top CNAME` should return `chr1sc2y.github.io`
3. Verify Pages config in repo Settings → Pages → custom domain

**Deployment failing:**
1. Check Actions tab in GitHub repo for error logs
2. Common causes: Hugo version mismatch, broken image path in `index.md`, submodule not initialised

**Broken image in gallery:**
1. Verify file exists in `content/<Album>/` and is listed in `index.md` resources
2. Check file is a valid JPEG (`file <image>`)
3. Re-run compression if needed, commit, push
