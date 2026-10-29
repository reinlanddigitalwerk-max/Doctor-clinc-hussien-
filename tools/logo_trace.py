"""Vectorise the practice logo: upscale, snap to 4 brand colours, trace with vtracer."""
import sys
import numpy as np
from PIL import Image, ImageFilter
import vtracer

src, out_png, out_svg, scale = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
im = Image.open(src).convert("RGBA")
big = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
a = np.array(big).astype(np.float32)
rgb, alpha = a[..., :3], a[..., 3]
# reference colours as they appear in the CMYK->RGB extraction
REF = np.array([[0, 48, 176], [48, 168, 240], [72, 240, 216], [216, 240, 240]], np.float32)
# true brand colours (from the practice's own PNG)
TRUE = np.array([[0x12, 0x4A, 0x87], [0x2A, 0x93, 0xC6], [0x4F, 0xD1, 0xC9], [0xFF, 0xFF, 0xFF]], np.uint8)
d = ((rgb[..., None, :] - REF[None, None]) ** 2).sum(-1)
cls = d.argmin(-1)
# light/white pixels that are just antialiasing against transparency -> keep only where alpha is solid
mask = alpha >= 140
res = np.zeros((*cls.shape, 4), np.uint8)
res[..., :3] = TRUE[cls]
res[..., 3] = np.where(mask, 255, 0)
Image.fromarray(res).save(out_png)
vtracer.convert_image_to_svg_py(out_png, out_svg, colormode="color", hierarchical="stacked", mode="spline",
    filter_speckle=10 * scale // 4, color_precision=8, layer_difference=24, corner_threshold=60,
    length_threshold=4.0, max_iterations=10, splice_threshold=45, path_precision=2)
print("ok", big.size)
