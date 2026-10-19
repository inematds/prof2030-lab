#!/usr/bin/env python3
"""Gera as páginas do prof2030-lab (PT na raiz, en/, es/) a partir de src/<lang>/*.html + data/.

Uso: python3 tools/build.py
Placeholders nos fragmentos:
  {{R}}  caminho até a raiz do idioma      {{P}}  caminho até a raiz PT (arquivos brutos, imagens)
  {{raw:caminho}}  conteúdo escapado de um arquivo bruto
  {{chat}} {{planilha}} {{pistas:peca}} {{gabarito}} {{mapa_falhas}}
"""
import csv, html, io, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = {"pt": "", "en": "en/", "es": "es/"}
HTML_LANG = {"pt": "pt-BR", "en": "en", "es": "es"}
SITE = "https://inematds.github.io/prof2030-lab/"

# página → (arquivo de saída relativo à raiz do idioma, fragmento)
PAGES = [
    ("index", "index.html"),
    ("pedidos", "pedidos/index.html"),
    ("admin", "pedidos/admin.html"),
    ("whatsapp", "whatsapp/index.html"),
    ("planilha", "planilha/index.html"),
    ("email-mcp", "email-mcp/index.html"),
    ("resumo-api", "resumo-api/index.html"),
    ("painel", "painel/index.html"),
    ("gabarito", "gabarito/index.html"),
    ("demo", "demo/index.html"),
]

