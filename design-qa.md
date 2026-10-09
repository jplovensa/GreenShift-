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
