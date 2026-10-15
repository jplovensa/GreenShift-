# GreenShift — reference website adaptation

GreenShift now uses one coherent studio layout: cinematic hero, the requested delivery explanation, studio identity, a full-width client presentation, an open refurbishment and material journey, development approaches, delivery context and inquiry. The stylesheet was rebuilt from scratch and captured inline layouts removed. Original brand assets and service copy remain. The refurbishment film uses the latest user upload; the other videos remain unchanged. The optional 540-to-45-day introduction remains skippable.

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

The studio at `#refurbish` is a GreenShift experience for development concepts, renovation aesthetics and asset repurposing. Clients watch the transformation, choose a starting direction, compare the existing-space and renovation studies with a keyboard-accessible reveal slider, browse six renovation categories, and collect a palette for their inquiry. A sticky desktop brief keeps their choices visible beside the library; mobile stacks the brief after the palette. The section uses original imagery and its own film; the Fjäll product catalog and Garuda Spark footage are removed from this journey.

The renovation library at `#material-library` covers finishing panels, partitions, wall finishes, flooring, joinery and lighting. Filter categories, open detail dialogs, save or remove selections, and pass the direction and palette into a Retrofit inquiry. Existing customer notes remain intact; repeated use updates the generated brief instead of duplicating it. Sending remains an explicit reviewed WhatsApp handoff.

Original concept studies support the renovation and material library. The current refurbishment film is the user-supplied 5.04-second 1080p MP4 at `assets/refurbishment-studio.mp4`, with its original H.264 video and AAC audio preserved. The MP4 is optimized for progressive playback and its poster is extracted from the upload. Provenance: `assets/studio-client-provenance.json`.

The film supports play/pause, a full-view dialog, reduced-motion fallback, final-frame hold, explicit replay, Escape dismissal and focus return. `scripts/render-asset-film.py` reproduces the previous concept montage and is retained as an archive helper. Static studio content and the contact route remain available without JavaScript.

## Current studio flow

The client presentation is full width, with film, walkthrough and spatial-model controls. Refurbishment is a continuous visible journey through film, direction, uploaded transformation timelapse, materials and brief. There are no dashboard tabs or fixed brief sidebar. Presentation dialogs, material details, tier details and WhatsApp inquiry review remain functional. Without JavaScript, the static content and contact information remain visible. Screenshots: verification/reset-site-*.png.

The considered-transformation section now uses the uploaded `assets/transformation-timelapse.mp4` with native video controls, a matching poster and original audio. Playback starts on user interaction; the previous image reveal slider is removed.

## Renovation Playground / WebGL planner

Open `assets/renovation-studio.html` directly or launch it from `#simulation-studio`. The planner uses the existing locally hosted Three.js library and procedural geometry, with no external 3D assets or build dependencies.

- Choose a 6×5 m lounge/work preset or a blank room; resize each side from 3–12 m.
- Place and drag nine object types (including EPS partitions), rotate in quarter-turns, or position them numerically. Objects snap to a 0.25 m grid. Boundary, overlap, entrance and design-credit checks reject invalid placement.
- Change floor/wall finishes, switch between 3D and top views, and walk with W A S D, arrows, or touch controls.
- Complete six design goals for XP. Credits are game points and never a renovation quote.
- Undo, autosave on the current browser/device, download a JSON plan, and import a previously downloaded plan. Up to 40 objects and 40 undo steps are retained during a session. A plan stores concept dimensions, placements and finishes; it does not provide construction documentation.
- “Use this plan” transfers a summary and positions to the existing project inquiry. It preserves existing notes and deduplicates repeat transfers. The parent accepts messages only from the currently open, same-origin planner iframe. Standalone mode returns to the contact form through a one-time local pending brief.

Checks: start `npm run dev`, then run `python scripts/verify-renovation-studio.py` with Python Playwright and Chromium installed. `GREENSHIFT_TEST_URL` can select another running site. The check exercises the actual WebGL scene, pointer placement/drag, collision rejection, rotation, finishes, undo, persistence, export/import validation, quests, credit limit, walkthrough, mobile controls, parent/standalone handoff and WebGL-unavailable fallback. Screenshots are in `verification/renovation-planner-*.png`. Existing films remain unchanged.

## Asset Repurposing Studio / EPS upgrade

The existing planner URL now opens the Asset Repurposing Studio. Existing v1 plans migrate into `greenshift:asset-repurposing:v2` without modifying the original `greenshift:renovation:v1` save. Version 1 and 2 JSON plans remain importable. Saved v2 plans contain the EPS scope, wall parameters and lighting choice; quantities are recalculated from geometry.

**EPS quantity scope:** placed EPS partitions and optional rear/left retained-wall lining. Thickness is EPS core thickness: 10, 12, 15 or 20 cm. Each EPS partition has an editable length, height, thickness and solid/door/window configuration. Retained lining has explicit opening-area deductions; the intersecting rear/left butt joint is counted once. Net surface area × core thickness gives installed m³. A separate 0–20% allowance gives indicative supply m³. Mixed thicknesses are grouped. CSV takeoff, JSON plans and project inquiry summaries preserve this information. Skins, finishes, adhesives and structure are excluded; this is a concept estimate for measured design review, not a structural specification or cost quotation.

Interaction upgrades include axis-constrained dragging, duplicate, redo, focus view, pinch/button zoom, existing/proposed/EPS views, screenshot capture and walkthrough collision through doors. On mobile, installed and supply core volumes remain visible in a fixed summary. Rendering uses beveled procedural geometry, PBR materials, fabric/wood/EPS bump textures, PMREM environment lighting, contact shadows and day/golden/evening moods. Native GPU rendering starts in Studio quality; software renderers start in Performance quality. Users can choose either. Static shadow maps are cached until geometry or lighting changes. This remains locally hosted Three.js/WebGL, with no Unreal Engine runtime, paid streaming service or remote asset dependency.

Verification: `node tests/eps-takeoff.mjs`; `python scripts/verify-asset-studio.py`; `python scripts/verify-asset-interactions.py`; `python scripts/verify-eps-walkthrough.py`; and the original planner regression `python scripts/verify-renovation-studio.py`. Run the local server first. EPS tests cover all four thicknesses, openings, mixed cores, corner deduction, scope exclusions, waste, invalid inputs and CSV totals. Browser tests cover actual WebGL, editing, quantity updates, compatibility, persistence, brief handoff, touch zoom, geometry-aware doors and fallback. Preview and captures are in `verification/asset-repurposing-*.png`.
