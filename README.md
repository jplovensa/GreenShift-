# GreenShift — reference website adaptation

The website now follows the captured greenshift.id layout: a transparent fixed header and full-screen architecture hero, white philosophy section, immersive studio video, dark ecosystem grid, four video-led architectural tiers, the 45-day timeline, contact form and white footer. The existing copy is preserved. The user-supplied GreenShift/Fjäll logo assets and 540-to-45-day opening video sequence remain.

## Hosting

This is browser-native HTML, CSS and JavaScript. The complete homepage, styles, behavior and content are embedded in index.html, so an unavailable companion script cannot leave a blank page. All videos, posters, icons and fonts are local assets with relative URLs, compatible with the repository path `/GreenShift-/` and a custom domain. No npm dependencies or bundler are required.

The GitHub Pages workflow deploys on pushes to main. The actual published website is https://jplovensa.github.io/GreenShift-/ . For a new repository, choose Settings → Pages → Source → GitHub Actions.

## Develop and package

Use the existing checkout, without creating a worktree. Node.js 18+ supports the helper scripts:

```sh
npm run dev -- --port 4173
npm run build
```

To validate repository-path hosting:

```sh
node scripts/serve.mjs --dist --port 4183 --base /GreenShift-/
```

Edit static section markup in index.html, behavior in app.js, styles in style.css, and optional content data in content.json. The build synchronizes embedded styles/behavior/data, updates cinematic.html and copies only website files to dist/. Editorial and atelier URLs forward to the selected website.

## Interaction behavior

- Scroll-aware fixed header, anchor navigation, responsive full-screen menu and keyboard dismissal.
- Exact reference tier details and local tier videos in native dialogs. A project action carries the selected tier to the inquiry form.
- Required fields and email validation, review of the inquiry, and an explicit WhatsApp handoff to the existing public contact number. The source site's contact backend is not copied or invoked; no automatic messages or fake submission states are used.
- Video playback follows viewport visibility and reduced-motion preference. The hero has a play/pause control.
- Opening countdown from 540 to 45 days, followed by GreenShift as part of Fjäll Group; Skip and Escape dismiss immediately. Reduced-motion mode uses a short static reveal. A fixed upper bound prevents a failed asset or animation from trapping visitors.
- Experience Studio pairs the Drop Pod Villas walkthrough with a locally hosted Three.js spatial presentation adapted from the supplied Garuda Spark Innovation Hub reference. Launchers load presentations only on demand; closing removes the frame and restores focus. Full-experience links remain available without JavaScript.
- Intro logos appear directly over the video, with a transparent reveal surface. The studio hierarchy uses Fjäll artwork.
- Full page content is present without JavaScript, and remains visible if assets fail.

## Sources and checks

Desktop/mobile source layouts, DOM styles and four tier-dialog states were captured after network access was activated. Live media files were copied from greenshift.id. Inter is hosted locally from the official Fontsource npm package because Google Fonts access was unavailable; its license is included. User-supplied inline logos remain prepared raster reproductions and can be replaced with original production artwork for exact brand fidelity.

The static build and JavaScript syntax checks passed. Chromium verified both 1440px and 390px layouts, all sections, all four dialogs and selected-tier handoffs, form review, mobile navigation, no horizontal overflow, no JavaScript errors, and no missing local assets. No-JavaScript / failed-asset checks and the normal-motion intro passed. Side-by-side source comparisons and screenshots are in verification/. See design-qa.md for deliberate differences and visual verification evidence.

The spatial presentation uses vendored Three.js 0.160.0 (MIT license included) and compiled Tailwind 3.4 utilities. It requires no CDN requests or package installation at runtime. Preview images are captures of the supplied experiences. The Drop Pod walkthrough remains embedded from its original GitHub Pages URL.

## Asset Repurposing Studio

The studio at `#refurbish` is a GreenShift experience for development concepts, renovation aesthetics and asset repurposing. Clients choose a starting direction, explore the existing-space study, browse six renovation categories, and collect a palette for their inquiry. The section uses original imagery and its own film; the Fjäll product catalog and Garuda Spark footage are removed from this journey.

The renovation library at `#material-library` covers finishing panels, partitions, wall finishes, flooring, joinery and lighting. Filter categories, open detail dialogs, save or remove selections, and pass the direction and palette into a Retrofit inquiry. Existing customer notes remain intact; repeated use updates the generated brief instead of duplicating it. Sending remains an explicit reviewed WhatsApp handoff.

Eight original AI-assisted visual studies support the experience. The 24-second MP4 is an original animated concept film assembled from the existing-shell and reimagined-interior studies, with one shared camera trajectory and a four-second dissolve. It is labelled as a concept film and does not claim to document a completed project or a measured before/after transformation. Media is hosted locally. Provenance: `assets/asset-studio-provenance.json`.

The 60fps film uses fractional-coordinate cubic sampling to avoid stepped zoom jitter, holds the finished interior at its end, and supports explicit replay. Re-render with `python scripts/render-asset-film.py` (FFmpeg required). The film supports play/pause, a full-view dialog, reduced-motion fallback, Escape dismissal and focus return. Static studio content and the contact route remain available without JavaScript. Deployment retains customer-focused cards and filters for new builds or existing spaces, and links directly into the studio.
