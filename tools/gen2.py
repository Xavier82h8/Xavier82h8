"""Segunda tanda de SVG animados del perfil: banner con olas, línea que se escribe sola,
tarjeta de cifras, pie con olas y tarjetas de proyecto con paquetes viajando por el flujo."""
import os
import sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(__file__))
import gen  # reutiliza THEMES, MONO, SANS y PROJECTS (y escribe header/cards base)

OUT = sys.argv[1] if __name__ == "__main__" else None
THEMES, MONO, SANS = gen.THEMES, gen.MONO, gen.SANS
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def wave_path(width, base, amp, period, height):
    """Ola periódica de ancho `width` (múltiplo de `period`), cerrada hacia arriba."""
    d = [f"M0 {base}"]
    x = 0
    while x < width:
        d.append(f"q{period/4} {-amp} {period/2} 0 t{period/2} 0")
        x += period
    d.append(f"V0 H0 Z")
    return " ".join(d)


def banner():
    W, H = 900, 250
    ink1, ink2 = "#102A3D", "#1F5272"
    amber = "#F2A93B"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Javier Karim, Backend Developer">',
         "<defs>",
         f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ink1}"/><stop offset="1" stop-color="{ink2}"/></linearGradient>',
         f'<radialGradient id="glow" cx="0.82" cy="0.25" r="0.45"><stop offset="0" stop-color="{amber}" stop-opacity=".22"/><stop offset="1" stop-color="{amber}" stop-opacity="0"/></radialGradient>',
         '<clipPath id="r"><path d="M0 14a14 14 0 0 1 14-14h872a14 14 0 0 1 14 14v236H0z"/></clipPath>',
         "</defs>",
         "<style>",
         ".w{animation:slide linear infinite}",
         ".w1{animation-duration:14s}.w2{animation-duration:9s;animation-direction:reverse}.w3{animation-duration:20s}",
         "@keyframes slide{from{transform:translateX(0)}to{transform:translateX(-300px)}}",
         ".pk{animation:pk linear infinite}",
         "@keyframes pk{from{transform:translateX(0)}to{transform:translateX(330px)}}",
         ".in{opacity:0;animation:in .7s ease-out forwards}",
         "@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}",
         REDUCED.replace("animation:none", "animation:none;opacity:1"),
         "</style>"]
    # Cuerpo: tres capas de ola desplazándose; la de abajo cierra el banner con borde ondulado
    o.append('<g clip-path="url(#r)">')
    o.append(f'<g class="w w3"><path d="{wave_path(W+600, 216, 14, 300, H)}" fill="{amber}" opacity=".35"/></g>')
    o.append(f'<g class="w w2"><path d="{wave_path(W+600, 205, 12, 300, H)}" fill="#2F7AA0" opacity=".7"/></g>')
    o.append(f'<g class="w w1"><path d="{wave_path(W+600, 194, 10, 300, H)}" fill="url(#g)"/></g>')
    o.append(f'<rect width="{W}" height="200" fill="url(#glow)"/>')
    o.append('</g>')
    # Tráfico: líneas finas con paquetes ámbar a la derecha
    for i, (y, dur, delay) in enumerate([(70, 3.4, 0), (98, 2.6, 1.1), (126, 4.1, .5), (154, 3.0, 1.9)]):
        o.append(f'<line x1="540" y1="{y}" x2="870" y2="{y}" stroke="#3A6A88" stroke-width="1"/>')
        o.append(f'<g class="pk" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
                 f'<rect x="532" y="{y-2}" width="14" height="4" rx="2" fill="{amber}" opacity=".9"/></g>')
    for i, y in enumerate([70, 98, 126, 154]):
        o.append(f'<circle cx="870" cy="{y}" r="3.5" fill="{ink1}" stroke="{amber}" stroke-width="1.5"/>')
    o.append(f'<text x="870" y="186" text-anchor="end" font-family="{MONO}" font-size="12" fill="#9DB4C4">:443 → nginx → api</text>')
    o.append(f'<text class="in" style="animation-delay:.1s" x="52" y="66" font-family="{MONO}" font-size="13" fill="{amber}">hermosillo, méxico</text>')
    o.append(f'<text class="in" style="animation-delay:.25s" x="50" y="122" font-family="{SANS}" font-size="56" font-weight="700" fill="#F4F7FA" letter-spacing="-1">Javier Karim</text>')
    o.append(f'<text class="in" style="animation-delay:.45s" x="52" y="158" font-family="{SANS}" font-size="19" fill="#C3D3DE">Backend Developer · APIs, autenticación e infraestructura</text>')
    o.append("</svg>")
    return "\n".join(o)


