"""Genera los SVG del README de perfil (header + tarjetas de proyecto), en tema oscuro y claro."""
import os
import sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1] if __name__ == "__main__" else None
if OUT:
    os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0F1A24", bar="#142330", border="#24384A", fg="#D3DEE7",
                 muted="#7F93A3", accent="#F2A93B", ok="#4CC38A"),
    "light": dict(bg="#FBFCFD", bar="#EEF3F7", border="#D3DDE5", fg="#17242F",
                  muted="#5B6E7D", accent="#A85F00", ok="#17803D"),
}
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', 'JetBrains Mono', Menlo, Consolas, monospace"
SANS = "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"


def span(text, color=None, weight=None):
    attrs = ""
    if color:
        attrs += f' fill="{color}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    return f"<tspan{attrs}>{esc(text)}</tspan>"


def header(t):
    W, H = 900, 372
    c = THEMES[t]
    fg, mu, ac, ok = c["fg"], c["muted"], c["accent"], c["ok"]
    lines = [
        # (y, font-size, contenido)
        (118, 22, span("● ", ok) + span("javier-karim.service", fg, 700) + span(" - Backend Developer", mu)),
        (152, 14, span("     Loaded: ", mu) + span("loaded (Ingeniería en Sistemas Computacionales, ITH; 8.º semestre)", fg)),
        (178, 14, span("     Active: ", mu) + span("active (running)", ok, 700) + span(" desde Hermosillo, Sonora, México", fg)),
        (204, 14, span("      Tasks: ", mu) + span("3 (franken-panel, musa-ai, musaaudio)", fg)),
        (230, 14, span("     CGroup: ", mu) + span("APIs · autenticación · bases de datos · Linux · Docker · CI/CD", fg)),
        (256, 14, span("       Docs: ", mu) + span("linkedin.com/in/javier-karim", ac)),
        (300, 14, span("javier-karim[1]: ", mu) + span("Abierto a puestos Backend Jr, en Hermosillo o remoto. Inglés B2.", fg)),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Javier Karim, Backend Developer en Hermosillo, México. Abierto a puestos Backend Jr.">',
           "<style>",
           f"text{{font-family:{MONO};}}",
           ".cmd{clip-path:inset(0 100% 0 0);animation:type 1.1s steps(31,end) .3s forwards}",
           ".ln{opacity:0;animation:in .35s ease-out forwards}",
           ".cur{animation:blink 1.1s steps(1,end) infinite}",
           "@keyframes type{to{clip-path:inset(0 0 0 0)}}",
           "@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}",
           "@keyframes blink{50%{opacity:0}}",
           "@media (prefers-reduced-motion:reduce){.cmd{clip-path:none;animation:none}.ln{opacity:1;animation:none}.cur{animation:none}}",
           "</style>",
           f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
           f'<path d="M0.5 12.5a12 12 0 0 1 12-12h{W-25}a12 12 0 0 1 12 12v23h-{W-1}z" fill="{c["bar"]}"/>',
           f'<line x1="0.5" y1="36" x2="{W-0.5}" y2="36" stroke="{c["border"]}"/>',
           f'<text x="24" y="23" font-size="12.5" fill="{mu}">javier@hermosillo: ~</text>',
           f'<text x="{W-24}" y="23" font-size="12.5" fill="{mu}" text-anchor="end">bash</text>',
           f'<text class="cmd" x="32" y="76" font-size="15">{span("$ ", ac, 700)}{span("systemctl status javier-karim", fg)}</text>']
    for i, (y, fs, content) in enumerate(lines):
        delay = 1.55 + i * 0.13
        out.append(f'<text class="ln" style="animation-delay:{delay:.2f}s" x="32" y="{y}" font-size="{fs}" '
                   f'xml:space="preserve">{content}</text>')
    d = 1.55 + len(lines) * 0.13
    out.append(f'<text class="ln" style="animation-delay:{d:.2f}s" x="32" y="340" font-size="15">'
               f'{span("$ ", ac, 700)}<tspan class="cur" fill="{fg}">▍</tspan></text>')
    out.append("</svg>")
    return "\n".join(out)


PROJECTS = [
    dict(slug="franken-panel", name="Franken Panel",
         desc=["Panel autohospedado para administrar sitios, Nginx,",
               "SSL y despliegues en Ubuntu Server desde el navegador."],
         flow="cloudflared → nginx → fastify :3001 → systemd",
         facts=["~50 endpoints REST", "RBAC, sesiones y auditoría", "Webhooks con firma HMAC"],
         stack="Node.js · Fastify · WebSockets · Bash · Nginx · Certbot"),
    dict(slug="musa-ai", name="MUSA-AI",
         desc=["Tutor musical con IA que escribe partituras reales,",
               "con un modelo propio afinado con QLoRA."],
         flow="caddy → fastapi (SSE) → cola redis → llama.cpp",
         facts=["OIDC + PKCE, Apple, sin contraseña", "Failover entre nodos de inferencia", "Dataset v7: 47 153 ejemplos"],
         stack="Python · FastAPI · PostgreSQL · Redis · Prometheus · Rust"),
    dict(slug="musaaudio", name="MusaAudio",
         desc=["Música de escritorio y web con búsqueda unificada",
               "en YouTube, Spotify y archivos locales."],
         flow="git push → GitHub Actions → docker → nginx (TLS)",
         facts=["~36 endpoints REST", "JWT, bcrypt y rate limiting", "Caché con TTL y métricas por ruta"],
         stack="TypeScript · Express · Prisma · Jest · Docker · Tauri"),
]


def card(p, t):
    W, H = 900, 200
    c = THEMES[t]
    fg, mu, ac, ok = c["fg"], c["muted"], c["accent"], c["ok"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{esc(p["name"])}: {esc(" ".join(p["desc"]))}">',
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
         f'<text x="32" y="56" font-family="{SANS}" font-size="27" font-weight="700" fill="{fg}">{esc(p["name"])}</text>']
    for i, line in enumerate(p["desc"]):
        o.append(f'<text x="32" y="{88 + i*22}" font-family="{SANS}" font-size="15.5" fill="{mu}">{esc(line)}</text>')
    o.append(f'<text x="32" y="150" font-family="{MONO}" font-size="13" fill="{ac}">{esc(p["flow"])}</text>')
    o.append(f'<text x="32" y="176" font-family="{MONO}" font-size="12.5" fill="{mu}">{esc(p["stack"])}</text>')
    o.append(f'<line x1="560" y1="28" x2="560" y2="172" stroke="{c["border"]}"/>')
    for i, f in enumerate(p["facts"]):
        y = 58 + i * 30
        o.append(f'<rect x="584" y="{y-9}" width="7" height="7" rx="1.5" fill="{ac}"/>')
        o.append(f'<text x="602" y="{y}" font-family="{SANS}" font-size="15" fill="{fg}">{esc(f)}</text>')
    o.append(f'<circle cx="589" cy="172" r="4" fill="{ok}"/>')
    o.append(f'<text x="602" y="176" font-family="{SANS}" font-size="13" fill="{mu}">Ficha técnica pública · código privado</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for t in THEMES:
        with open(os.path.join(OUT, f"header-{t}.svg"), "w", encoding="utf-8") as fh:
            fh.write(header(t))
        for p in PROJECTS:
            with open(os.path.join(OUT, f"{p['slug']}-{t}.svg"), "w", encoding="utf-8") as fh:
                fh.write(card(p, t))
    print("ok")
