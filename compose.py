#!/usr/bin/env python3
"""Draw 'THE WORLD TODAY' — a dense front page summing up Saturday
21 November 2026 world news. Flat vector-style art, drawn from scratch
with Pillow. No external images, no network, stdlib + Pillow only."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (139, 26, 26)
NAVY = (26, 47, 74)
GREY = (90, 86, 76)
LIGHT = (232, 226, 210)
MAP_LAND = (206, 198, 172)
MAP_SEA = (214, 226, 228)
GOLD = (176, 132, 32)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, fill=INK, w=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 26                      # side margin
CW = W - 2 * M              # content width

# ---------------------------------------------------------------- masthead
y = 14
f_title = font(F_SERIF, 60)
title = "THE WORLD TODAY"
tw = d.textlength(title, font=f_title)
d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
y += 68
rule(d, M, W - M, y, INK, 3)
y += 5
rule(d, M, W - M, y, INK, 1)
y += 8
f_date = font(F_SANS_B, 16)
dateline = "SATURDAY 21 NOVEMBER 2026  ·  36 STORIES FROM AROUND THE WORLD"
tw = d.textlength(dateline, font=f_date)
d.text(((W - tw) / 2, y), dateline, font=f_date, fill=RED)
y += 24
f_sub = font(F_SANS_I, 13)
sub = ("Russian missiles land in Poland  ·  COP31 talks slip into overtime with "
       "fossil fuels struck from the draft  ·  Wall Street falls into correction")
tw = d.textlength(sub, font=f_sub)
d.text(((W - tw) / 2, y), sub, font=f_sub, fill=INK)
y += 22
rule(d, M, W - M, y, INK, 2)

# ---------------------------------------------------------------- stat strip
y += 8
stats = [
    ("2", "missiles land\nin Poland"),
    ("42", "hurt in Kryvyi\nRih strike"),
    ("-3.7%", "S&P 500 on\nFriday"),
    ("372,000", "evacuated before\nCyclone Akvan"),
    ("\u20ac1bn", "EU military aid\nfor Ukraine"),
    ("159/1", "India at stumps\nin Wellington"),
]
f_num = font(F_SANS_B, 24)
f_lab = font(F_SANS, 11)
sw = CW / 6
for i, (num, lab) in enumerate(stats):
    x0 = M + i * sw
    if i:
        d.line([(x0, y), (x0, y + 44)], fill=GREY, width=1)
    nw = d.textlength(num, font=f_num)
    d.text((x0 + (sw - nw) / 2, y), num, font=f_num,
           fill=RED if i in (0, 2) else NAVY)
    ly = y + 27
    for ln in lab.split("\n"):
        lw = d.textlength(ln, font=f_lab)
        d.text((x0 + (sw - lw) / 2, ly), ln, font=f_lab, fill=INK)
        ly += 12
y += 54
rule(d, M, W - M, y, INK, 1)
y += 6
f_reg = font(F_SANS_B, 12)
regions = "THE AMERICAS 12   ·   EUROPE 13   ·   MIDDLE EAST 4   ·   ASIA-PACIFIC 7"
tw = d.textlength(regions, font=f_reg)
d.text(((W - tw) / 2, y), regions, font=f_reg, fill=NAVY)
y += 22
rule(d, M, W - M, y, INK, 2)

# ---------------------------------------------------------------- heroes
HY = y + 8
HCW = 310
HGAP = (CW - 3 * HCW) / 2
f_kick = font(F_SANS_B, 11)
f_head = font(F_SERIF, 19)
f_body = font(F_SANS, 12)


def hero_panel(x, art, kicker, headline, body):
    # illustration box
    d.rectangle([x, HY, x + HCW, HY + 84], outline=INK, width=2)
    art(x, HY, HCW, 84)
    yy = HY + 92
    d.text((x, yy), kicker, font=f_kick, fill=RED)
    yy += 15
    lines = wrap(d, headline, f_head, HCW)
    yy = draw_lines(d, lines[:2], x, yy, f_head, INK, 22)
    yy += 2
    blines = wrap(d, body, f_body, HCW)
    draw_lines(d, blines[:4], x, yy, f_body, INK, 14)


def art_poland(x, y0, w, h):
    d.rectangle([x, y0, x + w, y0 + h], fill=(38, 52, 78))
    # stars
    for sx, sy in [(30, 14), (90, 22), (150, 10), (210, 18), (260, 12), (280, 30)]:
        d.ellipse([x + sx, y0 + sy, x + sx + 2, y0 + sy + 2], fill=(255, 255, 255))
    # ground + pine trees
    d.rectangle([x, y0 + h - 18, x + w, y0 + h], fill=(52, 84, 52))
    for tx in (18, 52, 268, 292):
        d.polygon([(x + tx, y0 + h - 18), (x + tx + 9, y0 + h - 44),
                   (x + tx + 18, y0 + h - 18)], fill=(34, 66, 38))
    # missile with smoke trail
    d.line([(x + 30, y0 + 26), (x + 210, y0 + 52)], fill=(220, 220, 220), width=3)
    d.polygon([(x + 210, y0 + 44), (x + 244, y0 + 52), (x + 210, y0 + 60)],
              fill=(200, 200, 200))
    d.rectangle([x + 196, y0 + 48, x + 214, y0 + 56], fill=(160, 160, 160))
    # impact burst
    cx, cy = x + 252, y0 + 66
    for r, col in [(14, (255, 180, 60)), (9, (255, 120, 40)), (5, (255, 230, 120))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.text((x + 8, y0 + 4), "NOWY LIPOWIEC, POLAND", font=font(F_SANS_B, 9),
           fill=(255, 255, 255))


def art_cop(x, y0, w, h):
    d.rectangle([x, y0, x + w, y0 + h], fill=(214, 226, 228))
    d.ellipse([x + w - 66, y0 + 8, x + w - 26, y0 + 48], fill=(255, 196, 60))
    # sea
    d.rectangle([x, y0 + 58, x + w, y0 + h], fill=(64, 120, 150))
    d.line([(x, y0 + 66), (x + w, y0 + 66)], fill=(255, 255, 255), width=2)
    d.line([(x, y0 + 76), (x + w, y0 + 76)], fill=(255, 255, 255), width=1)
    # conference hall
    d.rectangle([x + 24, y0 + 30, x + 150, y0 + 58], fill=(250, 248, 240))
    d.polygon([(x + 24, y0 + 30), (x + 87, y0 + 12), (x + 150, y0 + 30)],
              fill=(139, 26, 26))
    for i in range(5):
        d.rectangle([x + 34 + i * 24, y0 + 40, x + 46 + i * 24, y0 + 58],
                    fill=NAVY)
    # flag poles
    for fx in (190, 220, 250):
        d.line([(x + fx, y0 + 18), (x + fx, y0 + 58)], fill=INK, width=2)
        d.rectangle([x + fx, y0 + 18, x + fx + 18, y0 + 28], fill=RED)
    d.text((x + 8, y0 + 4), "ANTALYA, TURKEY", font=font(F_SANS_B, 9),
           fill=NAVY)


def art_wallst(x, y0, w, h):
    d.rectangle([x, y0, x + w, y0 + h], fill=(232, 226, 210))
    # skyline
    for bx, bw, bh in [(10, 34, 46), (50, 26, 62), (82, 40, 38),
                       (128, 30, 56), (164, 34, 42), (204, 28, 66),
                       (238, 36, 50), (280, 24, 40)]:
        d.rectangle([x + bx, y0 + h - bh, x + bx + bw, y0 + h], fill=NAVY)
        for wy in range(y0 + h - bh + 6, y0 + h - 4, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 120))
    # falling red chart line
    pts = [(x + 12, y0 + 14), (x + 70, y0 + 22), (x + 120, y0 + 18),
           (x + 170, y0 + 36), (x + 220, y0 + 46), (x + 268, y0 + 62),
           (x + 300, y0 + 70)]
    d.line(pts, fill=RED, width=4)
    d.ellipse([x + 292, y0 + 62, x + 308, y0 + 78], fill=RED)
    d.text((x + 8, y0 + 4), "NEW YORK", font=font(F_SANS_B, 9), fill=RED)


heroes = [
    (art_poland, "POLAND  ·  NATO",
     "Russian missiles land in Poland",
     "Two Kh-101 missiles and a jet drone came down in south-east Poland "
     "during a huge Russian barrage. Tusk calls it a deliberate provocation; "
     "NATO's Rutte, a grave violation. No one was hurt."),
    (art_cop, "COP31  ·  ANTALYA",
     "Climate talks slip into overtime",
     "The draft deal drops every fossil-fuel reference and the \u20ac120bn "
     "adaptation target. Panama vows to object; France and seven others "
     "demand transition language restored. A third draft is due Saturday."),
    (art_wallst, "WALL STREET  ·  NEW YORK",
     "S&P 500 falls into correction",
     "The S&P 500 fell 3.7% on Friday, its seventh straight loss and more "
     "than 10% below its record. The Nasdaq sank 5.28%, erasing all its "
     "2026 gains, as the AI sell-off deepened. Nvidia fell 14%."),
]
for i, (art, kick, head, body) in enumerate(heroes):
    hero_panel(int(M + i * (HCW + HGAP)), art, kick, head, body)

y = HY + 210
rule(d, M, W - M, y, INK, 2)

# ---------------------------------------------------------------- grid of 9
y += 8
f_sec = font(F_SANS_B, 12)
d.text((M, y), "THE DAY IN BRIEF", font=f_sec, fill=INK)
d.text((W - M - d.textlength("9 MORE STORIES", font=f_sec), y),
       "9 MORE STORIES", font=f_sec, fill=RED)
y += 20
GW = 310
GGAP = (CW - 3 * GW) / 2
GROW = 60
f_gk = font(F_SANS_B, 10)
f_gh = font(F_SANS_B, 12)
f_gb = font(F_SANS, 11)


def icon(x, y0, kind, bg):
    d.rectangle([x, y0, x + 34, y0 + 34], fill=bg, outline=INK, width=1)
    cx, cy = x + 17, y0 + 17
    if kind == "missile":
        d.line([(x + 6, y0 + 28), (x + 28, y0 + 6)], fill=(255, 255, 255), width=3)
        d.polygon([(x + 24, y0 + 4), (x + 30, y0 + 10), (x + 24, y0 + 12)],
                  fill=(255, 255, 255))
    elif kind == "dome":
        d.polygon([(x + 6, y0 + 22), (cx, y0 + 8), (x + 28, y0 + 22)], fill=(255, 255, 255))
        d.rectangle([x + 8, y0 + 22, x + 26, y0 + 28], fill=(255, 255, 255))
    elif kind == "flag":
        d.line([(x + 10, y0 + 6), (x + 10, y0 + 28)], fill=(255, 255, 255), width=2)
        d.polygon([(x + 10, y0 + 6), (x + 26, y0 + 10), (x + 10, y0 + 15)],
                  fill=(255, 255, 255))
    elif kind == "megaphone":
        d.polygon([(x + 6, y0 + 14), (x + 20, y0 + 10), (x + 20, y0 + 24),
                   (x + 6, y0 + 20)], fill=(255, 255, 255))
        d.rectangle([x + 20, y0 + 12, x + 27, y0 + 22], fill=(255, 255, 255))
    elif kind == "capitol":
        d.rectangle([x + 6, y0 + 18, x + 28, y0 + 28], fill=(255, 255, 255))
        d.polygon([(x + 6, y0 + 18), (cx, y0 + 8), (x + 28, y0 + 18)],
                  fill=(255, 255, 255))
    elif kind == "storm":
        d.ellipse([x + 7, y0 + 7, x + 27, y0 + 27], outline=(255, 255, 255), width=3)
        d.ellipse([x + 12, y0 + 12, x + 22, y0 + 22], outline=(255, 255, 255), width=2)
    elif kind == "bat":
        d.rectangle([x + 15, y0 + 6, x + 19, y0 + 26], fill=(255, 255, 255))
        d.rectangle([x + 6, y0 + 12, x + 28, y0 + 15], fill=(255, 255, 255))
    elif kind == "coin":
        d.ellipse([x + 8, y0 + 8, x + 26, y0 + 26], outline=(255, 255, 255), width=3)
        d.text((x + 13, y0 + 11), "\u20ac", font=font(F_SANS_B, 13), fill=(255, 255, 255))
    elif kind == "gavel":
        d.rectangle([x + 8, y0 + 10, x + 26, y0 + 16], fill=(255, 255, 255))
        d.line([(x + 12, y0 + 16), (x + 24, y0 + 28)], fill=(255, 255, 255), width=3)


grid = [
    ("missile", NAVY, "UKRAINE", "110 missiles, 400 drones hit Kyiv",
     "Three Dnipro bridges struck; 8\u20139 dead, 17+ hurt in Kyiv. A double-tap "
     "on Kryvyi Rih kills 2, injures 42."),
    ("dome", RED, "RIYADH", "Houthi missiles intercepted over Riyadh",
     "Coalition says it downed three ballistic missiles; an earlier strike "
     "damaged the PIF tower. Hodeidah port hit."),
    ("flag", NAVY, "LONDON \u00b7 BRUSSELS", "EU\u2013UK reset sealed",
     "Burnham and von der Leyen scrap agrifood checks, link emissions "
     "trading and open a 100,000 under-30s scheme."),
    ("megaphone", RED, "EUROPE", "Cost-of-living protests sweep Europe",
     "Gen Z-led marches, biggest in Spain; Italy holds a nationwide "
     "strike across 45+ cities."),
    ("capitol", NAVY, "WASHINGTON", "Senate passes permitting reform",
     "The Bipartisan American Affordability and Jobs Act clears the "
     "Senate 62\u201333."),
    ("storm", NAVY, "ODISHA, INDIA", "372,000 flee Cyclone Akvan",
     "Mass evacuation before landfall near Gopalpur; the storm weakens "
     "and no deaths are reported."),
    ("bat", RED, "WELLINGTON", "India fight back to 159/1",
     "India reach 159 for 1 at stumps on day two after a strong reply "
     "with the bat."),
    ("coin", NAVY, "BRUSSELS", "EU adopts \u20ac1bn in aid for Ukraine",
     "Joint buying via the Peace Facility; Britain pledges 1,000+ drones "
     "in a \u00a3260m package."),
    ("gavel", RED, "WASHINGTON", "US sanctions four Iranians",
     "The Treasury targets four Iranians over Iranian oil revenues."),
]
for i, (kind, bg, kick, head, body) in enumerate(grid):
    gx = int(M + (i % 3) * (GW + GGAP))
    gy = y + (i // 3) * GROW
    icon(gx, gy, kind, bg)
    tx = gx + 42
    d.text((tx, gy), kick, font=f_gk, fill=RED)
    hlines = wrap(d, head, f_gh, GW - 42)
    hyy = draw_lines(d, hlines[:2], tx, gy + 13, f_gh, INK, 14)
    blines = wrap(d, body, f_gb, GW - 42)
    draw_lines(d, blines[:2], tx, hyy + 1, f_gb, INK, 13)
y += 3 * GROW + 4
rule(d, M, W - M, y, INK, 2)

# ---------------------------------------------------------------- map + date check
y += 8
MAP_W = 600
MAP_H = 124
d.text((M, y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
d.text((M + MAP_W + 16, y), "DATE CHECK", font=f_sec, fill=RED)
y += 18
map_y = y
d.rectangle([M, map_y, M + MAP_W, map_y + MAP_H], fill=MAP_SEA, outline=INK, width=1)

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-65, 45), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-95, 16), (-100, 18), (-105, 20),
     (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, 0), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50), (-73, -40),
     (-75, -30), (-80, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (43, 11), (48, 10), (51, 12), (45, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -30), (12, -18), (13, -5), (9, 0), (5, 4),
     (-5, 5), (-10, 7), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (12, 62), (18, 66), (25, 70), (30, 70), (40, 68),
     (45, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (20, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37)],
    [(40, 68), (55, 68), (70, 72), (90, 75), (110, 75), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 45), (140, 40),
     (130, 35), (127, 35), (122, 30), (120, 25), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 13), (77, 8), (72, 20),
     (65, 25), (60, 25), (55, 26), (50, 28), (48, 30), (44, 29), (40, 35),
     (35, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
]


def project(lon, lat):
    px = M + (lon + 170) / 360.0 * MAP_W
    py = map_y + (75 - lat) / 130.0 * MAP_H
    return px, py


for poly in CONTINENTS:
    d.polygon([project(lon, lat) for lon, lat in poly], fill=MAP_LAND)

DOTS = [
    (23, 52, "POLAND"), (30, 50, "KYIV"), (30, 37, "ANTALYA"),
    (-74, 41, "NEW YORK"), (47, 25, "RIYADH"), (0, 51, "LONDON"),
    (85, 20, "ODISHA"), (175, -41, "WELLINGTON"), (-77, 39, "WASHINGTON"),
    (107, 48, "MONGOLIA"), (-59, -35, "BUENOS AIRES"), (-48, -16, "BRASILIA"),
    (-4, 40, "MADRID"), (73, 33, "ISLAMABAD"), (104, 1, "SINGAPORE"),
    (37, 56, "MOSCOW"), (-84, 39, "CINCINNATI"), (-118, 34, "LOS ANGELES"),
]
f_dot = font(F_SANS_B, 8)
for lon, lat, label in DOTS:
    px, py = project(lon, lat)
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=(255, 255, 255))
d.text((M + 6, map_y + MAP_H - 14), "RED DOTS MARK THE STORY LOCATIONS",
       font=f_dot, fill=NAVY)

# date check box
dx = M + MAP_W + 16
dw = CW - MAP_W - 16
d.rectangle([dx, map_y, dx + dw, map_y + MAP_H], outline=RED, width=2)
f_dc = font(F_SANS, 10)
d.text((dx + 8, map_y + 5), "NOT SATURDAY'S NEWS \u2014 LEFT OUT ON PURPOSE:",
       font=font(F_SANS_B, 10), fill=RED)
dc_items = [
    "ICJ Myanmar genocide ruling \u2014 Thu 19 Nov",
    "Trump\u2013Xi\u2013Putin trilateral, Shenzhen \u2014 Thu 19 Nov",
    "Anthropic's record IPO \u2014 Thu 19 Nov",
    "Cyclone Akvan landfall \u2014 Fri 20 Nov",
    "Kerch Bridge span collapse \u2014 Tue 17 Nov",
    "Trump pardons Pete Rose \u2014 Fri 20 Nov",
]
yy = map_y + 20
for item in dc_items:
    d.text((dx + 8, yy), "\u2022  " + item, font=f_dc, fill=INK)
    yy += 15
d.text((dx + 8, yy), "Only 21 November stories appear above.",
       font=font(F_SANS_I, 10), fill=GREY)

y = map_y + MAP_H + 8
rule(d, M, W - M, y, INK, 2)

# ---------------------------------------------------------------- also list
y += 8
d.text((M, y), "ALSO ON SATURDAY 21 NOVEMBER", font=f_sec, fill=INK)
y += 20
also = [
    "Nvidia falls 14% on SEC probe report; AMD \u221213%",
    "Anthropic slides 9% on day two after record IPO",
    "Nasdaq erases all 2026 gains; worst week since 2020",
    "Nikkei and Kospi fall 5%+ as rout spreads to Asia",
    "VIX fear gauge soars 33% to 37",
    "Rutte due in Warsaw Saturday; NATO jets scrambled",
    "Poland seeks more Eastern Sentry forces on its flank",
    "Panama to object to COP31 draft; France + 7 join in",
    "Houthis warn airlines off Saudi airspace",
    "Houthis say 41 killed in 24h; coalition hit Hodeidah",
    "Mongolia's president resigns; snap election ahead",
    "Nikhil Gupta jailed 19+ years in US murder-plot case",
    "LA jury convicts man who started the Palisades Fire",
    "ECB names Boone and Brunnermeier to Executive Board",
    "Argentina's Senate backs a disability framework",
    "Brazil shields Indigenous land; Kayapo leader Raoni",
    "Fiona the hippo dies after eating a hat",
    "Amnesty: Spanish police used excess force in strike",
    "US presses Singapore and Malaysia on Iran sanctions",
    "Saudi Arabia warns of thunderstorms through Tuesday",
    "Malaysia to send 10,000 Rohingya to Turkey",
    "Russia jails a deputy defence minister for 10 years",
    "Ukraine says it finished a \u201cBear Trap\u201d for Kharkiv",
    "Pakistan's minerals worth $8\u201310tn, minister says",
]
assert len(also) == 24, len(also)
f_also = font(F_SANS, 11)
COLW = (CW - 2 * 14) / 3
for i, item in enumerate(also):
    col, row = i % 3, i // 3
    ax = M + col * (COLW + 14)
    ay = y + row * 17
    num = f"{13 + i}."
    d.text((ax, ay), num, font=font(F_SANS_B, 11), fill=RED)
    nw = d.textlength(num, font=font(F_SANS_B, 11))
    # fit the item on one line; shrink only if it would overflow
    fnt = f_also
    txt = item
    while d.textlength(txt, font=fnt) > COLW - nw - 5 and len(txt) > 20:
        txt = txt[:-1]
    d.text((ax + nw + 4, ay), txt, font=fnt, fill=INK)
y += 8 * 17 + 4
rule(d, M, W - M, y, INK, 2)

# ---------------------------------------------------------------- footer
y += 6
f_src = font(F_SANS_B, 11)
src = "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 Al Jazeera \u00b7 Kyiv Independent \u00b7 The Hindu"
tw = d.textlength(src, font=f_src)
d.text(((W - tw) / 2, y), src, font=f_src, fill=INK)
y += 15
f_note = font(F_SANS, 11)
note = ("All stories happened, or were first reported, on Saturday 21 November 2026 "
        "in some time zone. Figures as reported that day.")
tw = d.textlength(note, font=f_note)
d.text(((W - tw) / 2, y), note, font=f_note, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
