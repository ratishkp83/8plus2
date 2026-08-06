"""Extract the 8plus2 mark from brand-sheet.png exactly as-is.
No redrawing: crop + key out background to transparent by detecting navy/gold ink."""
from PIL import Image
import numpy as np

src = Image.open("brand-sheet.png").convert("RGBA")
arr = np.asarray(src).astype(np.int32)
R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
mx = np.maximum(np.maximum(R, G), B)
mn = np.minimum(np.minimum(R, G), B)
sat = mx - mn
darkness = 255 - mx

navy = (B > R + 15) & (mx < 160)                     # bluish and dark
gold = (R > 165) & ((R - B) > 45) & (G > 85)         # orange
ink = navy | gold                                    # strict logo mask, no neutrals

row_has = ink.any(axis=1)
rows = np.where(row_has)[0]
top, bottom = rows.min(), rows.max()

# widest empty-row run => split between mark (upper) and wordmark (lower)
best_start, best_len, run_start, run_len = None, 0, None, 0
for r in range(top, bottom + 1):
    if not row_has[r]:
        run_start = r if run_start is None else run_start
        run_len += 1
    else:
        if run_len > best_len:
            best_len, best_start = run_len, run_start
        run_start, run_len = None, 0
split = (best_start + best_len // 2) if best_start else bottom
print("rows", top, bottom, "split", split, "gap", best_len)

mark_mask = ink.copy(); mark_mask[split:, :] = False
mys, mxs = np.where(mark_mask)
x0, x1, y0, y1 = mxs.min(), mxs.max(), mys.min(), mys.max()
print("mark bbox", x0, y0, x1, y1, "w", x1 - x0, "h", y1 - y0)

# alpha: transparent for neutral background, smooth on ink edges
is_bg = (sat < 30) & (darkness < 135)
alpha = np.clip((np.maximum(sat, darkness) - 40) * 5, 0, 255)
alpha[is_bg] = 0
out = arr.copy(); out[..., 3] = alpha.astype(np.int32)
rgba = Image.fromarray(out.astype(np.uint8), "RGBA")

# tight crop for inline / header use
pad = 24
c = (max(0, x0 - pad), max(0, y0 - pad),
     min(src.width, x1 + pad), min(src.height, y1 + pad))
mark = rgba.crop(c)
mark.save("logo-mark.png")
print("saved logo-mark.png (tight)", mark.size)

# squared canvas with even padding for favicons / app icon
w, h = mark.size
side = int(max(w, h) * 1.16)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(mark, ((side - w) // 2, (side - h) // 2), mark)
canvas.save("logo-icon.png")
print("saved logo-icon.png (square)", canvas.size)

for s in (16, 32, 48, 180, 512):
    canvas.resize((s, s), Image.LANCZOS).save(f"favicon-{s}.png")
canvas.resize((256, 256), Image.LANCZOS).save(
    "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("saved favicons")
