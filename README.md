# GreenShift studio — three design directions

Three responsive frontend prototypes based on the approved design concepts:

1. `cinematic.html` — Cinematic Studio: immersive architecture video and warm ivory sections.
2. `editorial.html` — Editorial Architecture: paper, serif headlines and framed imagery.
3. `atelier.html` — Digital Atelier: sage surfaces, bold typography and a split hero.

`index.html` defaults to the cinematic direction. The bottom version selector links between all three. Each includes the complete shared studio, tiers, philosophy, ecosystem, delivery protocol and inquiry experience.

## Develop

Use the existing checkout; no worktree is necessary. Node.js 20.19+ or 22.12+ is required by Vite (validated using Node.js 24).

```sh
cd /workspace/GreenShift-
npm ci
npm run dev -- --port 4173 --strictPort
```

## Build

```sh
npm run build
```

The `dist/` directory contains all three pages and required assets. Deploy its contents to a static host, or serve it using `python3 -m http.server 4173 --directory dist`. Use an HTTP server rather than opening the HTML as local files because the production app uses JavaScript modules.

## Content and assets

Copy was recovered from the publicly served greenshift.id JavaScript bundle. Original wording, architectural tier specifications, delivery protocol and contact details are retained. The studio headline is promoted to the hero. Existing wording that describes GreenShift as the development and capital arm of Fjäll Group remains intact to respect the instruction to keep the copy.

The supplied hero-studio.mp4 is used unchanged. Its frame provides a static poster and reduced-motion fallback. The supplied house-shaped logo was reproduced as a transparent raster web asset using ImageGen because the inline attachment was not available as a directly downloadable file. Replace public/assets/logo.png with the original production artwork for exact logo fidelity.

Architecture imagery is conceptual; no fabricated completed projects or client names were added.

## Interactions

- Responsive navigation and three-direction selector.
- Tier details in an accessible native dialog, with Escape dismissal and tier selection carried into the inquiry.
- Video pause/play and reduced-motion support.
- Expandable ecosystem information.
- Required inquiry fields, email validation and a message review step.
- The user explicitly opens WhatsApp to send to the existing public contact number. No automatic submission, backend connection or fake success state.
- Editing a reviewed inquiry removes its stale send link.

## Validation

Production build passed. All three variants passed 84 DOM assertions across navigation, tier details, inquiry review and video controls. HTTP requests confirmed each page, video, poster and logo returns successfully. These checks do not establish real-browser behavior, responsive rendering, font rendering, keyboard focus behavior or visual fidelity. Browser screenshot comparison and design QA remain blocked because browser tools are unavailable in this chat; the user authorized this local fallback. See design-qa.md.

This prototype has not been published. Production integration, privacy/terms content and delivery of inquiries beyond the WhatsApp handoff are outside this frontend prototype.
