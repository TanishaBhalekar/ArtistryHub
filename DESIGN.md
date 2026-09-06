# Artistry Hub Design System & Token Specification

> **Source:** Extracted from Stitch Project `Artistry Hub` (`projects/10718570643310189056`).
> **Dual Theme:** Studio Obsidian Noir (Dark Theme) & Gallery Editorial Terracotta (Light Theme).

---

## 1. Brand & Design Philosophy

Artistry Hub is a museum-grade digital art discovery platform and studio management workspace tailored for visual artists, concept creators, and collectors. The interface bridges the contemplative stillness of an international exhibition catalog with the tactile precision of a modern creator workstation.

- **Curatorial Restraint:** UI elements frame and elevate the artwork rather than compete with it.
- **Material Authenticity:** Surfaces evoke elemental art materials—raw terracotta pottery, burnished gold leaf, frosted vitrine glass, and deep charcoal calligraphy inks.
- **High-Density Utility:** Clean typographic tension between romantic editorial serifs for showcase headings and mathematical, geometric sans-serifs for financial data and workflow statuses.

---

## 2. Color Palette Tokens

### 2.1 Dark Theme — Studio Obsidian Noir

Evoking a private, late-night gallery or studio darkroom where fine artworks act as the primary light sources.

| Token Name | Hex / Value | Usage & Context |
| :--- | :--- | :--- |
| `--bg-base` | `#0E0F12` | Main viewport foundation and noir canvas |
| `--bg-surface-dim` | `#121316` | Recessed structural sections and backdrop floor |
| `--bg-surface-elevated` | `#16181F` / `#1A1D27` | Glassmorphic cards (75% opacity with 20px–40px blur) |
| `--bg-surface-bright` | `#292A2D` | Hover states, active dropdown selections, and input backgrounds |
| `--border-frosted` | `rgba(255, 255, 255, 0.08)` | 1px frosted vitrine border for cards, inputs, and modals |
| `--border-focus` | `rgba(229, 169, 60, 0.35)` | Active focus halo for interactive inputs |
| `--text-primary` | `#F8FAFC` / `#E3E2E6` | High-contrast editorial titles and primary labels |
| `--text-secondary` | `#94A3B8` / `#D4C4B0` | Artist handles, subtitles, dates, and helper text |
| `--primary-amber` | `#E5A93C` (`#FFC665`) | Primary CTA buttons, upload actions, and active highlights |
| `--secondary-violet` | `#8B5CF6` (`#D0BCFF`) | Category tags, AI exploration tools, and creative chips |
| `--tertiary-cyan` | `#06B6D4` (`#59E0FF`) | Technical metadata (pixel dimensions) and active stages |
| `--status-error` | `#EF4444` (`#FFB4AB`) | "Need Revision" alert badge, overdue task flags |
| `--status-warning` | `#F59E0B` (`#FFDEAD`) | "Awaiting Client Feedback" alert badge |
| `--status-success` | `#10B981` (`#4CD7F6`) | "Ready for Delivery", finalized payouts, Pillow compression tag |

---

### 2.2 Light Theme — Gallery Editorial & Terracotta

Evoking an international fine art catalog and natural gallery exhibition walls with earthen South Asian clay tones.

| Token Name | Hex / Value | Usage & Context |
| :--- | :--- | :--- |
| `--bg-base` | `#FAF9F6` / `#F9F8F5` | Warm gallery bone canvas foundation (reduces eye strain) |
| `--bg-surface` | `#FFFFFF` | Pure elevated white surface for artwork cards, modals, and drawers |
| `--bg-surface-container` | `#EFEEEB` / `#F4F3F0` | Recessed input containers, filter pill trays, and table rows |
| `--border-hairline` | `#E6E3DD` | 1px architectural divider separating spatial elements |
| `--border-hover` | `#D96B43` | 1px terracotta hover transition border on cards |
| `--text-primary` | `#1A1A1E` / `#1A1C1A` | Deep slate-charcoal ink for maximum editorial legibility |
| `--text-secondary` | `#56423C` / `#64748B` | Museum placard metadata, medium identifiers, and time stamps |
| `--primary-terracotta` | `#D96B43` (`#9D3E1A`) | Solid primary submit CTAs, active filter pills, and brand accent |
| `--secondary-gold` | `#C58B2E` (`#825500`) | Curated verification seals, live auction reserves, milestone markers |
| `--tertiary-slate` | `#5C5B60` | Architectural borders and neutral structural furniture |
| `--status-error` | `#BA1A1A` / `#EF4444` | Revision required pills and urgent deadlines |
| `--status-warning` | `#F59E0B` / `#FFBD5C` | Pending review indicators |
| `--status-success` | `#10B981` | Delivered commissions and verified Pillow optimization badges |

---

## 3. Typography Scale & Hierarchy

The typographic pairing balances high-contrast editorial serifs with geometric, high-clarity interface typography.

- **Editorial Headings:** `Playfair Display` (serif)
- **Interface & Data Readouts:** `Plus Jakarta Sans` (sans-serif)
- **Financial Numbers:** Strictly enforced `font-variant-numeric: tabular-nums` for all Indian Rupee (`₹ INR`) amounts.

