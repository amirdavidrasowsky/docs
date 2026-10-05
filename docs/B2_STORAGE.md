# Backblaze B2 storage plan

The ChatGPT environment used to create this repository did not expose a Backblaze B2/S3 connector, so no files were uploaded to B2 from this chat. The two required source images are small enough to keep in GitHub without meaningful repository bloat, and they are committed under `assets/`.

For future large artifacts, B2 is a good fit. Recommended object layout:

```text
nir-dahan-plaque/
  source/nir_dahan_portrait_original.png
  source/reference_plaque_typography.jpg
  historical/NotoSansHebrewMedium/...
  historical/NarkisTamMedium/...
  generated/<font-preset>/<timestamp-or-version>/...
```

Keep a small JSON manifest in GitHub containing, for each B2 object: bucket, object key, byte size, SHA-256, MIME type, and optional signed/public URL. Do not store B2 application keys or S3 secrets in GitHub.

If a B2/S3 connector becomes available in a later ChatGPT session, upload large generated PDFs/ZIPs there and update the manifest rather than committing every generated binary to GitHub. Source code, specs, presets, documentation, manifests, and small reference images should remain in GitHub.