CSS = r"""
:root{--bg:#0c0c10;--bg2:#14141b;--card:#16161e;--line:#272730;--txt:#e9e9ee;--mut:#9a9aa6;--amb:#FACC15;--amb-ink:#1a1206;--sky:#38bdf8;--bad:#F0918A;--ok:#7CE0C6;--warm:#F2B45C;
--sys-bg:#f3f5f8;--sys-card:#ffffff;--sys-ink:#1d2330;--sys-mut:#5d6677;--sys-line:#dde2ea;--sys-brand:#0f5e7a;--sys-brand2:#e7f2f6;--sys-bad:#b42318;--sys-ok:#11734b}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.65 Inter,system-ui,sans-serif;overflow-wrap:anywhere}
h1,h2,h3,.sora{font-family:Sora,Inter,sans-serif;line-height:1.2;letter-spacing:-.01em}
h1{font-size:clamp(28px,4.6vw,46px);margin:.2em 0 .4em;font-weight:800}
h2{font-size:clamp(22px,3vw,30px);margin:2em 0 .6em;font-weight:700}
h3{font-size:19px;margin:1.6em 0 .5em}
a{color:var(--amb)}
p,li{max-width:74ch}
code,pre,.mono{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:14px}
.labfaixa{background:#1b1708;color:#f5e7a8;border-bottom:1px solid #3a3210;font:600 13px/1.4 Sora,Inter,sans-serif;padding:7px 16px;text-align:center}
.labfaixa b{color:var(--amb)}
.top{position:sticky;top:0;z-index:5;background:rgba(12,12,16,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.top .in{max-width:1160px;margin:0 auto;padding:10px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.logo{font:800 15px Sora,sans-serif;color:var(--txt);text-decoration:none;display:flex;align-items:center;gap:8px}
.logo i{display:inline-block;width:12px;height:12px;border-radius:3px;background:var(--amb)}
.top nav{display:flex;gap:12px;flex-wrap:wrap;font:600 13px Sora,sans-serif;margin-left:auto;align-items:center}
.top nav a{color:var(--mut);text-decoration:none}.top nav a:hover,.top nav a.on{color:var(--amb)}
.langs a{padding:2px 6px;border:1px solid var(--line);border-radius:999px;font-size:12px}
.wrap{max-width:1160px;margin:0 auto;padding:24px 16px 64px}
.chip{display:inline-block;font:700 12px Sora,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--amb);border:1px solid #3a3210;border-radius:999px;padding:3px 10px}
.mut{color:var(--mut)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}
.btn{display:inline-block;background:var(--amb);color:var(--amb-ink);font:700 14px Sora,sans-serif;border-radius:10px;padding:10px 16px;text-decoration:none;border:0}
.btn.sec{background:transparent;color:var(--txt);border:1px solid var(--line)}
.exercicio{border:1px solid #3a3210;background:#15130a;border-radius:14px;padding:16px 18px;margin:18px 0}
.exercicio h2{margin-top:0;font-size:20px}
.exercicio ol{margin:.4em 0 0;padding-left:1.3em}
.exercicio li{margin:.35em 0}
.scroll{overflow-x:auto;max-width:100%;-webkit-overflow-scrolling:touch}
pre{background:#101016;border:1px solid var(--line);border-radius:12px;padding:14px;overflow-x:auto;max-width:100%;white-space:pre;line-height:1.55;margin:.6em 0}
details{border:1px solid var(--line);border-radius:12px;background:var(--card);margin:10px 0}
details>summary{cursor:pointer;padding:12px 16px;font:600 15px Sora,sans-serif;list-style-position:outside}
details[open]>summary{border-bottom:1px solid var(--line)}
details .det{padding:12px 16px}
.hero{position:relative;border-radius:16px;overflow:hidden;box-shadow:0 30px 80px -30px #000;margin:8px 0 20px}
.hero img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.hero .cap{position:absolute;left:0;right:0;bottom:0;padding:18px;background:linear-gradient(transparent,rgba(12,12,16,.92))}
figure{margin:0}
.foot{border-top:1px solid var(--line);color:var(--mut);font-size:14px}
.foot .in{max-width:1160px;margin:0 auto;padding:22px 16px}
.foot a{color:var(--sky)}
/* "sistema interno" da PME */
.sys{background:var(--sys-bg);color:var(--sys-ink);border-radius:14px;overflow:hidden;border:1px solid #2f3440;margin:18px 0}
.sys a{color:var(--sys-brand)}
.sys .bar{display:flex;align-items:center;gap:8px;background:#e4e8ef;padding:8px 12px;border-bottom:1px solid var(--sys-line);font:12px "JetBrains Mono",monospace;color:var(--sys-mut)}
.sys .bar .dots{display:flex;gap:5px}.sys .bar .dots i{width:10px;height:10px;border-radius:50%;background:#c5ccd8;display:block}
.sys .bar .url{background:#fff;border:1px solid var(--sys-line);border-radius:6px;padding:2px 8px;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sys .apphead{background:var(--sys-brand);color:#fff;padding:12px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;font:700 15px Sora,sans-serif}
.sys .apphead small{font:500 12px Inter,sans-serif;opacity:.85}
.sys .apphead .sp{margin-left:auto}
.sys .body{padding:16px}
.sys .scard{background:var(--sys-card);border:1px solid var(--sys-line);border-radius:10px;padding:14px}
.sys table{border-collapse:collapse;width:100%;font-size:14px;background:#fff}
.sys th,.sys td{border:1px solid var(--sys-line);padding:7px 9px;text-align:left;white-space:nowrap}
.sys th{background:#eef1f5;font-weight:600;color:var(--sys-mut);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
.sys .tag{display:inline-block;font:600 11px Inter,sans-serif;border-radius:999px;padding:2px 8px;background:var(--sys-brand2);color:var(--sys-brand)}
.sys .tag.bad{background:#fde7e5;color:var(--sys-bad)}
.sys .tag.ok{background:#e3f5ec;color:var(--sys-ok)}
.sys .sbtn{display:inline-block;border:1px solid var(--sys-line);background:#fff;color:var(--sys-ink);border-radius:8px;padding:6px 10px;font:600 13px Inter,sans-serif;cursor:default}
.sys .sbtn.pri{background:var(--sys-brand);border-color:var(--sys-brand);color:#fff}
.sys .sbtn.del{color:var(--sys-bad)}
.sys pre{background:#0f1520;color:#dbe4f0;border-color:#0f1520}
.sys input{font:14px Inter,sans-serif;padding:7px 10px;border:1px solid var(--sys-line);border-radius:8px;width:100%;max-width:340px}
/* chat */
.chat{background:#e9e2d6;border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:85%;padding:8px 11px;border-radius:10px;font-size:14.5px;line-height:1.45;color:#1d2330;box-shadow:0 1px 0 rgba(0,0,0,.08)}
.msg.cliente{align-self:flex-start;background:#fff;border-top-left-radius:2px}
.msg.agente{align-self:flex-end;background:#d7f5cf;border-top-right-radius:2px}
.msg.colado{background:#fff8e1;border:1px dashed #c9a227}
.msg .h{display:block;font-size:11px;color:#5d6677;margin-top:3px;text-align:right}
.msg .quem{display:block;font:700 11px Inter,sans-serif;color:#0f5e7a;margin-bottom:2px}
.convhead{font:700 14px Sora,sans-serif;margin:14px 0 6px;color:var(--sys-ink)}
/* organograma */
.org{display:flex;flex-direction:column;align-items:center;gap:12px}
.org .n{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px;text-align:center;font-size:14px;min-width:0}
.org .n b{display:block;font-family:Sora,sans-serif;font-size:15px}
.org .n.top{border-color:#3a3210}
.org .row{display:grid;gap:10px;width:100%;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr))}
.tbl{border-collapse:collapse;width:100%;font-size:14.5px}
.tbl th,.tbl td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}
.tbl th{font:600 12px Sora,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}
.badge{display:inline-block;font:700 12px Sora,sans-serif;border-radius:999px;padding:2px 9px;border:1px solid var(--line);color:var(--mut)}
.badge.peca{color:var(--amb);border-color:#3a3210}
.badge.sombra{color:var(--warm);border-color:#4a3510}
.falha{border-left:3px solid var(--bad)}
.falha dl{display:grid;grid-template-columns:minmax(0,1fr);gap:4px 0;margin:0}
.falha dt{font:700 12px Sora,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-top:8px}
.falha dd{margin:0}
.idf{font:600 13px "JetBrains Mono",monospace;color:var(--amb)}
.fluxo{display:block;width:100%;height:auto;max-width:900px}
.kpis{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr))}
.kpi{background:#fff;border:1px solid var(--sys-line);border-radius:10px;padding:14px}
.kpi .v{font:800 26px Sora,sans-serif;color:var(--sys-ink)}
.kpi .l{font-size:13px;color:var(--sys-mut)}
.kpi .d{font:700 13px Inter,sans-serif;color:var(--sys-ok)}
.passos{counter-reset:p;list-style:none;padding:0}
.passos>li{counter-increment:p;position:relative;padding:0 0 14px 48px;max-width:none}
.passos>li:before{content:counter(p);position:absolute;left:0;top:0;width:34px;height:34px;border-radius:12px;background:var(--amb);color:var(--amb-ink);font:800 15px Sora,sans-serif;display:flex;align-items:center;justify-content:center}
@media (max-width:560px){.top nav{margin-left:0;width:100%}.hero .cap{position:static;background:var(--bg2)}}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">'


def esc(s):
    return html.escape(s, quote=False)


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def data_path(lang, name, pt_default):
    p = ROOT / "data" / lang / name
    return p if p.exists() else ROOT / pt_default


def render_chat(lang, ui):
    d = load_json(data_path(lang, "conversas.json", "whatsapp/conversas.json"))
    out = []
    for c in d["conversas"]:
        out.append(f'<div class="convhead">{esc(ui["conversa"])} {c["n"]} · {esc(c["cliente"])} · <span class="mono" style="font-weight:400">{esc(c["telefone"])}</span> · {esc(c["data"])}</div>')
        out.append('<div class="chat">')
        for m in c["mensagens"]:
            cls = m["de"] + (" colado" if m.get("colado") else "")
            quem = ui["quem_agente"] if m["de"] == "agente" else ui["quem_cliente"]
            out.append(f'<div class="msg {cls}"><span class="quem">{esc(quem)}</span>{esc(m["texto"])}<span class="h">{m["hora"]}</span></div>')
        out.append('</div>')
    return "\n".join(out)


def render_planilha(ui):
    lines = (ROOT / "planilha/clientes.csv").read_text(encoding="utf-8").splitlines()
    rows = list(csv.reader(io.StringIO("\n".join(l for l in lines if not l.startswith("#")))))
    cols = ui.get("planilha_cols") or rows[0]
    letras = "ABCDEFGHIJ"
    h = "".join(f"<th>{letras[i]} · {esc(x)}</th>" for i, x in enumerate(cols))
    body = "".join(f"<tr><td>{i + 2}</td>" + "".join(f"<td>{esc(x)}</td>" for x in r) + "</tr>" for i, r in enumerate(rows[1:]))
    return f'<div class="scroll"><table><thead><tr><th>#</th>{h}</tr></thead><tbody>{body}</tbody></table></div>'


def falhas(lang):
    return load_json(data_path(lang, "falhas.json", "data/pt/falhas.json"))


def render_pistas(lang, ui, peca, R):
    fs = [f for f in falhas(lang) if f["peca"] == peca]
    lis = "".join(f'<li>{esc(f["pista"])}</li>' for f in fs)
    return (f'<div class="exercicio"><span class="chip">{esc(ui["exercicio"])}</span>'
            f'<h2>{esc(ui["ache"].format(n=len(fs)))}</h2><ol>{lis}</ol>'
            f'<p class="mut" style="margin:.8em 0 0">{esc(ui["pistas_nota"])} '
            f'<a href="{R}gabarito/#peca-{peca}">{esc(ui["ver_gabarito"])}</a></p></div>')


def render_gabarito(lang, ui, R):
    pecas = ui["pecas"]
    out = []
    atual = None
    for f in falhas(lang):
        if f["peca"] != atual:
            atual = f["peca"]
            out.append(f'<h2 id="peca-{atual}">{esc(pecas[atual])} <a class="badge peca" style="font-size:12px;vertical-align:middle;text-decoration:none" href="{R}{"pedidos/" if atual=="pedidos" else atual + "/"}">{esc(ui["abrir_peca"])}</a></h2>')
        aulas = ", ".join(f["aulas"])
        b4 = f'<dt>{esc(ui["g_base4"])}</dt><dd>{esc(f["base4"])}</dd>' if f["base4"] else ""
        out.append(
            f'<details class="falha" id="{f["id"]}"><summary><span class="idf">{f["id"]}</span> · {esc(ui["g_mostrar"])}</summary>'
            f'<div class="det"><h3 style="margin-top:0">{esc(f["titulo"])}</h3><dl>'
            f'<dt>{esc(ui["g_onde"])}</dt><dd>{esc(f["onde"])}</dd>'
            f'<dt>{esc(ui["g_risco"])}</dt><dd>{esc(f["risco"])}</dd>'
            f'<dt>{esc(ui["g_correcao"])}</dt><dd>{esc(f["correcao"])}</dd>'
            f'<dt>{esc(ui["g_aulas"])}</dt><dd>{esc(aulas)}</dd>{b4}</dl></div></details>')
    return "\n".join(out)


def render_mapa_falhas(lang, ui):
    rows = []
    for f in falhas(lang):
        rows.append(f'<tr><td class="idf">{f["id"]}</td><td>{esc(ui["pecas"][f["peca"]])}</td><td>{esc(", ".join(f["aulas"]))}</td></tr>')
    return (f'<div class="scroll"><table class="tbl"><thead><tr><th>id</th><th>{esc(ui["col_peca"])}</th><th>{esc(ui["g_aulas"])}</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def build():
    total = 0
    for lang, pre in LANGS.items():
        ui = load_json(ROOT / "src" / lang / "ui.json")
        for key, out in PAGES:
            frag_p = ROOT / "src" / lang / f"{key}.html"
            if not frag_p.exists():
                print(f"[falta] {frag_p}", file=sys.stderr)
                continue
            frag = frag_p.read_text(encoding="utf-8")
            depth = out.count("/") + (1 if pre else 0)
            P = "../" * depth
            R = "../" * out.count("/")
            title_m = re.search(r"<!--\s*title:(.*?)-->", frag)
            desc_m = re.search(r"<!--\s*desc:(.*?)-->", frag)
            title = title_m.group(1).strip() if title_m else "Horizonte Lab"
            desc = desc_m.group(1).strip() if desc_m else ui["desc_padrao"]
            frag = re.sub(r"<!--\s*(title|desc):.*?-->\n?", "", frag)

            def raw(m):
                return esc((ROOT / m.group(1)).read_text(encoding="utf-8"))
            frag = re.sub(r"\{\{raw:([^}]+)\}\}", raw, frag)
            frag = frag.replace("{{chat}}", render_chat(lang, ui))
            frag = frag.replace("{{planilha}}", render_planilha(ui))
            frag = re.sub(r"\{\{pistas:([a-z-]+)\}\}", lambda m: render_pistas(lang, ui, m.group(1), R), frag)
            frag = frag.replace("{{gabarito}}", render_gabarito(lang, ui, R))
            frag = frag.replace("{{mapa_falhas}}", render_mapa_falhas(lang, ui))
            frag = frag.replace("{{R}}", R).replace("{{P}}", P)
            left = re.findall(r"\{\{[^}]*\}\}", frag)
            if left:
                sys.exit(f"placeholder sobrando em {lang}/{key}: {left}")

            nav = []
            for k, href in [("index", ""), ("gabarito", "gabarito/"), ("demo", "demo/")]:
                on = ' class="on"' if k == key else ""
                nav.append(f'<a{on} href="{(R + href) or "./"}">{esc(ui["nav"][k])}</a>')
            langs = []
            for l2, p2 in LANGS.items():
                href = "../" * depth + p2 + out.replace("index.html", "")
                langs.append(f'<a href="{href or "./"}" hreflang="{HTML_LANG[l2]}"{" class=on" if l2 == lang else ""}>{l2.upper()}</a>')
            alt = "".join(f'<link rel="alternate" hreflang="{HTML_LANG[l2]}" href="{SITE}{p2}{out.replace("index.html", "")}">' for l2, p2 in LANGS.items())
            page = f"""<!doctype html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index,follow">
{alt}
{FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="labfaixa">{ui["faixa"]}</div>
<header class="top"><div class="in"><a class="logo" href="{R or './'}"><i></i>Horizonte · Lab</a><nav>{''.join(nav)}<span class="langs">{' '.join(langs)}</span></nav></div></header>
<main class="wrap">
{frag.strip()}
</main>
<footer class="foot"><div class="in">{ui["rodape"]}</div></footer>
</body>
</html>
"""
            dest = ROOT / pre / out
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page, encoding="utf-8")
            total += 1
    print(f"gerou {total} páginas")


if __name__ == "__main__":
    build()
