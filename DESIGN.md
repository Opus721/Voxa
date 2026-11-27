# Voxa design

Voxa’s interface follows Linear’s application UI, using the tokens already worked out in [obsidian-buba-theme](https://github.com/Opus721/obsidian-buba-theme) (Sergei’s calm dark theme for the Buba plugin, inspired by Linear). Linear’s own redesign notes fill the gaps Buba does not spell out: [How we redesigned the Linear UI](https://linear.app/now/how-we-redesigned-the-linear-ui) and the settings screens on linear.app (preferences, security, connections).

Dark is the designed theme. Light uses the same roles, inverted, so the theme toggle still works.

## Principles

1. **Elevation is a background step, not a shadow.** The window frame is darker than the content panel, the panel is darker than a card, and a control is a step lighter again. Shadows are reserved for menus that float over the page (Buba `--menu-shadow`).
2. **Chrome recedes.** Labels, icons, and sidebar items are grey (`#939496`) and become white only on hover or when selected. Content and the selected row carry the contrast. This is the first rule in the Buba readme and the point of Linear’s 2024 chrome refresh.
3. **One accent, used rarely.** Indigo `#5e6ad2` (Buba accent `hsl(234 56% 60%)`, the same hue Linear uses for a control that is on) is for the on-state of a switch, a primary button, a focus ring, and a link. It is not a selected-row fill. Selected navigation is a neutral control fill (`#232325`) with white text.
4. **Density is 13px UI type on a 4px rhythm.** Inter at 12px for meta, 13px for rows and navigation, 14px for a section title. Weight stays 500. Line-height for UI is about 1.4. Tracking is slightly tight (`-0.006em`), which is how Buba sets Inter in place of a separate display cut.
5. **Icons are 16px, stroke 1.5, one color.** They inherit the row color. No filled illustrations in the chrome.
6. **1px borders, small radii.** Hairline `#1c1d1f` between rows, edge `#28292c` around a group. Radius 6px on controls and nav items, 8px on groups and menus. No heavy drop shadows, no large pills in the chrome.
7. **Settings are grouped rows.** A quiet section title, then a bordered group. Each row is a label (and a 12px grey description) on the left and the control on the right. Hover is a 4% white wash. Focus is a 1px accent ring.
8. **Motion is short.** Color and background transitions are 120–150ms. Nothing bounces.

## Tokens

Defined as CSS variables in `src/styles/theme.css` and registered for Tailwind in `src/App.css`. Dark values are Buba’s `--lin-*` names.

| Token                 | Dark                      | Light              | Role                                    |
| --------------------- | ------------------------- | ------------------ | --------------------------------------- |
| `--color-frame`       | `#09090a`                 | `#f3f3f4`          | Window and sidebar                      |
| `--color-panel`       | `#121213`                 | `#ffffff`          | Main column                             |
| `--color-card`        | `#1a1a1b`                 | `#ffffff`          | Grouped settings surface                |
| `--color-control`     | `#232325`                 | `#ececee`          | Selected nav, inputs, secondary buttons |
| `--color-hover`       | `rgba(255,255,255,0.045)` | `rgba(0,0,0,0.04)` | Row and nav hover                       |
| `--color-line`        | `#1c1d1f`                 | `#ececee`          | Dividers inside a group                 |
| `--color-edge`        | `#28292c`                 | `#e4e4e6`          | 1px group and field border              |
| `--color-edge-strong` | `#34353a`                 | `#d0d0d3`          | Hovered field border                    |
| `--color-text`        | `#e3e4e6`                 | `#1b1c1e`          | Primary text                            |
| `--color-emphasis`    | `#ffffff`                 | `#1b1c1e`          | Selected nav label                      |
| `--color-ink-2`       | `#939496`                 | `#6f7074`          | Secondary text, idle icons              |
| `--color-ink-3`       | `#636468`                 | `#8d8e93`          | Tertiary text                           |
| `--color-accent`      | `#5e6ad2`                 | `#5e6ad2`          | Switch on, primary button, focus        |
| `--color-accent-text` | `#a9b4ff`                 | `#3d4ac4`          | Links                                   |
| `--color-menu`        | `#212122`                 | `#ffffff`          | Menus                                   |

Type: Inter (bundled, latin, latin-ext, cyrillic). 12 / 13 / 14px. Weights 400 body, 500 UI, 600 for the wordmark only.

Radius: 6px controls and nav, 8px groups and menus, 10px the recording overlay.

The mark is `src/assets/voxa-mark.svg`: one geometric V, `currentColor`, drawn to read at 16px.
