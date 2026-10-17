# Design QA — greenshift.id adaptation

final result: passed

## Targets and evidence

Reference: https://www.greenshift.id/ . Source DOM, responsive styles and every section were captured at desktop 1440×1000 and mobile 390×844; all four tier-dialog states and mobile navigation were captured. Individual source captures are retained locally under reference/ (ignored by Git). Combined source/implementation evidence is committed in verification/compare-*.png.

Implementation: static homepage served under /GreenShift-/. Screenshots: verification/adopted-desktop-*.png and verification/adopted-mobile-*.png. Viewports and pixels are 1440×1000 and 390×844, deviceScaleFactor 1. Combined images concatenate equal-size source and implementation screenshots, with source on the left. No density resampling was used. Source videos were active and implementation comparison captures used reduced motion/posters; frame differences are expected because the files are moving media.

Source HTTPS resources were fetched through the configured proxy using Python's verified TLS trust and supplied unchanged to Chromium. Chromium's proxy CA error was not bypassed. The blocked Google Fonts CSS was replaced during capture with equivalent locally supplied Inter faces from the official Fontsource package; the implementation uses those same faces.

## Comparison findings and corrections

- [P1, fixed] The Google Fonts import contains semicolons in its URL. Initial removal truncated the import, leaving invalid CSS and breaking the source reset/typography. Removed the complete residual import, embedded valid local font declarations, reran browser checks and recaptured all implementation states. Post-fix comparisons show the source typography and section geometry restored.
- [P1, fixed] A poster was derived before its source path was rewritten, leaving /videos/design-studio-poster.jpg. Rewrote posters from final local video paths. Subsequent browser checks found no missing asset responses.
- [P2, fixed] The supplied studio logo's raster canvas proportions made it smaller than the source logo. Set its display to the source's 190×32 size with the proper crop. Recaptured and compared verification/compare-desktop-studio.png after correction.

## Required fidelity surfaces

- Typography: original Inter family and 300–700 weights are locally hosted. Captured inline sizes, line heights, tracking and heading/body hierarchy are retained. Desktop ecosystem/studio and mobile hero/tier comparisons show matched line wrapping and layout.
- Spacing/layout: source DOM inline styles and responsive grids are adopted. Hero placement, section padding, ecosystem tracks, studio split, card proportions and tier-modal details align in comparison evidence. No overflow was found at 1440 or 390px.
- Colors/tokens: source green/black/white surfaces, video overlays, subdued text and transparent/scrolled header states are retained.
- Images/assets: original hero, studio and all four tier videos are local, with extracted static posters. The user's house-shaped GreenShift logo intentionally replaces the reference's square symbol. Prepared Fjäll Group artwork is retained for the requested intro. The hamburger uses the included Phosphor library; the original close icon was copied with the source modal markup.
- Copy/content: original rendered copy and tier specifications are retained. Helper text explains the existing explicit WhatsApp review flow; no source backend submission is claimed.

## Deliberate adaptations

The user-supplied logos and requested 540-to-45 countdown remain. Native accessible dialogs replace the source custom overlay but retain its layout and detail copy; an inquiry action adds a direct conversion path. A hero playback control, focus outlines, reduced-motion behavior, Skip/Escape, and fail-safe static HTML are retained. Contact inquiries are reviewed and handed off to WhatsApp because this remains a frontend-only GitHub Pages website. These are intentional implementation constraints, not source drift.

## Functional verification

Chromium tests passed at desktop and mobile for all seven sections; four tier dialogs and selected-tier handoff; required/email fields; reviewed inquiry link and stale-link invalidation; full-screen mobile navigation; and native dialog dismissal. There were no JavaScript errors, missing local asset responses or horizontal overflow. JavaScript-disabled and blocked-asset tests confirmed the static homepage remains visible. Normal-motion intro test reached exactly 45, showed the Fjäll reveal, dismissed and restored main-page interaction.

## Remaining scope

