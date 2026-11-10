"""Generate neofetch-style profile card + pipeline SVGs (dark and light)."""
import html
import sys

ART_SRC, OUT = sys.argv[1], sys.argv[2]

# ---------- portrait: 2x2 density downsample ----------
RAMP = " .'`,:;!|/\\=+1vjxznuwopgmQU$X@"
DENS = {c: i / (len(RAMP) - 1) for i, c in enumerate(RAMP)}
raw = [html.unescape(l.rstrip("\n")) for l in open(ART_SRC)]
W0 = max(len(l) for l in raw)
raw = [l.ljust(W0) for l in raw]
art = []
art = list(raw)
for y in range(0, 0):
    row = ""
    for x in range(0, W0 - 1, 2):
        v = [DENS.get(raw[y + dy][x + dx], 0.5) for dy in (0, 1) for dx in (0, 1)]
        row += RAMP[round(sum(v) / 4 * (len(RAMP) - 1))]
    art.append(row)

BANNER = [
    "██████╗ ██╗███████╗██╗    ██╗ █████╗ ███████╗██╗  ██╗",
    "██╔══██╗██║██╔════╝██║    ██║██╔══██╗██╔════╝██║  ██║",
    "██████╔╝██║███████╗██║ █╗ ██║███████║███████╗███████║",
    "██╔══██╗██║╚════██║██║███╗██║██╔══██║╚════██║██╔══██║",
    "██████╔╝██║███████║╚███╔███╔╝██║  ██║███████║██║  ██║",
    "╚═════╝ ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
]

INFO = [  # (key, value) ; key None = section header ; "" = blank
    ("role", "AI Engineer"),
    ("focus", "agents · automation · data pipelines"),
    ("industry", "3PL / fulfillment"),
    ("shell", "zsh · Ghostty · Claude Code"),
    ("", ""),
    (None, "agents"),
    ("build", "Claude Code · MCP servers · skills"),
    ("bots", "Hermes · Grok Bot · Slack copilots"),
    ("ai.os", "shared context: Claude · Cursor · Codex"),
    ("", ""),
    (None, "data"),
    ("warehouse", "BigQuery · ShipHero WMS"),
    ("apps", "Supabase · Postgres · Next.js"),
    ("bi", "Power BI · scheduled refreshes"),
    ("", ""),
    (None, "cloud"),
    ("gcp", "Cloud Run · Functions · Scheduler"),
    ("ci/cd", "GitHub Actions · WIF · monorepo"),
    ("lang", "Python · TypeScript · SQL"),
]

THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#c9d1d9", art="#8b949e",
                 key="#ffa657", val="#a5d6ff", head="#d2a8ff", ok="#3fb950", dim="#484f58",
                 banner="#79c0ff", red="#ff7b72", yel="#d29922", grn="#3fb950"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#24292f", art="#6e7781",
                  key="#953800", val="#0a3069", head="#8250df", ok="#1a7f37", dim="#afb8c1",
                  banner="#0969da", red="#cf222e", yel="#9a6700", grn="#1a7f37"),
}
FONT = "'JetBrains Mono','SFMono-Regular','Menlo','Consolas','DejaVu Sans Mono',monospace"


def esc(s):
    return html.escape(s, quote=False)


def tline(x, y, s, cw, fill, size, extra=""):
    """Text line forced to exact monospace width so box chars align on any font."""
    if not s.strip():
        return ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
            f'textLength="{len(s) * cw:.1f}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve"{extra}>{esc(s)}</text>')


