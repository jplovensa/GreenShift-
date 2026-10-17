# GreenShift — reference website adaptation

GreenShift’s client journey now starts with its design/development identity and three service routes: interior refurbishment, facade facelift and development concepts. The cinematic opening, uploaded films, client presentations, material library and advanced WebGL studios remain available. Housing delivery copy is retained in its modular-development context with explicit eligibility and programme notes.

## Indonesia and bilingual experience

The opening positions GreenShift for architecture, refurbishment and development concepts in Indonesia. A keyboard-accessible local/overseas client path explains site information, remote design reviews, scope, responsibilities and project-specific approvals. The Projects section links directly to **https://jplovensa.github.io/FG_Website/index.html** in a new tab. GreenShift’s interactive studies remain clearly identified as concept presentations.

Choose **ID / EN** in the header or studio. The language follows an explicit `?lang=id` / `?lang=en` link, then the saved preference, then the browser’s Indonesian/English setting. It persists on this device and accompanies shared briefs and local studio launches. Local/overseas origin is retained in the Space brief. The inquiry also records preferred conversation language and an optional client-selected IDR investment range; those ranges are not service prices or a construction quotation.

Edit translations in `assets/language-id.json`. The build generates `assets/language-data.js`; `assets/language.js` applies reversible local translations, including dynamically created controls, while preserving canonical option values, measurements, user-authored notes and city names. User text is excluded from automatic translation. PDFs and WhatsApp summaries use the selected language. The process film retains its original bytes with optional Bahasa Indonesia captions. English and normal contact remain available if language assets cannot load. No external translation API is used.

Bilingual workflow checks: `python scripts/verify-indonesia-journey.py` and `python scripts/verify-language-fallback.py` against the production-path development server. Existing Space and studio tests still apply.

## Start with your space

The guided, mobile-friendly brief accepts an optional local photo, dimensions, a goal, city, timing and one of six coordinated style references. Drafts save on the current device. Clients can return, copy a share link (photo excluded), download JSON, open a print-ready PDF view or carry the brief into an explicit WhatsApp inquiry preview. Photos are downscaled locally and never uploaded by this feature; they can be attached separately in WhatsApp by the client.

The reference imagery is rendered from the actual studios and labelled as illustrative, not an automatic alteration of the uploaded photo. A measured footprint/elevation preview and a visible scope note keep the actual brief separate from the studios’ model bounds. Launching a studio offers **Apply brief to a new concept** or **Keep current plan**. Applying is explicit and undoable. A same-origin message supports the handoff even when local storage is blocked.

- Shared schema: `assets/space-brief-model.js`; guided UI: `assets/space-builder.js`; explicit studio handoff: `assets/space-studio-bridge.js`.
- Interior models: 3–12 m in half-metre increments, 2.4–4.5 m height. Facade models: 3–20 m width/depth, 2.4–12 m height. The brief retains original entered dimensions, and any adjusted model study zone is explained before launch.
- First-party `greenshift:journey` browser events expose service selection, completed briefs, studio opening, inquiry preparation and WhatsApp clicks. Only event/service/source are emitted; no photo, project notes or contact data. No third-party analytics provider is configured.
- Existing Drop Pod / Garuda Spark presentations are labelled presentation studies. Completed-project case studies, verified client testimonials, actual fees and availability must come from approved business records; none have been invented.

For production-path checks, build and run `node scripts/serve.mjs --dist --port 4174 --base /GreenShift-/`, then run `node tests/space-brief.mjs`, `python scripts/verify-space-journey.py` and `python scripts/verify-space-edge-cases.py`. The studio regression suite remains in `tests/` and `scripts/verify-studio-forms.py`.


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

## Measured EPS and facade facelift studios

Both studios retain Inter and use local WebGL assets. Choose a studio through the illustrated 3D selector. Furniture catalog images are captures of the actual procedural assets, rather than Unicode symbols. Existing uploaded films remain unchanged.

Interior (`assets/renovation-studio.html?v=studio4`):

- New plans start with zero EPS; existing v2 plans keep their checked lining scope.
- A guided measured-wall form accepts length, height, core thickness and actual door/window sizes. The inspector edits those measurements, position and a precise 0–359° angle. Quick controls turn ±15° or 90°. Rotation changes the layout, not the material quantity.
- Each surface shows `(length × height − openings) × thickness in metres`, including individual opening dimensions. Core volume and extra supply allowance are separate. Quantities display up to six decimals without unnecessary trailing zeros.
- Oriented rectangle collision checks validate arbitrary-angle walls against objects, entrance and room limits. Walls cannot overlap, avoiding duplicate EPS volumes. Rear/left lining keeps the existing butt-joint rule.
- Per-wall values, imported legacy files, saved layouts, CSV schedules and inquiry summaries share the same estimator. Position snapping does not round the wall's measured length/height.

Facade (`assets/facade-studio.html?v=studio4`, launched at `#facelift-studio`):

- Independent concept, browser save, JSON import/export and inquiry handoff.
- Measured width/depth/height, floor count, custom window/door dimensions, three finishing directions, trim, canopy, shading fins, roofline frame and lighting.
- Orbit/pinch/keyboard camera, front elevation, street view, existing/proposed/EPS phases, direct 3D surface selection and PNG capture. Five journey tasks award exploration XP.
- Selected front EPS deducts the actual front cutouts; optional side returns are solid. With front EPS, returns extend by core thickness at exterior butt joints, without overlapping the front panel. The rendered geometry and schedule use that joint rule.
- Concept extensions move the front and lengthen the side returns. Added footprint is reported separately; the tool performs no engineering or structural verification. Canopy, finish layers, frames, roof detailing, fixings and structure are excluded from EPS core quantity.