Source Privacy and Terms controls have no substantive policy destination and retain the source behavior. Contact delivery is a WhatsApp handoff, not an integration with the original site's backend. Exact original logo artwork can replace prepared raster assets. Video-frame differences in comparisons are expected. Live deployment is checked separately after push; local visual QA passing does not itself establish publication.

## Experience Studio update

The opening reveal now has a transparent surface, legible logos over the video, and no white panel. Fjäll artwork replaces the studio hierarchy's text heading. Existing homepage copy remains intact; an Experience Studio section extends VR Spatial Planning with two actual project previews and a conceive → experience → refine sequence.

The Drop Pod preview was captured after entering the supplied cinematic walkthrough. Its launcher embeds the original experience. The Garuda Spark preview and presentation retain the supplied architectural scene and controls; Three.js 0.160.0, compiled Tailwind utilities, and Inter are hosted locally so that the WebGL presentation does not depend on third-party CDNs. Both cards also link to the original full experiences. Frames are created only after a visitor launches a project and removed on close.

Chromium verified desktop (1440px) and mobile (390px) layouts, image loading, no horizontal overflow, actual WebGL initialization and Next Insight transitions, both launchers, frame cleanup, focus return, intro transparency and automatic dismissal. No homepage JavaScript errors occurred. Repository-path hosting and no-JavaScript links were checked separately. Screenshots: verification/experience-desktop.png, experience-mobile.png, experience-webgl-desktop.png, experience-webgl-mobile.png, and experience-intro.png.

## Refurbishment Studio and deployment update

Added a dedicated refurbishment journey at #refurbish: the existing adaptive-reuse film, three selectable brief focuses (layout, materials, next use), a real spatial-study launcher, preparation steps, and a Retrofit inquiry action. The selected focus fills only an empty message, preserving customer notes and invalidating any stale inquiry review. Tabs support arrow keys, Home/End, selection state and labelled panels; all service content remains available without JavaScript.

Deployment cards now lead with customer goals while retaining the original descriptions, categories, and detail dialogs. Filters distinguish new builds from existing spaces; a direct refurbishment route connects the two sections. Refurbishment is linked from desktop/mobile navigation, with the compact menu available through 1200px.

Chromium passed desktop/mobile tab selection and keyboard navigation, all three filters, four tier dialogs and inquiry handoffs, preservation of existing messages, stale inquiry review invalidation, and WebGL initialization from the refurbishment section. Navigation was checked at 390, 768, 1024, 1200 and 1440px. No horizontal overflow, missing local assets or homepage JavaScript errors were observed. Static refurbishment content and contact links remained available without JavaScript. Screenshots are verification/refurbish-*.png and verification/tiers-*.png.

The refurbishment film is labelled as a studio concept; the page does not present it as a measured before/after case study. Service ranges and technical descriptions come from the existing Retrofit offering. Newly added copy describes the customer journey and avoids invented prices or site-specific schedules.

## Fjäll materials and project-film alignment

Replaced the refurbishment concept film with an interior-focused excerpt of Fjäll's Garuda Spark Innovation Hub retrofit at Malang Creative Center. The full 51-second film opens in a native dialog with playback controls. Actual project imagery is used for reduced-motion fallback; closing pauses the film and restores focus. The source is the user-supplied Fjäll website, not an invented before/after project.

Added the material library inside the refurbishment studio: GX-100, BEMMELS braided basalt composites, RoR roofing and materials at scale. Each has three study views, documented material descriptions, preparation notes and a specification inquiry action. Media and descriptions follow Fjäll's own material studio, with illustrative imagery labelled accordingly. Specification actions preserve existing notes, avoid duplicate additions and invalidate a stale inquiry review. Updated GreenShift's studio positioning to design and development, with development concepts and refurbishment as its focus.

The WebGL prototype's previous steel-skin EPS claim conflicted with Fjäll's current GX-100 description. Its material scene and explanatory text now use a nine-layer mirrored build-up: finish, Kalci board, fibreglass, PU glue, EPS, and mirrored faces. Undocumented thermal/acoustic/tolerance values were removed from that local prototype; the source project remains linked separately.

