from pathlib import Path
from zipfile import ZipFile
source=Path("source")
archives=["Clover Valley V2 Free.zip","pokemon-rpg-android-clover-valley-map.zip"]
for archive in archives:
    print("\\n===== "+archive+" =====")
    with ZipFile(source/archive) as z:
        for info in z.infolist():
            if info.is_dir(): continue
            print(info.filename)
            if info.filename.lower().endswith((".md",".kt",".xml",".yml",".txt",".properties",".kts")) and info.file_size < 20000:
                try:
                    body=z.read(info.filename).decode("utf-8",errors="replace")
                    print("--- BEGIN "+info.filename+" ---")
                    print(body[:5000])
                    print("--- END "+info.filename+" ---")
                except Exception as e: print("TEXT READ ERROR",e)
