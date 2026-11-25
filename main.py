# news-image-20261125: sum up Wednesday 25 November 2026 in one image.
# Pure Python 3 standard library. No network, no randomness, no time.
# Draws a 1024x1024 PNG newspaper front page: masthead, world map with
# 10 numbered markers, 8 drawn vector scenes, 34 region briefs, sources.
# Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
import os
import struct
import zlib

W, H = 1024, 1024

# ---- palette: warm off-white paper, dark blue ink, red date accents ----
PAPER = (247, 242, 231)
INK = (22, 41, 77)
NAVY = (22, 41, 77)
NAVY_LT = (38, 64, 110)
RED = (178, 44, 32)
WHITE = (250, 248, 243)
CARD = (255, 253, 247)
LINE = (196, 186, 168)
GOLD = (176, 124, 32)
SEA = (168, 196, 205)
LAND = (222, 208, 178)
LAND_EDGE = (150, 138, 108)

REGION_COLORS = {
    "ASIA": (14, 124, 123),
    "MIDEAST": (176, 124, 32),
    "EUROPE": (43, 94, 167),
    "AFRICA": (74, 124, 47),
    "AMERICAS": (176, 58, 46),
    "OCEANIA": (108, 79, 161),
    "WORLD": (90, 107, 124),
}

# ---- 5x7 bitmap font, hand-drawn, one glyph per printable ASCII char ----
# Each glyph is 7 rows of 5 bits, written as strings of '1'/'0'.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "00010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    'q': ("00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("00100", "00100", "11110", "00100", "00100", "00100", "00011"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "10001", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    ',': ("00000", "00000", "00000", "00000", "00100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "00000", "00100"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    ':': ("00000", "00100", "00000", "00000", "00000", "00100", "00000"),
    ';': ("00000", "00100", "00000", "00000", "00000", "00100", "01000"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '@': ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    '[': ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    '\\': ("10000", "01000", "01000", "00100", "00100", "00010", "00010"),
    ']': ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    '^': ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '`': ("01000", "00100", "00010", "00000", "00000", "00000", "00000"),
    '{': ("00010", "00100", "00100", "01100", "00100", "00100", "00010"),
    '|': ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    '}': ("01000", "00100", "00100", "00110", "00100", "00100", "01000"),
    '~': ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
    '\u2022': ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}

BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")


def text_width(s, scale):
    return len(s) * 6 * scale - scale if s else 0