The calculation is exact for the rectangular geometry and opening dimensions entered, subject to display rounding. Site measurements, construction tolerances, assembly specification and procurement quantities require a measured review. A volume is not a construction cost or an approved EPS product system.

Checks: `node tests/eps-takeoff.mjs`, `node tests/facade-takeoff.mjs`, `python scripts/verify-studio-upgrade.py`. The browser check covers measured custom openings, arbitrary rotation, validation, four core thicknesses, facade returns/extensions, 3D selection, CSV/JSON/PNG, separate saves, homepage/standalone briefs, mobile pinch and WebGL fallback. `GREENSHIFT_TEST_URL` can target a production-style `/GreenShift-/` build.

## Form and style simulation — studio 4

The facade studio now changes the actual building envelope, with six form presets: architectural box, sweeping curve, organic wave, folded planes, asymmetric wing and pitched pavilion. Projection, eaves height, roof shape/rise and extension remain independently editable. The camera toolbar includes a quick form selector. Roof slabs, side returns, facade panels, glazing and frames follow the selected profile. Click a window or its frame to edit that opening's developed position, sill, width and height. A retained-shell outline supports comparison; the retained view is a rectangular concept baseline, not a measured site scan.

Both studios share six complete design specifications: Contemporary, Japandi, Tropical Modern, Industrial, Mediterranean and Urban Colour. These coordinate materials, palette, lighting and details. Interior variants also change furnishings, feature-wall treatments and ceiling/pendant assemblies while preserving measured layout and EPS quantities. Facade finishes can still be customised independently. Styles, form parameters and individual opening edits persist in saved/exported plans. Old plans receive defaults for new fields.

A six-stage sequence previews Survey, Prepare, Envelope, Services, Finish and Handover. Interior preparation shows indicative studs and opening headers; services show indicative routes; finishes precede furnishing. Facade preparation shows support rails, followed by the EPS envelope, service/support studies and finish layers. These are visual concept stages, not a site programme or an approved structural/MEP assembly. Walkthrough returns to the furnished proposal so hidden objects do not produce invisible collisions.

Facade EPS quantities are computed from closed, normal-offset solids with actual opening cutouts and profiled roof heights. Curves use a 96-segment base profile with additional feature/opening splits. End trims and solid side returns meet at vertical butt joints without volume overlap. The exposed rendering boundary has the same volume as the closed calculation mesh; hidden internal faces are removed to avoid striping. Tight profiles that fold an EPS offset back through itself are rejected. This is exact for the segmented model, subject to numeric/display rounding, and approximates a continuous fabricated curve.

Build schedules export developed facade length, front finish and opening areas, roof surface, added concept footprint, canopy allowance, shading fin count and EPS supply. Interior schedules cover floor finish, visible retained walls, both faces of placed EPS partitions, ceiling raft and furniture count. Roofs, finish layers, fixings and structure remain excluded from EPS core quantities. Final fabrication, structure, weathering details, service design and procurement still require project detailing.

Validation: `node tests/facade-forms.mjs` independently integrates profile cross-sections and verifies 24 form/thickness combinations, render-boundary/solid volume equality, opening-volume subtraction, roof areas and invalid profiles. `python scripts/verify-studio-forms.py` exercises actual desktop/mobile WebGL form/style/opening edits, build stages, schedules, save/restore and website handoff. `scripts/capture-studio-variants.py` captures the actual procedural forms and coordinated styles used in the menus. All uploaded films and Inter remain unchanged.

### Consolidated studio journey (October 2026)

The homepage has eight primary sections: hero, GreenShift introduction, services, Fjäll projects, one studio hub, working together, Space brief and inquiry. New-development approaches live beside services in an optional disclosure. The studio has keyboard-accessible Presentation / Refurbishment / Facade modes; refurbishment films and materials open on demand. Existing studio and material fragment links reveal the relevant mode and disclosure.

The refurbishment planner now offers architectural elements only: measured EPS partitions, glazed screens, feature panels, portals and ceiling rafts. Furnishing objects in imported legacy plans are excluded from this architectural planner. Version 3 uses a separate local save key, leaving the previous version 2 save intact. Finishes and architectural elements are excluded from EPS core quantities. Final light fixtures appear in the handover stage after the finish stage.

`assets/hero-architecture.mp4` uses the original five-second hero footage with the lower 7% cropped because the small Chinese text was present throughout. The original source is retained. Both the hero and cinematic introduction use the cropped clip and its matching poster.

Additional functional check (with a production server at the Pages path):

```sh
GREENSHIFT_TEST_URL=http://localhost:4175/GreenShift-/ python scripts/verify-consolidated-studio.py
```

This exercises the shortened page, keyboard modes, fragment links, materials-to-inquiry, real WebGL studios, EPS invariance, architecture-only plans, import/export, bilingual labels and mobile overflow. It does not send an external message.

### Restored opening, deployment and HD cover

The cinematic video countdown now opens on every page load, with Skip/Escape and the existing timeout and reduced-motion support. Deployment scale is again a visible standalone section after services, including four approaches, filters and detail dialogs. The Space brief no longer offers photo upload, reference images or photo output in its PDF. Legacy stored photos are cleared when opening the brief. The asset repurposing cover is a new 2560 × 1387 WebP capture (approximately 110 KB) of the actual architecture-only WebGL studio, without the old interface screenshot.