Chromium passed all 12 material views on desktop and mobile, image decoding, no horizontal overflow, project film metadata/playback readiness, Escape dismissal, pause and focus return, specification handoff, preservation and deduplication of customer notes, and the static initial library without JavaScript. No missing local resources or homepage JavaScript errors occurred. The nine-layer WebGL scene and material-slide navigation were also checked. Screenshots are verification/materials-*.png. Source provenance is in assets/fjall-source-media.json.

## GreenShift Asset Repurposing Studio — replacement

Final result: passed.

Replaced the refurbishment section from scratch with an original GreenShift journey: choose a repurposing direction, understand the existing asset, explore an interior renovation palette, assemble a brief, and discuss the project. The previous GSIH film and copied Fjäll catalog are removed from this section and their unused media files removed from the build. GreenShift's relationship to Fjäll remains a short positioning statement.

Eight original AI-assisted images share warm mineral, oak, reeded glass and sage-green art direction. The new 24-second animated concept film uses original existing-shell, material, partition and reimagined-interior studies. It is clearly identified as conceptual imagery; no finished-project or measured before/after claim is made. The new library covers finishing panels, partitions, wall finishes, flooring, joinery and lighting with project-oriented usage and detailing notes.

Visual inspection at 1440×1000 and 390×844 confirmed the film, three-column desktop/single-column mobile library, direction controls and brief summary fit without horizontal overflow. Image crops retain their material focal points, type hierarchy is consistent with the existing GreenShift site, and all images resolve. Screenshots: verification/asset-refurbish-*.png, asset-asset-direction-*.png, asset-material-library-*.png and asset-asset-brief-*.png.

Chromium passed all three direction states, four filters, six detail dialogs, save/remove selections, updated inquiry brief with preserved customer notes, duplicate-brief prevention, full film metadata/playback readiness, Escape dismissal and focus return, and deployment-to-Retrofit details. No homepage JavaScript errors or missing local assets occurred. Static studio content and the contact route remained available without JavaScript.

## Smooth refurbishment transformation film

Final result: passed.

Replaced the stepped four-shot zoom montage with a 24-second, 60fps move directly from the existing space into the renovation concept. A shared cosine-eased trajectory uses fractional perspective coordinates and cubic sampling, avoiding integer crop rounding. The four-second dissolve at 00:10–00:14 replaces hard cuts and intermediate sample shots. The background holds the final renovated interior and offers explicit replay rather than snapping back on a loop. A new media filename prevents cached copies of the old film from being reused.

FFprobe confirmed 1280×720, 60fps, 1,440 frames and 24 seconds. FFmpeg scene detection found no transitions above a 0.1 scene-change threshold. The encoded final frame was inspected directly. Chromium verified desktop/mobile manual play and pause, persistence of pause across scrolling, final-frame hold, replay, full-view duration and timeline, dismissal and focus return. Screenshots at the start, dissolve and end are verification/smooth-film-*.png. The render is reproducible with scripts/render-asset-film.py. The film remains labelled as a concept study using the existing original imagery.

## Refurbishment studio redesign — v9

Passed desktop (1440px) and mobile (390px) browser checks. The section now leads with the transformation film and chapter navigation, then direction selection, an interactive existing-space/renovation concept comparison, and a material workspace with a sticky desktop brief. The existing service copy, original renovation imagery and smooth 60fps film remain. On mobile the brief follows the palette.

Verified comparison slider input and arrow keys, direction changes, material filtering, detail-dialog selection, checkbox synchronization, transfer of direction and finishes into the inquiry, deduplication of repeated transfers, film dialog, zero horizontal overflow and zero JavaScript errors. Screenshots are saved as `verification/refurbishment-v9-*.png`. Concept imagery remains labelled. Build and JavaScript syntax checks passed.

## Website flow — studio-v10

