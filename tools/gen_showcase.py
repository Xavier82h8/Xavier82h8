"""Banners nocturnos de los repos showcase + gráfica de latencia de MusaAudio.

Uso: python gen_showcase.py <dir_salida>
Escribe <dir>/franken-panel-banner.svg, musa-ai-banner.svg, musaaudio-banner.svg, musaaudio-latencia.svg
"""
import os
import sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(__file__))
import gen4  # noqa: E402

MONO, SANS, TEXT, PAL = gen4.MONO, gen4.SANS, gen4.TEXT, gen4.PAL
fan = gen4.fan

SHOW = {
    "franken-panel": dict(
        pal="ambar", name="Franken Panel", tag="Panel autohospedado para Ubuntu Server",
        flow="cloudflared → nginx → fastify :3001 → systemd",
        chips=[("~50", "endpoints REST"), ("5", "roles RBAC"), ("23", "tests en verde")],
        fans=[(990, 330, fan(990, 330, 196, 252, 7, 420, 640, 70, 120)),
              (780, -90, fan(780, -90, 128, 160, 4, 260, 360, 50, 80))]),
    "musa-ai": dict(
        pal="medianoche", name="MUSA-AI", tag="Tutor musical con IA que escribe partituras reales",
        flow="caddy → fastapi (SSE) → cola redis → llama.cpp",
        chips=[("47 153", "ejemplos curados"), ("12", "notebooks de entrenamiento"), ("504", "commits")],
        fans=[(990, -80, fan(990, -80, 126, 170, 7, 420, 620, 70, 115)),
              (760, 360, fan(760, 360, 214, 246, 4, 260, 360, 50, 80))]),
    "musaaudio": dict(
        pal="ambar", name="MusaAudio", tag="Música de escritorio y web con búsqueda unificada",
        flow="git push → GitHub Actions → docker → nginx (TLS)",
        chips=[("~36", "endpoints REST"), ("183", "tests de frontend"), ("14 → 5 s", "reproducir en frío")],
        fans=[(1010, 120, fan(1010, 120, 160, 204, 7, 420, 620, 70, 115)),
              (620, -120, fan(620, -120, 100, 130, 4, 260, 340, 46, 70))]),
}


def banner(key):
    s = SHOW[key]
    W, H = 900, 280
    pal = s["pal"]
    ac = PAL[pal]["accent"]
    d, el = gen4.canvas(W, H, 18, pal, s["fans"], "bn", glow_spec=(800, 140, 340, .26))
    shade = ('<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050507" stop-opacity=".95"/>'
             '<stop offset=".55" stop-color="#050507" stop-opacity=".6"/><stop offset=".85" stop-color="#050507" stop-opacity="0"/></linearGradient>')
    chips_d, chips = "", ""
    x = 44
    for i, (num, label) in enumerate(s["chips"]):
        nw = len(num) * 12.6
        w = 18 + nw + 10 + len(label) * 7.0 + 18
        cd, ce = gen4.glass(x, 190, w, 54, 12, pal, s["fans"], f"c{i}", tint=.55, blur=14)
        chips_d += cd
        chips += ce + (f'<text x="{x+18}" y="225" font-family="{SANS}" font-size="22" font-weight="700" fill="{TEXT["fg"]}">{esc(num)}</text>'
                       f'<text x="{x+18+nw+10:.0f}" y="223" font-family="{SANS}" font-size="13.5" fill="{TEXT["muted"]}">{esc(label)}</text>')
        x += w + 12
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="{esc(s["name"])}: {esc(s["tag"])}. ' + "; ".join(f"{n} {l}" for n, l in s["chips"]) + '">',
        f"<defs>{d}{shade}{chips_d}</defs>",
        "<style>" + gen4.SWAY + ".ln{opacity:0;animation:in .7s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>",
        el, f'<rect width="{W}" height="{H}" rx="18" fill="url(#sh)"/>',
        f'<text class="ln" style="animation-delay:.1s;font-family:{MONO}" x="46" y="62" font-size="13" fill="{ac}">{esc(s["flow"])}</text>',
        f'<text class="ln" style="animation-delay:.25s" x="42" y="122" font-family="{SANS}" font-size="54" font-weight="700" fill="#F5F6F8" letter-spacing="-1">{esc(s["name"])}</text>',
        f'<text class="ln" style="animation-delay:.4s" x="45" y="158" font-family="{SANS}" font-size="19" fill="#B6BEC6">{esc(s["tag"])}</text>',
        f'<g class="ln" style="animation-delay:.6s">{chips}</g>',
        "</svg>"])


