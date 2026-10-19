"""Gera as imagens do README do perfil nas versões clara e escura.

Uso: python assets/src/gerar_assets.py
Saída: assets/light/*.svg e assets/dark/*.svg

Clara = "dreamy gradient" (degradê rosa/lilás/pêssego, vidro, estrelas cromadas).
Escura = "neon night" (fundo noturno, grade, brilho rosa/lilás/menta).
Os SVGs são estáticos com animações CSS leves, desligadas quando o visitante
pede movimento reduzido.
"""

from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parents[1]

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
SERIF = "Georgia, 'Times New Roman', serif"

TEMAS = {
    "light": {
        "bg0": "#FDE7F3", "bg1": "#EBDDFF", "bg2": "#FFE3D3",
        "ink": "#2B1B3D", "muted": "#5B4A6E", "soft": "#8C7AA0",
        "pink": "#E2408F", "violet": "#8A5CF6", "peach": "#F28B5B", "mint": "#1FA37A",
        "blob1": "#FF8FCB", "blob2": "#A88BFF", "blob3": "#FFC27A",
        "glass": "#FFFFFF", "glass_op": ".55", "stroke": "#FFFFFF", "stroke_op": "1",
        "grid_op": "0", "glow": False, "cat": "#2B1B3D",
    },
    "dark": {
        "bg0": "#0E0B1F", "bg1": "#170D2A", "bg2": "#1C0F2E",
        "ink": "#F5EFFF", "muted": "#C9BEE6", "soft": "#8E82B0",
        "pink": "#FF4FB8", "violet": "#B57BFF", "peach": "#FF9F6B", "mint": "#4FF0D0",
        "blob1": "#FF4FB8", "blob2": "#7B4DFF", "blob3": "#4FF0D0",
        "glass": "#1E1438", "glass_op": ".72", "stroke": "#B57BFF", "stroke_op": ".45",
        "grid_op": ".10", "glow": True, "cat": "#0B0818",
    },
}


def estilos(t):
    return f"""<style>
.ink{{fill:{t['ink']}}} .muted{{fill:{t['muted']}}} .soft{{fill:{t['soft']}}}
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}} .serif{{font-family:{SERIF}}}
.twinkle{{animation:tw 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
.d1{{animation-delay:.8s}} .d2{{animation-delay:1.6s}} .d3{{animation-delay:2.4s}}
.spin{{animation:sp 9s linear infinite;transform-box:fill-box;transform-origin:center}}
.float{{animation:fl 6s ease-in-out infinite}}
.blink{{animation:bl 1.1s steps(1) infinite}}
.eq{{animation:eq 1.4s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}}
@keyframes tw{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.35;transform:scale(.7)}}}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
@keyframes bl{{50%{{opacity:0}}}}
@keyframes eq{{0%,100%{{transform:scaleY(.35)}}50%{{transform:scaleY(1)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>"""


def defs(t):
    glow = (
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="5" result="g"/>'
        '<feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        if t["glow"] else
        '<filter id="glow"><feDropShadow dx="0" dy="4" stdDeviation="6" '
        'flood-color="#8A5CF6" flood-opacity=".18"/></filter>'
    )
    return f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg0']}"/><stop offset=".5" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{t['pink']}"/><stop offset=".55" stop-color="{t['violet']}"/><stop offset="1" stop-color="{t['mint'] if t['glow'] else t['peach']}"/></linearGradient>
