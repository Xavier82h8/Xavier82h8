"""Cuarta tanda: modo nocturno. Fondo casi negro con pétalos curvos (inspirado en los fondos
oscuros de macOS Ventura, formas propias) y dos paletas que se alternan para no cansar la vista:

  ámbar      pétalos naranjas      banner, terminal, Franken Panel, MusaAudio, pie
  medianoche pétalos azul petróleo barra de texto, cifras, MUSA-AI

Uso: python tools/gen4.py assets
"""
import math
import os
import re
import sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(__file__))
import gen   # noqa: E402
import gen2  # noqa: E402

MONO, SANS = gen.MONO, gen.SANS

PAL = {
    "ambar": dict(stops=["#160400", "#6E1C00", "#D94E0A", "#FF8A2A", "#FFC994"], accent="#FFA552",
                  glow="#FF6A00", edge="#FFD9B0"),
    "medianoche": dict(stops=["#00060C", "#062A42", "#0D6684", "#39B1CF", "#B4F0F8"], accent="#72D6EA",
                       glow="#1690B4", edge="#C8F4FA"),
}
BASE = "#050507"
TEXT = dict(fg="#ECEFF2", muted="#8F99A3", border="#26292F", ok="#4CC38A")

# Paleta de cada pieza
for key, pal in PAL.items():
    gen.THEMES[key] = dict(bg=BASE, bar="#0C0D10", border=TEXT["border"], fg=TEXT["fg"], muted=TEXT["muted"],
                           accent=pal["accent"], ok=TEXT["ok"])


