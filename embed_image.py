#!/usr/bin/env python
"""Embed an image into a notebook markdown cell as a base64 data URI.

The Voici build is invoked as `voici build --contents enob-explorer.ipynb`,
which ships ONLY the notebook -- any externally-referenced image file
(``<img src="foo.png">``) is not uploaded, so it renders broken in the deployed
app. Embedding the image as a ``data:`` URI makes the markdown self-contained
(no CI change, and no trouble with spaces in filenames).

This rewrites just the ``src`` of the first ``<img>`` in the target cell, so the
surrounding markdown text is preserved -- run it again any time you swap the
diagram.

Usage:
    python embed_image.py "Block Diagram.png"
    python embed_image.py diagram.png --notebook enob-explorer.ipynb --cell 65a8e395

Run with the project venv (needs nbformat):
    .venv/Scripts/python.exe embed_image.py "Block Diagram.png"
"""
import argparse
import base64
import pathlib
import re
import sys

import nbformat

MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}

IMG_SRC_RE = re.compile(r'(<img\b[^>]*?\bsrc=")[^"]*(")', re.IGNORECASE)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", help="path to the image file to embed")
    ap.add_argument("--notebook", default="enob-explorer.ipynb",
                    help="notebook to edit (default: enob-explorer.ipynb)")
    ap.add_argument("--cell", default="65a8e395",
                    help="id of the markdown cell holding the <img> (default: 65a8e395)")
    args = ap.parse_args()

    img_path = pathlib.Path(args.image)
    if not img_path.is_file():
        print(f"error: image not found: {img_path}", file=sys.stderr)
        return 1
    mime = MIME.get(img_path.suffix.lower())
    if mime is None:
        print(f"error: unsupported image type: {img_path.suffix}", file=sys.stderr)
        return 1

    b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
    data_uri = f"data:{mime};base64,{b64}"

    nb = nbformat.read(args.notebook, as_version=4)
    for cell in nb.cells:
        if cell.get("id") == args.cell:
            if cell.get("cell_type") != "markdown":
                print(f"error: cell {args.cell} is not markdown", file=sys.stderr)
                return 1
            new_src, n = IMG_SRC_RE.subn(rf"\g<1>{data_uri}\g<2>", cell["source"], count=1)
            if n == 0:
                print(f"error: no <img ... src=\"...\"> found in cell {args.cell}", file=sys.stderr)
                return 1
            cell["source"] = new_src
            break
    else:
        print(f"error: cell id {args.cell} not found in {args.notebook}", file=sys.stderr)
        return 1

    nbformat.write(nb, args.notebook)
    print(f"embedded {img_path.name} ({len(b64)} b64 chars) into "
          f"cell {args.cell} of {args.notebook}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
