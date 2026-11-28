# Libre Bodoni bleed

Sergei's pick from the display italics: Libre Bodoni Italic, weight 600 (Impallari Type, Pablo Impallari and Rodrigo Fuenzalida, SIL OFL 1.1). The letter is the outlined V in `voxa-mark-italic-4.svg`, and that path is now `src/assets/voxa-mark.svg`.

Variant 2, the medium bleed, is every app icon: white on `#09090a`, about 20% past the left and bottom. `scripts/generate-voxa-icons.py` renders the Windows ICO and DPI-sized tray images from `voxa-mark-bodoni-bleed-2.svg`. The sidebar and onboarding display that SVG directly. Other platform assets use the matching PNG master.

The three tiles draw that V large and toward the bottom-left, so the rounded square crops the left and bottom edges. The top-right serif stays inside.

|     | Placement                                                          |
| --- | ------------------------------------------------------------------ |
| 1   | About 10% past the left and bottom. `voxa-mark-bodoni-bleed-1.svg` |
| 2   | About 20%. This is the app tile. `voxa-mark-bodoni-bleed-2.svg`    |
| 3   | About 30%. `voxa-mark-bodoni-bleed-3.svg`                          |

White and periwinkle `#8f97ff`, on `#09090a`. The comparison sheet is `voxa-mark-bodoni-bleed-contact-sheet.png`. The shipped sizes, each one the medium bleed, are `voxa-icon-sizes.png`.

# Sharp-style mark

Previous direction. A, B, and C are drawn by hand as vector paths. They are not outlines of a Sharp Type font, and this repo does not include a Sharp Type font file.

The reference is the wide, heavy V on the Sharp Type homepage type tester: flared, cupped wedge terminals, a sharp bottom point, and a heavier left stroke. These drawings follow that spirit.

None of these files is connected to the app. The wired mark is the Libre Bodoni V.

|     | Drawing                                                                             |
| --- | ----------------------------------------------------------------------------------- |
| A   | Upright. `voxa-mark-sharp-A.svg`                                                    |
| B   | Slanted 11 degrees. `voxa-mark-sharp-B.svg`                                         |
| C   | The same italic, larger than the rounded tile, so the terminals and the point crop. |

White and periwinkle `#8f97ff`, on a `#09090a` tile. The sheet is `voxa-mark-sharp-contact-sheet.png`.

The 16px tray previews are the fitted letters, A and B, with no bleed. C is cropped by the tile, so it is the wrong source for a tray glyph. At 16px both fitted letters still read as a V. A is the clearer of the two.

# Earlier options

The script and display-italic sheets below are previous directions. They are not the current candidates.

# Script mark options

Comparison only. The wired-in mark is still the Instrument Serif italic V in `src/assets/voxa-mark.svg`. Each SVG is the capital V converted to vector paths, so the app does not need the font.

|     | Font                             | Foundry                          | License     | Source                                                                                                          |
| --- | -------------------------------- | -------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------- |
| 1   | Great Vibes, elegant calligraphy | TypeSETit (Robert E. Leuschke)   | SIL OFL 1.1 | https://fonts.google.com/specimen/Great+Vibes · https://github.com/googlefonts/great-vibes                      |
| 2   | La Belle Aurore, casual pen      | Kimberly Geswein                 | SIL OFL 1.1 | https://fonts.google.com/specimen/La+Belle+Aurore · https://github.com/google/fonts/tree/main/ofl/labelleaurore |
| 3   | Caveat Brush, brush              | Impallari Type (Pablo Impallari) | SIL OFL 1.1 | https://fonts.google.com/specimen/Caveat+Brush · https://github.com/googlefonts/caveat                          |

The SIL Open Font License allows a glyph to be outlined and used as a logo. License texts: `licenses/`.

At 16px, Great Vibes' entry swash fills into a blob. La Belle Aurore still reads as a V. Caveat Brush stays a thick V.

# Display italic options

Also comparison only. The wired-in mark is unchanged. These are display italics with a swash, ball terminals, a teardrop, a didone serif, and a sharp contemporary cut.

|     | Font                                | Foundry                                              | License                   | Source                                                                                                |
| --- | ----------------------------------- | ---------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | Mazius Display Extra Italic         | Collletttivo (Alberto Casagrande)                    | SIL OFL 1.1               | https://www.collletttivo.it/typefaces/mazius-display · https://github.com/collletttivo/mazius-display |
| 2   | Playfair Display Italic, weight 700 | Claus Eggers Sørensen                                | SIL OFL 1.1               | https://fonts.google.com/specimen/Playfair+Display · https://github.com/clauseggers/Playfair-Display  |
| 3   | Cormorant Italic, weight 600        | Catharsis Fonts (Christian Thalmann)                 | SIL OFL 1.1               | https://fonts.google.com/specimen/Cormorant · https://github.com/CatharsisFonts/Cormorant             |
| 4   | Libre Bodoni Italic, weight 600     | Impallari Type (Pablo Impallari, Rodrigo Fuenzalida) | SIL OFL 1.1               | https://fonts.google.com/specimen/Libre+Bodoni · https://github.com/googlefonts/Libre-Bodoni          |
| 5   | Boska Light Italic                  | Indian Type Foundry (Barbara Bigosinska)             | ITF Free Font License 2.0 | https://www.fontshare.com/fonts/boska · https://www.fontshare.com/licenses/itf-free-font-license      |

OFL allows a glyph to be outlined into a logo. The ITF license also allows logos and outlined letters, and does not allow shipping or modifying the font file. Boska's font file is not in the repo. See `licenses/Boska-ITF-FFL.txt`.

At 16px each of these still reads as a V. The thin stroke is about one pixel. Mazius keeps its swash.
