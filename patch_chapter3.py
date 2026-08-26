"""Retire the two 'details to follow' lines from Ana's Chapter III plate.

Chapter III promised "Details coming soon" (welcome drinks) and "More
information to follow" (pool party). Both are now confirmed and printed on
the following page, so the promises are stale. The artwork is a flat JPEG
with no editable source on this machine — the Canva master belongs to the
designer — so the lines are patched out by lifting clean parchment from
directly beneath each one, brightness-matched and feathered at the edges.

Reads the untouched 6000px export, writes the 3000px page the booklet serves.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = os.path.expanduser('~/crusty-backups/wedding-booklet-originals-6000px/19.jpg')
DST = 'images-new/19.jpg'
OUT_W = 3000

# (target box, donor box) in 6000x3375 coordinates. Donors sit directly below
# each line so the paper grain and lighting gradient already match.
PATCHES = [
    ((1520, 1760, 2140, 1865), (1520, 1880, 2140, 1985)),   # "Details coming soon."
    ((3830, 1672, 4630, 1765), (3830, 1790, 4630, 1883)),   # "More information to follow."
]
FEATHER = 9


def background_mean(gray, box):
    """Mean of the box ignoring ink, so brightness matching is not dragged down."""
    sub = gray.crop(box)
    arr = np.array(sub, dtype=float)
    paper = arr[arr >= 150]
    return paper.mean() if paper.size else arr.mean()


def main():
    im = Image.open(SRC).convert('RGB')
    gray = im.convert('L')

    for target, donor in PATCHES:
        tw, th = target[2] - target[0], target[3] - target[1]
        patch = im.crop(donor).resize((tw, th), Image.LANCZOS)

        # match the donor's paper tone to the target's own paper tone
        delta = background_mean(gray, target) - background_mean(gray, donor)
        patch = Image.fromarray(
            np.clip(np.array(patch, dtype=float) + delta, 0, 255).astype(np.uint8))

        mask = Image.new('L', (tw, th), 0)
        ImageDraw.Draw(mask).rectangle(
            [FEATHER, FEATHER, tw - FEATHER - 1, th - FEATHER - 1], fill=255)
        im.paste(patch, (target[0], target[1]), mask.filter(ImageFilter.GaussianBlur(FEATHER / 2)))

    h = round(OUT_W * im.size[1] / im.size[0])
    im.resize((OUT_W, h), Image.LANCZOS).save(
        DST, 'JPEG', quality=88, optimize=True, progressive=True)
    print(f'{DST}: {OUT_W}x{h}, {os.path.getsize(DST) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
