#!/usr/bin/env python3
"""Draw the 20 Nov 2026 news image: a dense 1024x1024 front page.

33 stories, every continent, all first reported Friday 20 November
2026: 3 illustrated leads, 10 grid stories, a world map and 20 indexed
briefs, plus a DATE CHECK that names what was left out for being
another day's news. Flat vector style only (no faces, no photos).
Run:  python3 generate.py   ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (22, 40, 63)
TEAL = (14, 116, 144)
CREAM = (255, 253, 245)
GREY = (90, 90, 90)
LIGHT = (226, 232, 240)
SEA = (198, 222, 235)
LAND = (232, 214, 170)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def _disc(d, cx, cy, r, flag_img):
    mask = Image.new("L", (2 * r, 2 * r), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    img.paste(flag_img, (cx - r, cy - r), mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)


def flag_us(d, cx, cy, r):
    f = Image.new("RGB", (2 * r, 2 * r), (255, 255, 255))
    fd = ImageDraw.Draw(f)
    for i in range(13):
        y0 = i * (2 * r) // 13
        y1 = (i + 1) * (2 * r) // 13
        fd.rectangle([0, y0, 2 * r, y1], fill=RED if i % 2 == 0 else (255, 255, 255))
    fd.rectangle([0, 0, int(2 * r * 0.4), int(2 * r * 7 / 13)], fill=(30, 58, 138))
    _disc(d, cx, cy, r, f)


def flag_cn(d, cx, cy, r):
    f = Image.new("RGB", (2 * r, 2 * r), (222, 0, 0))
    fd = ImageDraw.Draw(f)
    fd.text((int(2 * r * 0.14), int(2 * r * 0.10)), "\u2605",
            font=font(BOLD, int(r * 0.9)), fill=(255, 222, 0))
    _disc(d, cx, cy, r, f)


def flag_ru(d, cx, cy, r):
    f = Image.new("RGB", (2 * r, 2 * r), (255, 255, 255))
    fd = ImageDraw.Draw(f)
    fd.rectangle([0, 0, 2 * r, int(2 * r / 3)], fill=(255, 255, 255))
    fd.rectangle([0, int(2 * r / 3), 2 * r, int(4 * r / 3)], fill=(0, 57, 166))
    fd.rectangle([0, int(4 * r / 3), 2 * r, 2 * r], fill=(213, 0, 50))
    _disc(d, cx, cy, r, f)


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, place="ANTALYA", topic="CLIMATE",
         head="COP31 ends with no deal as fossil fuels vanish",
         body="Talks run past Friday's deadline; the draft drops the $120bn aid goal. \u2014 Reuters",
         src="Reuters", region="Europe", mx=174, my=50, art="climate"),
    dict(n=2, place="ODISHA", topic="STORM",
         head="Cyclone Akvan hits Odisha coast, spares lives",
         body="Landfall at Gopalpur at 70\u201380 km/h; no major damage after 300,000 were evacuated. \u2014 IMD",
         src="IMD", region="Asia", mx=228, my=62, art="storm"),
    dict(n=3, place="KYIV", topic="WAR",
         head="Russia's overnight strikes kill 8 in Kyiv",
         body="Bridges hit in the capital; 28 hurt across nine regions as peace talks stall. \u2014 AP",
         src="AP", region="Europe", mx=170, my=30, art="war"),
]

GRID = [
    dict(n=4, place="WARSAW", topic="SECURITY",
         head="Russia breaches Polish airspace",
         body="Three objects \u2014 two missiles, one drone \u2014 cross overnight.",
         src="Just Security", region="Europe", mx=152, my=22, icon="missile"),
    dict(n=5, place="TALLINN", topic="SECURITY",
         head="Estonia shuts Russia border",
         body="Crossing closed for at least six months; Moscow vows a reply.",
         src="Just Security", region="Europe", mx=None, my=None, icon="flag"),
    dict(n=6, place="BRUSSELS", topic="DIPLOMACY",
         head="UK and EU seal food and youth deals",
         body="100,000 under-30s can move for 3 years; fees put off.",
         src="Reuters", region="Europe", mx=None, my=None, icon="march"),
    dict(n=7, place="WASHINGTON", topic="WAR",
         head="Kushner floated NATO-for-Donbas swap",
         body="WSJ: Ukraine would cede land for membership; Kyiv balks.",
         src="WSJ", region="Americas", mx=None, my=None, icon="gavel"),
    dict(n=8, place="BAGHDAD", topic="SECURITY",
         head="Iraq moves on Iran-backed militia",
         body="Troops deploy in Jurf al-Sakhar to curb oil smuggling.",
         src="Just Security", region="Middle East", mx=190, my=56, icon="flag"),
    dict(n=9, place="NEW YORK", topic="MARKETS",
         head="AMD crashes 13% on China bombshell",
         body="Short-seller Hunterbrook's report hits the chipmaker.",
         src="ET", region="Americas", mx=55, my=45, icon="chart"),
    dict(n=10, place="TEHRAN", topic="SECURITY",
         head="Iran rejects US bioweapon claims",
         body="Tehran denies developing biological and chemical arms.",
         src="ET", region="Middle East", mx=204, my=46, icon="flag"),
    dict(n=11, place="MEXICO CITY", topic="DIPLOMACY",
         head="Sheinbaum's economy flight goes viral",
         body="21-hour trip to APEC wins praise on Chinese internet.",
         src="Bloomberg", region="Americas", mx=42, my=58, icon="flag"),
    dict(n=12, place="SYDNEY", topic="SECURITY",
         head="Sydney man charged over car-bomb research",
         body="Police say he studied how to build a vehicle bomb.",
         src="NZ Herald", region="Oceania", mx=272, my=118, icon="gavel"),
    dict(n=13, place="LONDON", topic="JUSTICE",
         head="RAF Fairford suspects face 2027 trial",
         body="Two men charged over the September airbase incident.",
         src="Just Security", region="Europe", mx=None, my=None, icon="gavel"),
]

INDEX = [
    (14, "KHARTOUM", "Sudan suspends all imports from Kenya", "BBC", "Africa"),
    (15, "DARFUR", "Darfur women demand protection, war-crimes trials", "Radio Dabanga", "Africa"),
    (16, "NAIROBI", "Chief Justice vows purge of corrupt judges", "The Standard", "Africa"),
    (17, "KENEMA", "Teen gets 100 years for teacher's murder", "Calabash", "Africa"),
    (18, "MOGADISHU", "Gulf bloc condemns Somalia's UAE remarks", "AllAfrica", "Africa"),
    (19, "NAIROBI", "Kenya opposition seeks election law changes", "Reports", "Africa"),
    (20, "KAMPALA", "Uganda curbs gatherings near Ebola-risk border", "Reports", "Africa"),
    (21, "DAR ES SALAAM", "Tanzania re-elected to UN telecom council", "Reports", "Africa"),
    (22, "DHAKA", "Tarique Rahman blames India for Bangladesh violence", "ET", "Asia"),
    (23, "ISLAMABAD", "Pakistan army says 22 militants killed in raids", "The Hindu", "Asia"),
    (24, "NEW DELHI", "IAF's active Rafale jets down to 32", "FlightGlobal", "Asia"),
    (25, "TAIPEI", "TSMC tightens China AI chip curbs", "ET", "Asia"),
    (26, "WASHINGTON", "US to put $1,000 in retirement accounts from 2027", "ET", "Americas"),
    (27, "WASHINGTON", "Trump says Vance erred on Iran war critique", "WSJ", "Americas"),
    (28, "WASHINGTON", "Trump and Xi want moderate AI rules", "ET", "Global"),
    (29, "BRUSSELS", "EU confirms first AI-assisted cyberattack", "ET", "Europe"),
    (30, "CINCINNATI", "P&G targets $10bn in productivity savings", "ET", "Americas"),
    (31, "WELLINGTON", "India hit back on day two of NZ Test", "EIN", "Oceania"),
    (32, "NIUE", "Niue wins Earthshot 2026 prize", "SMC", "Oceania"),
    (33, "WELLINGTON", "NZ rejects becoming Australia's 7th state", "The Post", "Oceania"),
]

REGIONS = [("ASIA", 5, (180, 83, 9)), ("MIDDLE EAST", 2, (14, 116, 144)),
           ("EUROPE", 7, (30, 58, 138)), ("AFRICA", 8, (22, 101, 52)),
           ("AMERICAS", 6, (126, 34, 206)), ("OCEANIA", 4, (14, 116, 144)),
           ("GLOBAL", 1, (90, 90, 90))]

BIG = [("92,000", "people at COP31, a record"), ("300,000", "evacuated before Akvan"),
       ("8", "killed in Kyiv strikes"), ("100,000", "in UK\u2013EU youth deal"),
       ("13%", "AMD's crash on China report"), ("$10bn", "P&G productivity savings")]

# simplified continents, in a 300x150 map box
CONTINENTS = [
    [(12, 32), (55, 18), (88, 26), (95, 45), (70, 68), (42, 74), (16, 56)],   # N America
    [(86, 84), (108, 78), (120, 106), (102, 138), (88, 114)],                  # S America
    [(142, 26), (168, 18), (180, 34), (162, 50), (146, 40)],                    # Europe
    [(146, 56), (174, 50), (186, 78), (166, 104), (150, 84)],                   # Africa
    [(182, 20), (248, 14), (270, 38), (252, 68), (212, 74), (186, 48)],         # Asia
    [(250, 108), (280, 104), (286, 124), (260, 130)],                           # Australia
]


def icon(d, kind, x, y, s, color):
    """Tiny pictogram inside a square of side s at (x, y)."""
    if kind == "bridge":
        d.line([x, y + s * 0.7, x + s, y + s * 0.7], fill=color, width=3)
        for px in (x + s * 0.2, x + s * 0.5, x + s * 0.8):
            d.line([px, y + s * 0.2, px, y + s * 0.7], fill=color, width=2)
        d.arc([x, y + s * 0.3, x + s, y + s * 0.9], 0, 180, fill=color, width=2)
    elif kind == "missile":
        d.line([x + s * 0.2, y + s * 0.8, x + s * 0.8, y + s * 0.2], fill=color, width=3)
        d.polygon([(x + s * 0.8, y + s * 0.2), (x + s * 0.55, y + s * 0.25),
                   (x + s * 0.75, y + s * 0.45)], fill=color)
        for i in range(3):
            d.ellipse([x + s * 0.15 - i * 3, y + s * 0.75 + i * 3,
                       x + s * 0.25 - i * 3, y + s * 0.85 + i * 3],
                      outline=color, width=1)
    elif kind == "cyclone":
        cx, cy = x + s / 2, y + s / 2
        for r in range(int(s * 0.45), 3, -3):
            d.arc([cx - r, cy - r, cx + r, cy + r], 0, 270, fill=color, width=2)
    elif kind == "gavel":
        d.line([x + s * 0.2, y + s * 0.7, x + s * 0.8, y + s * 0.3], fill=color, width=3)
        d.rectangle([x + s * 0.55, y + s * 0.1, x + s * 0.95, y + s * 0.3], fill=color)
        d.rectangle([x + s * 0.1, y + s * 0.75, x + s * 0.9, y + s * 0.85], fill=color)
    elif kind == "flag":
        d.line([x + s * 0.25, y + s * 0.1, x + s * 0.25, y + s * 0.9], fill=color, width=2)
        d.polygon([(x + s * 0.25, y + s * 0.1), (x + s * 0.85, y + s * 0.3),
                   (x + s * 0.25, y + s * 0.5)], fill=color)
    elif kind == "chart":
        pts = [(x + s * 0.1, y + s * 0.7), (x + s * 0.3, y + s * 0.5),
               (x + s * 0.5, y + s * 0.6), (x + s * 0.7, y + s * 0.3),
               (x + s * 0.9, y + s * 0.15)]
        d.line(pts, fill=color, width=3)
        d.line([x + s * 0.1, y + s * 0.85, x + s * 0.9, y + s * 0.85], fill=color, width=2)
    elif kind == "game":
        d.rounded_rectangle([x + s * 0.1, y + s * 0.3, x + s * 0.9, y + s * 0.75],
                            radius=6, outline=color, width=2)
        d.ellipse([x + s * 0.62, y + s * 0.45, x + s * 0.72, y + s * 0.55], fill=color)
        d.ellipse([x + s * 0.76, y + s * 0.45, x + s * 0.86, y + s * 0.55], fill=color)
    elif kind == "march":
        for i, px in enumerate((0.2, 0.45, 0.7)):
            d.ellipse([x + s * px, y + s * 0.15, x + s * (px + 0.12), y + s * 0.3], fill=color)
            d.rectangle([x + s * px, y + s * 0.32, x + s * (px + 0.12), y + s * 0.75],
                        fill=color)
    elif kind == "tanker":
        d.rectangle([x + s * 0.1, y + s * 0.55, x + s * 0.9, y + s * 0.8], fill=color)
        d.rectangle([x + s * 0.6, y + s * 0.35, x + s * 0.75, y + s * 0.55], fill=color)
        for fx in (0.2, 0.4, 0.6):
            d.polygon([(x + s * fx, y + s * 0.35), (x + s * (fx + 0.07), y + s * 0.12),
                       (x + s * (fx + 0.14), y + s * 0.35)], fill=(249, 115, 22))


def lead_art(d, topic, x, y, w, h):
    """Illustration strip at the top of a lead card."""
    if topic == "climate":
        # globe + thermometer, 1.5C limit breached
        d.rectangle([x, y, x + w, y + h], fill=(14, 116, 144))
        d.ellipse([x + 18, y + 14, x + 98, y + 94], fill=(34, 139, 230))
        d.ellipse([x + 34, y + 28, x + 58, y + 48], fill=(34, 197, 94))
        d.ellipse([x + 62, y + 56, x + 88, y + 76], fill=(34, 197, 94))
        d.ellipse([x + 26, y + 62, x + 44, y + 78], fill=(34, 197, 94))
        # thermometer
        d.rounded_rectangle([x + w - 52, y + 16, x + w - 32, y + 78], radius=9,
                            outline=(255, 255, 255), width=3)
        d.ellipse([x + w - 56, y + 70, x + w - 28, y + 98], fill=RED)
        d.rectangle([x + w - 46, y + 30, x + w - 38, y + 76], fill=RED)
        d.rectangle([x + 108, y + 22, x + w - 70, y + 52], fill=(255, 255, 255))
        d.text((x + 116, y + 29), "1.5\u00b0C LIMIT", font=font(BOLD, 15), fill=RED)
        d.rectangle([x + 108, y + 62, x + w - 70, y + 92], fill=RED)
        d.text((x + 116, y + 68), "BREACHED", font=font(BOLD, 17), fill=(255, 255, 255))
    elif topic == "storm":
        # cyclone spiral + rain + coastline, wind banner
        d.rectangle([x, y, x + w, y + h], fill=(30, 58, 138))
        cx, cy = x + 72, y + 54
        for r in (38, 30, 22, 14):
            d.arc([cx - r, cy - r, cx + r, cy + r], 0, 270, fill=(255, 255, 255), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(250, 204, 21))
        # rain, right half below the banner
        for i in range(6):
            rx = x + 158 + i * 24
            d.line([rx, y + 50, rx - 10, y + 76], fill=(198, 222, 235), width=2)
        # coastline strip
        d.rectangle([x, y + h - 14, x + w, y + h], fill=LAND)
        d.rectangle([x + 150, y + 12, x + w - 12, y + 38], fill=(250, 204, 21))
        d.text((x + 158, y + 18), "70\u201380 KM/H", font=font(BOLD, 14), fill=INK)
    else:
        # war: skyline, flames, smoke, KYIV banner
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        for bx, bt, bw, bh in [(16, 48, 40, 60), (64, 30, 36, 78), (108, 56, 32, 52),
                               (148, 38, 38, 70), (194, 52, 36, 56), (238, 34, 34, 74),
                               (280, 58, 22, 50)]:
            d.rectangle([x + bx, y + bt, x + bx + bw, y + h], fill=(90, 90, 90))
        # flames on two buildings
        for fx, fy in [(x + 74, y + 30), (x + 252, y + 34)]:
            d.polygon([(fx - 14, fy + 26), (fx, fy - 12), (fx + 14, fy + 26)],
                      fill=(249, 115, 22))
            d.polygon([(fx - 8, fy + 26), (fx, fy + 2), (fx + 8, fy + 26)],
                      fill=RED)
        # smoke
        for sx, sy, sr in [(x + 74, y + 8, 10), (x + 252, y + 12, 9), (x + 160, y + 16, 8)]:
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(160, 160, 160))
        d.rectangle([x + 12, y + 10, x + 76, y + 36], fill=RED)
        d.text((x + 44, y + 14), "KYIV", font=font(BOLD, 16), fill=(255, 255, 255),
               anchor="ma")


def main():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)
    d.rectangle([10, 10, W - 11, H - 11], outline=RED, width=2)

    # --- kicker + masthead ---
    d.text((16, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 16), fill=RED)
    d.text((W - 16, 18), "33 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY",
           font=font(BOLD, 16), fill=INK, anchor="ra")
    d.text((512, 38), "Friday 20 November 2026", font=font(SERIF, 46),
           fill=INK, anchor="ma")
    d.text((512, 88),
           "COP31 ends with no deal \u00b7 Cyclone Akvan hits Odisha \u00b7 Russia strikes Kyiv",
           font=font(REG, 16), fill=RED, anchor="ma")
    d.line([16, 112, W - 16, 112], fill=INK, width=2)

    # --- stats strip: region blocks + big numbers ---
    x = 16
    seg_w = (W - 32) / 7
    for name, count, color in REGIONS:
        d.rectangle([x, 118, x + seg_w - 2, 136], fill=color)
        d.text((x + seg_w / 2, 120), f"{name} {count}", font=font(BOLD, 11),
               fill=(255, 255, 255), anchor="ma")
        x += seg_w
    x = 16
    col_w = (W - 32) / 6
    for big, label in BIG:
        d.text((x + col_w / 2, 142), big, font=font(BOLD, 22), fill=INK, anchor="ma")
        lab = wrap(d, label, font(REG, 11), col_w - 8)
        draw_lines(d, lab, x + 4, 168, font(REG, 11), GREY, 13)
        x += col_w
    d.line([16, 190, W - 16, 190], fill=INK, width=2)

    # --- three leads ---
    lead_w, lead_h, lead_y = 322, 210, 196
    for i, s in enumerate(LEADS):
        lx = 16 + i * (lead_w + 8)
        d.rectangle([lx, lead_y, lx + lead_w, lead_y + lead_h], fill=CREAM,
                    outline=INK, width=2)
        lead_art(d, s["art"], lx + 2, lead_y + 2, lead_w - 4, 108)
        d.text((lx + 10, lead_y + 118), f"{s['n']}  {s['place']} \u00b7 {s['topic']}",
               font=font(BOLD, 12), fill=RED)
        hl = wrap(d, s["head"], font(BOLD, 17), lead_w - 20)
        draw_lines(d, hl, lx + 10, lead_y + 136, font(BOLD, 17), INK, 20)
        bd = wrap(d, s["body"], font(REG, 12), lead_w - 20)
        draw_lines(d, bd, lx + 10, lead_y + 136 + len(hl) * 20 + 3,
                   font(REG, 12), (51, 51, 51), 15)

    # --- grid: 10 stories, 2 rows x 5 ---
    gw, gh, gy = 196, 112, 414
    for i, s in enumerate(GRID):
        gx = 16 + (i % 5) * (gw + 4)
        gy2 = gy + (i // 5) * (gh + 4)
        d.rectangle([gx, gy2, gx + gw, gy2 + gh], fill=CREAM, outline=INK, width=1)
        icon(d, s["icon"], gx + 8, gy2 + 8, 26, RED)
        d.text((gx + 42, gy2 + 8), f"{s['n']}", font=font(BOLD, 15), fill=RED)
        d.text((gx + 42, gy2 + 26), f"{s['place']} \u00b7 {s['topic']}",
               font=font(BOLD, 10), fill=RED)
        hl = wrap(d, s["head"], font(BOLD, 13), gw - 16)
        draw_lines(d, hl, gx + 8, gy2 + 44, font(BOLD, 13), INK, 15)
        bd = wrap(d, s["body"], font(REG, 11), gw - 16)
        draw_lines(d, bd, gx + 8, gy2 + 44 + len(hl) * 15 + 2,
                   font(REG, 11), (51, 51, 51), 13)

    # --- map + index ---
    my = 650
    d.text((16, my), "WHERE IT HAPPENED", font=font(BOLD, 13), fill=RED)
    d.text((16, my + 16), "numbers match the stories",
           font=font(REG, 11), fill=GREY)
    map_x, map_y, map_w, map_h = 16, my + 36, 300, 150
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA,
                outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px, map_y + py) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(180, 160, 120))
    for s in LEADS + GRID:
        if s.get("mx") is None:
            continue
        px, py = map_x + s["mx"], map_y + s["my"]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 2), str(s["n"]), font=font(BOLD, 10), fill=(255, 255, 255),
               anchor="mm")
    d.text((16, map_y + map_h + 6), "Red numbers mark stories 1\u201313.",
           font=font(REG, 11), fill=GREY)
    # index, two columns: one line per brief, source inline
    ix0, ix1 = 340, 680
    d.text((ix0, my), "ALSO ON FRIDAY 20 NOVEMBER 2026", font=font(BOLD, 13), fill=RED)
    d.text((ix0, my + 16), "place \u00b7 what happened \u00b7 source", font=font(REG, 11), fill=GREY)
    for j, (n, place, head, src, region) in enumerate(INDEX):
        col = ix0 if j < 10 else ix1
        yy = my + 36 + (j % 10) * 25
        d.text((col, yy), str(n), font=font(BOLD, 11), fill=RED)
        line = f"{place} \u2014 {head}. \u2014 {src}"
        ln = wrap(d, line, font(REG, 10), (ix1 - ix0 - 30) if j < 10 else (W - 16 - ix1 - 30))
        draw_lines(d, ln, col + 24, yy, font(REG, 10), INK, 12)

    # --- date check + sources ---
    d.rectangle([16, 946, W - 16, 984], outline=RED, width=2)
    d.text((512, 950),
           "DATE CHECK \u2713  Every story on this page happened, or was first reported, on Friday 20 November 2026.",
           font=font(BOLD, 12), fill=INK, anchor="ma")
    d.text((512, 966),
           "LEFT OUT AS OF OTHER DAYS' NEWS: 19 NOV: Shenzhen summit \u00b7 ICJ ruling \u00b7 GTA VI \u00b7 Anthropic IPO \u00b7 Somalia envoy out \u00b7 Haiti raid \u00b7 JPMorgan leak \u00b7 Venezuela ties",
           font=font(REG, 11), fill=GREY, anchor="ma")
    d.text((512, 992),
           "Claims are attributed, not stated as fact \u00b7 Pictures and map: original, drawn in code \u00b7 Sources: Reuters, AP, WSJ, ET, The Hindu, NDTV, Just Security, BBC, SMC \u00b7 2026-11-20",
           font=font(REG, 10), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