def latency():
    """Barras horizontales, una escala (segundos). Gris = antes, ámbar = después; cada fila lo dice en texto."""
    W, H = 900, 250
    rows = [("Antes · reproducir en frío", "búsqueda del audio + primer byte", 14.4, "antes", "14,4 s"),
            ("Después · reproducir en frío", "yt-dlp más rápido y menos reintentos", 5.0, "despues", "~5 s"),
            ("Después · repetir una canción", "URL de stream servida desde caché", 0.12, "despues", "~0,12 s")]
    x0, x1, vmax = 330, 840, 16
    sx = lambda v: x0 + (x1 - x0) * v / vmax
    ac = PAL["ambar"]["accent"]
    col = {"antes": "#4A5059", "despues": ac}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Latencia de reproducción: antes en frío 14,4 s; después en frío unos 5 s; repetir unos 0,12 s">',
         "<style>.b{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:g .9s cubic-bezier(.2,.7,.2,1) forwards}"
         "@keyframes g{to{transform:scaleX(1)}}@media (prefers-reduced-motion:reduce){.b{transform:none;animation:none}}</style>",
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{gen4.BASE}" stroke="{TEXT["border"]}"/>',
         f'<text x="32" y="44" font-family="{SANS}" font-size="17" font-weight="600" fill="{TEXT["fg"]}">Latencia de reproducción, en segundos</text>',
         f'<text x="32" y="66" font-family="{SANS}" font-size="13" fill="{TEXT["muted"]}">Medido desde el servidor de producción, antes y después de la fase 3 de optimización</text>']
    for v in range(0, vmax + 1, 4):
        x = sx(v)
        o.append(f'<line x1="{x:.1f}" y1="88" x2="{x:.1f}" y2="214" stroke="#fff" stroke-opacity="{.16 if v == 0 else .06}"/>')
        o.append(f'<text x="{x:.1f}" y="232" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{TEXT["muted"]}" style="font-variant-numeric:tabular-nums">{v}</text>')
    for i, (label, sub, v, kind, shown) in enumerate(rows):
        y = 104 + i * 40
        w = max(sx(v) - x0, 3)
        o.append(f'<text x="32" y="{y+6}" font-family="{SANS}" font-size="14" font-weight="600" fill="{TEXT["fg"]}">{esc(label)}</text>')
        o.append(f'<text x="32" y="{y+23}" font-family="{SANS}" font-size="11.5" fill="{TEXT["muted"]}">{esc(sub)}</text>')
        o.append(f'<rect class="b" style="animation-delay:{.2 + i*.15:.2f}s" x="{x0}" y="{y-6}" width="{w:.1f}" height="16" rx="4" fill="{col[kind]}"/>')
        o.append(f'<text x="{x0 + w + 10:.1f}" y="{y+7}" font-family="{SANS}" font-size="14" font-weight="700" fill="{TEXT["fg"]}" style="font-variant-numeric:tabular-nums">{shown}</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for k in SHOW:
        open(os.path.join(out, f"{k}-banner.svg"), "w", encoding="utf-8").write(banner(k))
    open(os.path.join(out, "musaaudio-latencia.svg"), "w", encoding="utf-8").write(latency())
    print("ok")