Passed desktop and mobile Chromium checks: section order, all three project routes, responsive navigation open/close, comparison input, material-to-inquiry handoff, film dialog and absence of runtime errors or horizontal overflow. Inspected the project-route screenshot. All seven local MP4 files match their pre-change SHA-256 hashes. Existing videos, project dialogs, embedded spatial experience and service copy remain; hero CTAs now lead to services and studio. Delivery copy follows development approaches and is labelled as the new-development delivery system. Build, JavaScript syntax and whitespace checks passed.

## Unified working studio — v11

The explanation of GreenShift now follows the hero. Removed the separate project-route, studio introduction, experience-studio, and refurbishment section wrappers. One studio contains three accessible panels: walkthrough/WebGL, renovation exploration, and material palette. One brief persists across all panels. Redundant studio process lists, repeated introductions and separate contact prompts were removed.

Desktop and mobile Chromium checks passed: explanation order; one studio and one brief; tab arrows and panel visibility; direction selection; reveal slider; film modal; material filtering/detail selection; selections surviving panel changes; WebGL iframe opening and cleanup; inquiry handoff; previous refurbishment deep links; mobile navigation; no horizontal overflow or JavaScript errors. All seven MP4 files match their original hashes. Build, JavaScript syntax and whitespace checks passed. Screenshots: `verification/unified-studio-*.png`.

## Studio image sizing repair

Removed the obsolete `#studio img:not(.studio-fjall-logo)` rule that forced all studio images to 190 × 32 pixels. Project previews, both renovation comparison layers and six material images now use their component dimensions. Also separated brief labels from edit controls after visual review.

Verified that all visible studio images decode and fill their containers on desktop and mobile. Comparison input and material dialog still work, with no horizontal overflow or JavaScript errors. Inspected renovation and mobile palette screenshots; evidence: `verification/studio-images-*.png`. All source JPGs decoded successfully; no video assets changed. Build and whitespace checks passed.

## Client presentation studio — v12

Moved the exact delivery-system section from the supplied screenshot directly below the hero, without rewriting its copy. Rebuilt the studio’s opening experience as a three-slide client presentation: studio film, Drop Pod Villas walkthrough and Garuda Spark spatial model. Walkthrough/WebGL launch in the existing dialog and offer full-presentation links. Shared renovation direction and material brief continue through the session.

Replaced all studio stills with fresh concept renovation and material imagery or actual presentation screenshots; refreshed video poster frames. Branding stays original. Seven video hashes match the previous version. Desktop/mobile checks passed: hero/explanation order, slide visibility, both presentation dialogs, comparison input, material atlas/detail tile selection, saved finishes and direction reaching inquiry, decoded images, zero horizontal overflow and runtime errors. Screenshots: verification/client-studio-*.png. Concept visuals and image origins are recorded in assets/studio-client-provenance.json. Build and JavaScript syntax checks passed.

## Whole-site studio redesign — v13

Rebuilt the stylesheet and removed captured inline layouts across the entire page. One visual system uses warm paper, forest green, generous spacing, large sans-serif headings and restrained serif emphasis. Hero now leads with the original studio phrase “Where vision becomes structure.” The requested delivery explanation stays directly under it. A full-width client presentation replaces the dashboard, followed by an open refurbishment journey and one brief at its end. Development, ecosystem, timeline and contact now use the same layout system; supporting technical copy is expandable.

Desktop and mobile Chromium checks passed for section order, absence of dashboard tabs, one brief, navigation, both presentation dialogs and iframe cleanup, renovation comparison, material selection/details, brief handoff, development filtering, tier details and inquiry review. No horizontal overflow or runtime errors. Inspected hero, full-width presentation and mobile contact screenshots, then corrected logo framing and replaced new arrow glyphs with inline SVG. Build, syntax and whitespace checks passed. All seven MP4 hashes are unchanged. Verification: verification/reset-site-*.png.

## Inter and presentation cover fix

Removed Georgia and serif styling from emphasized headings; they now inherit Inter with normal styling. Presentation previews previously kept their HTML height of 900px even when their width shrank. Their container now reserves a 16:10 frame, with the image positioned inside at 100% width and height using object-fit: cover. Original screenshots retain their natural proportions.

