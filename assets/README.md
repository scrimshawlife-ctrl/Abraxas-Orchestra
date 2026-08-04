# Assets

## Hero

| File | Role |
|------|------|
| `hero.svg` | **Default README hero** (text-safe; always in repo) |
| `hero.jpg` | Optional photographic/sigil art (1200×1800 progressive JPEG ~180 KB) |
| `hero.webp` | Optional WebP sibling |

### README wiring

Prefer SVG so the badge renders without a binary push:

```html
<img src="assets/hero.svg" alt="Abraxas Orchestra" width="720"/>
```

If `hero.jpg` is present, you may switch the README `src` to the JPEG for the full sigil image.

### Commit photographic hero (local git)

```bash
# requires Pillow
python3 - <<'PY'
from PIL import Image
img = Image.open("source.jpg").convert("RGB")
img = img.resize((1200, 1800), Image.Resampling.LANCZOS)
img.save("assets/hero.jpg", "JPEG", quality=72, optimize=True, progressive=True, subsampling=2)
PY
git add assets/hero.jpg && git commit -m "assets: photographic hero" && git push
```

The GitHub text connector cannot push JPEG/WebP bytes.
