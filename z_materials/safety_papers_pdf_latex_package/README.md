# Safety Papers PDF and LaTeX Source Package

Prepared on: 2026-05-02

## Contents

- `papers/`: downloaded public PDFs, organized by topic and paper title.
- `download_status.csv`: per-paper download status.
- `arxiv_source_urls.csv`: arXiv source bundle URLs for all arXiv papers.
- `metadata.json`: structured paper metadata used for this package.
- `scripts/download_arxiv_sources.py`: local helper script to download arXiv source bundles and extract the likely main `.tex` file.

## Download summary

- Total requested records: 46
- PDF files successfully included: 44
- PDF files not included:
  - `07 Red Teaming LLMs: A Stackelberg Game Approach to AI Safety`: IEEE Xplore stamp URL failed in this runtime, likely due access/anti-bot restrictions.
  - `14 Disentangling Intent from Role: Adversarial Self-Play for Persona-Invariant Safety Alignment`: no public URL/arXiv ID found from the provided hint `lijiajia-PIA`.

## LaTeX source note

The arXiv source endpoint is normally:

```text
https://arxiv.org/e-print/<arxiv_id>
```

In this runtime, the binary arXiv source endpoint could not be fetched even though the PDF endpoint worked. Therefore the `.tex` files are not included directly. To make this still useful, I included:

1. `arxiv_source_urls.csv` with all source URLs.
2. `scripts/download_arxiv_sources.py`, which can be run locally to download each arXiv source bundle, unpack it, detect the likely main `.tex`, and save it beside the PDF using the paper title as the filename.

Run locally from the unzipped folder:

```bash
python scripts/download_arxiv_sources.py
```

The script uses only Python standard library modules.