Chromium checks passed at desktop, tablet and mobile widths: Inter font loaded, Inter heading family, proportional preview frames, decoded images filling each frame, and no horizontal overflow or runtime errors. Inspected mobile walkthrough screenshot. Build and whitespace checks passed. Evidence: verification/inter-cover-*.png.

## Distinct material image repair

The full-site cleanup removed inline crop selections, causing all six cards to show the atlas’s first image. Category-specific stylesheet rules now select the six views using stable material keys; filtering cannot change their mapping.

Desktop/mobile verification passed: six different rendered-image screenshot hashes, the correct view in every detail dialog, and the partition image after filtering. Inspected the full desktop palette. Build and whitespace checks passed. Evidence: verification/distinct-materials-*.png.

## User-uploaded refurbishment film

Replaced the refurbishment background and full-view sources with the uploaded 1080p, 24fps, 5.04-second MP4. Original H.264 video and AAC audio were preserved via stream copy; fast-start metadata enables progressive playback. Extracted a fresh poster and updated the duration label and provenance.

Desktop/mobile Chromium checks passed for the new source/poster, loaded duration, reduced-motion pause, manual play/pause, final-frame hold, explicit replay, full-view playback and focus return on close. No runtime errors. Build and whitespace checks passed. Evidence: verification/uploaded-refurbishment-*.png.

## Uploaded considered-transformation timelapse

Replaced the considered-transformation image reveal slider with the uploaded 1080p, 24fps, 5.04-second video and a poster from that upload. H.264 video and AAC audio are preserved by stream copy, with MP4 fast-start enabled. Native controls support user-initiated playback, audio and fullscreen. This video is excluded from the background-video observer so playback and pause remain under user control. Removed the old slider handler without affecting material selection.

Desktop/mobile Chromium checks passed: removed slider, correct video source and duration, 16:9 framing, native click-to-play, pause surviving scrolling, final-frame hold, replay, and material selection/inquiry handoff. No runtime errors or overflow. The previous refurbishment film remains unchanged. Build, syntax and whitespace checks passed. Evidence: verification/transformation-timelapse-*.png.

## Gamified WebGL renovation studio

Built a locally hosted Three.js room planner and a launch section on the homepage. The interactive room supports presets, 3–12 m dimensions, eight furniture/partition types, snapped drag placement, numerical positioning, rotation, boundary/overlap/entrance checks, floor and wall finishes, top/3D views, orbit/zoom, and a collision-aware walkthrough with keyboard/touch controls. Five design goals award XP; a 180-credit game allowance limits placement. Credits are explicitly not a price quote. Undo, browser autosave and validated JSON import/export preserve work. One-time or iframe brief transfer adds room information and placements to the inquiry without overwriting notes or duplicating the simulation block.

Chromium with software WebGL rendered the actual scene. Desktop tests passed for pointer placing/dragging, invalid overlap/boundary rejection, rotation, finishes, undo, local save/reload, export/import and invalid-file rejection, credit limits, all quests and walk-camera movement. Website tests passed for real modal loading, same-origin handoff, note preservation, focus restoration and deduplication; standalone return passed. Mobile tests passed for touch catalog/placement, precise positioning, rotation, walking controls and no horizontal overflow. A browser with WebGL disabled showed the fallback and retained export availability. Inspected desktop/mobile captures; adjusted responsive camera framing and keyboard focus for walkthrough. Screenshots: verification/renovation-planner-*.png. Repeatable checks: scripts/verify-renovation-studio.py. All existing video assets remain unchanged.

## Asset repurposing and EPS quantities — v2

Upgraded the planner with adjustable EPS partitions, four core thicknesses (10/12/15/20 cm), actual door/window cutouts, retained rear/left lining, measured height/opening inputs, mixed-thickness takeoff, explicit corner deductions and separate supply allowance. Added takeoff CSV, quantities in inquiry summaries, v2 plan persistence with original-save preservation, and a fixed mobile quantity summary. The core estimator is isolated in assets/asset-studio-model.js and tested against independently calculated numerical examples.