def card(t):
    c = THEMES[t]
    W, H = 996, 640
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="Biswash Kunwar · AI Engineer · neofetch-style profile card" '
           f'font-family="{FONT}">',
           f'''<style>
.type{{animation:type 1.4s steps(30,end) .3s backwards}}
@keyframes type{{from{{width:0}}}}
.in{{animation:fade .35s ease-out backwards}}
@keyframes fade{{from{{opacity:0}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.scan{{animation:scan 6s linear infinite}}
@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY(560px)}}}}
@media (prefers-reduced-motion:reduce){{.type,.in,.cur,.scan{{animation:none;opacity:1}}}}
</style>''',
           f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>',
           f'<path d="M1 36V11a10 10 0 0 1 10-10h{W - 22}a10 10 0 0 1 10 10v25z" fill="{c["bar"]}"/>',
           f'<line x1="1" y1="36" x2="{W - 1}" y2="36" stroke="{c["border"]}"/>']
    for i, col in enumerate((c["red"], c["yel"], c["grn"])):
        out.append(f'<circle cx="{22 + i * 20}" cy="18.5" r="6" fill="{col}"/>')
    out.append(tline(W / 2 - 75, 23, "biswash@kunwar: ~", 8.4, c["art"], 13))

    # prompt + typed command
    out.append(f'<clipPath id="tc"><rect class="type" x="24" y="48" width="290" height="22"/></clipPath>')
    out.append(f'<g clip-path="url(#tc)">{tline(24, 64, "biswash@kunwar ~ $ neofetch --ai", 8.4, c["ok"], 14)}</g>')

    # portrait (left)
    acw, alh, ax, ay = 3.1, 6.8, 24, 92
    out.append('<g class="in" style="animation-delay:1.7s">')
    for i, row in enumerate(art):
        out.append(tline(ax, ay + i * alh, row, acw, c["art"], 5.4))
    out.append('</g>')
    art_w = len(art[0]) * acw
    # scanline over portrait
    out.append(f'<clipPath id="ac"><rect x="{ax}" y="{ay - 12}" width="{art_w}" height="{len(art) * alh + 6}"/></clipPath>')
    out.append(f'<g clip-path="url(#ac)"><rect class="scan" x="{ax}" y="{ay - 70}" width="{art_w}" height="40" '
               f'fill="{c["banner"]}" opacity=".07"/></g>')

    # right panel
    rx = ax + art_w + 36
    bcw, blh = 8.0, 15
    out.append('<g class="in" style="animation-delay:1.9s">')
    for i, row in enumerate(BANNER):
        out.append(tline(rx, 92 + i * blh, row, bcw, c["banner"], 13))
    out.append('</g>')
    y = 92 + len(BANNER) * blh + 14
    cw, lh = 8.0, 19.5
    rule_w = 54
    out.append(f'<g class="in" style="animation-delay:2.1s">'
               + tline(rx, y, "─" * rule_w, cw, c["dim"], 13) + '</g>')
    y += lh
    delay = 2.2
    for k, v in INFO:
        if k == "":
            y += lh * 0.45
            continue
        g = [f'<g class="in" style="animation-delay:{delay:.2f}s">']
        if k is None:
            label = f"── {v} "
            g.append(tline(rx, y, label, cw, c["head"], 13, ' font-weight="700"'))
            g.append(tline(rx + len(label) * cw, y, "─" * (rule_w - len(label)), cw, c["dim"], 13))
        else:
            dots = "." * (12 - len(k))
            g.append(tline(rx, y, k, cw, c["key"], 13))
            g.append(tline(rx + len(k) * cw, y, dots + " ", cw, c["dim"], 13))
            g.append(tline(rx + 13 * cw, y, v, cw * 0.98 if len(v) > 38 else cw, c["val"], 13))
        g.append('</g>')
        out.append("".join(g))
        y += lh
        delay += 0.07

    # palette blocks + final prompt
    y += 8
    out.append(f'<g class="in" style="animation-delay:{delay + .1:.2f}s">')
    for i, col in enumerate((c["red"], c["yel"], c["grn"], c["banner"], c["head"], c["key"], c["val"], c["text"])):
        out.append(f'<rect x="{rx + i * 30}" y="{y - 12}" width="26" height="14" rx="2" fill="{col}"/>')
    out.append('</g>')
    py = H - 22
    out.append(f'<g class="in" style="animation-delay:{delay + .3:.2f}s">'
               + tline(24, py, "biswash@kunwar ~ $", 8.4, c["ok"], 14)
               + f'<rect class="cur" x="{24 + 19 * 8.4}" y="{py - 13}" width="8.4" height="16" fill="{c["text"]}"/></g>')
    out.append('</svg>')
    return "\n".join(x for x in out if x)


