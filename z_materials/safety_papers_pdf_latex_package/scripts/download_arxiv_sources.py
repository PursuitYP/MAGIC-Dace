#!/usr/bin/env python3
"""
Download arXiv source bundles and extract the likely main .tex file.

Usage:
  python scripts/download_arxiv_sources.py

Outputs:
  papers/<category>/<id_title>/<title>.tex
  source_archives/<id>_<arxiv_id>.src
  latex_source_status.csv

No third-party packages required.
"""
from __future__ import annotations

import csv, gzip, io, json, os, pathlib, re, shutil, tarfile, tempfile, time, urllib.request, zipfile, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
META = ROOT / "metadata.json"
ARCHIVES = ROOT / "source_archives"
ARCHIVES.mkdir(exist_ok=True)

def slugify(text: str, max_len: int = 135) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s.-]", "", text, flags=re.ASCII)
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"_+", "_", text)
    return text[:max_len].strip("._-") or "paper"

def cat_slug(cat: str) -> str:
    return slugify(cat.replace(" ", "_"), 80)

def download(url: str, dest: pathlib.Path, retries: int = 3) -> tuple[bool, str]:
    headers = {"User-Agent": "Mozilla/5.0 arxiv-source-downloader/1.0"}
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                ctype = resp.headers.get("content-type", "")
            if len(data) < 100:
                return False, f"too small: {len(data)} bytes"
            if b"<html" in data[:500].lower() or b"not found" in data[:1000].lower():
                return False, f"looks like html/error page; content-type={ctype}"
            dest.write_bytes(data)
            return True, f"downloaded {len(data)} bytes"
        except Exception as e:
            if attempt == retries:
                return False, repr(e)
            time.sleep(2 * attempt)
    return False, "unknown failure"

def safe_extract_tar(tar: tarfile.TarFile, dest: pathlib.Path) -> None:
    dest_real = dest.resolve()
    for member in tar.getmembers():
        target = (dest / member.name).resolve()
        if not str(target).startswith(str(dest_real)):
            raise RuntimeError(f"unsafe path in tar: {member.name}")
    tar.extractall(dest)

def unpack_archive(path: pathlib.Path, dest: pathlib.Path) -> tuple[bool, str]:
    data = path.read_bytes()
    try:
        if tarfile.is_tarfile(path):
            with tarfile.open(path) as tf:
                safe_extract_tar(tf, dest)
            return True, "tar"
    except Exception:
        pass
    try:
        with zipfile.ZipFile(path) as zf:
            zf.extractall(dest)
        return True, "zip"
    except Exception:
        pass
    try:
        decompressed = gzip.decompress(data)
        # Single gzipped tar can be detected after decompression.
        bio = io.BytesIO(decompressed)
        try:
            with tarfile.open(fileobj=bio, mode="r:*") as tf:
                safe_extract_tar(tf, dest)
            return True, "gzip-tar"
        except Exception:
            (dest / "source.tex").write_bytes(decompressed)
            return True, "gzip-single"
    except Exception:
        pass
    if data.lstrip().startswith(b"\\") or b"\\documentclass" in data[:20000]:
        (dest / "source.tex").write_bytes(data)
        return True, "plain-tex"
    return False, "unknown archive format"

def score_tex(path: pathlib.Path) -> tuple[int, str]:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return (-999, "")
    lowname = path.name.lower()
    score = 0
    if "\\documentclass" in text: score += 50
    if "\\begin{document}" in text: score += 40
    if "\\title" in text: score += 8
    if "\\author" in text: score += 6
    if "\\maketitle" in text: score += 6
    if "\\bibliography" in text or "\\printbibliography" in text: score += 3
    if any(x in lowname for x in ["main", "paper", "article", "ms", "manuscript"]): score += 8
    if any(x in lowname for x in ["supp", "appendix", "response", "rebuttal", "camera", "neurips_202", "iclr202"]): score -= 20
    score += min(path.stat().st_size // 10000, 10)
    return score, text

def find_main_tex(src_dir: pathlib.Path) -> tuple[pathlib.Path | None, str]:
    tex_files = [p for p in src_dir.rglob("*.tex") if p.is_file()]
    if not tex_files:
        return None, "no .tex files"
    ranked = sorted(((score_tex(p)[0], p) for p in tex_files), reverse=True)
    best_score, best = ranked[0]
    if best_score < 50:
        return None, "no strong main tex candidate; candidates=" + "; ".join(f"{p.name}:{s}" for s,p in ranked[:5])
    return best, f"selected {best.name} score={best_score}; candidates=" + "; ".join(f"{p.name}:{s}" for s,p in ranked[:5])

def main() -> None:
    records = json.loads(META.read_text(encoding="utf-8"))
    rows = []
    for r in records:
        if not r.get("arxiv"):
            continue
        rid, arxiv_id = r["id"], r["arxiv"]
        title_slug = slugify(r["title"])
        paper_dir = ROOT / "papers" / cat_slug(r["category"]) / f"{rid}_{title_slug}"
        paper_dir.mkdir(parents=True, exist_ok=True)
        url = f"https://arxiv.org/e-print/{arxiv_id}"
        archive_path = ARCHIVES / f"{rid}_{arxiv_id}.src"
        ok, msg = download(url, archive_path)
        if not ok:
            rows.append({"id": rid, "title": r["title"], "arxiv_id": arxiv_id, "status": "download_failed", "detail": msg})
            print(rid, "download failed:", msg)
            continue
        with tempfile.TemporaryDirectory() as td:
            src_dir = pathlib.Path(td)
            ok, unpack_msg = unpack_archive(archive_path, src_dir)
            if not ok:
                rows.append({"id": rid, "title": r["title"], "arxiv_id": arxiv_id, "status": "unpack_failed", "detail": unpack_msg})
                print(rid, "unpack failed:", unpack_msg)
                continue
            main_tex, detail = find_main_tex(src_dir)
            if not main_tex:
                rows.append({"id": rid, "title": r["title"], "arxiv_id": arxiv_id, "status": "main_tex_not_found", "detail": detail})
                print(rid, "main tex not found:", detail)
                continue
            out_tex = paper_dir / f"{title_slug}.tex"
            shutil.copy2(main_tex, out_tex)
            rows.append({"id": rid, "title": r["title"], "arxiv_id": arxiv_id, "status": "tex_extracted", "detail": str(out_tex.relative_to(ROOT)) + " | " + detail})
            print(rid, "tex extracted:", out_tex)
        time.sleep(1.0)
    with open(ROOT / "latex_source_status.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id","title","arxiv_id","status","detail"])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
