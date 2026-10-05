# Source assets

The exact binary source files were available in the originating ChatGPT conversation, but the GitHub connector exposed in that session did not support arbitrary local binary upload, and no Backblaze B2 connector was exposed. The repository therefore records the exact identities of the source files rather than pretending they were uploaded.

Required binaries:

- `nir_dahan_portrait_original.png`
  - 1118 x 1536 px
  - SHA-256 `2bbdf94550fb3c907479647e3cfdcf4090cca6c6285f5e39d7d952bcea251c4f`
  - original portrait supplied for the plaque
- `reference_plaque_typography.jpg`
  - 1536 x 1152 px
  - SHA-256 `07eac106b62dd80d31eb7f035c7e5513d964efa7eb09786b84b28676c9b13ec8`
  - photographed reference plaque used to match Hebrew typography and spacing

The canonical print crop is generated from the portrait by center-cropping horizontally to 176:247. For this source that yields 1094 x 1536 px and historical SHA-256 `972ed549ecc6d317f4726d83eb5c38d28cbadf044a87e66cfffb149d4c252163` with the original generator settings.

Font binaries are deliberately excluded. See `docs/REPRODUCTION.md` and `docs/FONT_ALTERNATIVES.md`.

A complete source/reproduction ZIP is provided from the originating chat. Copy the two source images from that ZIP into this directory, or upload them to Backblaze B2 and add their object keys to a manifest.
