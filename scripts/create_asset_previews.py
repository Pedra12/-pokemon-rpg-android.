#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
from PIL import Image, ImageDraw, ImageFont
import tempfile
import shutil

source = Path("source")
out = Path("asset-previews")
out.mkdir(exist_ok=True)
clover_zip = source / "Clover Valley V2 Free.zip"
map_zip = source / "pokemon-rpg-android-clover-valley-map.zip"

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    clover_dir = tmp / "clover"
    map_dir = tmp / "map"
    with ZipFile(clover_zip) as z:
        z.extractall(clover_dir)
    with ZipFile(map_zip) as z:
        z.extractall(map_dir)

    for name in ("map_preview.png", "map_preview2.png"):
        matches = list(map_dir.rglob(name))
        if matches:
            Image.open(matches[0]).convert("RGBA").save(out / name)

    shutil.copytree(clover_dir, out / "raw", dirs_exist_ok=True)

    # Numbered 16x16 tile previews for authoring a real Tiled map.
    tiles_dir = clover_dir / "Clover Valley V2 Free" / "Tilesets"
    for tile_name in ("Grass_free.png", "Path_spring.png", "Water_free.png", "Fences.png"):
        p = tiles_dir / tile_name
        im = Image.open(p).convert("RGBA")
        scale = 5
        enlarged = im.resize((im.width * scale, im.height * scale), Image.Resampling.NEAREST)
        overlay = Image.new("RGBA", enlarged.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        cols, rows = im.width // 16, im.height // 16
        for ty in range(rows):
            for tx in range(cols):
                idx = ty * cols + tx
                x, y = tx * 16 * scale, ty * 16 * scale
                d.rectangle((x, y, x + 16 * scale - 1, y + 16 * scale - 1), outline=(255, 255, 255, 180), width=1)
                d.text((x + 2, y + 2), str(idx), fill=(255, 0, 0, 255))
        enlarged = Image.alpha_composite(enlarged, overlay)
        enlarged.save(out / ("indexed_" + tile_name))

    images = []
    for p in sorted(clover_dir.rglob("*.png")):
        try:
            im = Image.open(p).convert("RGBA")
            images.append((p.relative_to(clover_dir).as_posix(), im))
        except Exception:
            pass

    cols, cell_w, cell_h = 4, 240, 205
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (38, 42, 50))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception:
        font = ImageFont.load_default()

    for i, (name, im) in enumerate(images):
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        draw.rectangle((x + 6, y + 6, x + cell_w - 6, y + 166), fill=(65, 70, 80))
        im.thumbnail((cell_w - 20, 150), Image.Resampling.NEAREST)
        px = x + (cell_w - im.width) // 2
        py = y + 10 + (150 - im.height) // 2
        sheet.paste(im, (px, py), im)
        draw.text((x + 8, y + 170), name[:38], fill=(255, 255, 255), font=font)
        draw.text((x + 8, y + 187), f"{Image.open(clover_dir / name).size[0]} x {Image.open(clover_dir / name).size[1]}", fill=(190, 195, 205), font=font)

    sheet.save(out / "clover-contact-sheet.png")
    print(f"Generated preview for {len(images)} Clover Valley images.")
    print("Preview files:", ", ".join(p.name for p in out.iterdir()))
