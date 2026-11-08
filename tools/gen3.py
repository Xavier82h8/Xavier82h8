"""Tercera tanda: estilo vidrio (glassmorphism) y terminal tipo macOS.

El README no admite backdrop-filter dentro de un SVG servido como imagen, así que el vidrio se
simula: manchas de color difuminadas con feGaussianBlur detrás de un panel translúcido con
brillo superior y borde de luz. Reescribe header-*, tarjetas de proyecto, numbers-* y typing-*.
"""
import os
import re
import sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(__file__))
import gen   # noqa: E402  (escribe la versión base)
import gen2  # noqa: E402  (escribe la versión animada)

OUT = sys.argv[1] if __name__ == "__main__" else None
THEMES, MONO, SANS = gen.THEMES, gen.MONO, gen.SANS

GLASS = {
    "dark": dict(base="#0A1520", fill="rgba(14,26,38,0.62)", sheen=0.11, edge_top="rgba(255,255,255,0.26)",
                 edge_bot="rgba(255,255,255,0.05)", amber=("#F2A93B", .55), teal=("#2F7AA0", .85),
                 violet=("#5B4FC4", .6), rose=("#C2557A", .45), shadow=.55),
    "light": dict(base="#E8EFF5", fill="rgba(255,255,255,0.44)", sheen=0.75, edge_top="rgba(255,255,255,0.95)",
                  edge_bot="rgba(23,36,47,0.14)", amber=("#F6C177", .8), teal=("#7FB8D6", .85),
                  violet=("#B8B0F2", .75), rose=("#F2A7BF", .6), shadow=.18),
}


def glass_defs(t, W, H, rx, blur=36, pid="p"):
    g = GLASS[t]
    return (f'<filter id="{pid}b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{blur}"/></filter>'
            f'<clipPath id="{pid}c"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>'
            f'<linearGradient id="{pid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="{g["sheen"]}"/>'
            f'<stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{pid}e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g["edge_top"]}"/>'
            f'<stop offset="1" stop-color="{g["edge_bot"]}"/></linearGradient>')


def blobs(t, spec, pid="p", cls="blob"):
    g = GLASS[t]
    out = [f'<g filter="url(#{pid}b)">']
    for i, (color, cx, cy, r) in enumerate(spec):
        col, op = g[color]
        out.append(f'<circle class="{cls} {cls}{i}" cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}"/>')
    out.append("</g>")
    return "".join(out)


def glass_panel(t, W, H, rx, spec, pid="p"):
    """Panel de vidrio completo: base, manchas, tinte, brillo y borde."""
    g = GLASS[t]
    return (f'<g clip-path="url(#{pid}c)"><rect width="{W}" height="{H}" fill="{g["base"]}"/>'
            f'{blobs(t, spec, pid)}'
            f'<rect width="{W}" height="{H}" fill="{g["fill"]}"/><rect width="{W}" height="{H}" fill="url(#{pid}s)"/></g>'
            f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="{rx-0.75}" fill="none" stroke="url(#{pid}e)" stroke-width="1.5"/>')


DRIFT = (".blob{animation:drift 18s ease-in-out infinite alternate}"
         ".blob1{animation-duration:23s;animation-direction:alternate-reverse}.blob2{animation-duration:29s}"
         "@keyframes drift{from{transform:translate(0,0)}to{transform:translate(38px,-22px)}}")
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.cmd{clip-path:none}.ln{opacity:1}}"