Advanced interaction checks passed for axis-constrained dragging, duplicate/redo, focus, phase comparison, native screenshot capture, mobile pinch zoom, collision through a door and blocking by solid EPS. Rendering now includes beveled geometry, procedural PBR materials, environment lighting, contact shadows, lighting moods, quality modes and cached static shadows. Software rendering selects Performance; Studio remains selectable. This is browser WebGL rather than an Unreal runtime. Existing videos and Inter fonts remain.

Passed node tests/eps-takeoff.mjs and actual desktop/mobile WebGL workflow checks in scripts/verify-asset-studio.py, including CSV totals, quantities across four thicknesses/openings, saved plans, legacy import and inquiry handoff. Original planner regression passed, including export/import, collision, credit limit, quests, modal/standalone handoff and unavailable-WebGL fallback. Separate interaction tests passed axis move/orbit/pinch and walkthrough tests passed doors/solid walls. Verified automatic v1 local-save migration preserves original JSON and writes a separate v2 save. Inspected updated overview and mobile captures. Build, JS syntax and whitespace checks passed.

Final production-path smoke check passed under `/GreenShift-/`: local EPS module loading, WebGL launch, 15 cm scope/partition placement and EPS quantities in the inquiry. A deliberately blocked EPS module showed the load fallback without changing a sentinel save. Starter furniture now leaves clearance for all four lining thicknesses; verified every choice against the independent lining formula. Walkthrough movement uses bounded collision substeps so low frame rates cannot jump through thin EPS walls. Cached static shadows and lower software-renderer resolution keep interaction usable while detailed rendering remains selectable.

## Measured EPS and facade facelift — studio 3

Simplified the quantity path with a measured-wall form and visible per-surface equations. New plans include no EPS until the user adds a partition or checks lining; saved scope remains intact. Added custom opening dimensions, precise-angle/15°/90° EPS rotation, oriented collisions and illustrated 3D asset selection. Volumes and supply allowance display separately with up to six decimals. The interior estimator remains the shared source for geometry and downloads.

Added a separate facade service and WebGL studio, with independently saved building measurements, facade directions, openings, shading, arrival details, optional concept extensions and selected exterior EPS surfaces. Before/proposed/core views, front/street cameras, direct mesh selection, touch pinch, quests and exports support client presentations. Its estimator supplies both mesh cutouts and the schedule, including solid side returns and non-overlapping exterior butt joints. Structural changes remain clearly labelled concept proposals, rather than validated engineering.

Repeatable checks: tests/eps-takeoff.mjs, tests/facade-takeoff.mjs and scripts/verify-studio-upgrade.py. Verification captures: verification/studio3-*.png. All new asset cards are actual locally rendered WebGL captures. Existing user video files and locally hosted Inter remain unchanged.

Final production-path run passed under `/GreenShift-/`, including the measured-opening/rotation workflow, facade dimensions/returns/extension, finish and phase views, direct surface selection, CSV/JSON/PNG, save/restore, independent studio selection, both inquiry handoffs, mobile editing/pinch and unavailable-WebGL quantity tools. A blocked facade-model request displayed the load fallback without replacing a sentinel save. Reference quantities: custom 3.17 × 2.71 m partition at 15 cm, less 1.01 × 2.13 m door and 1.23 × 1.11 m window, gives 0.761115 m³. Default front facade at 12 cm gives 4.4616 m³, or 4.68468 m³ with 5% extra supply. The existing v2 EPS workflow and axis-drag/door collision regressions also passed. Mobile facade includes an explicit Recenter button.

## Form-based simulation and coordinated styles — studio 4

