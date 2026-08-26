"""Render the three booklet pages that Ana's artwork promises but does not contain.

Each new page mounts its content as a card on a copy of the back-cover plate
(images-new/23.jpg), so the paper, gold rule and florals are Ana's own.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H  = 2400, 1350
WINE  = (91, 26, 42)
INK   = (74, 42, 34)
GOLD  = (176, 143, 74)
CREAM = (252, 249, 242)
FB    = '/System/Library/Fonts/Supplemental/Baskerville.ttc'
REG, BOLD, ITAL, SEMI = 0, 1, 2, 4


def font(sz, face=REG):
    return ImageFont.truetype(FB, sz, index=face)


def base():
    return Image.open('images-new/23.jpg').convert('RGB').resize((W, H), Image.LANCZOS)


def tracked(d, xy, text, f, fill, track=0, anchor='mm'):
    ws = [d.textlength(c, font=f) for c in text]
    total = sum(ws) + track * (len(text) - 1)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=f, fill=fill, anchor='l' + anchor[1])
        x += w + track
    return total


def shadow(page, x0, y0, w, h, pad=14):
    sh = Image.new('L', (w + pad * 6, h + pad * 6), 0)
    ImageDraw.Draw(sh).rectangle([pad * 3, pad * 3, pad * 3 + w, pad * 3 + h], fill=105)
    sh = sh.filter(ImageFilter.GaussianBlur(pad * 1.7))
    page.paste(Image.new('RGB', sh.size, (58, 38, 28)), (x0 - pad * 3, y0 - pad * 3 + 9), sh)


def art_card(page, img, w_frac=None, h_frac=None, cx=0.5, cy=0.5, pad=16):
    if w_frac:
        tw = int(W * w_frac); th = int(tw * img.size[1] / img.size[0])
    else:
        th = int(H * h_frac); tw = int(th * img.size[0] / img.size[1])
    im2 = img.resize((tw, th), Image.LANCZOS)
    x0, y0 = int(W * cx) - tw // 2, int(H * cy) - th // 2
    shadow(page, x0 - pad, y0 - pad, tw + 2 * pad, th + 2 * pad)
    page.paste(Image.new('RGB', (tw + 2 * pad, th + 2 * pad), (253, 251, 246)), (x0 - pad, y0 - pad))
    page.paste(im2, (x0, y0))
    return x0, y0, tw, th


def paper_card(page, w_frac, h_frac, cx=0.5, cy=0.5):
    tw, th = int(W * w_frac), int(H * h_frac)
    x0, y0 = int(W * cx) - tw // 2, int(H * cy) - th // 2
    shadow(page, x0, y0, tw, th)
    page.paste(Image.new('RGB', (tw, th), CREAM), (x0, y0))
    d = ImageDraw.Draw(page)
    d.rectangle([x0 + 12, y0 + 12, x0 + tw - 13, y0 + th - 13], outline=GOLD, width=2)
    return x0, y0, tw, th


def rule(d, cx, y, half=95):
    d.line([cx - half, y, cx + half, y], fill=GOLD, width=2)


# ── PAGE: THE SEATING PLAN ────────────────────────────────────────────────
def page_seating():
    pg = base(); d = ImageDraw.Draw(pg)
    x0, y0, tw, th = art_card(pg, Image.open('images/seating-plan.jpg'), w_frac=0.545, cy=0.565)
    tracked(d, (W * 0.5, y0 - 132), 'CHAPTER VI', font(36, SEMI), WINE, 12)
    tracked(d, (W * 0.5, y0 - 74), 'THE SEATING PLAN', font(56, SEMI), WINE, 8)
    rule(d, W * 0.5, y0 - 34, 110)
    pg.save('images-new/24-seating.jpg', 'JPEG', quality=88, optimize=True, progressive=True)


# ── PAGE: THE MENU ────────────────────────────────────────────────────────
def page_menu():
    pg = base(); d = ImageDraw.Draw(pg)
    art_card(pg, Image.open('images/menu.jpg'), h_frac=0.70, cx=0.655, cy=0.50)
    cx = W * 0.30
    tracked(d, (cx, H * 0.355), 'CHAPTER VI', font(34, SEMI), WINE, 12)
    tracked(d, (cx, H * 0.412), 'THE MENU', font(58, SEMI), WINE, 8)
    rule(d, cx, H * 0.455, 95)
    for i, line in enumerate(['The banquet prepared for the evening,', 'served at your table beneath the stars.']):
        d.text((cx, H * 0.505 + i * 52), line, font=font(35, ITAL), fill=INK, anchor='mm')
    pg.save('images-new/25-menu.jpg', 'JPEG', quality=88, optimize=True, progressive=True)


# ── PAGE: THE WEEKEND, CONFIRMED ──────────────────────────────────────────
ENTRIES = [
    ('THURSDAY · 27 AUGUST', 'Welcome Drinks',
     ['22:00 · Carpe Diem Lounge Club (CDLC)', 'Pg. Marítim de la Barceloneta 32']),
    ('FRIDAY · 28 AUGUST', 'The Wedding',
     ['Please arrive by 18:15 · Ceremony 18:30', 'Castell de Sant Marçal, Cerdanyola del Vallès']),
    ('SATURDAY · 29 AUGUST', 'Pool Party',
     ['15:00–19:00 · Private house', 'Passeig de Turull 40 · bring a pool towel']),
    ('THE WEDDING DAY', 'Private Bus',
     ['Departs 17:30 · Carrer del Dos de Maig 328', 'Returns from the castle at 00:30 and 03:30']),
]


def page_details():
    pg = base(); d = ImageDraw.Draw(pg)
    x0, y0, tw, th = paper_card(pg, 0.665, 0.745, cy=0.505)
    cx = x0 + tw / 2
    tracked(d, (cx, y0 + 76), 'THE WEEKEND', font(52, SEMI), WINE, 9)
    rule(d, cx, y0 + 118, 105)
    d.text((cx, y0 + 158), 'everything now confirmed', font=font(29, ITAL), fill=(126, 96, 82), anchor='mm')
    colx = [x0 + tw * 0.27, x0 + tw * 0.73]
    rowy = [y0 + 245, y0 + 450]
    for i, (day, title, lines) in enumerate(ENTRIES):
        px, py = colx[i % 2], rowy[i // 2]
        tracked(d, (px, py), day, font(24, SEMI), GOLD, 5)
        d.text((px, py + 48), title, font=font(44, REG), fill=WINE, anchor='mm')
        for j, ln in enumerate(lines):
            d.text((px, py + 100 + j * 42), ln, font=font(29, REG), fill=INK, anchor='mm')
    rule(d, cx, y0 + 648, 70)
    tracked(d, (cx, y0 + 700), 'DRESS CODE', font(26, SEMI), GOLD, 6)
    d.text((cx, y0 + 754), 'Chic wedding attire \u2014 not Bridgerton.', font=font(38, REG), fill=WINE, anchor='mm')
    for j, ln in enumerate(['Ladies, please do not wear white and avoid black.',
                            'Gentlemen, black tie is not required.']):
        d.text((cx, y0 + 806 + j * 42), ln, font=font(29, REG), fill=INK, anchor='mm')
    pg.save('images-new/26-details.jpg', 'JPEG', quality=88, optimize=True, progressive=True)


if __name__ == '__main__':
    page_seating(); page_menu(); page_details()
    print('built')