<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#E4D8FF"/><stop offset=".55" stop-color="#9C87D8"/><stop offset="1" stop-color="#F6E9FF"/></linearGradient>
<radialGradient id="b1"><stop offset="0" stop-color="{t['blob1']}" stop-opacity=".75"/><stop offset="1" stop-color="{t['blob1']}" stop-opacity="0"/></radialGradient>
<radialGradient id="b2"><stop offset="0" stop-color="{t['blob2']}" stop-opacity=".7"/><stop offset="1" stop-color="{t['blob2']}" stop-opacity="0"/></radialGradient>
<radialGradient id="b3"><stop offset="0" stop-color="{t['blob3']}" stop-opacity=".55"/><stop offset="1" stop-color="{t['blob3']}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{t['violet']}" stroke-opacity="{t['grid_op']}"/></pattern>
{glow}
</defs>"""


def fundo(t, w, h, blobs):
    out = [f'<clipPath id="moldura"><rect width="{w}" height="{h}" rx="26"/></clipPath>',
           f'<rect width="{w}" height="{h}" rx="26" fill="url(#bg)"/><g clip-path="url(#moldura)">']
    for gid, cx, cy, r in blobs:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#grid)"/></g>')
    out.append(
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="25" fill="none" '
        f'stroke="{t["stroke"]}" stroke-opacity="{t["stroke_op"]}" stroke-width="1.5"/>'
    )
    return "".join(out)


def estrela(t, x, y, s, cls=""):
    """Estrela de quatro pontas: cromada no claro, neon no escuro."""
    fill = t["pink"] if t["glow"] else "url(#chrome)"
    stroke = "none" if t["glow"] else "#FFFFFF"
    flt = ' filter="url(#glow)"' if t["glow"] else ""
    d = (f"M{x} {y-s} Q{x+s*.18} {y-s*.18} {x+s} {y} Q{x+s*.18} {y+s*.18} {x} {y+s} "
         f"Q{x-s*.18} {y+s*.18} {x-s} {y} Q{x-s*.18} {y-s*.18} {x} {y-s}Z")
    return f'<path class="twinkle {cls}" d="{d}" fill="{fill}" stroke="{stroke}"{flt}/>'


def vidro(t, x, y, w, h, rx=20):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t["glass"]}" '
            f'fill-opacity="{t["glass_op"]}" stroke="{t["stroke"]}" '
            f'stroke-opacity="{t["stroke_op"]}" stroke-width="1.5"/>')


def largura_chip(texto):
    return int(len(texto) * 8.2 + 30)


def chip(t, x, y, texto, cor, w=None):
    w = w or largura_chip(texto)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="32" rx="16" fill="{cor}" fill-opacity=".14" '
            f'stroke="{cor}" stroke-opacity=".8"/>'
            f'<text x="{x+w/2}" y="{y+21}" text-anchor="middle" class="mono" font-size="13" '
            f'fill="{cor}">{escape(texto)}</text>')


def vinil(t, cx, cy, r):
    return (f'<g class="spin"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#120C22"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.8}" fill="none" stroke="#3A2E5C" stroke-width="1.2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.62}" fill="none" stroke="#3A2E5C" stroke-width="1.2"/>'
            f'<path d="M{cx-r*.7} {cy-r*.35} A{r*.78} {r*.78} 0 0 1 {cx-r*.2} {cy-r*.75}" stroke="#FFFFFF" '
            f'stroke-opacity=".35" stroke-width="2" fill="none"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.34}" fill="url(#hl)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*.07}" fill="#120C22"/></g>')


def gato(t, x, y, s=1.0):
    """Gatinho preto espiando: cabeça, orelhas, olhos e bigodes."""
    c = t["cat"]
    eye = t["mint"] if t["glow"] else "#FFD36B"
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M0 40 L6 4 L24 20 Q40 14 56 20 L74 4 L80 40 Q80 62 40 62 Q0 62 0 40Z" fill="{c}"/>'
            f'<ellipse cx="26" cy="38" rx="6" ry="7" fill="{eye}"/><ellipse cx="54" cy="38" rx="6" ry="7" fill="{eye}"/>'
            f'<ellipse cx="26" cy="39" rx="2" ry="5" fill="{c}"/><ellipse cx="54" cy="39" rx="2" ry="5" fill="{c}"/>'
            f'<path d="M37 48 L40 51 L43 48Z" fill="{t["pink"]}"/>'
            f'<path d="M16 50 H-6 M16 54 L-4 60 M64 50 H86 M64 54 L84 60" stroke="{t["soft"]}" stroke-width="1.4"/>'
            f'</g>')


def flor(t, cx, cy, r, cor):
    petalas = "".join(
        f'<ellipse cx="{cx}" cy="{cy-r}" rx="{r*.55}" ry="{r*.9}" fill="{cor}" '
        f'transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 72))
    return f'<g>{petalas}<circle cx="{cx}" cy="{cy}" r="{r*.45}" fill="#FFE7A8"/></g>'


def svg(w, h, label, corpo, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}">{estilos(t)}{defs(t)}{corpo}</svg>\n')


# ---------------------------------------------------------------- peças

def banner(t):
    w, h = 1200, 420
    neon = ' filter="url(#glow)"' if t["glow"] else ""
    corpo = [fundo(t, w, h, [("b1", 1000, 90, 260), ("b2", 740, 360, 230), ("b3", 1150, 380, 180)])]
    corpo.append(chip(t, 68, 56, "✦ IA · DADOS · SISTEMAS", t["violet"]))
    corpo.append(f'<text x="64" y="172" class="sans ink" font-size="76" font-weight="800" letter-spacing="-2">oi, eu sou</text>')
    corpo.append(f'<text x="64" y="262" class="sans" font-size="92" font-weight="800" letter-spacing="-3" fill="url(#hl)"{neon}>a gabi.</text>')
    corpo.append(f'<text x="70" y="314" class="sans muted" font-size="22">psicóloga que programa · pessoas × dados × impacto</text>')
    cx = 70
    for texto, cor in (("♡ people_first", t["pink"]), ("✦ data_driven", t["mint"]), ("↻ always_learning", t["violet"])):
        corpo.append(chip(t, cx, 344, texto, cor))
        cx += largura_chip(texto) + 12
    # janela de código com o gato espiando
    gx, gy = 742, 96
    corpo.append(f'<g class="float">')
    corpo.append(gato(t, gx + 300, gy - 50, 0.9))
    corpo.append(vidro(t, gx, gy, 400, 230))
    corpo.append("".join(f'<circle cx="{gx+26+i*20}" cy="{gy+24}" r="6" fill="{c}"/>'
                         for i, c in enumerate((t["pink"], t["peach"], t["mint"]))))
    corpo.append(f'<text x="{gx+340}" y="{gy+29}" class="mono soft" font-size="12" text-anchor="end">gabi.js</text>')
    linhas = [
        [(t["violet"], "const "), (t["ink"], "gabi = {")],
        [(t["pink"], "  formação: "), (t["muted"], '"Psicologia",')],
        [(t["pink"], "  estudando: "), (t["muted"], '"IA & Dados · IFMT",')],
        [(t["pink"], "  foco: "), (t["muted"], '["dados", "automação"],')],
        [(t["pink"], "  vibe: "), (t["muted"], '"sempre criando ✦"')],
        [(t["ink"], "}")],
    ]
    for i, partes in enumerate(linhas):
        spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for c, s in partes)
        corpo.append(f'<text x="{gx+26}" y="{gy+70+i*27}" class="mono" font-size="15" xml:space="preserve">{spans}</text>')
    corpo.append(f'<rect class="blink" x="{gx+40}" y="{gy+70+5*27-14}" width="9" height="17" fill="{t["mint"] if t["glow"] else t["violet"]}"/>')
    corpo.append("</g>")
    corpo.append(vinil(t, 1106, 352, 42))
    corpo.append(flor(t, 700, 96, 9, t["pink"]))
    corpo.append(flor(t, 1160, 236, 7, t["violet"]))
    corpo.append(estrela(t, 700, 330, 13))
    corpo.append(estrela(t, 640, 70, 18, "d1"))
    corpo.append(estrela(t, 1164, 60, 11, "d2"))
    corpo.append(estrela(t, 560, 250, 8, "d3"))
    return svg(w, h, "Oi, eu sou a Gabi. Psicóloga que programa: pessoas, dados e impacto. "
               "Estudante de IA e Ciência de Dados no IFMT.", "".join(corpo), t)


ICONES = {
    "ia": lambda t, x, y: (f'<circle cx="{x}" cy="{y-8}" r="5" fill="{t["pink"]}"/><circle cx="{x-12}" cy="{y+8}" r="5" fill="{t["violet"]}"/>'
                           f'<circle cx="{x+12}" cy="{y+8}" r="5" fill="{t["mint"]}"/>'
                           f'<path d="M{x} {y-8} L{x-12} {y+8} L{x+12} {y+8}Z" fill="none" stroke="{t["muted"]}" stroke-width="1.5"/>'),
    "dados": lambda t, x, y: "".join(f'<rect x="{x-14+i*10}" y="{y+12-hh}" width="7" height="{hh}" rx="2" fill="{c}"/>'
                                     for i, (hh, c) in enumerate(((12, t["violet"]), (22, t["pink"]), (16, t["mint"])))),
    "dev": lambda t, x, y: f'<text x="{x}" y="{y+6}" text-anchor="middle" class="mono" font-size="17" font-weight="700" fill="{t["violet"]}">&lt;/&gt;</text>',
    "auto": lambda t, x, y: (f'<path d="M{x-11} {y} A11 11 0 1 1 {x} {y+11}" fill="none" stroke="{t["pink"]}" stroke-width="3" stroke-linecap="round"/>'
                             f'<path d="M{x-16} {y-4} L{x-11} {y+3} L{x-5} {y-3}" fill="none" stroke="{t["pink"]}" stroke-width="3" stroke-linecap="round"/>'),
    "edu": lambda t, x, y: (f'<path d="M{x-15} {y-8} H{x-2} Q{x} {y-8} {x} {y-6} V{y+12} Q{x-1} {y+9} {x-4} {y+9} H{x-15}Z" fill="{t["violet"]}"/>'
                            f'<path d="M{x+15} {y-8} H{x+2} Q{x} {y-8} {x} {y-6} V{y+12} Q{x+1} {y+9} {x+4} {y+9} H{x+15}Z" fill="{t["pink"]}"/>'),
    "pessoas": lambda t, x, y: f'<path d="M{x} {y+12} C{x-22} {y-2} {x-12} {y-18} {x} {y-6} C{x+12} {y-18} {x+22} {y-2} {x} {y+12}Z" fill="{t["pink"]}"/>',
}


def areas(t):
    w, h = 1200, 300
    itens = [("ia", "Inteligência Artificial", "modelos, LLMs e IA aplicada"),
             ("dados", "Ciência de Dados", "explorar, interpretar, decidir"),
             ("dev", "Desenvolvimento", "interfaces e sistemas web"),
             ("auto", "Automação", "menos tarefa repetitiva"),
             ("edu", "Tecnologia & Educação", "aprender e ensinar com tech"),
             ("pessoas", "Pessoas & UX", "psicologia aplicada ao design")]
    corpo = [fundo(t, w, h, [("b2", 120, 280, 220), ("b1", 1100, 40, 220)])]
    corpo.append(f'<text x="44" y="52" class="mono" font-size="15" letter-spacing="3" fill="{t["violet"]}">✦ ÁREAS DE INTERESSE</text>')
    corpo.append(f'<text x="1156" y="52" class="sans soft" font-size="14" text-anchor="end">onde a curiosidade me leva</text>')
    for i, (ic, titulo, sub) in enumerate(itens):
        x = 40 + (i % 3) * 377
        y = 78 + (i // 3) * 104
        corpo.append(vidro(t, x, y, 357, 88, 18))
        corpo.append(f'<rect x="{x+16}" y="{y+16}" width="56" height="56" rx="16" fill="{t["violet"]}" fill-opacity=".12"/>')
        corpo.append(ICONES[ic](t, x + 44, y + 44))
        corpo.append(f'<text x="{x+90}" y="{y+40}" class="sans ink" font-size="19" font-weight="700">{escape(titulo)}</text>')
        corpo.append(f'<text x="{x+90}" y="{y+64}" class="sans muted" font-size="14">{escape(sub)}</text>')
    corpo.append(estrela(t, 1160, 270, 9))
    return svg(w, h, "Áreas de interesse: Inteligência Artificial, Ciência de Dados, Desenvolvimento, "
               "Automação, Tecnologia e Educação, Pessoas e UX.", "".join(corpo), t)


def stack(t):
    w, h = 1200, 200
    itens = [("Python", "#3776AB"), ("JavaScript", "#E3B70B"), ("HTML", "#E34F26"), ("CSS", "#663399"),
             ("Apps Script", "#4285F4"), ("Google Sheets", "#0F9D58"), ("Git", "#F05032"), ("GitHub", t["ink"])]
    corpo = [fundo(t, w, h, [("b3", 1100, 180, 200), ("b2", 200, 0, 200)])]
    corpo.append(f'<text x="44" y="50" class="mono" font-size="15" letter-spacing="3" fill="{t["violet"]}">✦ TECNOLOGIAS &amp; FERRAMENTAS</text>')
    corpo.append(f'<text x="1156" y="50" class="sans soft" font-size="14" text-anchor="end">learning · building · experimenting</text>')
    larg = 266
    for i, (nome, cor) in enumerate(itens):
        x, y = 44 + (i % 4) * (larg + 12), 74 + (i // 4) * 56
        corpo.append(vidro(t, x, y, larg, 44, 22))
        corpo.append(f'<circle cx="{x+24}" cy="{y+22}" r="7" fill="{cor}"/>')
        corpo.append(f'<text x="{x+42}" y="{y+28}" class="sans ink" font-size="17" font-weight="600">{escape(nome)}</text>')
    return svg(w, h, "Tecnologias com as quais tenho contato profissional ou acadêmico: Python, JavaScript, "
               "HTML, CSS, Google Apps Script, Google Sheets, Git e GitHub.", "".join(corpo), t)


def ilustracao(t, tipo, x, y):
    if tipo == "sistemas":
        return (vidro(t, x, y, 170, 112, 14)
                + f'<rect x="{x}" y="{y}" width="170" height="24" rx="14" fill="{t["violet"]}" fill-opacity=".25"/>'
                + "".join(f'<circle cx="{x+16+i*14}" cy="{y+12}" r="4" fill="{c}"/>' for i, c in enumerate((t["pink"], t["peach"], t["mint"])))
                + f'<rect x="{x+14}" y="{y+38}" width="46" height="60" rx="8" fill="{t["pink"]}" fill-opacity=".5"/>'
                + f'<rect x="{x+70}" y="{y+38}" width="86" height="12" rx="6" fill="{t["violet"]}" fill-opacity=".6"/>'
                + f'<rect x="{x+70}" y="{y+60}" width="64" height="12" rx="6" fill="{t["mint"]}" fill-opacity=".6"/>'
                + f'<rect x="{x+70}" y="{y+82}" width="76" height="12" rx="6" fill="{t["peach"]}" fill-opacity=".6"/>')
    if tipo == "dados":
        barras = "".join(f'<rect class="eq" style="animation-delay:{i*.2}s" x="{x+14+i*30}" y="{y+112-hh}" width="20" height="{hh}" rx="6" fill="{c}"/>'
                         for i, (hh, c) in enumerate(((44, t["violet"]), (76, t["pink"]), (56, t["mint"]), (96, t["peach"]), (68, t["violet"]))))
        return barras + f'<path d="M{x+24} {y+52} L{x+54} {y+22} L{x+84} {y+40} L{x+144} {y+4}" fill="none" stroke="{t["ink"]}" stroke-width="2.5" stroke-linecap="round"/>'
    if tipo == "automacao":
        nos = [(x + 20, y + 56, t["pink"]), (x + 85, y + 16, t["violet"]), (x + 85, y + 96, t["mint"]), (x + 150, y + 56, t["peach"])]
        linhas = "".join(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{t["muted"]}" stroke-width="2" stroke-dasharray="5 5"/>'
                         for a, b in ((nos[0], nos[1]), (nos[0], nos[2]), (nos[1], nos[3]), (nos[2], nos[3])))
        return linhas + "".join(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{c}"/>' for cx, cy, c in nos)
    # pessoas
    return (f'<circle cx="{x+55}" cy="{y+38}" r="22" fill="{t["violet"]}"/>'
            f'<path d="M{x+15} {y+112} Q{x+55} {y+52} {x+95} {y+112}Z" fill="{t["violet"]}" fill-opacity=".7"/>'
            f'<circle cx="{x+118}" cy="{y+46}" r="18" fill="{t["mint"]}"/>'
            f'<path d="M{x+86} {y+112} Q{x+118} {y+64} {x+150} {y+112}Z" fill="{t["mint"]}" fill-opacity=".7"/>'
            f'<path class="twinkle" d="M{x+92} {y+22} C{x+80} {y+12} {x+86} {y+2} {x+92} {y+9} C{x+98} {y+2} {x+104} {y+12} {x+92} {y+22}Z" fill="{t["pink"]}"/>')


def card(t, num, tipo, rotulo, titulo, sub, tags):
    w, h = 600, 250
    blob = {"sistemas": "b1", "dados": "b2", "automacao": "b3", "pessoas": "b1"}[tipo]
    corpo = [fundo(t, w, h, [(blob, 520, 60, 200)])]
    corpo.append(f'<text x="34" y="52" class="mono" font-size="14" letter-spacing="3" fill="{t["violet"]}">{num} / {escape(rotulo)}</text>')
    corpo.append(f'<text x="32" y="112" class="sans ink" font-size="29" font-weight="800" letter-spacing="-.5">{escape(titulo)}</text>')
    corpo.append(f'<text x="34" y="146" class="sans muted" font-size="17">{escape(sub)}</text>')
    corpo.append(f'<rect x="34" y="168" width="64" height="4" rx="2" fill="url(#hl)"/>')
    corpo.append(f'<text x="34" y="214" class="mono soft" font-size="13">{escape(tags)}</text>')
    corpo.append(ilustracao(t, tipo, 396, 66))
    corpo.append(estrela(t, 566, 222, 8, "d2"))
    return svg(w, h, f"{titulo}: {sub}", "".join(corpo), t)


def musica(t):
    w, h = 1200, 190
    corpo = [fundo(t, w, h, [("b1", 160, 100, 200), ("b2", 1100, 160, 200)])]
    corpo.append(vinil(t, 112, 95, 62))
    corpo.append(f'<text x="210" y="70" class="mono" font-size="14" letter-spacing="3" fill="{t["violet"]}">♫ ON REPEAT</text>')
    corpo.append(f'<text x="208" y="112" class="sans ink" font-size="30" font-weight="800">trilha sonora para codar</text>')
    corpo.append(f'<text x="210" y="142" class="sans muted" font-size="16">playlist pública em breve ✦</text>')
    cores = (t["pink"], t["violet"], t["mint"], t["peach"])
    for i in range(18):
        hh = (24, 52, 36, 64, 44, 30, 58)[i % 7]
        corpo.append(f'<rect class="eq" style="animation-delay:{(i % 6) * .15:.2f}s" x="{860+i*16}" y="{140-hh}" '
                     f'width="9" height="{hh}" rx="4" fill="{cores[i % 4]}"/>')
    return svg(w, h, "Card musical decorativo com disco de vinil. Minha playlist pública será adicionada futuramente.",
               "".join(corpo), t)


def rodape(t):
    w, h = 1200, 130
    corpo = [fundo(t, w, h, [("b1", 300, 130, 200), ("b2", 900, 0, 200), ("b3", 1150, 130, 140)])]
    corpo.append(f'<text x="600" y="62" text-anchor="middle" class="serif ink" font-size="28" font-style="italic">mesmos caminhos, novas possibilidades</text>')
    corpo.append(f'<text x="600" y="96" text-anchor="middle" class="mono" font-size="14" letter-spacing="4" fill="url(#hl)">PEOPLE · DATA · PURPOSE</text>')
    corpo.append(estrela(t, 210, 66, 12))
    corpo.append(estrela(t, 990, 66, 12, "d1"))
    corpo.append(gato(t, 1086, 70, 0.62))
    return svg(w, h, "Mesmos caminhos, novas possibilidades. People, data, purpose.", "".join(corpo), t)


CARDS = [
    ("01", "sistemas", "SISTEMAS", "Sistemas & aplicações", "organizar informações e fluxos", "desenvolvimento · interfaces · web"),
    ("02", "dados", "DADOS", "Dados & análise", "transformar dados em decisões", "python · indicadores · análise"),
    ("03", "automacao", "AUTOMAÇÃO", "Automações", "menos repetição, mais tempo", "javascript · apps script · fluxos"),
    ("04", "pessoas", "PESSOAS", "Pessoas & tecnologia", "comportamento humano + design", "psicologia · UX · educação"),
]


def main():
    for nome, t in TEMAS.items():
        pasta = RAIZ / nome
        (pasta / "cards").mkdir(parents=True, exist_ok=True)
        (pasta / "banner.svg").write_text(banner(t), encoding="utf-8")
        (pasta / "areas.svg").write_text(areas(t), encoding="utf-8")
        (pasta / "stack.svg").write_text(stack(t), encoding="utf-8")
        (pasta / "musica.svg").write_text(musica(t), encoding="utf-8")
        (pasta / "footer.svg").write_text(rodape(t), encoding="utf-8")
        for num, tipo, rotulo, titulo, sub, tags in CARDS:
            (pasta / "cards" / f"{tipo}.svg").write_text(card(t, num, tipo, rotulo, titulo, sub, tags), encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