def petal_path(ox, oy, ang, length, width, bend):
    """Pétalo en forma de lente curva que nace en (ox, oy)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    tx, ty = ox + ux * length, oy + uy * length

    def pt(t, off):
        return ox + ux * length * t + px * off, oy + uy * length * t + py * off

    c1 = pt(.30, width * (1 + bend))
    c2 = pt(.80, width * (.95 + bend))
    c3 = pt(.74, -width * (.6 - bend))
    c4 = pt(.28, -width * (.45 - bend))
    tl = pt(.97, width * .16)
    tr = pt(.97, -width * .12)
    tip = (tx + ux * width * .10, ty + uy * width * .10)
    f = lambda p: f"{p[0]:.1f} {p[1]:.1f}"
    return (f"M{ox:.1f} {oy:.1f} C{f(c1)} {f(c2)} {f(tl)} Q{f(tip)} {f(tr)} C{f(c3)} {f(c4)} {ox:.1f} {oy:.1f}Z",
            (ox, oy, tx, ty))


def petals(pal_key, fans, pid, blur=None, sway=True):
    """Dibuja abanicos de pétalos. fans: [(ox, oy, [(ang, largo, ancho, curva), ...])]"""
    pal = PAL[pal_key]
    s = pal["stops"]
    defs, body = [], []
    n = 0
    for fi, (ox, oy, items) in enumerate(fans):
        g = [f'<g class="sw sw{fi % 3}" style="transform-origin:{ox}px {oy}px">']
        for ang, length, width, bend in items:
            d, (x1, y1, x2, y2) = petal_path(ox, oy, ang, length, width, bend)
            gid = f"{pid}g{n}"
            defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">'
                        f'<stop offset="0" stop-color="{s[0]}"/><stop offset=".35" stop-color="{s[1]}"/>'
                        f'<stop offset=".7" stop-color="{s[2]}"/><stop offset=".9" stop-color="{s[3]}"/>'
                        f'<stop offset="1" stop-color="{s[4]}"/></linearGradient>')
            g.append(f'<path d="{d}" fill="url(#{gid})" opacity=".92"/>')
            g.append(f'<path d="{d}" fill="none" stroke="{pal["edge"]}" stroke-opacity=".16" stroke-width="1"/>')
            n += 1
        g.append("</g>")
        body.append("".join(g))
    filt = f' filter="url(#{pid}f)"' if blur else ""
    if blur:
        defs.append(f'<filter id="{pid}f" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{blur}"/></filter>')
    return "".join(defs), f'<g{filt}>' + "".join(body) + "</g>"


def glow(pal_key, cx, cy, r, op, pid):
    c = PAL[pal_key]["glow"]
    return (f'<radialGradient id="{pid}"><stop offset="0" stop-color="{c}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>',
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{pid})"/>')


SWAY = (".sw{animation:sway 14s ease-in-out infinite alternate}.sw1{animation-duration:19s;animation-direction:alternate-reverse}"
        ".sw2{animation-duration:23s}@keyframes sway{from{transform:rotate(-2.2deg)}to{transform:rotate(2.2deg)}}"
        "@media (prefers-reduced-motion:reduce){.sw,.w,.pk,.dot,.cur,.ln,.cmd,.n,.u,[class^=c],[class^=k]{animation:none!important}"
        ".ln,.n{opacity:1}.cmd{clip-path:none}.u{transform:none}}")


def edge_defs(pid):
    return (f'<linearGradient id="{pid}e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity=".04"/></linearGradient>'
            f'<linearGradient id="{pid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".07"/>'
            f'<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>')


def glass(x, y, w, h, rx, pal_key, fans, pid, tint=.58, blur=16):
    """Panel de vidrio: los mismos pétalos del fondo, difuminados y tintados, recortados al panel."""
    d, body = petals(pal_key, fans, pid + "b", blur=blur)
    defs = d + f'<clipPath id="{pid}c"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>' + edge_defs(pid)
    el = (f'<g clip-path="url(#{pid}c)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BASE}"/>{body}'
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#08090C" fill-opacity="{tint}"/>'
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{pid}s)"/></g>'
          f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="{rx-.75}" fill="none" stroke="url(#{pid}e)" stroke-width="1.5"/>')
    return defs, el


def canvas(W, H, rx, pal_key, fans, pid, glow_spec=None):
    """Lienzo negro con pétalos nítidos y borde fino."""
    d, body = petals(pal_key, fans, pid)
    gd, ge = ("", "")
    if glow_spec:
        gd, ge = glow(pal_key, *glow_spec, pid + "gl")
    defs = d + gd + f'<clipPath id="{pid}k"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>'
    el = (f'<g clip-path="url(#{pid}k)"><rect width="{W}" height="{H}" fill="{BASE}"/>{ge}{body}</g>'
          f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx-.5}" fill="none" stroke="{TEXT["border"]}"/>')
    return defs, el


def fan(ox, oy, a0, a1, n, l0, l1, w0, w1):
    """Abanico de n pétalos entre los ángulos a0 y a1, con largos y anchos interpolados."""
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        wave = math.sin(i * 1.7)
        out.append((a0 + (a1 - a0) * t, l0 + (l1 - l0) * (0.5 + 0.5 * wave), w0 + (w1 - w0) * t, 0.18 * wave))
    return out


# ---------------------------------------------------------------- piezas

def banner():
    W, H = 900, 250
    pal = "ambar"
    fans = [(990, 330, fan(990, 330, 196, 252, 7, 420, 640, 70, 120)),
            (760, -90, fan(760, -90, 128, 162, 4, 260, 360, 50, 80))]
    d, el = canvas(W, H, 18, pal, fans, "bn", glow_spec=(820, 160, 320, .25))
    ac = PAL[pal]["accent"]
    shade = ('<linearGradient id="bnsh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050507" stop-opacity=".95"/>'
             '<stop offset=".5" stop-color="#050507" stop-opacity=".6"/><stop offset=".85" stop-color="#050507" stop-opacity="0"/></linearGradient>')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Javier Karim, Backend Developer">',
         f"<defs>{d}{shade}</defs>",
         "<style>" + SWAY + ".ln{opacity:0;animation:in .7s ease-out forwards}"
         "@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>",
         el,
         f'<rect width="{W}" height="{H}" rx="18" fill="url(#bnsh)"/>',
         f'<text class="ln" style="animation-delay:.1s;font-family:{MONO}" x="54" y="74" font-size="13" fill="{ac}">hermosillo, méxico · utc−7</text>',
         f'<text class="ln" style="animation-delay:.25s" x="50" y="136" font-family="{SANS}" font-size="60" font-weight="700" fill="#F5F6F8" letter-spacing="-1.2">Javier Karim</text>',
         f'<text class="ln" style="animation-delay:.45s" x="53" y="174" font-family="{SANS}" font-size="19" fill="#B6BEC6">Backend Developer · APIs, autenticación e infraestructura</text>',
         "</svg>"]
    return "\n".join(o)


def footer():
    W, H = 900, 70
    fans = [(-110, 150, fan(-110, 150, -26, -4, 6, 560, 820, 44, 70)), (1010, 160, fan(1010, 160, 184, 206, 5, 420, 620, 36, 60))]
    d, el = canvas(W, H, 14, "ambar", fans, "ft", glow_spec=(450, 90, 260, .3))
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">',
                      f"<defs>{d}</defs><style>{SWAY}</style>", el, "</svg>"])


def typing():
    W, H = 900, 76
    pal = "medianoche"
    c = gen.THEMES[pal]
    fans = [(990, 120, fan(990, 120, 186, 214, 5, 230, 320, 30, 46))]
    d, el = canvas(W, H, 22, pal, fans, "ty", glow_spec=(860, 40, 160, .35))
    svg = gen2.typing(pal)
    svg = svg.replace('width="900" height="52" viewBox="0 0 900 52"', f'width="{W}" height="{H}" viewBox="0 0 {W} {H}"', 1)
    svg = re.sub(r'<text x="26" y="33"[^>]*>›</text>', "", svg)
    style_end = svg.index("</style>") + len("</style>")
    head = (f"<defs>{d}</defs><style>{SWAY}</style>{el}"
            f'<circle cx="34" cy="37" r="8.5" fill="none" stroke="{c["accent"]}" stroke-width="2.4"/>'
            f'<line x1="40.5" y1="43.5" x2="47" y2="50" stroke="{c["accent"]}" stroke-width="2.6" stroke-linecap="round"/>')
    body = svg[style_end:svg.rindex("</svg>")]
    return svg[:style_end] + head + f'<g transform="translate(10 12)">{body}</g></svg>'


def terminal():
    W, H = 900, 430
    pal = "ambar"
    fg, mu, ac, ok = TEXT["fg"], TEXT["muted"], PAL[pal]["accent"], TEXT["ok"]
    wx, wy, ww, wh = 46, 34, 808, 356
    fans = [(-80, 520, fan(-80, 520, -18, -62, 7, 520, 760, 80, 130)),
            (990, -60, fan(990, -60, 112, 150, 5, 300, 460, 60, 90))]
    d, el = canvas(W, H, 20, pal, fans, "wp", glow_spec=(180, 380, 340, .28))
    # Mismos pétalos desplazados a coordenadas de ventana, para el vidrio
    wfans = [(ox - wx, oy - wy, items) for ox, oy, items in fans]
    gd, gel = glass(0, 0, ww, wh, 14, pal, wfans, "win", tint=.62, blur=18)
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
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Terminal: systemctl status javier-karim. Backend Developer, Ingeniería en Sistemas Computacionales en el ITH, activo desde Hermosillo, México. Abierto a puestos Backend Jr.">',
         f"<defs>{d}{gd}"
         f'<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="20" stdDeviation="22" flood-color="#000" flood-opacity=".7"/></filter></defs>',
         "<style>", f"text{{font-family:{MONO}}}", SWAY,
         ".cmd{clip-path:inset(0 100% 0 0);animation:type 1.1s steps(31,end) .5s forwards}",
         ".ln{opacity:0;animation:in .35s ease-out forwards}.cur{animation:blink 1.1s steps(1,end) infinite}",
         "@keyframes type{to{clip-path:inset(0 0 0 0)}}",
         "@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}@keyframes blink{50%{opacity:0}}",
         "</style>",
         el,
         f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="#000" filter="url(#sh)"/>',
         f'<g transform="translate({wx} {wy})">', gel,
         f'<rect x="1" y="1" width="{ww-2}" height="37" rx="13" fill="#fff" fill-opacity=".035"/>',
         f'<line x1="1" y1="38.5" x2="{ww-1}" y2="38.5" stroke="#fff" stroke-opacity=".08"/>']
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


def numbers():
    W, H = 900, 150
    pal = "medianoche"
    c = gen.THEMES[pal]
    fans = [(450, 330, fan(450, 330, 222, 318, 11, 250, 330, 40, 62))]
    d, el = canvas(W, H, 18, pal, fans, "nb", glow_spec=(450, 170, 300, .35))
    svg = gen2.numbers(pal)
    old = f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>'
    assert old in svg
    tiles_d, tiles = "", ""
    for i in range(4):
        x = 10 + i * 222.5
        gd, gel = glass(x, 10, 213, 130, 12, pal, fans, f"t{i}", tint=.6, blur=14)
        tiles_d += gd
        tiles += gel
    svg = svg.replace(old, el + tiles, 1)
    svg = re.sub(r'<line x1="[\d.]+" y1="28" x2="[\d.]+" y2="122" stroke="[^"]+"/>', "", svg)
    head_end = svg.index(">") + 1
    return svg[:head_end] + f"<defs>{d}{tiles_d}</defs><style>{SWAY}</style>" + svg[head_end:]


CARD_PAL = {"franken-panel": "ambar", "musa-ai": "medianoche", "musaaudio": "ambar"}
CARD_FANS = {
    "franken-panel": [(980, 280, fan(980, 280, 196, 236, 6, 300, 420, 46, 80))],
    "musa-ai": [(980, -80, fan(980, -80, 126, 166, 6, 300, 420, 46, 80))],
    "musaaudio": [(1000, 120, fan(1000, 120, 168, 206, 6, 300, 430, 46, 80))],
}


def card(p):
    W, H = 900, 200
    pal = CARD_PAL[p["slug"]]
    c = gen.THEMES[pal]
    fans = CARD_FANS[p["slug"]]
    d, el = canvas(W, H, 16, pal, fans, "cd", glow_spec=(860, 100, 260, .3))
    gd, gel = glass(556, 16, 328, 168, 12, pal, fans, "fx", tint=.6, blur=14)
    svg = gen2.card(p, pal)
    old = f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>'
    assert old in svg
    shade = ('<linearGradient id="cdsh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050507" stop-opacity=".9"/>'
             '<stop offset=".55" stop-color="#050507" stop-opacity=".55"/><stop offset=".75" stop-color="#050507" stop-opacity="0"/></linearGradient>')
    svg = svg.replace(old, el + f'<rect width="{W}" height="{H}" rx="16" fill="url(#cdsh)"/>' + gel, 1)
    svg = svg.replace(f'<line x1="560" y1="28" x2="560" y2="172" stroke="{c["border"]}"/>', "")
    head_end = svg.index(">") + 1
    return svg[:head_end] + f"<defs>{d}{gd}{shade}</defs><style>{SWAY}</style>" + svg[head_end:]


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    files = {"banner.svg": banner(), "footer.svg": footer(), "typing.svg": typing(),
             "terminal.svg": terminal(), "numbers.svg": numbers()}
    for p in gen.PROJECTS:
        files[f"card-{p['slug']}.svg"] = card(p)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    print("ok", len(files))
