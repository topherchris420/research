# Design System — Dynamic Location Theory

## Product Context
- **What this is:** Research paper landing page for Dynamic Location Theory, a frequency-based framework claiming location is an intrinsic property of the object
- **Who it's for:** Physicists, researchers, and technically curious readers evaluating a theoretical physics framework
- **Space/industry:** Theoretical physics, quantum mechanics, science communication
- **Project type:** Research paper / editorial landing page

## Aesthetic Direction
- **Direction:** Editorial/Manuscript
- **Decoration level:** Intentional — subtle grain texture on background, thin rule lines between sections (printed journal feel), no gratuitous ornamentation
- **Mood:** Opening a serious journal article that respects the web as a medium. Warm, grounded, intellectual. The design carries the weight of the claim without resorting to startup aesthetics.
- **Reference sites:** Quanta Magazine (editorial serif + generous whitespace), Distill.pub (clarity-first interactive layouts), Nature Physics (institutional credibility)

## Typography
- **Display/Hero:** Instrument Serif — high-contrast, sharp modern serif with real weight at display size. Communicates intellectual gravity without feeling dusty.
- **Body:** Source Serif 4 — excellent reading comfort for dense scientific prose, journal-paper legitimacy
- **UI/Labels:** Instrument Sans — clean geometric sans that pairs naturally with Instrument Serif
- **Data/Tables:** JetBrains Mono — clear monospace for citations, equation labels, and code blocks
- **Code:** JetBrains Mono
- **Loading:** Google Fonts CDN
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,500&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  ```
- **Scale:**
  - Hero: clamp(2.5rem, 5.5vw, 4.2rem) / line-height 0.98 / letter-spacing -0.03em
  - Section heading: clamp(1.7rem, 3vw, 2.4rem) / line-height 1.15
  - Card heading: 1.15rem
  - Body: 1.05rem / line-height 1.8
  - UI/Labels: 0.88rem / font-weight 500-600
  - Kickers: 0.72rem / letter-spacing 0.14em / uppercase
  - Mono: 0.85-0.92rem / line-height 1.7

## Color

### Dark Mode (default)
- **Approach:** Restrained — warm palette, color is rare and meaningful
- **Background:** `#0C0A07` — warm near-black, aged paper burned dark
- **Surface:** `#161310` — warm dark brown for panels
- **Primary text:** `#E6DFD0` — parchment white
- **Muted strong:** `#C4BAA8` — warm light stone
- **Muted:** `#9B8F7E` — warm stone
- **Accent:** `#C4993C` — amber/gold (oscilloscope phosphor, scientific instrument brass)
- **Accent strong:** `#D4A94C` — brighter amber for hover states
- **Accent soft:** `rgba(196, 153, 60, 0.12)` — amber glow for backgrounds
- **Borders:** `rgba(196, 153, 60, 0.15)` — warm amber tint
- **Semantic:** success `#4A8E50`, warning `#C4993C`, error `#C4443C`, info `#648CB4`

### Light Mode
- **Background:** `#F5F0E8` — warm cream
- **Surface:** `#FFFDF8` — near-white warm
- **Primary text:** `#1A1714` — warm near-black
- **Muted strong:** `#3D372E`
- **Muted:** `#6B6256`
- **Accent:** `#9A7420` — darkened amber for contrast on light
- **Accent strong:** `#7D5E18`
- **Strategy:** Swap surfaces, darken accent, reduce saturation slightly

## Spacing
- **Base unit:** 8px
- **Density:** Comfortable
- **Scale:** xs(4) sm(8) md(16) lg(24) xl(32) 2xl(48) 3xl(64)

## Layout
- **Approach:** Grid-disciplined with editorial rhythm
- **Max content width:** 1080px
- **Reading column max:** 720px (for abstract, equations, dense prose)
- **Hero grid:** asymmetric (1.4fr / 0.9fr)
- **Card grids:** 3 columns desktop, 1 column mobile
- **Border radius:** sm: 8px (inputs, alerts), md: 16px (panels, cards), pill: 999px (buttons, nav)

## Motion
- **Approach:** Minimal-functional
- **Easing:** ease for general transitions
- **Duration:** 150ms for hover states, 200ms for color transitions
- **Rules:** No entrance animations, no typewriter effects. This is a research paper. Hover lifts (translateY -1px to -2px) and border-color transitions only.

## Design Decisions & Rationale

### Key Departures
1. **Amber/gold accent instead of blue.** Every physics site defaults to blue. Amber says "scientific instrument, brass clockwork, precision" which maps to the resonance/frequency thesis. Distinctive warm palette nobody in this space uses.
2. **Full serif typography stack.** Instrument Serif + Source Serif 4 commits to the editorial identity. The site reads like a published paper, not a README. Authority and differentiation over "modern startup" feel.
3. **Greek symbols as card icons.** Using relevant Greek letters (omega, psi, xi) instead of generic Font Awesome icons. Ties the visual language to the mathematical content.

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-04 | Initial design system created | Created by /design-consultation based on product context + competitive research (Quanta, Distill, Nature) + independent Claude subagent voice |
| 2026-04-04 | Chose amber/gold over blue | Differentiation from generic physics sites, maps to resonance/frequency/instrument theme |
| 2026-04-04 | Chose Instrument Serif over Cormorant Garamond | Better legibility at display size on dark backgrounds, sharp modern serif vs thin classical |
| 2026-04-04 | Rejected typewriter animation | Credibility risk for a research paper site, motion should be minimal-functional |