# ---------- pipeline ----------
BOXES = [
    ("ShipHero WMS", ["orders · stock", "webhooks + API"]),
    ("Cloud Run", ["functions · ETL", "Cloud Scheduler"]),
    ("BigQuery", ["warehouse", "SQL models"]),
    ("AI Agents", ["Claude · Grok", "MCP tools"]),
    ("Outputs", ["Slack · Power BI", "dashboards"]),
]
BW, GAP = 20, 6


def pipeline(t):
    c = THEMES[t]
    cw, lh, size = 7.8, 18, 13
    ncols = len(BOXES) * BW + (len(BOXES) - 1) * GAP
    x0, y0 = 30, 58
    W = int(ncols * cw + 2 * x0)
    H = 210
    rows = ["", "", "", "", ""]
    for i, (title, lines) in enumerate(BOXES):
        inner = BW - 2
        top = "┌" + ("─ " + title + " ").ljust(inner, "─") + "┐"
        body = ["│" + (" " * ((inner - len(s)) // 2) + s).ljust(inner) + "│" for s in lines]
        bot = "└" + "─" * inner + "┘"
        seg = [top, " " * BW, body[0], body[1], bot]
        seg[1] = "│" + " " * inner + "│"
        conn = [" " * GAP] * 5
        if i < len(BOXES) - 1:
            conn[2] = "─" * (GAP - 1) + "▶"
        for r in range(5):
            rows[r] += seg[r] + (conn[r] if i < len(BOXES) - 1 else "")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="Pipeline: ShipHero to Cloud Run to BigQuery to AI agents to Slack and dashboards" '
           f'font-family="{FONT}">',
           '<style>@media (prefers-reduced-motion:reduce){.dot{display:none}}'
           '.cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}</style>',
           f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>',
           tline(x0, 34, "$ cat pipeline.txt", cw, c["ok"], size)]
    # box frames dim (letters blanked), then bright overlays for titles and body
    for r, row in enumerate(rows):
        frame = "".join(ch if ch in "┌┐└┘─│▶ " else " " for ch in row)
        out.append(tline(x0, y0 + r * lh, frame, cw, c["dim"], size))
    for i, (title, lines) in enumerate(BOXES):
        bx = x0 + i * (BW + GAP) * cw
        out.append(tline(bx + 3 * cw, y0, title, cw, c["key"], size, ' font-weight="700"'))
        for j, s in enumerate(lines):
            off = (BW - 2 - len(s)) // 2 + 1
            out.append(tline(bx + off * cw, y0 + (2 + j) * lh, s, cw, c["val"], size))
    # moving data dots along connectors
    for i in range(len(BOXES) - 1):
        sx = x0 + ((i + 1) * BW + i * GAP) * cw
        ex = sx + (GAP - 1) * cw
        cy = y0 + 2 * lh - 4.5
        for k in range(2):
            out.append(f'<circle class="dot" r="3" cx="{sx:.1f}" opacity="0" cy="{cy}" fill="{c["ok"]}">'
                       f'<animate attributeName="cx" from="{sx:.1f}" to="{ex:.1f}" dur="1.6s" '
                       f'begin="{i * .3 + k * .8:.1f}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="opacity" values="0;1;1;0" dur="1.6s" '
                       f'begin="{i * .3 + k * .8:.1f}s" repeatCount="indefinite"/></circle>')
    ly = y0 + 5 * lh + 14
    out.append(tline(x0, ly, "[ok]", cw, c["ok"], size)
               + tline(x0 + 5 * cw, ly, "orders → warehouse → agents → answers in Slack", cw, c["art"], size))
    out.append(f'<rect class="cur" x="{x0 + 53 * cw}" y="{ly - 12}" width="{cw}" height="15" fill="{c["text"]}"/>')
    out.append('</svg>')
    return "\n".join(x for x in out if x)


for t in THEMES:
    open(f"{OUT}/card_{t}.svg", "w").write(card(t))
    open(f"{OUT}/pipeline_{t}.svg", "w").write(pipeline(t))
print("art", len(art), "x", len(art[0]))
