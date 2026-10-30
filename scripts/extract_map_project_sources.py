from pathlib import Path
from zipfile import ZipFile
from shutil import copyfileobj

source=Path("source")
out=Path("map-project-source")
out.mkdir(exist_ok=True)
archive=source/"pokemon-rpg-android-clover-valley-map.zip"
wanted=[]
with ZipFile(archive) as z:
    for info in z.infolist():
        if info.is_dir(): continue
        name=info.filename
        suffix=Path(name).suffix.lower()
        if (name.endswith("MainActivity.kt") or name.endswith("README.md") or name.endswith("ASSET_NOTES.md")
            or name.endswith("AndroidManifest.xml") or name.endswith("build.gradle.kts")
            or name.endswith("settings.gradle.kts") or name.endswith("gradle.properties")
            or name.endswith("android.yml")):
            target=out/name
            target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(info) as src,target.open("wb") as dst: copyfileobj(src,dst)
            wanted.append((name,info.file_size))
print("ANDROID SOURCE FILES EXTRACTED")
for name,size in wanted: print(f"{name} ({size} bytes)")
main=out/"app/src/main/java/br/com/aventuraelemental/MainActivity.kt"
if main.exists():
    print("\\n===== MainActivity.kt (first 16000 chars) =====")
    print(main.read_text(encoding="utf-8",errors="replace")[:16000])