Replaced the flat-only proposed facade with a profile-based envelope: six forms, three roof silhouettes, projection and eaves/rise controls, conforming openings, roof slabs, returns and facade details. Added direct 3D opening/frame selection and measured per-opening edits. Complete style specifications coordinate six facade and interior looks, including interior feature geometry, furnishing palette/proportions and ceiling fixtures. Both studios expose a six-stage build sequence and downloadable fit-out/build schedules.

The quantity model and renderer share closed normal-offset panel geometry, including opening deductions and roof height. Curved quantities describe the segmented model rather than an exact analytic continuous curve. Independently verified cross-section integration, hole subtraction, render-boundary volume, roof area and 24 form/core combinations. Removed internal render faces that caused visible striping; the boundary is closed and has the same volume as the quantity mesh. Retained-shell comparison and structural/MEP/fabrication assumptions remain explicit. Existing movies, Inter and the inquiry review flow are preserved.

Final production-path desktop/mobile workflow passed for all six forms and four EPS cores, all six styles in both studios, individual curved-window/frame selection and measured edits, invalid-edit rejection, all build stages, schedule/JSON downloads, persistence, undo/redo, walkthrough and website handoff. The existing EPS regression also passed: four thicknesses, custom cutouts, mixed cores, retained lining/corners/allowance, save/import/export and desktop/mobile inquiry flow. Build views cut away the ceiling raft; walkthrough restores overhead assemblies. Screenshots: verification/studio4-*.png. All new form/style menu images are captures of the actual WebGL models.

## Cinematic countdown opening

Reworked the existing muted hero film into a 7.6-second opening: a 540-day hold, accelerated 540→45 countdown, a deliberate 45-day landing and a transparent GreenShift / Fjäll logo reveal. Inter remains in use. Widescreen framing, a slow film push, subtle grain, a circular guide and a synchronized timeline establish the visual sequence without flashing or requesting audio playback. The timeline describes the brand story, not asset download progress. Existing studio and refurbishment films are unchanged.

The intro has an independent 8.5-second upper bound, Skip/Escape, trapped keyboard focus with focus restored into the page, hidden-tab dismissal and a short static reduced-motion reveal. A failed video uses its poster and does not stop the timer; the HTML homepage remains accessible without JavaScript. `scripts/verify-cinematic-intro.py` exercises actual video playback, countdown/landing/reveal/exit at desktop, portrait and landscape sizes, plus skip, keyboard, reduced-motion, blocked-video, stalled-animation, hidden-tab and no-script exits on the `/GreenShift-/` production path. Screenshots: `verification/cinematic-*.png`.

## Representative client Studio Film

Replaced the five-second hologram presentation in the client Studio Film slide with an original 18-second film rendered from the actual local GreenShift interior and facade studio geometry. Five moving-camera chapters show a retained shell, a measured EPS partition/door, coordinated Japandi finishes/furniture/lighting, a curved EPS facade and the completed tropical facade. Eased camera paths and half-second dissolves keep movement smooth. Captions identify this as an illustrative concept study. The user-uploaded refurbishment/timelapse and cinematic preloader footage are unchanged.

The new H.264 1280×720 / 24 fps film is optimized for progressive playback, silent and about 1.5 MB. A dedicated frame/poster and `16:9; object-fit:contain` preserve the complete composition and captions at every breakpoint. Native controls, the existing presentation tabs and reduced-motion manual playback remain available. `scripts/render-studio-film.py` captures the actual model into temporary frames using capture-only instrumentation, then assembles the film with FFmpeg; no production model hooks are added. `scripts/verify-studio-film.py` checks metadata, actual playback, seeks in every chapter, desktop/mobile composition and slide-change pause. Its media route reproduces GitHub Pages byte-range support, which the minimal development server lacks. Asset provenance records the source and scope.

## Client journey and Start with your space

Preserved the existing Inter identity, cinematic opening, uploaded refurbishment/timelapse films, new process film, material library, client presentations and full interior/facade studios. The hero now leads to a personal Space brief. GreenShift’s identity follows the hero, followed by three distinct service routes and the guided brief. The modular housing delivery explanation, ecosystem and timeline remain in the development context, with eligibility and individual refurbishment/facade scheduling made explicit. The opening is shown once per browser session, with `?replayIntro=1` available for replay.