def footer():
    W, H = 900, 110
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">',
         '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F5272"/><stop offset="1" stop-color="#102A3D"/></linearGradient></defs>',
         "<style>.w{animation:slide linear infinite}.w1{animation-duration:16s}.w2{animation-duration:11s;animation-direction:reverse}"
         "@keyframes slide{from{transform:translateX(0)}to{transform:translateX(-300px)}}" + REDUCED + "</style>",
         f'<g transform="translate(0 {H}) scale(1 -1)">',
         f'<g class="w w2"><path d="{wave_path(W+600, 80, 12, 300, H)}" fill="#F2A93B" opacity=".35"/></g>',
         f'<g class="w w2" style="animation-duration:7s"><path d="{wave_path(W+600, 73, 11, 300, H)}" fill="#2F7AA0" opacity=".7"/></g>',
         f'<g class="w w1"><path d="{wave_path(W+600, 66, 10, 300, H)}" fill="url(#g)"/></g>',
         "</g></svg>"]
    return "\n".join(o)


PHRASES = [
    "Diseño APIs REST con Node.js, TypeScript y FastAPI",
    "Autenticación: OAuth 2.0, OIDC + PKCE, JWT y RBAC",
    "PostgreSQL, Redis y Prisma en la capa de datos",
    "Docker, Nginx y GitHub Actions hasta producción",
    "Busco mi primer puesto como Backend Developer Jr",
]


def typing(t):
    c = THEMES[t]
    W, H = 900, 52
    fs, cw = 21, 12.6  # ancho de carácter fijo vía textLength
    x0 = 56
    TYPE, HOLD, DEL, GAP = 0.055, 1.9, 0.022, 0.35
    slots = []
    tot = 0.0
    for p in PHRASES:
        n = len(p)
        dur = n * TYPE + HOLD + n * DEL + GAP
        slots.append((tot, n, dur))
        tot += dur
    css = [f"text{{font-family:{MONO}}}",
           ".cur{animation:blink 1s steps(1,end) infinite}",
           "@keyframes blink{50%{opacity:0}}"]
    body = []
    for i, (p, (start, n, dur)) in enumerate(zip(PHRASES, slots)):
        a = start / tot * 100
        b = (start + n * TYPE) / tot * 100
        cc = (start + n * TYPE + HOLD) / tot * 100
        d = (start + n * TYPE + HOLD + n * DEL) / tot * 100
        w = n * cw
        css.append(
            f"@keyframes c{i}{{0%,{a:.3f}%{{transform:scaleX(0);animation-timing-function:steps({n},end)}}"
            f"{b:.3f}%{{transform:scaleX(1)}}{cc:.3f}%{{transform:scaleX(1);animation-timing-function:steps({n},end)}}"
            f"{d:.3f}%,100%{{transform:scaleX(0)}}}}")
        css.append(
            f"@keyframes k{i}{{0%,{a:.3f}%{{opacity:0;transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{a+0.001:.3f}%{{opacity:1}}"
            f"{b:.3f}%{{opacity:1;transform:translateX({w:.1f}px)}}{cc:.3f}%{{opacity:1;transform:translateX({w:.1f}px);animation-timing-function:steps({n},end)}}"
            f"{d:.3f}%{{opacity:1;transform:translateX(0)}}{d+0.001:.3f}%,100%{{opacity:0}}}}")
        css.append(f".c{i}{{transform-box:fill-box;transform-origin:left;animation:c{i} {tot:.2f}s infinite}}"
                   f".k{i}{{animation:k{i} {tot:.2f}s infinite}}")
        body.append(f'<clipPath id="m{i}"><rect class="c{i}" x="{x0}" y="8" width="{w:.1f}" height="36"/></clipPath>')
        body.append(f'<text clip-path="url(#m{i})" x="{x0}" y="33" font-size="{fs}" fill="{c["fg"]}" '
                    f'textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{esc(p)}</text>')
        body.append(f'<rect class="k{i}" x="{x0+2}" y="13" width="11" height="25" fill="{c["accent"]}" opacity="0"/>')
    # Sin movimiento: primera frase completa y fija
    css.append("@media (prefers-reduced-motion:reduce){[class^=c],[class^=k]{animation:none!important}"
               ".c0{transform:none}.c1,.c2,.c3,.c4{transform:scaleX(0)}}")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{esc(" · ".join(PHRASES))}">',
         "<style>" + "".join(css) + "</style>",
         f'<text x="26" y="33" font-size="{fs}" font-weight="700" fill="{c["accent"]}">›</text>',
         *body, "</svg>"]
    return "\n".join(o)


