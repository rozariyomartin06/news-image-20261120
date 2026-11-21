#!/usr/bin/env python3
"""Draw the 20 Nov 2026 news image: a dense 1024x1024 front page.

36 stories, every continent, all first reported Friday 20 November
2026: 3 illustrated leads, 10 grid stories with illustrated banners,
a world map and 23 indexed briefs, plus a DATE CHECK that names what
was left out for being another day's news. Flat vector style only
(no faces, no photos). Run:  python3 generate.py  ->  writes entry.png.
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


def label_box(d, x, y, text, fg, bg, size=11):
    """Small label: text in fg on a bg box, returns box width."""
    fnt = font(BOLD, size)
    tw = d.textlength(text, font=fnt)
    d.rectangle([x, y, x + tw + 12, y + size + 8], fill=bg)
    d.text((x + 6, y + 4), text, font=fnt, fill=fg)
    return tw + 12


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, place="KYIV, UKRAINE", topic="WAR",
         head="Russian missiles hit three Kyiv bridges",
         body="About 110 missiles and 400 drones; at least eight killed, power and water cut. \u2014 Kyiv Independent",
         src="Kyiv Independent", region="Europe", mx=174, my=50, art="war"),
    dict(n=2, place="ODISHA, INDIA", topic="CYCLONE",
         head="Cyclone Akvan comes ashore in eastern India",
         body="Crossed the coast near Gopalpur from 8 am; 440,000 moved to shelters, no deaths. \u2014 IMD",
         src="IMD", region="Asia", mx=228, my=62, art="storm"),
    dict(n=3, place="TAIPEI \u00b7 SEOUL \u00b7 TOKYO", topic="MARKETS",
         head="AI sell-off sinks Asia's stock markets",
         body="Taiwan fell 6.2%, its worst week since 1991; Seoul -5.2%, Tokyo -5.1%. \u2014 Nikkei Asia",
         src="Nikkei Asia", region="Asia", mx=252, my=42, art="markets"),
]

GRID = [
    dict(n=4, place="ANTALYA", topic="CLIMATE",
         head="COP31 reaches its last day with no deal",
         body="Draft omits fossil fuels.",
         src="UN News", region="Europe", mx=170, my=30, art="cop31",
         label="COP31: NO DEAL"),
    dict(n=5, place="SHENZHEN", topic="DIPLOMACY",
         head="Xi hails 'full turnaround' in ties with Australia",
         body="Met the morning after APEC.",
         src="Reuters", region="Asia", mx=246, my=56, art="xi",
         label="XI \u2013 ALBANESE"),
    dict(n=6, place="COX'S BAZAR", topic="JUSTICE",
         head="Rohingya weep and pray after ICJ ruling",
         body="Camps react to ICJ judgment.",
         src="Al Jazeera", region="Asia", mx=234, my=60, art="rohingya",
         label="ROHINGYA CAMPS"),
    dict(n=7, place="BRUSSELS", topic="DIPLOMACY",
         head="Burnham seals EU-UK reset deal",
         body="Food, visas, carbon link.",
         src="Al Jazeera", region="Europe", mx=152, my=22, art="ukeu",
         label="UK\u2013EU DEAL"),
    dict(n=8, place="EASTERN POLAND", topic="SECURITY",
         head="Russian cruise missile lands in Poland",
         body="Fell in a field; airports shut.",
         src="Reuters", region="Europe", mx=164, my=28, art="poland",
         label="POLAND: MISSILE"),
    dict(n=9, place="CENTRAL IRAQ", topic="SECURITY",
         head="Iraqi army enters a militia stronghold",
         body="Troops enter Jurf al-Sakhar.",
         src="Reuters", region="Middle East", mx=190, my=56, art="iraq",
         label="IRAQ: ARMY IN"),
    dict(n=10, place="TOKYO", topic="ECONOMY",
         head="Japan's inflation picks up to 2.3%",
         body="December rate rise in view.",
         src="Reuters", region="Asia", mx=262, my=44, art="japan",
         label="JAPAN: +2.3%"),
    dict(n=11, place="MERCURY", topic="SPACE",
         head="BepiColombo reaches Mercury",
         body="Orbit burn set for Saturday.",
         src="ESA", region="Global", mx=18, my=128, art="space",
         label="MERCURY"),
    dict(n=12, place="SAN SALVADOR", topic="POLITICS",
         head="Bukele files to run for a third term",
         body="Vote is 28 February 2027.",
         src="AP", region="Americas", mx=42, my=58, art="bukele",
         label="BUKELE: 3RD BID"),
    dict(n=13, place="ITALY", topic="LABOUR",
         head="General strike over Italy's budget",
         body="Workers and students march.",
         src="Reuters", region="Europe", mx=158, my=38, art="italy",
         label="ITALY: STRIKE"),
]

INDEX = [
    (14, "WELLINGTON", "Phillips hits 118 vs India; first Kiwi with tons in all formats vs same side", "ICC", "Oceania"),
    (15, "WELLINGTON", "Nicholls 175* powers NZ to 368; 216-run stand with Phillips", "Cricbuzz", "Oceania"),
    (16, "TURKANA", "Kenya starts drilling its first oil well; crude due 1 Dec", "Capital FM", "Africa"),
    (17, "HORMUZ", "Brent $92.57 as tankers hit mines; Houthis attack Riyadh", "Reuters", "Middle East"),
    (18, "RIYADH", "Saudi coalition downs Houthi missiles; 5 drones, 1 missile Friday", "Reuters", "Middle East"),
    (19, "BLANTYRE", "Malawi fuel crisis; 4 hours for 20 litres, black market", "Al Jazeera", "Africa"),
    (20, "LAS VEGAS", "Russell fastest in wet F1 practice, 1:47.272", "Formula1.com", "Americas"),
    (21, "BEIJING", "China holds loan rates at 3.0%/3.5% for 18th month", "Reuters", "Asia"),
    (22, "SEOUL", "Ruling party moves to impeach Chief Justice Cho", "Yonhap", "Asia"),
    (23, "LVIV", "Strike on railway station kills 2; 10 hurt", "NV.ua", "Europe"),
    (24, "GANJAM", "209mm rain as Akvan crosses Odisha", "PTI", "Asia"),
    (25, "BARCELONA", "Pancreatic cancer pill shrinks tumours in 60.7%", "EORTC", "Europe"),
    (26, "BERLIN", "School pupils strike against military service", "Al Jazeera", "Europe"),
    (27, "LONDON", "General says UK runs cyber attacks abroad", "Sky News", "Europe"),
    (28, "KAMPALA", "Police told to enforce Ebola ban on rallies", "allAfrica", "Africa"),
    (29, "SYDNEY", "Australian shares fall 1.6% in sell-off", "Reuters", "Oceania"),
    (30, "ANTALYA", "Panama asks COP31 to cap world oil output", "Anadolu", "Americas"),
    (31, "ANTALYA", "EU official calls climate draft unacceptable", "RTE", "Europe"),
    (32, "TURIN", "ATP backs plan to lift player pay past $350m", "ATP", "Europe"),
    (33, "LEBANON", "Israeli air strikes hit south and east", "Anadolu", "Middle East"),
    (34, "YEMEN", "Gunmen fire on cargo ship off coast", "UKMTO", "Middle East"),
    (35, "ABUJA", "Court bars new evidence against Tinubu", "Channels TV", "Africa"),
    (36, "AFRICA", "AfDB says 22 countries in debt distress", "ThisDay", "Africa"),
]

REGIONS = [("EUROPE", 11, (30, 58, 138)), ("ASIA", 8, (180, 83, 9)),
           ("MIDDLE EAST", 5, (14, 116, 144)), ("AFRICA", 5, (22, 101, 52)),
           ("AMERICAS", 3, (126, 34, 206)), ("OCEANIA", 3, (14, 116, 144)),
           ("GLOBAL", 1, (90, 90, 90))]

BIG = [("3", "Kyiv bridges hit"), ("440,000", "moved to safety before Akvan"),
       ("-6.2%", "Taiex, worst week since 1991"),
       ("100,000", "youth visas a year in UK\u2013EU deal"),
       ("2.3%", "Japan inflation, 1-year high"),
       ("8 yrs", "BepiColombo reaches Mercury")]

# simplified continents, in a 300x150 map box
CONTINENTS = [
    [(12, 32), (55, 18), (88, 26), (95, 45), (70, 68), (42, 74), (16, 56)],   # N America
    [(86, 84), (108, 78), (120, 106), (102, 138), (88, 114)],                  # S America
    [(142, 26), (168, 18), (180, 34), (162, 50), (146, 40)],                    # Europe
    [(146, 56), (174, 50), (186, 78), (166, 104), (150, 84)],                   # Africa
    [(182, 20), (248, 14), (270, 38), (252, 68), (212, 74), (186, 48)],         # Asia
    [(250, 108), (280, 104), (286, 124), (260, 130)],                           # Australia
]


def lead_art(d, kind, x, y, w, h):
    """Illustration strip at the top of a lead card."""
    if kind == "war":
        # night sky, missile trails, skyline, bridge over the Dnipro, flames
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        for sx, sy in [(30, 14), (70, 8), (120, 18), (170, 10), (210, 16),
                       (250, 8), (290, 14), (50, 26), (150, 24), (230, 26),
                       (95, 10), (270, 24)]:
            d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                      fill=(255, 255, 255))
        # missile trails: dotted arcs from top-right down to the city
        for (x0, y0, x1, y1, x2, y2) in [(300, 4, 240, 34, 190, 66),
                                         (270, 2, 210, 30, 150, 62),
                                         (230, 6, 180, 36, 120, 70)]:
            for t in range(0, 21):
                tt = t / 20.0
                px = int((1 - tt) ** 2 * x0 + 2 * (1 - tt) * tt * x1 + tt * tt * x2)
                py = int((1 - tt) ** 2 * y0 + 2 * (1 - tt) * tt * y1 + tt * tt * y2)
                r = 2 if t % 2 == 0 else 1
                d.ellipse([x + px - r, y + py - r, x + px + r, y + py + r],
                          fill=(250, 204, 21))
            d.ellipse([x + x2 - 4, y + y2 - 4, x + x2 + 4, y + y2 + 4],
                      fill=(249, 115, 22))
        # skyline with lit windows
        for bx, bt, bw in [(8, 46, 38), (52, 30, 34), (92, 52, 30),
                           (128, 36, 36), (170, 50, 32), (208, 32, 32),
                           (246, 54, 28), (280, 40, 30)]:
            d.rectangle([x + bx, y + bt, x + bx + bw, y + h - 18], fill=(70, 70, 70))
            for wy in range(bt + 8, h - 24, 12):
                for wx in range(bx + 6, bx + bw - 4, 10):
                    if (wx + wy) % 3 == 0:
                        d.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 5],
                                    fill=(250, 204, 21))
        # river + bridge at the bottom
        d.rectangle([x, y + h - 18, x + w, y + h], fill=(30, 80, 140))
        d.rectangle([x + 14, y + h - 32, x + w - 14, y + h - 18], fill=(40, 40, 40))
        d.arc([x + 90, y + h - 34, x + 220, y + h - 6], 180, 360, fill=(40, 40, 40),
              width=4)
        for fx in (70, 250):
            d.polygon([(x + fx - 12, y + h - 32), (x + fx, y + h - 52),
                       (x + fx + 12, y + h - 32)], fill=(249, 115, 22))
            d.polygon([(x + fx - 6, y + h - 32), (x + fx, y + h - 40),
                       (x + fx + 6, y + h - 32)], fill=RED)
        label_box(d, x + 10, y + 8, "KYIV", (255, 255, 255), RED, 15)
        label_box(d, x + 10, y + 34, "3 BRIDGES HIT", RED, (255, 255, 255), 11)
    elif kind == "storm":
        # Bay of Bengal: coastline, cyclone spiral, rain, landfall marker
        d.rectangle([x, y, x + w, y + h], fill=(30, 58, 138))
        # India's east coast (tan) on the left
        d.polygon([(x, y + h), (x, y + 8), (x + 52, y + 2), (x + 84, y + 30),
                   (x + 78, y + 66), (x + 58, y + h)], fill=LAND)
        d.text((x + 8, y + 82), "BAY OF", font=font(BOLD, 10), fill=(198, 222, 235))
        d.text((x + 8, y + 94), "BENGAL", font=font(BOLD, 10), fill=(198, 222, 235))
        # spiral
        cx, cy = x + 150, y + 56
        for r in (40, 32, 24, 16):
            d.arc([cx - r, cy - r, cx + r, cy + r], 0, 270, fill=(255, 255, 255),
                  width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(250, 204, 21))
        # rain bands, right side
        for i in range(7):
            rx = x + 210 + i * 15
            d.line([rx, y + 48, rx - 8, y + 74], fill=(198, 222, 235), width=2)
        # landfall dot on the coast
        d.ellipse([x + 78 - 6, y + 44 - 6, x + 78 + 6, y + 44 + 6], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((x + 8, y + 58), "GOPALPUR", font=font(BOLD, 10), fill=INK)
        label_box(d, x + 150, y + 8, "LANDFALL \u00b7 8 AM", INK, (255, 255, 255), 12)
        label_box(d, x + 150, y + 32, "70\u201380 KM/H", INK, (250, 204, 21), 11)
    else:
        # markets: downtrend chart + closing table
        d.rectangle([x, y, x + w, y + h], fill=(38, 10, 10))
        # gridlines + chart
        for gy in (24, 48, 72):
            d.line([x + 12, y + gy, x + 176, y + gy], fill=(90, 50, 50), width=1)
        pts = [(x + 14, y + 16), (x + 52, y + 34), (x + 90, y + 52),
               (x + 128, y + 70), (x + 168, y + 92)]
        d.line(pts, fill=(239, 68, 68), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(239, 68, 68))
        d.text((x + 14, y + 92), "ASIA, FRIDAY'S CLOSE", font=font(BOLD, 9),
               fill=(198, 222, 235))
        # table
        d.rectangle([x + 186, y + 8, x + w - 8, y + h - 8], fill=(255, 255, 255))
        rows = [("TAIPEI", "-6.2%"), ("SEOUL", "-5.2%"),
                ("TOKYO", "-5.1%"), ("HONG KONG", "-1.9%")]
        for i, (mkt, val) in enumerate(rows):
            ry = y + 14 + i * 22
            d.text((x + 194, ry), mkt, font=font(BOLD, 11), fill=INK)
            d.text((x + w - 16, ry), val, font=font(BOLD, 11), fill=RED, anchor="ra")
        label_box(d, x + 10, y + 8, "AI SELL-OFF", (255, 255, 255), RED, 13)


def grid_art(d, kind, x, y, w, h, label):
    """Illustrated banner at the top of a grid cell + label box."""
    if kind == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=TEAL)
        d.ellipse([x + 14, y + 6, x + 44, y + 36], fill=(34, 139, 230))
        d.ellipse([x + 20, y + 12, x + 32, y + 22], fill=(34, 197, 94))
        d.ellipse([x + 30, y + 24, x + 40, y + 32], fill=(34, 197, 94))
        d.rounded_rectangle([x + 56, y + 6, x + 66, y + 28], radius=4,
                            outline=(255, 255, 255), width=2)
        d.ellipse([x + 52, y + 26, x + 70, y + 40], fill=RED)
        d.rectangle([x + 59, y + 12, x + 63, y + 28], fill=RED)
    elif kind == "xi":
        d.rectangle([x, y, x + w, y + h], fill=(254, 243, 199))
        # China flag
        d.rectangle([x + 12, y + 8, x + 62, y + 30], fill=(222, 0, 0))
        d.text((x + 16, y + 10), "\u2605", font=font(BOLD, 14), fill=(255, 222, 0))
        # Australia flag
        d.rectangle([x + 70, y + 8, x + 120, y + 30], fill=(0, 40, 104))
        d.text((x + 74, y + 10), "\u2605", font=font(BOLD, 10), fill=(255, 255, 255))
        d.text((x + 100, y + 12), "\u2605", font=font(BOLD, 8), fill=(255, 255, 255))
        # two figures shaking hands
        for fx in (140, 168):
            d.ellipse([x + fx, y + 8, x + fx + 10, y + 18], fill=(17, 17, 17))
            d.rectangle([x + fx + 1, y + 19, x + fx + 9, y + 36], fill=(17, 17, 17))
    elif kind == "rohingya":
        d.rectangle([x, y, x + w, y + h], fill=(22, 101, 52))
        for tx in (16, 56, 96, 136):
            d.polygon([(x + tx, y + 34), (x + tx + 14, y + 12),
                       (x + tx + 28, y + 34)], fill=(255, 253, 245))
            d.ellipse([x + tx + 34, y + 22, x + tx + 40, y + 28], fill=(250, 204, 21))
            d.rectangle([x + tx + 35, y + 29, x + tx + 39, y + 38], fill=(250, 204, 21))
    elif kind == "ukeu":
        d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
        # EU stars circle
        for i in range(8):
            import math
            a = i * math.pi / 4
            sx = x + 34 + int(12 * math.cos(a))
            sy = y + 20 + int(12 * math.sin(a))
            d.text((sx - 3, sy - 4), "\u2605", font=font(BOLD, 7), fill=(255, 222, 0))
        # Union Jack (simplified)
        d.rectangle([x + 66, y + 6, x + 122, y + 34], fill=(1, 33, 105))
        d.line([x + 66, y + 6, x + 122, y + 34], fill=(255, 255, 255), width=3)
        d.line([x + 122, y + 6, x + 66, y + 34], fill=(255, 255, 255), width=3)
        d.line([x + 94, y + 6, x + 94, y + 34], fill=RED, width=4)
        d.line([x + 66, y + 20, x + 122, y + 20], fill=RED, width=4)
    elif kind == "poland":
        d.rectangle([x, y, x + w, y + h], fill=(134, 239, 172))
        d.line([x + 20, y + 30, x + 120, y + 8], fill=(90, 90, 90), width=3)
        d.polygon([(x + 120, y + 8), (x + 104, y + 4), (x + 112, y + 18)],
                  fill=(90, 90, 90))
        d.polygon([(x + 18, y + 30), (x + 30, y + 22), (x + 36, y + 32)],
                  fill=(249, 115, 22))
        d.ellipse([x + 130, y + 24, x + 160, y + 34], fill=(90, 90, 90))
        for tx in (150, 170):
            d.polygon([(x + tx, y + 34), (x + tx + 6, y + 18),
                       (x + tx + 12, y + 34)], fill=(22, 101, 52))
    elif kind == "iraq":
        d.rectangle([x, y, x + w, y + h], fill=(254, 215, 170))
        for tx in (16, 76):
            d.rectangle([x + tx, y + 20, x + tx + 44, y + 32], fill=(22, 101, 52))
            d.rectangle([x + tx + 14, y + 10, x + tx + 30, y + 20], fill=(22, 101, 52))
            d.line([x + tx + 30, y + 12, x + tx + 44, y + 8], fill=(22, 101, 52),
                   width=3)
        d.line([x + 140, y + 34, x + 140, y + 10], fill=(120, 53, 15), width=3)
        for a in range(5):
            import math
            ang = a * 3.14159 / 2.5 - 1.2
            d.line([x + 140, y + 12, x + 140 + int(12 * math.cos(ang)),
                    y + 12 + int(10 * math.sin(ang))], fill=(22, 101, 52), width=2)
    elif kind == "japan":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.ellipse([x + 12, y + 6, x + 40, y + 34], fill=RED)
        for i, bh in enumerate((8, 14, 20, 28)):
            d.rectangle([x + 56 + i * 18, y + 36 - bh, x + 56 + i * 18 + 12, y + 36],
                        fill=(90, 90, 90))
        d.text((x + 140, y + 10), "+2.3%", font=font(BOLD, 15), fill=RED)
    elif kind == "space":
        d.rectangle([x, y, x + w, y + h], fill=(15, 23, 42))
        for sx, sy in [(120, 8), (150, 20), (170, 10), (130, 30), (185, 28)]:
            d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                      fill=(255, 255, 255))
        d.ellipse([x + 14, y + 4, x + 50, y + 40], fill=(160, 160, 160))
        d.ellipse([x + 22, y + 12, x + 30, y + 20], fill=(120, 120, 120))
        d.ellipse([x + 34, y + 24, x + 40, y + 30], fill=(120, 120, 120))
        d.line([x + 60, y + 20, x + 100, y + 14], fill=(250, 204, 21), width=2)
        d.ellipse([x + 98, y + 11, x + 106, y + 19], fill=(250, 204, 21))
        d.text((x + 112, y + 22), "8 YRS", font=font(BOLD, 9),
               fill=(255, 255, 255))
    elif kind == "bukele":
        d.rectangle([x, y, x + w, y + h], fill=(30, 58, 138))
        d.rectangle([x + 60, y + 14, x + 110, y + 36], fill=(255, 255, 255))
        d.rectangle([x + 76, y + 18, x + 94, y + 22], fill=INK)
        d.rectangle([x + 78, y + 6, x + 92, y + 16], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.text((x + 118, y + 18), "FEB 2027", font=font(BOLD, 10),
               fill=(255, 255, 255))
        d.text((x + 14, y + 18), "\u2713", font=font(BOLD, 18), fill=(250, 204, 21))
    else:  # italy: crowd of protesters with signs
        d.rectangle([x, y, x + w, y + h], fill=(254, 242, 242))
        for i, px in enumerate((18, 48, 78, 108, 138, 168)):
            d.ellipse([x + px, y + 10, x + px + 12, y + 22], fill=(17, 17, 17))
            d.rectangle([x + px + 1, y + 23, x + px + 11, y + 38], fill=(17, 17, 17))
            if i % 2 == 0:
                d.rectangle([x + px - 6, y + 2, x + px + 18, y + 12],
                            fill=RED if i % 4 == 0 else (22, 101, 52))
    # label box, top-left over the scene
    label_box(d, x + 4, y + 4, label, (255, 255, 255), RED, 10)


def main():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)
    d.rectangle([10, 10, W - 11, H - 11], outline=RED, width=2)

    # --- kicker + masthead ---
    d.text((16, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 16), fill=RED)
    d.text((W - 16, 18), "36 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY",
           font=font(BOLD, 16), fill=INK, anchor="ra")
    d.text((512, 38), "Friday 20 November 2026", font=font(SERIF, 46),
           fill=INK, anchor="ma")
    d.text((512, 88),
           "Russian missiles hit Kyiv's bridges \u00b7 Cyclone Akvan strikes India \u00b7 An AI sell-off sinks Asia's markets",
           font=font(REG, 15), fill=RED, anchor="ma")
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

    # --- grid: 10 stories, 2 rows x 5, each with an illustrated banner ---
    gw, gh, gy = 196, 116, 414
    for i, s in enumerate(GRID):
        gx = 16 + (i % 5) * (gw + 4)
        gy2 = gy + (i // 5) * (gh + 4)
        d.rectangle([gx, gy2, gx + gw, gy2 + gh], fill=CREAM, outline=INK, width=1)
        grid_art(d, s["art"], gx + 1, gy2 + 1, gw - 2, 40, s["label"])
        d.text((gx + 8, gy2 + 46), f"{s['n']}  {s['place']} \u00b7 {s['topic']}",
               font=font(BOLD, 10), fill=RED)
        hl = wrap(d, s["head"], font(BOLD, 13), gw - 16)
        draw_lines(d, hl, gx + 8, gy2 + 62, font(BOLD, 13), INK, 15)
        bd = wrap(d, s["body"], font(REG, 11), gw - 16)
        draw_lines(d, bd, gx + 8, gy2 + 62 + len(hl) * 15 + 2,
                   font(REG, 11), (51, 51, 51), 13)

    # --- map + index ---
    my = 660
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
    d.text((16, map_y + map_h + 20), "11 is in space (Mercury).",
           font=font(REG, 11), fill=GREY)
    # index, two columns: 12 in col 1, 11 in col 2
    ix0, ix1 = 340, 680
    d.text((ix0, my), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES",
           font=font(BOLD, 13), fill=RED)
    d.text((ix0, my + 16), "place \u00b7 what happened \u00b7 source", font=font(REG, 11), fill=GREY)
    for j, (n, place, head, src, region) in enumerate(INDEX):
        col = ix0 if j < 12 else ix1
        yy = my + 36 + (j % 12) * 21
        d.text((col, yy), str(n), font=font(BOLD, 10), fill=RED)
        line = f"{place} \u2014 {head}. \u2014 {src}"
        col_w = (ix1 - ix0 - 28) if j < 12 else (W - 16 - ix1 - 28)
        ln = wrap(d, line, font(REG, 9), col_w)
        draw_lines(d, ln, col + 24, yy, font(REG, 9), INK, 11)

    # --- date check + sources ---
    d.rectangle([16, 956, W - 16, 994], outline=RED, width=2)
    d.text((512, 960),
           "DATE CHECK \u2713  Every story on this page happened, or was first reported, on Friday 20 November 2026.",
           font=font(BOLD, 11), fill=INK, anchor="ma")
    d.text((512, 976),
           "LEFT OUT: 19 NOV: Shenzhen summit \u00b7 ICJ ruling \u00b7 GTA VI \u00b7 Anthropic IPO \u00b7 Somalia envoy out \u00b7 Haiti raid \u00b7 JPMorgan leak \u00b7 Venezuela ties \u00b7 Senegal boat \u00b7 Senegal decree \u00b7 Tonga drought",
           font=font(REG, 10), fill=GREY, anchor="ma")
    d.text((512, 998),
           "Claims are attributed, not stated as fact \u00b7 Pictures and map: original, drawn in code \u00b7 Sources: Reuters, AP, WSJ, ET, The Hindu, NDTV, BBC, Al Jazeera, Kyiv Independent, ICC, ATP, UKMTO \u00b7 2026-11-20",
           font=font(REG, 10), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
