#!/usr/bin/env python3
"""Inspect the user's uploaded art packs without changing or overwriting game assets."""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import struct

ROOT = Path("source")
PACKS = [
    ROOT / "Clover Valley V2 Free.zip",
    ROOT / "pokemon-rpg-android-clover-valley-map.zip",
    ROOT / "PokeRPG-main.zip",
]
OUT = Path("asset-pack-report.txt")
lines = ["ASSET PACK INSPECTION", "No source files or archives were modified.", ""]

def png_size(zf, name):
    try:
        with zf.open(name) as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return f"{struct.unpack('>I', head[16:20])[0]}x{struct.unpack('>I', head[20:24])[0]}"
    except Exception:
        pass
    return ""

for archive in PACKS:
    lines.append(f"## {archive.name}")
    if not archive.exists():
        lines.append("MISSING")
        lines.append("")
        continue
    try:
        with ZipFile(archive) as zf:
            files = [x for x in zf.infolist() if not x.is_dir()]
            ext = Counter(Path(x.filename).suffix.lower() or "[sem extensão]" for x in files)
            lines.append(f"Files: {len(files)}")
            lines.append("Extensions: " + ", ".join(f"{k}={v}" for k,v in ext.most_common()))
            interesting = []
            for x in files:
                p = x.filename.lower()
                if Path(p).suffix.lower() in {".tmx", ".tsx", ".json", ".atlas", ".png", ".jpg", ".jpeg", ".webp"}:
                    dims = png_size(zf, x.filename) if p.endswith(".png") else ""
                    interesting.append((x.filename, dims, x.file_size))
            lines.append("Relevant files:")
            for name, dims, size in interesting[:300]:
                suffix = f" [{dims}]" if dims else ""
                lines.append(f"- {name}{suffix} ({size} bytes)")
            if len(interesting) > 300:
                lines.append(f"... {len(interesting)-300} more relevant files omitted")
    except BadZipFile:
        lines.append("INVALID ZIP")
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
