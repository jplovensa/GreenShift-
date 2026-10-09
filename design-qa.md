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
