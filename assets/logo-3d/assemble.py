"""Assemble Blender spin frames into the animated WebP + still poster used on the home page."""
import glob, sys
from PIL import Image

frames_dir, out_dir = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 480
quality = int(sys.argv[4]) if len(sys.argv) > 4 else 80
files = sorted(glob.glob(f"{frames_dir}/frame_*.png"))
frames = [Image.open(f).convert("RGBA").resize((size, size), Image.LANCZOS) for f in files]
frames[0].save(f"{out_dir}/emblem-spin-poster.webp", "WEBP", quality=90, method=6)
frames[0].save(f"{out_dir}/emblem-spin.webp", "WEBP", save_all=True, append_images=frames[1:],
               duration=50, loop=0, quality=quality, method=6, allow_mixed=False)
import os
print(len(files), "frames;", os.path.getsize(f"{out_dir}/emblem-spin.webp") // 1024, "KB anim;",
      os.path.getsize(f"{out_dir}/emblem-spin-poster.webp") // 1024, "KB poster")