def terminal(t):
    W, H = 900, 430
    c, g = THEMES[t], GLASS[t]
    fg, mu, ac, ok = c["fg"], c["muted"], c["accent"], c["ok"]
    wx, wy, ww, wh = 46, 34, 808, 356
    span = gen.span
    lines = [
        (108, 22, span("● ", ok) + span("javier-karim.service", fg, 700) + span(" - Backend Developer", mu)),
        (140, 14, span("     Loaded: ", mu) + span("loaded (Ingeniería en Sistemas Computacionales, ITH; 8.º semestre)", fg)),
        (166, 14, span("     Active: ", mu) + span("active (running)", ok, 700) + span(" desde Hermosillo, Sonora, México", fg)),
        (192, 14, span("      Tasks: ", mu) + span("3 (franken-panel, musa-ai, musaaudio)", fg)),
        (218, 14, span("     CGroup: ", mu) + span("APIs · autenticación · bases de datos · Linux · Docker · CI/CD", fg)),
        (244, 14, span("       Docs: ", mu) + span("linkedin.com/in/javier-karim", ac)),
        (284, 14, span("javier-karim[1]: ", mu) + span("Abierto a puestos Backend Jr, en Hermosillo o remoto.", fg)),
    ]
    wall = [("violet", 150, 90, 150), ("amber", 760, 70, 140), ("teal", 260, 400, 190), ("rose", 640, 420, 130)]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Terminal: systemctl status javier-karim. Backend Developer, Ingeniería en Sistemas Computacionales en el ITH, activo desde Hermosillo, México. Abierto a puestos Backend Jr.">',
         "<defs>", glass_defs(t, W, H, 20, 46, "w"),
         glass_defs(t, ww, wh, 14, 70, "g"),
         f'<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#000" flood-opacity="{g["shadow"]}"/></filter>',
         "</defs>",
         "<style>",
         f"text{{font-family:{MONO}}}", DRIFT,
         ".cmd{clip-path:inset(0 100% 0 0);animation:type 1.1s steps(31,end) .5s forwards}",
         ".ln{opacity:0;animation:in .35s ease-out forwards}",
         ".cur{animation:blink 1.1s steps(1,end) infinite}",
         "@keyframes type{to{clip-path:inset(0 0 0 0)}}",
         "@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}",
         "@keyframes blink{50%{opacity:0}}", REDUCED,
         "</style>",
         # Fondo de escritorio
         f'<g clip-path="url(#wc)"><rect width="{W}" height="{H}" fill="{g["base"]}"/>{blobs(t, wall, "w")}</g>',
         # Ventana: sombra, vidrio con el mismo fondo más difuminado, barra de título
         f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="{g["base"]}" filter="url(#sh)" opacity=".9"/>',
         f'<g transform="translate({wx} {wy})">',
         f'<g clip-path="url(#gc)"><rect width="{ww}" height="{wh}" fill="{g["base"]}"/>'
         f'<g transform="translate({-wx} {-wy})">{blobs(t, wall, "g")}</g>'
         f'<rect width="{ww}" height="{wh}" fill="{g["fill"]}"/><rect width="{ww}" height="{wh}" fill="url(#gs)"/>'
         f'<rect width="{ww}" height="38" fill="#fff" opacity="{.05 if t == "dark" else .35}"/>'
         f'<line x1="0" y1="38.5" x2="{ww}" y2="38.5" stroke="{c["border"]}" opacity=".7"/></g>',
         f'<rect x="0.75" y="0.75" width="{ww-1.5}" height="{wh-1.5}" rx="13.25" fill="none" stroke="url(#ge)" stroke-width="1.5"/>']
    for i, (col, stroke) in enumerate([("#FF5F57", "#E0443E"), ("#FEBC2E", "#DEA123"), ("#28C840", "#1AAB29")]):
        o.append(f'<circle cx="{22 + i*20}" cy="19" r="6" fill="{col}" stroke="{stroke}" stroke-width=".8"/>')
    o.append(f'<text x="{ww/2}" y="23.5" text-anchor="middle" style="font-family:{SANS}" font-size="12.5" font-weight="600" fill="{mu}">javier — systemctl — 80×24</text>')
    o.append('<g transform="translate(26 0)">')
    o.append(f'<text class="cmd" x="0" y="70" font-size="15">{span("$ ", ac, 700)}{span("systemctl status javier-karim", fg)}</text>')
    for i, (y, fs, content) in enumerate(lines):
        o.append(f'<text class="ln" style="animation-delay:{1.75 + i*0.13:.2f}s" x="0" y="{y}" font-size="{fs}" xml:space="preserve">{content}</text>')
    o.append(f'<text class="ln" style="animation-delay:{1.75 + len(lines)*0.13:.2f}s" x="0" y="322" font-size="15">'
             f'{span("$ ", ac, 700)}<tspan class="cur" fill="{fg}">▍</tspan></text>')
    o.append("</g></g></svg>")
    return "\n".join(o)