def wrap_text(s, max_chars):
    """Greedy word wrap; overlong words are hard-split."""
    lines, cur = [], ""
    for word in s.split(" "):
        if len(word) > max_chars:
            if cur:
                lines.append(cur)
                cur = ""
            while len(word) > max_chars:
                lines.append(word[:max_chars])
                word = word[max_chars:]
            cur = word
            continue
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set_px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c):
        self.fill_rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.fill_rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            if t == 1:
                self.set_px(x, y, c)
            else:
                self.fill_rect(x - t // 2, y - t // 2, t, t, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, c, fill=False):
        x, y, d = 0, r, 1 - r
        pts = []
        while x <= y:
            for px, py in ((x, y), (y, x), (-x, y), (-y, x),
                           (x, -y), (y, -x), (-x, -y), (-y, -x)):
                pts.append((cx + px, cy + py))
            if fill:
                self.hline(cx - x, cy + y, 2 * x + 1, c)
                self.hline(cx - x, cy - y, 2 * x + 1, c)
                self.hline(cx - y, cy + x, 2 * y + 1, c)
                self.hline(cx - y, cy - x, 2 * y + 1, c)
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
        if not fill:
            for px, py in pts:
                self.set_px(px, py, c)

    def polygon(self, points, c):
        """Scanline fill of a simple polygon (list of (x, y))."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.hline(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), c)

    def polyline(self, points, c, t=1):
        for i in range(len(points) - 1):
            self.line(points[i][0], points[i][1],
                      points[i + 1][0], points[i + 1][1], c, t)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, c)
            cx += 6 * scale
        return cx

    def text_center(self, x, y, w, s, scale, c):
        tw = text_width(s, scale)
        self.text(x + max(0, (w - tw) // 2), y, s, scale, c)


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", comp) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


# ---- world map: simplified continent polygons in (lon, lat) ----
# Equirectangular projection; Mediterranean/Black Sea cut out in sea colour.
NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-65, 62), (-55, 52), (-60, 47),
                 (-70, 44), (-75, 35), (-80, 32), (-81, 26), (-84, 30),
                 (-90, 21), (-97, 26), (-105, 20), (-110, 23), (-117, 33),
                 (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)]
SOUTH_AMERICA = [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0),
                 (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-58, -35),
                 (-65, -41), (-68, -52), (-70, -54), (-73, -44), (-72, -30),
                 (-70, -18), (-77, -12), (-80, -5), (-81, 1), (-80, 7)]
AFRICA = [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
          (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (40, -20),
          (33, -26), (26, -34), (19, -35), (15, -27), (12, -18), (9, 4),
          (-8, 5), (-13, 8)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53),
           (8, 57), (10, 59), (5, 60), (5, 62), (12, 65), (18, 69),
           (25, 71), (32, 70), (40, 68), (50, 69), (60, 69), (70, 72),
           (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
           (140, 72), (150, 70), (160, 70), (170, 67), (178, 65), (170, 60),
           (162, 56), (158, 52), (150, 60), (142, 59), (140, 53), (135, 44),
           (130, 42), (127, 40), (122, 38), (120, 32), (118, 25), (110, 21),
           (108, 18), (105, 10), (100, 8), (98, 10), (95, 16), (92, 21),
           (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (72, 20),
           (68, 23), (62, 25), (58, 26), (55, 26), (52, 28), (50, 30),
           (48, 30), (44, 29), (40, 31), (36, 36), (30, 36), (27, 37),
           (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43),
           (-2, 37), (-6, 36), (-9, 37)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
             (132, -32), (136, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
             (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
             (126, -14), (122, -17), (118, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 54), (1, 51), (-3, 50)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44),
         (141, 42), (139, 37), (135, 34), (131, 33)]
NEW_ZEALAND = [(167, -45), (170, -42), (174, -39), (177, -38), (175, -40),
               (172, -43), (168, -46)]
MADAGASCAR = [(44, -16), (47, -20), (50, -25), (45, -25), (43, -20)]
NEW_GUINEA = [(131, -1), (136, -3), (141, -6), (146, -8), (150, -10),
              (147, -9), (141, -8), (136, -4), (132, -2)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 0), (117, -3), (110, -3)]
SUMATRA = [(95, 5), (100, 0), (105, -5), (106, -6), (102, -4), (97, 2)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68),
             (-25, 70), (-20, 74), (-25, 77), (-35, 77), (-45, 75),
             (-55, 72), (-58, 68)]
ICELAND = [(-22, 64), (-18, 63), (-14, 64), (-16, 66), (-20, 66)]
MEDITERRANEAN = [(-6, 36), (3, 37), (10, 37), (12, 40), (19, 40),
                 (23, 36), (27, 37), (30, 36), (36, 36), (36, 33),
                 (34, 31), (30, 32), (25, 32), (20, 32), (15, 33),
                 (11, 34), (8, 37), (3, 38), (-2, 36)]
BLACK_SEA = [(28, 41), (33, 41), (38, 41), (41, 43), (39, 46), (33, 46),
             (28, 45)]
LAND_POLYS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, AUSTRALIA,
              UK, JAPAN, NEW_ZEALAND, MADAGASCAR, NEW_GUINEA, BORNEO,
              SUMATRA, GREENLAND, ICELAND]
SEA_CUTOUTS = [MEDITERRANEAN, BLACK_SEA]

# Numbered story markers: (number, lon, lat, label)
MARKERS = [
    (1, 98.5, 39.7, "JIUQUAN"),
    (2, 42.9, 14.8, "HODEIDAH"),
    (3, 121.5, 25.0, "TAIPEI"),
    (4, 160.0, -9.4, "HONIARA"),
    (5, 54.4, 24.5, "ABU DHABI"),
    (6, -74.0, 40.7, "NEW YORK"),
    (7, 28.0, 38.5, "TURKIYE"),
    (8, -3.7, 40.4, "MADRID"),
    (9, -75.5, 10.4, "CARTAGENA"),
    (10, 149.1, -35.3, "CANBERRA"),
]


def draw_map(cv, x, y, w, h):
    """Equirectangular world map with numbered markers."""
    cv.fill_rect(x, y, w, h, SEA)
    # faint latitude/longitude grid
    for gx in range(1, 12):
        cv.vline(x + w * gx // 12, y, h, (186, 208, 215))
    for gy in range(1, 6):
        cv.hline(x, y + h * gy // 6, w, (186, 208, 215))

    def proj(lon, lat):
        return (x + int((lon + 180) / 360 * w),
                y + int((90 - lat) / 180 * h))

    for poly in LAND_POLYS:
        cv.polygon([proj(lon, lat) for lon, lat in poly], LAND)
    for poly in SEA_CUTOUTS:
        cv.polygon([proj(lon, lat) for lon, lat in poly], SEA)
    # coastlines: light outline pass
    for poly in LAND_POLYS:
        pts = [proj(lon, lat) for lon, lat in poly]
        cv.polyline(pts + [pts[0]], LAND_EDGE)
    cv.rect(x, y, w, h, INK)
    for num, lon, lat, _label in MARKERS:
        mx, my = proj(lon, lat)
        cv.circle(mx, my, 8, RED, fill=True)
        cv.circle(mx, my, 8, WHITE)
        cv.text_center(mx - 8, my - 3, 16, str(num), 1, WHITE)


# ---- 8 drawn vector scenes (each draws inside a rect) ----
def scene_rocket(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (16, 32, 64))
    for sx, sy in ((6, 8), (w - 12, 14), (w // 2, 6), (12, h - 18), (w - 8, h - 10)):
        cv.fill_rect(x + sx, y + sy, 2, 2, WHITE)
    # station ring upper right
    cv.circle(x + w - 26, y + 22, 12, (120, 180, 220))
    cv.circle(x + w - 26, y + 22, 8, (16, 32, 64))
    cv.fill_rect(x + w - 40, y + 20, 28, 4, (120, 180, 220))
    # rocket body
    bx, by = x + w // 2 - 9, y + 14
    cv.polygon([(bx + 9, by), (bx + 18, by + 16), (bx + 18, by + 52),
                (bx, by + 52), (bx, by + 16)], WHITE)
    cv.polygon([(bx + 9, by), (bx + 18, by + 16), (bx, by + 16)], RED)
    cv.fill_rect(bx + 4, by + 24, 10, 6, INK)
    cv.polygon([(bx, by + 52), (bx - 8, by + 64), (bx, by + 58)], RED)
    cv.polygon([(bx + 18, by + 52), (bx + 26, by + 64), (bx + 18, by + 58)], RED)
    # flame
    cv.polygon([(bx + 4, by + 52), (bx + 14, by + 52), (bx + 9, by + h - 20)],
               (245, 176, 65))
    cv.polygon([(bx + 6, by + 52), (bx + 12, by + 52), (bx + 9, by + h - 26)],
               (245, 110, 40))
    # ground
    cv.fill_rect(x, y + h - 4, w, 4, (120, 180, 220))


def scene_port(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (214, 196, 158))
    # sky + sun
    cv.fill_rect(x, y, w, h // 2, (240, 214, 170))
    cv.circle(x + w - 20, y + 14, 9, (245, 176, 65), fill=True)
    # cranes
    for cx in (x + 14, x + 52):
        cv.fill_rect(cx, y + 8, 4, h // 2, (120, 90, 60))
        cv.line(cx, y + 8, cx + 30, y + 26, (120, 90, 60), 2)
        cv.line(cx + 2, y + 26, cx + 2, y + 40, (120, 90, 60), 2)
    # sea
    cv.fill_rect(x, y + h // 2, w, h // 2, (44, 92, 130))
    for wy in range(3):
        cv.hline(x + 6 + wy * 12, y + h // 2 + 8 + wy * 9, w - 20, (140, 190, 220))
    # ship
    sx, sy = x + w - 78, y + h // 2 + 6
    cv.polygon([(sx, sy), (sx + 66, sy), (sx + 56, sy + 18), (sx + 8, sy + 18)],
               (30, 50, 90))
    for i in range(3):
        cv.fill_rect(sx + 10 + i * 18, sy - 14, 14, 14, (200, 60, 40) if i % 2 == 0 else (30, 90, 140))
    cv.fill_rect(sx + 46, sy - 26, 4, 12, INK)
    # explosion bursts over the port
    for ex, ey, r in ((x + 26, y + 20, 10), (x + 58, y + 12, 8)):
        for dx, dy in ((0, -r), (r, 0), (0, r), (-r, 0), (7, -7), (7, 7), (-7, 7), (-7, -7)):
            cv.line(ex, ey, ex + dx, ey + dy, (200, 60, 40), 2)
        cv.circle(ex, ey, 3, (245, 176, 65), fill=True)
    # smoke
    cv.circle(x + 26, y + 12, 5, (90, 90, 90), fill=True)
    cv.circle(x + 58, y + 6, 4, (90, 90, 90), fill=True)


def scene_chart(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (24, 44, 84))
    # grid
    for gy in range(1, 4):
        cv.hline(x + 8, y + h * gy // 4, w - 16, (52, 74, 118))
    # candles plunging (fractions of the panel height)
    fracs = [0.18, 0.26, 0.22, 0.38, 0.34, 0.48, 0.44, 0.58]
    bw = (w - 24) // len(fracs)
    for i, f in enumerate(fracs):
        cx = x + 12 + i * bw + bw // 2
        top = y + int(f * h)
        bot = top + max(6, h // 5)
        cv.vline(cx, top - 5, bot - top + 10, (220, 90, 70))
        cv.fill_rect(cx - bw // 4, top, bw // 2, bot - top, (220, 90, 70))
    # red arrow plunging
    cv.line(x + 10, y + 8, x + w - 12, y + h - 10, RED, 3)
    cv.polygon([(x + w - 12, y + h - 10), (x + w - 26, y + h - 16),
                (x + w - 22, y + h - 2)], RED)
    cv.text(x + 10, y + 2, "-8.6%", 1, (255, 120, 100))


def scene_treaty(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (232, 222, 196))
    # two flag poles
    cv.vline(x + 26, y + 10, h - 22, (90, 70, 50))
    cv.vline(x + w - 30, y + 10, h - 22, (90, 70, 50))
    # Australian flag (blue, stars, Union Jack corner)
    cv.fill_rect(x + 28, y + 10, 44, 26, (20, 40, 110))
    cv.fill_rect(x + 28, y + 10, 20, 13, (200, 30, 30))
    cv.line(x + 28, y + 10, x + 48, y + 23, WHITE, 2)
    cv.line(x + 48, y + 10, x + 28, y + 23, WHITE, 2)
    for sx, sy in ((60, 30), (66, 18), (56, 20)):
        cv.fill_rect(x + sx, y + sy, 3, 3, WHITE)
    # Solomon Islands flag (blue/green, yellow stripe, stars)
    cv.fill_rect(x + w - 74, y + 10, 44, 26, (30, 90, 160))
    cv.polygon([(x + w - 74, y + 36), (x + w - 30, y + 10), (x + w - 30, y + 36)],
               (40, 140, 80))
    cv.line(x + w - 74, y + 36, x + w - 30, y + 10, (245, 200, 60), 2)
    for sx, sy in ((8, 6), (16, 12), (12, 18)):
        cv.fill_rect(x + w - 74 + sx, y + sy, 3, 3, WHITE)
    # document + pen on the table
    cv.fill_rect(x + w // 2 - 26, y + h - 34, 52, 26, WHITE)
    cv.rect(x + w // 2 - 26, y + h - 34, 52, 26, INK)
    for i in range(3):
        cv.hline(x + w // 2 - 20, y + h - 28 + i * 6, 30, INK)
    cv.line(x + w // 2 + 22, y + h - 14, x + w // 2 + 34, y + h - 26, INK, 2)
    # handshake: two clasped shapes
    cv.circle(x + w // 2 - 8, y + h - 44, 7, (200, 150, 110), fill=True)
    cv.circle(x + w // 2 + 8, y + h - 44, 7, (150, 105, 75), fill=True)


def scene_talks(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (228, 222, 210))
    # round table
    tr = min(26, h // 2 - 6)
    cv.circle(x + w // 2, y + h // 2 + 4, tr, (120, 90, 60), fill=True)
    cv.circle(x + w // 2, y + h // 2 + 4, tr, (90, 65, 40))
    cv.circle(x + w // 2, y + h // 2 + 4, tr - 8, (150, 115, 75), fill=True)
    # three flags behind the table: US, UA, RU (simplified stripes)
    for i, cols in enumerate((((200, 30, 30), WHITE, (20, 40, 110)),
                             ((40, 110, 200), (245, 200, 60), None),
                             ((255, 255, 255), (20, 60, 160), (200, 30, 30)))):
        fx = x + 16 + i * (w - 32) // 3
        cv.vline(fx, y + 6, 30, (90, 70, 50))
        cv.fill_rect(fx + 2, y + 6, 26, 8, cols[0])
        if cols[1] is not None:
            cv.fill_rect(fx + 2, y + 14, 26, 8, cols[1])
        if cols[2] is not None:
            cv.fill_rect(fx + 2, y + 22, 26, 8, cols[2])
        else:
            cv.fill_rect(fx + 2, y + 22, 26, 8, cols[0])
    # "NO DEAL" stamp
    cv.rect(x + w // 2 - 30, y + h - 24, 60, 16, RED, 2)
    cv.text_center(x + w // 2 - 30, y + h - 21, 60, "NO DEAL", 1, RED)


def scene_gavel(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (236, 228, 212))
    # columns
    for cx in (x + 12, x + w - 20):
        cv.fill_rect(cx, y + 8, 8, h - 20, (180, 168, 140))
        cv.fill_rect(cx - 2, y + 6, 12, 4, (150, 138, 110))
        cv.fill_rect(cx - 2, y + h - 14, 12, 4, (150, 138, 110))
    # gavel head + handle
    cv.line(x + w // 2 - 22, y + 22, x + w // 2 + 18, y + 38, (90, 65, 40), 5)
    cv.fill_rect(x + w // 2 - 26, y + 14, 16, 12, (120, 90, 60))
    cv.fill_rect(x + w // 2 + 14, y + 32, 16, 12, (120, 90, 60))
    # sound block
    cv.fill_rect(x + w // 2 - 18, y + h - 26, 36, 10, (90, 65, 40))
    cv.fill_rect(x + w // 2 - 22, y + h - 18, 44, 4, (120, 90, 60))
    # verdict slip
    cv.fill_rect(x + w // 2 - 14, y + h - 44, 28, 10, WHITE)
    cv.rect(x + w // 2 - 14, y + h - 44, 28, 10, INK)
    cv.text_center(x + w // 2 - 14, y + h - 42, 28, "10/12", 1, RED)


def scene_helicopter(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (196, 214, 228))
    # clouds
    for cx, cy in ((14, 12), (w - 40, 8), (w // 2, 20)):
        cv.circle(x + cx, y + cy, 8, WHITE, fill=True)
        cv.circle(x + cx + 10, y + cy + 3, 6, WHITE, fill=True)
    # rotor
    cv.hline(x + 14, y + 16, w - 28, INK)
    cv.vline(x + w // 2, y + 16, 8, INK)
    # body
    bx, by = x + w // 2 - 34, y + 24
    cv.polygon([(bx, by + 14), (bx + 68, by + 14), (bx + 60, by + 34),
                (bx + 8, by + 34)], (60, 90, 110))
    cv.fill_rect(bx + 44, by + 4, 16, 12, (140, 190, 220))
    cv.circle(bx + 52, by + 24, 5, (140, 190, 220), fill=True)
    # tail
    cv.polygon([(bx + 68, by + 16), (bx + w - 74 + 30, by + 10),
                (bx + w - 74 + 30, by + 20), (bx + 68, by + 26)], (60, 90, 110))
    cv.vline(bx + w - 74 + 28, by + 2, 20, INK)
    # skids
    cv.hline(bx + 4, by + 42, 60, INK)
    cv.line(bx + 12, by + 34, bx + 12, by + 42, INK, 2)
    cv.line(bx + 52, by + 34, bx + 52, by + 42, INK, 2)
    # mountains below
    cv.polygon([(x, y + h), (x + w // 3, y + h - 22), (x + 2 * w // 3, y + h),
                (x + w, y + h - 16), (x + w, y + h)], (90, 120, 90))


def scene_chess(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (238, 226, 200))
    # board 4x4
    bs = min(w, h) - 24
    bx, by = x + (w - bs) // 2, y + (h - bs) // 2
    cell = bs // 4
    for r in range(4):
        for c in range(4):
            col = WHITE if (r + c) % 2 == 0 else (60, 50, 40)
            cv.fill_rect(bx + c * cell, by + r * cell, cell, cell, col)
    cv.rect(bx, by, bs, bs, INK, 2)
    # white king on a light square, black king on a dark square
    kx, ky = bx + cell + cell // 2, by + cell + cell // 2
    cv.circle(kx, ky - 4, 9, WHITE, fill=True)
    cv.fill_rect(kx - 2, ky - 16, 4, 12, WHITE)
    cv.fill_rect(kx - 6, ky - 12, 12, 3, WHITE)
    cv.fill_rect(kx - 8, ky + 4, 16, 5, WHITE)
    kx2, ky2 = bx + 2 * cell + cell // 2, by + 2 * cell + cell // 2
    cv.circle(kx2, ky2 - 4, 9, INK, fill=True)
    cv.fill_rect(kx2 - 2, ky2 - 16, 4, 12, INK)
    cv.fill_rect(kx2 - 6, ky2 - 12, 12, 3, INK)
    cv.fill_rect(kx2 - 8, ky2 + 4, 16, 5, INK)
    # clock
    cv.fill_rect(x + w - 30, y + 6, 24, 12, WHITE)
    cv.rect(x + w - 30, y + 6, 24, 12, INK)
    cv.text(x + w - 28, y + 8, "0:03", 1, RED)


# ---- the day's news: 42 stories, Wednesday-led ----
# date: "25 NOV" (Wed), "24 NOV" (Tue), "23 NOV" (Mon). Tue/Mon items
# are labelled with their day everywhere they appear.
# Illustrated: (scene_fn, region, title, body, date)
ILLUSTRATED = [
    (scene_rocket, "ASIA",
     "SHENZHOU-24 TO TIANGONG",
     "Pakistan's Zeeshan Ali, 40, is the first foreign astronaut to visit "
     "Tiangong. Launch 08:18, docking 11:56.",
     "25 NOV"),
    (scene_port, "MIDEAST",
     "SAUDI STRIKES HODEIDAH PORT",
     "Coalition says it hit the Houthi-run port after an evacuation "
     "warning; Houthis threaten Saudi Red Sea ports.",
     "25 NOV"),
    (scene_chart, "ASIA",
     "CHIP ROUT HITS ASIA",
     "Taipei fell as much as 8.6% intraday, Seoul 6.4%, Nikkei 3.7%; "
     "SoftBank -14% as the AI rally fades.",
     "25 NOV"),
    (scene_treaty, "OCEANIA",
     "SOLOMONS PICK AUSTRALIA",
     "Canberra becomes the primary security partner; Honiara says no "
     "foreign military base. Fate of the 2022 China pact unconfirmed.",
     "25 NOV"),
    (scene_talks, "MIDEAST",
     "ABU DHABI TALKS FAIL",
     "US-mediated Ukraine-Russia talks close without a breakthrough; "
     "envoys head to Moscow and Dublin.",
     "24 NOV"),
    (scene_gavel, "AMERICAS",
     "HUAWEI GUILTY 10 OF 12",
     "US jury convicts on trade-secret theft, fraud and sanctions "
     "charges; Huawei plans to appeal.",
     "24 NOV"),
]

STRIP = [
    (scene_helicopter, "ASIA",
     "HELICOPTER CRASH",
     "Turkish AS-532 Cougar down in training; five crew killed "
     "in western Turkiye.",
     "25 NOV"),
    (scene_chess, "ASIA",
     "GUKESH HOLDS ON",
     "World chess title: Gukesh weathers time pressure to draw "
     "with Sindarov.",
     "25 NOV"),
]

# Briefs: (region, title, date). Titles fit two lines at 14px in a
# 194px cell (15 chars a line).
BRIEFS = [
    ("OCEANIA", "AUSTRALIA CPI JUMPS TO 4.9%", "25 NOV"),
    ("WORLD", "16 DAYS AGAINST ABUSE BEGIN", "25 NOV"),
    ("OCEANIA", "NZ-EUROPOL BUST DARKNET RING", "25 NOV"),
    ("ASIA", "BANGLADESH PAY RISE 36%", "25 NOV"),
    ("ASIA", "JAPAN 40Y BOND SALE WEAK", "25 NOV"),
    ("MIDEAST", "HAMAS SECURITY CHIEF KILLED", "25 NOV"),
    ("EUROPE", "FRANCE SEIZES 3.3T OF METH", "25 NOV"),
    ("EUROPE", "REAL MADRID ROUT PSV", "25 NOV"),
    ("EUROPE", "SINNER MAY MISS AUSTRALIAN OPEN", "25 NOV"),
    ("EUROPE", "ENGLAND LEVEL T20 SERIES", "25 NOV"),
    ("AMERICAS", "SHEIN TO PAY $100M TO FTC", "25 NOV"),
    ("AMERICAS", "SOLDIER ADMITS SELLING SECRETS", "25 NOV"),
    ("WORLD", "5 WOMEN KILLED EVERY HOUR", "25 NOV"),
    ("WORLD", "UN CHIEF URGES AI SAFETY TALKS", "25 NOV"),
    ("EUROPE", "SPAIN VOTES ON SUNDAY", "25 NOV"),
    ("EUROPE", "MET 'STILL RACIST': REPORT", "25 NOV"),
    ("AFRICA", "RSF SPY CHIEF DEFECTS TO ARMY", "25 NOV"),
    ("AFRICA", "17 KILLED IN SA MASS SHOOTINGS", "25 NOV"),
    ("AFRICA", "BORNO SCHOOL ROLLS DOUBLE", "25 NOV"),
    ("OCEANIA", "EL NINO DROUGHT RESPONSE GROWS", "25 NOV"),
    ("ASIA", "HANOI GAS BLAST KILLS SIX", "25 NOV"),
    ("ASIA", "BJP AND AKALI DAL REUNITE", "25 NOV"),
    ("ASIA", "CHEN JINING UNDER PROBE", "24 NOV"),
    ("AMERICAS", "30 HELD HOSTAGE IN CARTAGENA", "24 NOV"),
    ("AMERICAS", "US CONFIDENCE JUMPS TO 103", "24 NOV"),
    ("ASIA", "CHINA EXTENDS MINERALS PAUSE", "24 NOV"),
    ("ASIA", "RUSSIAN JETS IN KOREAN ADIZ", "24 NOV"),
    ("EUROPE", "ZELENSKY MEETS MAGYAR", "24 NOV"),
    ("EUROPE", "SARKOZYS TO STAND TRIAL", "24 NOV"),
    ("AFRICA", "WHO PULLS EBOLA STAFF FROM AKWE", "24 NOV"),
    ("AMERICAS", "BRAZIL PASSES FISCAL PACKAGE", "23 NOV"),
    ("AMERICAS", "VENEZUELA DEBT $237.5BN", "23 NOV"),
    ("MIDEAST", "QATAR RESTARTS IRAN MEDIATION", "23 NOV"),
    ("ASIA", "XIAMEN AIR TO BUY 50 BOEINGS", "24 NOV"),
]


def draw_illustrated(cv, x, y, w, h, scene, region, title, body, date):
    cv.fill_rect(x, y, w, h, CARD)
    cv.rect(x, y, w, h, LINE)
    scene(cv, x + 4, y + 4, w - 8, 68)
    lines = wrap_text(title, 13)
    ty = y + 78
    for ln in lines[:2]:
        cv.text(x + 8, ty, ln, 3, INK)
        ty += 21
    cv.text(x + 8, y + h - 13, region, 1, REGION_COLORS[region])
    dx = x + 8 + text_width(region, 1) + 6
    cv.text(dx, y + h - 13, "- " + date, 1, RED)
    # body goes in the strip panels only; side panels carry title + tag


def draw_strip(cv, x, y, w, h, scene, region, title, body, date):
    cv.fill_rect(x, y, w, h, CARD)
    cv.rect(x, y, w, h, LINE)
    scene(cv, x + 4, y + 6, 120, h - 12)
    tx = x + 132
    cv.text(tx, y + 10, title, 3, INK)
    lines = wrap_text(body, 58)
    by = y + 38
    for ln in lines[:2]:
        cv.text(tx, by, ln, 1, (64, 76, 100))
        by += 9
    cv.text(tx, y + h - 14, region, 1, REGION_COLORS[region])
    dx = tx + text_width(region, 1) + 6
    cv.text(dx, y + h - 14, "- " + date, 1, RED)


def draw_brief(cv, x, y, w, h, region, title, date):
    cv.fill_rect(x, y, w, h, CARD)
    cv.rect(x, y, w, h, LINE)
    cv.fill_rect(x, y, 3, h, REGION_COLORS[region])
    cv.text(x + 8, y + 3, region, 1, REGION_COLORS[region])
    dx = x + 8 + text_width(region, 1) + 6
    cv.text(dx, y + 3, "- " + date, 1, RED)
    lines = wrap_text(title, 15)
    ty = y + 13
    for ln in lines[:2]:
        cv.text(x + 8, ty, ln, 2, INK)
        ty += 14


def build():
    cv = Canvas(W, H, PAPER)
    # ---- masthead: 92px ----
    cv.fill_rect(0, 0, W, 92, NAVY)
    cv.text_center(0, 12, W, "THE WORLD IN ONE IMAGE", 6, WHITE)
    cv.text_center(0, 62, W,
                   "WEDNESDAY 25 NOVEMBER 2026 - 42 STORIES - 7 REGIONS",
                   2, (214, 222, 236))
    cv.fill_rect(0, 88, W, 4, RED)

    # ---- map band: 92-522 (430px) ----
    # side illustration panels: 3 left, 3 right, 248 wide
    panel_w, panel_h = 248, 135
    panel_ys = [100, 243, 386]
    for i, item in enumerate(ILLUSTRATED):
        scene, region, title, body, date = item
        px = 12 if i < 3 else 764
        py = panel_ys[i % 3]
        draw_illustrated(cv, px, py, panel_w, panel_h,
                         scene, region, title, body, date)
    # central world map
    mx, my, mw, mh = 272, 100, 480, 290
    draw_map(cv, mx, my, mw, mh)
    cv.text_center(mx, 396, mw,
                   "1 JIUQUAN - 2 HODEIDAH - 3 TAIPEI - 4 HONIARA - 5 ABU DHABI",
                   1, INK)
    cv.text_center(mx, 408, mw,
                   "6 NEW YORK - 7 TURKIYE - 8 MADRID - 9 CARTAGENA - 10 CANBERRA",
                   1, INK)
    # stories by region: horizontal bars
    counts = {}
    for _s, region, _t, _b, _d in ILLUSTRATED:
        counts[region] = counts.get(region, 0) + 1
    for _s, region, _t, _b, _d in STRIP:
        counts[region] = counts.get(region, 0) + 1
    for region, _t, _d in BRIEFS:
        counts[region] = counts.get(region, 0) + 1
    order = ["ASIA", "MIDEAST", "EUROPE", "AFRICA", "AMERICAS", "OCEANIA", "WORLD"]
    cv.text(mx, 422, "STORIES BY REGION", 1, INK)
    for i, region in enumerate(order):
        ry = 434 + i * 12
        cv.text(mx, ry, region, 1, REGION_COLORS[region])
        n = counts.get(region, 0)
        bw = int(n / 12 * 260)
        cv.fill_rect(mx + 62, ry + 1, bw, 5, REGION_COLORS[region])
        cv.text(mx + 62 + bw + 6, ry, str(n), 1, INK)

    # ---- strip band: 522-616 (94px), 2 more illustrations ----
    for i, item in enumerate(STRIP):
        scene, region, title, body, date = item
        sx = 12 if i == 0 else 518
        draw_strip(cv, sx, 522, 494, 94, scene, region, title, body, date)

    # ---- briefs band: 616-986 (370px), 34 stories ----
    cv.text(12, 620, "THE DAY IN BRIEF - 34 STORIES", 2, INK)
    cv.fill_rect(12, 638 - 4, W - 24, 2, RED)
    cols, rows = 5, 7
    cell_w, cell_h, gap = 194, 46, 4
    for idx, (region, title, date) in enumerate(BRIEFS):
        r, c = divmod(idx, cols)
        bx = 12 + c * (cell_w + 8)
        by = 638 + r * (cell_h + gap)
        draw_brief(cv, bx, by, cell_w, cell_h, region, title, date)

    # ---- footnote: 986-1024 (38px) ----
    cv.text_center(
        0, 990, W,
        "Sources: Reuters, AP, AFP, Al Jazeera, SCMP, Nature, UN News, Xinhua.",
        1, (90, 96, 110))
    cv.text_center(
        0, 1002, W,
        "Stories dated 25 Nov 2026 unless marked 24 NOV (Tue) or 23 NOV (Mon). "
        "Market moves are intraday, not closes.",
        1, (90, 96, 110))
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = build()
    write_png(os.path.join(out_dir, "entry.png"), cv)


if __name__ == "__main__":
    main()