| Token Name | Font Family | Size | Weight | Line Height | Tracking | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `display-lg` | Playfair Display | 64px (4rem) | 700 (Bold) | 72px | `-0.02em` | Exhibition monograph titles, hero banners |
| `headline-lg` | Playfair Display | 40px (2.5rem) | 600 (SemiBold) | 48px | `-0.015em` | Page titles, primary dashboard greetings |
| `headline-md` | Playfair Display | 28px (1.75rem) | 500 (Medium) | 36px | `0` | Section titles ("Today's Focus", "Masonry Gallery") |
| `title-lg` | Plus Jakarta Sans | 20px (1.25rem) | 600 (SemiBold) | 28px | `0` | Artwork titles on cards, modal titles |
| `body-lg` | Plus Jakarta Sans | 18px (1.125rem) | 400 (Regular) | 28px | `0.01em` | Curatorial introductions, artist bios |
| `body-md` | Plus Jakarta Sans | 16px (1rem) | 400 (Regular) | 24px | `0` | Standard UI body, form field inputs |
| `currency-inr` | Plus Jakarta Sans | 18px / 24px | 700 (Bold) | 24px | `0.02em` | `tabular-nums` tabular pricing (`₹ 28,000 INR`) |
| `label-md` | Plus Jakarta Sans | 14px (0.875rem) | 600 (SemiBold) | 20px | `0.05em` | Form labels, button text, table column headers |
| `label-sm` | Plus Jakarta Sans | 12px (0.75rem) | 500 (Medium) | 16px | `0.08em` | Status badges, category pills, dimension chips |

---

## 4. Layout, Grid & Spacing Tokens

### 4.1 Grid Architecture
- **Max Viewport Width:** `1440px` (`90rem`) centered container.
- **Desktop Margins:** `64px` (`4rem`) outer boundary simulating museum matting.
- **Tablet Margins:** `32px` (`2rem`).
- **Mobile Margins:** `20px` (`1.25rem`).
- **Column Structure:** 12-column fluid responsive grid with a standard `24px` gutter (`gutter-md`).
- **Curator's Gap:** `80px` (`5rem`) vertical separation between major exhibition sections to allow visual rest.

### 4.2 Spacing Scale (8px Rhythmic Grid)
- `--spacing-xs`: `4px` (`0.25rem`) — Micro icon offsets and inner badge paddings
- `--spacing-sm`: `8px` (`0.5rem`) — Stack spacing between compact elements
- `--spacing-md`: `16px` (`1rem`) — Card internal padding, form input spacing
- `--spacing-lg`: `24px` (`1.5rem`) — Standard component gutter
- `--spacing-xl`: `32px` (`2rem`) — Container section padding
- `--spacing-2xl`: `48px` (`3rem`) — Modal inner margins
- `--spacing-section`: `80px` (`5rem`) — Sectional breathing rhythm

### 4.3 Masonry Responsive Columns
- **Mobile (< 576px):** 1 Column, `16px` gap
- **Tablet (576px – 991px):** 2 Columns, `20px` gap
- **Desktop (992px – 1399px):** 3 Columns, `24px` gap
- **Workstation (≥ 1400px):** 4 Columns, `24px` gap

---

## 5. Elevation, Shapes & Depth Tokens

### 5.1 Border Radius Tokens
- `rounded-sm`: `4px` (`0.25rem`) — Checkboxes, radio buttons, micro-tags
- `rounded-md`: `8px` (`0.5rem`) — Form inputs, dropdown selectors, action buttons
- `rounded-lg`: `16px` (`1rem`) — Artwork cards, Kanban task tickets, floating dialogs
- `rounded-xl`: `24px` (`1.5rem`) — Hero exhibition monograph cards, upload dropzone
- `rounded-full`: `9999px` — Filter chips, status pills, user avatars, tag chips

### 5.2 Elevation & Glassmorphism
- **Level 0 (Floor Canvas):** Flat base (`#0E0F12` Dark / `#FAF9F6` Light) with 0px blur.
- **Level 1 (Cards & Sidebars):**
  - **Dark:** `background: rgba(26, 29, 39, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08);`
  - **Light:** `background: #FFFFFF; border: 1px solid #E6E3DD; box-shadow: 0 4px 20px -2px rgba(26, 26, 30, 0.05);`
- **Level 2 (Modals & Drawers):**
  - **Dark:** `background: rgba(22, 24, 31, 0.85); backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 24px 64px -12px rgba(0, 0, 0, 0.6);`
  - **Light:** `background: #FFFFFF; border: 1px solid #E6E3DD; box-shadow: 0 20px 48px -8px rgba(26, 26, 30, 0.12);`
- **Action Glow (Interactive Focus):**
  - **Dark Amber:** `box-shadow: 0 0 20px rgba(229, 169, 60, 0.28);`
  - **Light Terracotta:** `box-shadow: 0 0 0 3px rgba(217, 107, 67, 0.15);`

---

## 6. Preserved Data Contracts & Component Specs

### 6.1 INR (`₹`) Currency Contract
All financial amounts must be strictly formatted with the Indian Rupee symbol and tabular alignment:
```html
<span class="currency-inr" style="font-variant-numeric: tabular-nums;">
    ₹ 28,000 INR
</span>
```

### 6.2 Artwork Tag Contract
Interactive pill chips formatted with an initial hashtag `#` or clickable `+` addition trigger:
```html
<span class="badge tag-pill">#cyberpunk</span>
<span class="badge tag-pill">#concept-art</span>
<span class="badge tag-pill">#heritage</span>
```

### 6.3 Workflow Status Pills
Real-time artist daily status badges with standard icon indicators:
- `💼 4 Active Commissions`
- `🔴 2 Need Revision` (`#EF4444`)
- `🟡 1 Awaiting Client Feedback` (`#F59E0B`)
- `🟢 1 Ready for Delivery` (`#10B981`)

### 6.4 Image Upload & Local Edge Optimization
Asset dropzones display real-time dimension parsing and Pillow engine local optimization tags:
- **Dimensions Pill:** `3840 × 2160 px`
- **Compression Pill:** `14.2 MB (Compressed to 2.4 MB)`
- **Engine Badge:** `Zero-cloud edge optimization via localized Pillow engine.`
