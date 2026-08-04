# Assets

## Hero (`hero.jpg`)

| Spec | Value |
|------|--------|
| Dimensions | 1200 × 1800 (2× for ~720px README display) |
| Format | Progressive JPEG |
| Quality | ~72 |
| Target weight | ~180 KB |
| Alt | Abraxas Orchestra — symbolic architecture skill |

Optional:

| File | Notes |
|------|--------|
| `hero.webp` | Same dimensions; often ~100 KB — use if you prefer WebP |
| `hero-light.jpg` | Slightly lower quality JPEG |
| `hero-sm.webp` | Smaller WebP (~87 KB) |

### Re-optimize from source

```bash
# requires Pillow
python3 - <<'PY'
from PIL import Image
img = Image.open("source.jpg").convert("RGB")
img = img.resize((1200, 1800), Image.Resampling.LANCZOS)
img.save("assets/hero.jpg", "JPEG", quality=72, optimize=True, progressive=True, subsampling=2)
img.save("assets/hero.webp", "WEBP", quality=78, method=6)
PY
```

### Commit the binary (connector cannot push image bytes)

```bash
git add assets/hero.jpg assets/hero.webp assets/README.md
git commit -m "assets: optimized GitHub hero"
git push origin main
```
