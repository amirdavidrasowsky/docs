# Backblaze B2 storage plan

The ChatGPT environment used to create this repository did **not** expose a Backblaze B2/S3 connector, so no files were uploaded to B2 from this chat. This is documented explicitly so a future session does not assume objects exist when they do not.

Recommended object layout if B2 is connected later:

```text
nir-dahan-plaque/
  source/nir_dahan_portrait_original.png
  source/reference_plaque_typography.jpg
  historical/NotoSansHebrewMedium/...
  historical/NarkisTamMedium/...
  generated/<font-preset>/<version>/...
```

For each B2 object, keep a small JSON manifest in GitHub containing:

- bucket name
- object key
- byte size
- SHA-256
- MIME type
- optional public or signed URL
- source/version note

Do not store B2 application keys, S3 keys, or secrets in GitHub.

Source assets expected by the renderer:

- `nir_dahan_portrait_original.png`: 1118 x 1536 px, SHA-256 `2bbdf94550fb3c907479647e3cfdcf4090cca6c6285f5e39d7d952bcea251c4f`
- `reference_plaque_typography.jpg`: 1536 x 1152 px, SHA-256 `07eac106b62dd80d31eb7f035c7e5513d964efa7eb09786b84b28676c9b13ec8`

Until B2 is connected, the originating chat provides a downloadable source/reproduction bundle containing those binaries. Once uploaded to B2, record the exact B2 keys and hashes here or in a dedicated JSON manifest.