CARD_BLOBS = {
    "franken-panel": [("violet", 120, 30, 120), ("teal", 820, 190, 130), ("amber", 640, 0, 70)],
    "musa-ai": [("amber", 90, 190, 120), ("rose", 820, 20, 120), ("violet", 520, 210, 80)],
    "musaaudio": [("teal", 140, 10, 120), ("rose", 860, 170, 120), ("amber", 560, 220, 70)],
}


def glassify(svg, t, W, H, spec, extra_css=""):
    """Sustituye el rectángulo de fondo de una tarjeta por un panel de vidrio."""
    c = THEMES[t]
    old = f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>'
    assert old in svg, "fondo no encontrado"
    svg = svg.replace(old, glass_panel(t, W, H, 14, spec), 1)
    head_end = svg.index(">") + 1
    svg = svg[:head_end] + "\n<defs>" + glass_defs(t, W, H, 14, 40) + "</defs>\n<style>" + DRIFT + extra_css + \
        "@media (prefers-reduced-motion:reduce){.blob{animation:none}}</style>" + svg[head_end:]
    return svg


def spotlight(t):
    """Barra estilo Spotlight de vidrio con la línea que se escribe sola."""
    W, H = 900, 76
    c = THEMES[t]
    svg = gen2.typing(t)
    svg = svg.replace('width="900" height="52" viewBox="0 0 900 52"', f'width="{W}" height="{H}" viewBox="0 0 {W} {H}"', 1)
    svg = re.sub(r'<text x="26" y="33"[^>]*>›</text>', "", svg)
    open_tag_end = svg.index(">") + 1
    style_end = svg.index("</style>") + len("</style>")
    spec = [("teal", 80, 70, 90), ("amber", 840, 10, 80), ("violet", 470, 90, 70)]
    panel = (f'<defs>{glass_defs(t, W, H, 22, 30)}</defs>'
             f'<style>{DRIFT}@media (prefers-reduced-motion:reduce){{.blob{{animation:none}}}}</style>'
             f'{glass_panel(t, W, H, 22, spec)}'
             f'<circle cx="34" cy="37" r="8.5" fill="none" stroke="{c["accent"]}" stroke-width="2.4"/>'
             f'<line x1="40.5" y1="43.5" x2="47" y2="50" stroke="{c["accent"]}" stroke-width="2.6" stroke-linecap="round"/>'
             f'<text x="{W-26}" y="44" text-anchor="end" style="font-family:{SANS}" font-size="12.5" fill="{c["muted"]}">⌘ espacio</text>')
    body = svg[style_end:svg.rindex("</svg>")]
    return svg[:style_end] + panel + f'<g transform="translate(10 12)">{body}</g></svg>'


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)


if __name__ == "__main__":
    for t in THEMES:
        write(f"header-{t}.svg", terminal(t))
        write(f"typing-{t}.svg", spotlight(t))
        write(f"numbers-{t}.svg", glassify(gen2.numbers(t), t, 900, 150,
                                           [("teal", 60, 150, 110), ("amber", 470, 0, 90), ("violet", 860, 140, 110)]))
        for p in gen.PROJECTS:
            write(f"{p['slug']}-{t}.svg", glassify(gen2.card(p, t), t, 900, 200, CARD_BLOBS[p["slug"]]))
    print("ok")