NUMBERS = [
    ("~100", "endpoints REST", "en tres APIs"),
    ("~330", "tests automatizados", "backend y datos de MUSA-AI"),
    ("47 153", "ejemplos curados", "dataset propio para afinar un LLM"),
    ("3", "proyectos completos", "de la idea al servidor"),
]


def numbers(t):
    c = THEMES[t]
    W, H = 900, 150
    col = W / 4
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{esc("; ".join(n + " " + a + " " + b for n, a, b in NUMBERS))}">',
         "<style>.u{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow .9s cubic-bezier(.2,.7,.2,1) forwards}"
         "@keyframes grow{to{transform:scaleX(1)}}"
         ".n{opacity:0;animation:in .6s ease-out forwards}@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
         "@media (prefers-reduced-motion:reduce){.u{transform:none;animation:none}.n{opacity:1;animation:none}}</style>",
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>']
    for i, (num, a, b) in enumerate(NUMBERS):
        x = 32 + i * col
        dl = 0.15 + i * 0.18
        if i:
            o.append(f'<line x1="{i*col:.1f}" y1="28" x2="{i*col:.1f}" y2="{H-28}" stroke="{c["border"]}"/>')
        o.append(f'<g class="n" style="animation-delay:{dl:.2f}s">'
                 f'<text x="{x:.1f}" y="70" font-family="{SANS}" font-size="38" font-weight="700" fill="{c["fg"]}" letter-spacing="-.5">{esc(num)}</text>'
                 f'<text x="{x:.1f}" y="100" font-family="{SANS}" font-size="15" font-weight="600" fill="{c["fg"]}">{esc(a)}</text>'
                 f'<text x="{x:.1f}" y="121" font-family="{SANS}" font-size="12.5" fill="{c["muted"]}">{esc(b)}</text></g>')
        o.append(f'<rect class="u" style="animation-delay:{dl+.25:.2f}s" x="{x:.1f}" y="80" width="40" height="3" rx="1.5" fill="{c["accent"]}"/>')
    o.append("</svg>")
    return "\n".join(o)


def card(p, t):
    """Tarjeta base de gen.py + flujo con ancho fijo y un paquete que lo recorre."""
    svg = gen.card(p, t)
    c = THEMES[t]
    cw = 7.8
    w = len(p["flow"]) * cw
    old = f'<text x="32" y="150" font-family="{MONO}" font-size="13" fill="{c["accent"]}">{esc(p["flow"])}</text>'
    assert old in svg
    new = (f'<text x="32" y="150" font-family="{MONO}" font-size="13" fill="{c["accent"]}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{esc(p["flow"])}</text>'
           f'<line x1="32" y1="158" x2="{32+w:.1f}" y2="158" stroke="{c["border"]}"/>'
           f'<rect class="pk" x="28" y="156.5" width="12" height="3" rx="1.5" fill="{c["accent"]}"/>')
    svg = svg.replace(old, new)
    style = ("<style>.pk{animation:pk 3.2s cubic-bezier(.45,0,.55,1) infinite}"
             f"@keyframes pk{{0%{{transform:translateX(0);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateX({w-4:.1f}px);opacity:0}}}}"
             ".dot{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}"
             "@keyframes pulse{50%{transform:scale(1.6);opacity:.45}}"
             "@media (prefers-reduced-motion:reduce){.pk,.dot{animation:none}}</style>")
    svg = svg.replace('">\n<rect x="0.5"', '">\n' + style + '\n<rect x="0.5"', 1)
    svg = svg.replace(f'<circle cx="589" cy="172" r="4" fill="{c["ok"]}"/>',
                      f'<circle class="dot" cx="589" cy="172" r="4" fill="{c["ok"]}"/>')
    return svg


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)


if __name__ == "__main__":
    write("banner.svg", banner())
    write("footer.svg", footer())
    for t in THEMES:
        write(f"typing-{t}.svg", typing(t))
        write(f"numbers-{t}.svg", numbers(t))
        for p in gen.PROJECTS:
            write(f"{p['slug']}-{t}.svg", card(p, t))
    print("ok")
