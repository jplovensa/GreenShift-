# GreenShift Design Studio

Version 1 (Cinematic Studio), implemented in browser-native JavaScript, HTML and CSS. The repository root is a complete static website. The entire homepage is real HTML, with styles, content data and interaction JavaScript embedded directly in index.html. No companion script, CSS file, Vite, npm package or runtime build tool is required to show the page.

The website uses the supplied hero video, a prepared transparent house-shaped logo asset, and the original site copy. Studio capabilities lead to architectural tier details and a project inquiry review. Visitors send the reviewed inquiry themselves through WhatsApp; there is no automatic submission or simulated success message.

## GitHub Pages

All URLs are relative, so the website supports both a custom domain and the repository path `/GreenShift-/`.

The `.github/workflows/pages.yml` workflow copies the site into `dist/` and deploys it on pushes to `main`.

If this repository has not already enabled Pages with Actions, open **Settings → Pages → Build and deployment → Source → GitHub Actions**, then run **Actions → Deploy GreenShift to GitHub Pages → Run workflow**. The deployment job reports the actual published URL. Changing repository Pages settings could not be verified here because access to GitHub's Pages API was denied.

Alternatively, the root files also support branch-based Pages hosting: choose **Deploy from a branch**, `main`, `/ (root)`. The `.nojekyll` file disables unnecessary Jekyll processing. Use one publishing method.

The selected website is `index.html`. The prior `cinematic.html` URL also works; `editorial.html` and `atelier.html` forward to the selected version.

## Local development

Node.js 18+ is enough for the helper scripts. No dependencies need installing.

```sh
npm run dev -- --port 4173
```

Or serve the repository using any static HTTP server. JavaScript and styles are embedded in the homepage. Images, video and the icon font are local optional assets; a failure to load them does not remove the page content.

## Optional static packaging

```sh
npm run build
node scripts/serve.mjs --dist --port 4173
```

`dist/` contains only public website files. To simulate the GitHub repository URL:

```sh
node scripts/serve.mjs --dist --port 4183 --base /GreenShift-/
```

## Checks

- Dependency-free static packaging passed.
- JavaScript syntax checks passed.
- Headless Chromium rendered desktop (1440px) and mobile (390px) under `/GreenShift-/` with no JavaScript errors or horizontal overflow.
- All four real dialog interactions, selected-tier handoff, inquiry review and mobile navigation passed Chromium checks.
- With JavaScript disabled and all media/font assets blocked, the complete page and contact information remain visible.
- Screenshots are saved in verification/.
- All four tier dialogs and selected-tier inquiry handoffs passed DOM checks.
- Navigation and reviewed WhatsApp inquiry payload passed DOM checks.
- Every HTML-referenced script, stylesheet, logo, poster, video and the local icon font returned successfully under the repository path.

Local browser rendering and interactions are verified. Live GitHub Pages deployment remains unverified because network access to the reported URL returned 403. The original inline logo was reproduced as a raster asset; replace `assets/logo.png` with original production artwork for exact logo fidelity. See `design-qa.md`.

## Video introduction

The homepage opens with the supplied architecture video behind a 540-to-45-day countdown, followed by GreenShift as part of Fjäll Group. The countdown takes 2.6 seconds, holds at 45 for 0.35 seconds, reveals the brands for 1.5 seconds and fades away in 0.5 seconds. Skip or Escape dismisses it immediately. Background content is inert only while the introduction is active; focus and scrolling return on dismissal. Reduced-motion visitors receive a brief static brand reveal without video autoplay or countdown animation.

A separate 6.2-second upper bound prevents media/animation failures from trapping visitors. With JavaScript disabled, the introduction does not appear and the static homepage remains available. Local Chromium checks passed at 1440px and 390px for all stages, automatic cleanup, Skip, Escape, reduced motion, missing media/logo/font assets, and no-JavaScript loading. Intro screenshots are in verification/intro-*.png.

The Fjäll Group inline logo reference was prepared as a transparent raster reproduction in assets/fjall-group.png. Replace with original brand artwork when available for exact production fidelity.