The Space brief has four stages: project/optional photo, measurements/timing, coordinated style/priorities, and a personal summary. It uses a shared bounded schema, downscales optional JPG/PNG/WebP images locally, saves locally, retains exact original brief measurements and renders a measured 2D footprint/elevation. Clean WebP style references come from the real studios without baked-in sample dimensions. The reference does not claim to remodel the client photo. Users can download JSON, copy a Unicode-safe shared link without a photo, open a print-ready PDF view, request a review or launch a measured advanced studio concept. Model bounds/half-metre interior increments are explained before launch; an explicit, undoable Apply action protects prior studio plans. A same-origin parent handoff supports blocked local storage. No photos are uploaded or included in shared links or WhatsApp text.

Added project-fit and deliverable explanations, review/fee/programme FAQs, a direct WhatsApp link and accurately named “Review WhatsApp inquiry” action. The inquiry carries selected service, city, area, timing and brief. Existing presentation studies are labelled honestly; no completed-project claims, testimonials, prices, response-time commitments or appointment availability are invented. First-party journey events expose event/service/source only, ready for a future analytics integration; no analytics service is connected.

Mobile changes include usable service cards, four-stage controls, 16px inputs, touch-size actions, responsive previews, a context-aware bottom action, and a full-height studio dialog with sticky close controls. Main workflows verified at desktop and 390px; edge layouts checked at 320px and landscape 844px. Validation covered invalid/corrupt photos, invalid measurements/shared links, Unicode round-trip, escaping in the printable brief, local-save restrictions, photo exclusions, large-project model limits, reset, inquiry continuity and keyboard focus on dialog close. New semantic/bounded-schema checks are in `tests/space-brief.mjs`; browser checks are in `scripts/verify-space-journey.py` and `scripts/verify-space-edge-cases.py`. Captures: `verification/space-*.png`.

Regression checks passed for all six facade forms/four EPS cores, all coordinated styles in both studios, editable openings, six build phases, measured quantities, downloads, undo/redo, persistence, walkthroughs, mobile edits and the existing website handoff. The independent EPS/facade takeoff/form-volume suites remain unchanged and passed. Production-path checks use `/GreenShift-/`; final media integrity checks confirm existing film bytes are unchanged by this work.


## Indonesia positioning and bilingual client journey

Updated the opening around design and development in Indonesia while retaining Inter, the cinematic films, measured Space brief and advanced studios. Added local/overseas client paths with keyboard tab navigation, a practical site-to-design roadmap, scope/IDR/communication explanations and a dedicated Fjäll Group portfolio link at the exact user-supplied URL. No project results, people, certifications, fees or response guarantees were invented. The portfolio remains on Fjäll Group; GreenShift’s existing examples are presentation studies.

Added reversible, device-persistent Bahasa Indonesia and English, with browser/query preference and explicit header/studio controls. A local dictionary covers the main site, generated brief/status text, material descriptions and studio controls/guidance. Option values remain canonical; user text is excluded. Shared briefs carry language and planning origin. PDF and WhatsApp output are localized; preferred conversation language and client-supplied investment range remain explicit. Studio launch URLs include the selected language; switching languages does not mutate geometry, EPS quantities or the saved plan. A ResizeObserver fits desktop studio content below translated controls and the optional brief banner. The original process film is unchanged; a local Indonesian caption track accompanies it.

Checks cover ID/EN on 320px, 390px and 844px landscape, local/remote keyboard tabs, return visits, language switching with an existing draft, decimal measurements, untouched user notes, printable brief, share language, canonical IDR selections, WhatsApp preview, both studio languages, saved preference and model invariance. Language data/runtime failures leave the English site, Space brief and contact usable. Captures: verification/indonesia-*.png. Scripts: verify-indonesia-journey.py and verify-language-fallback.py. These are functional and responsive checks, not a claim of full accessibility compliance or measured conversion improvement.
