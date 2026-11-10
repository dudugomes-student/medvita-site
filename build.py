#!/usr/bin/env python3
"""Gera as páginas do site da Medvita a partir das partes comuns.

Uso:  python3 build.py
Não edite os .html direto: o próximo build sobrescreve.
Quando o domínio próprio estiver no ar, troque SITE_URL e rode de novo.
Tudo o que ainda precisa de confirmação aparece no site com a marca [CONFIRMAR] (função `confirmar`).
"""
import json, pathlib, datetime, html
from urllib.parse import urlparse

SITE_URL = "https://dudugomes-student.github.io/medvita-site"   # sem barra no fim

# [CONFIRMAR] o (11) 92626-4855 é o telefone do site antigo; falta confirmar se atende WhatsApp.
WA_NUMBER = "5511926264855"
WA_SHOW = "(11) 92626-4855"
WA = f"https://wa.me/{WA_NUMBER}"
EMAIL = "licitacoes@medvitamulti.com.br"           # [CONFIRMAR] e-mail do site antigo
INSTAGRAM = "https://www.instagram.com/medvita.multi/"
RAZAO = "MED VITA SERVIÇOS DE SAÚDE LTDA"
CNPJ = "14.826.508/0001-58"                         # da política de privacidade do site antigo
DPO_NOME = "Marciano Rodrigues Morais"
DPO_EMAIL = "equilibriummulti@gmail.com"            # [CONFIRMAR] é o e-mail que está na política antiga
DPO_TEL = "(11) 94000-1970"

ROOT = pathlib.Path(__file__).parent
esc = html.escape

def confirmar(texto="CONFIRMAR"):
    """Marca visível do que ainda falta confirmar antes do domínio oficial."""
    return f'<mark class="confirmar">[{texto}]</mark>'

# ---------- ícones de interface (traço arredondado, 24x24) ----------
I = {
    "wa": '<path d="M4 19.5 5.3 15.6A8 8 0 1 1 8.6 18.8Z"/><path d="M9 10.5h6M9 13.5h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "menu": '<path d="M4 8h16M4 16h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
}
def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg>'

NEW_TAB = '<span class="sr-only"> (abre em nova aba)</span>'
def wa_btn(label="Falar no WhatsApp", cls="btn btn-primary"):
    return f'<a class="{cls}" href="{WA}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>{label}</span>{NEW_TAB}</a>'

def stroke(word):
    """Palavra-chave em roxo com o traço que se desenha embaixo."""
    return (f'<span class="stroke">{word}<svg viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true">'
            '<path class="draw" pathLength="1" style="--delay:.5s;--dur:1.1s" d="M2 6.5C26 2.5 62 8.5 98 4"/></svg></span>')

# ---------- ilustrações 3D (assets/3d) ----------
SIZES = {}
def img3d(name, alt="", cls="art3d", eager=False):
    from PIL import Image
    if name not in SIZES:
        SIZES[name] = Image.open(ROOT / "assets" / "3d" / f"{name}.webp").size
    w, h = SIZES[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    alt_attr = f'alt="{esc(alt)}"' if alt else 'alt="" aria-hidden="true"'
    return f'<img class="{cls}" src="assets/3d/{name}.webp" width="{w}" height="{h}" {alt_attr} {load}>'

def float3d(name, cls="", depth=0.3, delay=0.0):
    return (f'<span class="float {cls}" data-depth="{depth}" style="--fd:{delay:.2f}s">'
            f'{img3d(name, cls="float-img")}</span>')

# As quatro áreas: ícone, nome, profissional, conselho
AREAS = [("osso", "Fisioterapia", "Fisioterapeutas", "CREFITO"),
         ("curativo", "Enfermagem", "Enfermeiros", "COREN"),
         ("pensamento", "Psicologia", "Psicólogos", "CRP"),
         ("maca", "Nutrição", "Nutricionistas", "CRN")]

ORBITA = ["osso", "curativo", "pensamento", "maca", "prancheta", "maos"]
def orbit(label):
    n = len(ORBITA)
    items = "".join(
        f'<li style="--i:{i};--n:{n}"><span class="orbit-item">{img3d(x, cls="orbit-img")}</span></li>' for i, x in enumerate(ORBITA))
    return f'''<figure class="orbit-stage" role="img" aria-label="{label}">
  <span class="orbit-glow" aria-hidden="true"></span>
  <svg class="orbit-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="49"/></svg>
  <svg class="orbit-ring orbit-ring-2" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="49"/></svg>
  <ul class="orbit" aria-hidden="true">{items}</ul>
  <span class="orbit-center" data-depth="0.15">{img3d("coracao", cls="orbit-hub", eager=True)}</span>
</figure>'''

FAIXA = [("osso", "Fisioterapia"), ("curativo", "Enfermagem"), ("pensamento", "Psicologia"), ("maca", "Nutrição"),
         ("coracao", "Empatia e respeito"), ("maos", "Trabalho em equipe"), ("escudo", "Integridade"), ("livros", "Cuidado baseado em evidências")]
def marquee():
    row = "".join(f'<li>{img3d(n, cls="mq-img")}<span>{t}</span></li>' for n, t in FAIXA)
    return (f'<div class="marquee" aria-label="Áreas e valores"><ul class="mq-track">{row}</ul>'
            f'<ul class="mq-track" aria-hidden="true">{row}</ul></div>')

PATHS = '<div class="paths-bg" data-paths aria-hidden="true"></div>'
DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
        '<linearGradient id="traco" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B79CE8"/>'
        '<stop offset="1" stop-color="#62229C"/></linearGradient></defs></svg>')

NAV = [("index.html", "Início"), ("para-instituicoes.html", "Para instituições"), ("trabalhe-conosco.html", "Trabalhe conosco"),
       ("sobre.html", "Sobre"), ("contato.html", "Contato")]

def header(active):
    on = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{on if h == active else ""}>{t}</a></li>' for h, t in NAV)
    cur = on if active == "index.html" else ""
    return f'''<header class="site-header">
  <div class="wrap header-bar">
    <a class="brand" href="index.html"{cur}><picture><source type="image/webp" srcset="assets/logo-80.webp 105w, assets/logo-160.webp 210w" sizes="92px"><img src="assets/logo-80.png" srcset="assets/logo-80.png 105w, assets/logo-160.png 210w" sizes="92px" width="105" height="80" alt="Med Vita Saúde: página inicial"></picture></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-principal" aria-label="Abrir menu">{icon("menu", "icon i-open")}{icon("close", "icon i-close")}</button>
    <nav class="nav" id="menu-principal" aria-label="Principal">
      <ul class="nav-list">{items}</ul>
      {wa_btn("WhatsApp", "btn btn-primary header-cta")}
    </nav>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/logo-branco-160.png" width="210" height="160" alt="Med Vita Saúde: Qualidade e Humanização" loading="lazy">
        <p>Fisioterapia, enfermagem, psicologia e nutrição.</p>
      </div>
      <div>
        <h2>Navegue</h2>
        <ul>
          <li><a href="para-instituicoes.html">Para instituições</a></li>
          <li><a href="trabalhe-conosco.html">Trabalhe conosco</a></li>
          <li><a href="sobre.html">Sobre a Medvita</a></li>
          <li><a href="privacidade.html">Política de Privacidade</a></li>
        </ul>
      </div>
      <div>
        <h2>Fale com a Medvita</h2>
        <ul>
          <li><a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp {WA_SHOW}{NEW_TAB}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@medvita.multi{NEW_TAB}</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© <span data-year>{datetime.date.today().year}</span> {RAZAO} · CNPJ {CNPJ}</span>
      <span>Responsável técnico: {confirmar("CONFIRMAR nome e registro")}</span>
    </div>
  </div>
</footer>
<nav class="mobile-bar" aria-label="Atalhos">
  {wa_btn("WhatsApp")}
  <a class="btn btn-outline" href="para-instituicoes.html"><span>Montar equipe</span></a>
</nav>'''

def page(slug, title, desc, body, scripts=("main", "paths-bg", "motion"), noindex=False):
    url = f"{SITE_URL}/" if slug == "index.html" else f"{SITE_URL}/{slug}"
    js = "".join(f'<script src="js/{s}.js" defer></script>' for s in scripts)
    ld = ""
    if slug == "index.html":
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Organization", "name": RAZAO,
            "alternateName": "Medvita", "url": f"{SITE_URL}/", "logo": f"{SITE_URL}/assets/logo.png",
            "telephone": "+55-11-92626-4855", "email": EMAIL, "taxID": CNPJ, "areaServed": "BR",
            "sameAs": [INSTAGRAM]}, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    if slug == "404.html":
        robots += f'<base href="{urlparse(SITE_URL).path.rstrip("/")}/">'
    out = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.classList.add('js');try{{if(sessionStorage.getItem('medvita-nav')==='1'&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{document.documentElement.classList.add('arriving');}}sessionStorage.removeItem('medvita-nav')}}catch(e){{}}</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">{robots}
<meta name="theme-color" content="#FFFFFF">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/og-medvita.png">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="preload" href="fonts/plus-jakarta-sans-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/plus-jakarta-sans-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/medvita.css">
{ld}{js}
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
<div class="curtain" aria-hidden="true"><div class="curtain-panel"><span class="curtain-badge"><img src="assets/logo-160.png" width="210" height="160" alt=""></span><span class="curtain-line"></span></div></div>
<div class="progress" aria-hidden="true"></div>
{DEFS}
{header(slug)}
<main id="conteudo" tabindex="-1">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    (ROOT / slug).write_text(out, encoding="utf-8")

def cta(title_html, text, button=None):
    button = button or wa_btn("Falar no WhatsApp", "btn btn-white")
    return f'''<section class="section" aria-labelledby="cta-title"><div class="wrap">
  <div class="cta reveal">{PATHS.replace('paths-bg', 'paths-bg paths-light')}
    <h2 class="title" id="cta-title">{title_html}</h2>
    <p class="lede">{text}</p>
    <div class="btn-row">{button}</div>
  </div>
</div></section>'''

def form_result():
    return (f'<div class="form-result" data-form-result hidden><p role="status"></p>'
            f'<a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>Abrir no WhatsApp</span>{NEW_TAB}</a></div>')

def area_tiles():
    return '<div class="tiles">' + "".join(
        f'<article class="tile{" tile-blue" if i == 1 else ""} reveal" data-tilt style="--d:{i*0.08:.2f}s"><span class="tile-art">{img3d(n)}</span><h3>{t}</h3><p>{p} com registro no {c}.</p></article>'
        for i, (n, t, p, c) in enumerate(AREAS)) + "</div>"

JEITO = [("check", "Atendimento integral", "A pessoa inteira, não só a queixa."),
         ("livros", "Baseado em evidências", "Conduta apoiada em estudo e protocolo."),
         ("coracao", "Acolhimento", "Segurança e bem-estar em primeiro lugar.")]
def jeito_tiles():
    return '<div class="tiles tiles-3">' + "".join(
        f'<article class="tile reveal" data-tilt style="--d:{i*0.08:.2f}s"><span class="tile-art">{img3d(n)}</span><h3>{t}</h3><p>{p}</p></article>'
        for i, (n, t, p) in enumerate(JEITO)) + "</div>"

TRUST = f'''<div class="trust reveal">
  <span class="float trust-float" data-depth="0.2">{img3d("escudo", cls="trust-art")}</span>
  <div><h2 class="subtitle">Dados protegidos pela LGPD</h2>
  <p>Encarregado de dados nomeado e política publicada. CNPJ {CNPJ}.</p></div>
  <a class="btn btn-outline" href="privacidade.html"><span>Ler a política</span>{icon("arrow")}</a>
</div>'''

TURNOS = '''<div class="field full"><fieldset><legend>Turnos</legend><div class="options">
        <label><input type="checkbox" value="Dia" data-label="Turnos"> Dia</label>
        <label><input type="checkbox" value="Noite" data-label="Turnos"> Noite</label>
        <label><input type="checkbox" value="Fim de semana" data-label="Turnos"> Fim de semana</label>
      </div></fieldset></div>'''

UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()
uf_opts = "".join(f'<option value="{u}"{" selected" if u == "SP" else ""}>{u}</option>' for u in UFS)

# =====================================================================
# Início
# =====================================================================
page("index.html",
 "Medvita | Fisioterapia, enfermagem, psicologia e nutrição",
 "Fisioterapeutas, enfermeiros, psicólogos e nutricionistas para instituições públicas e privadas. Monte a equipe e fale com a Medvita pelo WhatsApp.",
 f'''<section class="hero" aria-labelledby="hero-title">{PATHS}
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">Fisioterapia · Enfermagem · Psicologia · Nutrição</p>
      <h1 class="display" id="hero-title" data-draw>Profissionais de saúde para a sua {stroke("unidade")}</h1>
      <div class="doors">
        <a class="door" data-tilt href="para-instituicoes.html">{img3d("predio", cls="door-img")}<small>Sou instituição</small><strong>Preciso de profissionais</strong><span class="go">Montar equipe {icon("arrow")}</span></a>
        <a class="door door-blue" data-tilt href="trabalhe-conosco.html">{img3d("prancheta", cls="door-img")}<small>Sou profissional de saúde</small><strong>Quero trabalhar</strong><span class="go">Fazer cadastro {icon("arrow")}</span></a>
      </div>
    </div>
    {orbit("Coração roxo em 3D no centro, com osso, curativo, balão de pensamento, maçã, prancheta e aperto de mãos girando em volta.")}
  </div>
</section>

<section class="band-navy band-thin" aria-label="Áreas e valores">{marquee()}</section>

<section class="section" aria-labelledby="areas-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Quem trabalha com a Medvita</p>
    <h2 class="title" id="areas-title">Quatro áreas, <span class="blue">uma equipe</span></h2>
  </div>
  {area_tiles()}
  <div class="btn-row reveal"><a class="btn btn-primary" href="para-instituicoes.html"><span>Montar minha equipe</span>{icon("arrow")}</a></div>
</div></section>

<section class="section section-sky" aria-labelledby="jeito-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Como a Medvita cuida</p>
    <h2 class="title" id="jeito-title">Qualidade e <span class="blue">humanização</span></h2>
  </div>
  {jeito_tiles()}
</div></section>

<section class="section" aria-label="Proteção de dados"><div class="wrap">{TRUST}</div></section>

{cta('Precisa montar uma <span class="blue">equipe?</span>', "Diga a unidade, as áreas e os turnos.")}
''')

# =====================================================================
# Para instituições (montar equipe)
# =====================================================================
picker = "".join(
    f'<label class="pick"><input type="checkbox" name="area" value="{t}" data-label="Áreas"><span>{img3d(n, cls="pick-img")}{t}</span></label>'
    for n, t, p, c in AREAS)

STEPS = [("Conversa", "Entender a unidade e a demanda."), ("Proposta", "Áreas, turnos e escala."),
         ("Começo", "Equipe apresentada à unidade."), ("Acompanhamento", "Ajustes ao longo do contrato.")]

page("para-instituicoes.html",
 "Para instituições de saúde | Medvita",
 "Prefeituras, secretarias, hospitais e clínicas: escolha as áreas e os turnos e monte o pedido de fisioterapeutas, enfermeiros, psicólogos e nutricionistas.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Para instituições públicas e privadas</p>
    <h1 class="display" id="hero-title" data-draw>Sua equipe de {stroke("saúde")}</h1>
    <div class="btn-row">{wa_btn()}<a class="btn btn-outline" href="#equipe"><span>Montar equipe</span>{icon("arrow")}</a></div>
  </div>
  <figure class="hero-cluster" aria-hidden="true">{float3d("predio", "c-main", 0.25)}{float3d("prefeitura", "c-a", 0.55, 0.5)}{float3d("calendario", "c-b", 0.45, 1.1)}{float3d("prancheta", "c-c", 0.7, 1.7)}</figure>
</div></section>

<section class="section" id="equipe" aria-labelledby="equipe-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Monte sua equipe</p>
    <h2 class="title" id="equipe-title">Quais áreas <span class="blue">você precisa?</span></h2>
  </div>
  <form class="team-builder" data-whatsapp-form="instituicao" data-number="{WA_NUMBER}" data-team novalidate>
    <fieldset class="picks picks-4"><legend class="sr-only">Áreas</legend>{picker}</fieldset>
    <div class="team-side">
      <div class="team-summary" aria-live="polite">
        <p class="team-big" data-team-count>0</p>
        <p class="muted" data-team-text>Escolha uma ou mais áreas.</p>
      </div>
      {TURNOS}
      <div class="field"><label for="h-tipo">Tipo de instituição</label><select id="h-tipo" name="tipo" required data-label="Tipo de instituição"><option value="">Escolha</option><option>Prefeitura ou secretaria de saúde</option><option>Hospital</option><option>Clínica</option><option>Outra</option></select></div>
      <div class="field"><label for="h-inst">Instituição</label><input id="h-inst" name="instituicao" autocomplete="organization" required maxlength="160" data-label="Instituição"></div>
      <div class="field"><label for="h-cidade">Cidade e estado</label><input id="h-cidade" name="cidade" required maxlength="120" placeholder="Ex.: Barueri (SP)" data-label="Cidade"></div>
      <div class="field"><label for="h-nome">Seu nome</label><input id="h-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Enviar pedido</span></button>
      <p class="hint muted">Sem dados de pacientes. Nada fica guardado no site.</p>
      {form_result()}
    </div>
  </form>
</div></section>

<section class="section section-sky" aria-labelledby="como-title"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Como funciona {confirmar()}</p><h2 class="title" id="como-title">Do pedido à <span class="blue">equipe na unidade</span></h2></div>
  <ol class="steps">{"".join(f"<li><h3>{t}</h3><p>{p}</p></li>" for t, p in STEPS)}</ol>
</div></section>

<section class="section" aria-labelledby="areas-title"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Áreas</p><h2 class="title" id="areas-title">Quem vai para a <span class="blue">sua unidade</span></h2></div>
  {area_tiles()}
</div></section>

{cta('Contratação por <span class="blue">licitação?</span>', f"Envie o edital para {EMAIL}.", f'<a class="btn btn-white" href="mailto:{EMAIL}">{icon("mail")}<span>Enviar e-mail</span></a>')}
''', scripts=("main", "paths-bg", "motion", "forms"))

# =====================================================================
# Trabalhe conosco (cadastro de profissionais)
# =====================================================================
prof_opts = ('<option value="Fisioterapeuta">Fisioterapeuta</option><option value="Enfermeiro(a)">Enfermeiro(a)</option>'
             '<option value="Psicólogo(a)">Psicólogo(a)</option><option value="Nutricionista">Nutricionista</option>')

page("trabalhe-conosco.html",
 "Trabalhe conosco | Medvita",
 "Fisioterapeutas, enfermeiros, psicólogos e nutricionistas: deixe seu cadastro com a Medvita pelo WhatsApp.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Para profissionais de saúde {confirmar()}</p>
    <h1 class="display" id="hero-title" data-draw>Trabalhe com a {stroke("Medvita")}</h1>
    <p class="lede">Fisioterapeutas, enfermeiros, psicólogos e nutricionistas.</p>
  </div>
  <figure class="hero-cluster" aria-hidden="true">{float3d("prancheta", "c-main", 0.25)}{float3d("osso", "c-a", 0.55, 0.5)}{float3d("maca", "c-b", 0.45, 1.1)}{float3d("pensamento", "c-c", 0.7, 1.7)}</figure>
</div></section>

<section class="section section-sky" id="cadastro" aria-labelledby="cad-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Cadastro</p>
    <h2 class="title" id="cad-title">Deixe seu <span class="blue">cadastro</span></h2>
    <p class="lede">A mensagem sai pronta no WhatsApp. Não mande documentos por aqui.</p>
  </div>
  <form class="form-card reveal" data-whatsapp-form="profissional" data-number="{WA_NUMBER}" style="--d:.1s" novalidate>
    <div class="form-grid">
      <div class="field full"><label for="p-nome">Nome completo</label><input id="p-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <div class="field"><label for="p-prof">Profissão</label><select id="p-prof" name="profissao" required data-label="Profissão"><option value="">Escolha</option>{prof_opts}</select></div>
      <div class="field"><label for="p-reg">Registro no conselho</label><input id="p-reg" name="registro" required maxlength="20" placeholder="Ex.: COREN-SP 123456" data-label="Registro"></div>
      <div class="field"><label for="p-cidade">Cidade onde mora</label><input id="p-cidade" name="cidade" autocomplete="address-level2" required maxlength="80" data-label="Cidade"></div>
      <div class="field"><label for="p-uf">Estado</label><select id="p-uf" name="uf" required data-label="Estado">{uf_opts}</select></div>
      {TURNOS}
    </div>
    <div class="form-foot"><button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Preparar mensagem</span></button>
    <p>Nada fica guardado no site. <a href="privacidade.html">Privacidade</a></p></div>
    {form_result()}
  </form>
</div></section>
''', scripts=("main", "paths-bg", "motion", "forms"))

# =====================================================================
# Sobre
# =====================================================================
VALORES = [("check", "Qualidade", "Cuidado pensado para cada pessoa."),
           ("coracao", "Empatia e respeito", "Dignidade e atenção ao que cada um precisa."),
           ("brilho", "Atualização", "Métodos e práticas revistos sempre."),
           ("maos", "Trabalho em equipe", "As áreas trabalham juntas."),
           ("escudo", "Integridade", "Ética, transparência e honestidade.")]

page("sobre.html",
 "Sobre a Medvita | Serviços de saúde multiprofissionais",
 f"{RAZAO}: fisioterapia, enfermagem, psicologia e nutrição. Missão, visão, valores e dados da empresa.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Sobre</p>
    <h1 class="display" id="hero-title" data-draw>Quem é a {stroke("Medvita")}</h1>
    <p class="lede">Uma empresa de serviços de saúde que junta fisioterapia, enfermagem, psicologia e nutrição.</p>
  </div>
  {orbit("Coração roxo em 3D no centro, com as quatro áreas da Medvita girando em volta.")}
</div></section>

<section class="section" aria-labelledby="mv-title"><div class="wrap">
  <h2 class="sr-only" id="mv-title">Missão e visão</h2>
  <div class="tiles tiles-2">
    <article class="tile reveal"><span class="tile-art">{img3d("broto")}</span><h3>Missão</h3><p>Melhorar a qualidade de vida dos pacientes com atendimento multiprofissional, integral, acessível e baseado em evidências, num ambiente acolhedor.</p></article>
    <article class="tile tile-blue reveal" style="--d:.08s"><span class="tile-art">{img3d("lupa")}</span><h3>Visão</h3><p>Unir conhecimento técnico e cuidado humano nos serviços de saúde e de apoio interdisciplinar.</p></article>
  </div>
</div></section>

<section class="section section-sky" aria-labelledby="val-title"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Valores</p><h2 class="title" id="val-title">No que a Medvita <span class="blue">acredita</span></h2></div>
  <div class="tiles tiles-5">{"".join(f'<article class="tile reveal" style="--d:{i*0.06:.2f}s"><span class="tile-art">{img3d(n)}</span><h3>{t}</h3><p>{p}</p></article>' for i, (n, t, p) in enumerate(VALORES))}</div>
</div></section>

<section class="section" aria-labelledby="dados-title"><div class="wrap split">
  <div class="reveal"><p class="kicker">Empresa</p><h2 class="title" id="dados-title">Dados da <span class="blue">empresa</span></h2></div>
  <dl class="facts reveal" style="--d:.1s">
    <div><dt>Razão social</dt><dd>{RAZAO}</dd></div>
    <div><dt>CNPJ</dt><dd>{CNPJ}</dd></div>
    <div><dt>Responsável técnico</dt><dd>{confirmar("CONFIRMAR nome e registro")}</dd></div>
    <div><dt>Encarregado de dados</dt><dd>{DPO_NOME}</dd></div>
    <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
  </dl>
</div></section>

<section class="section" aria-label="Proteção de dados" style="padding-top:0"><div class="wrap">{TRUST}</div></section>
''')

# =====================================================================
# Contato
# =====================================================================
page("contato.html",
 "Contato | Medvita",
 f"WhatsApp {WA_SHOW}, e-mail {EMAIL} e Instagram @medvita.multi.",
 f'''<section class="page-hero" aria-labelledby="hero-title">{PATHS}<div class="wrap">
  <p class="kicker">Contato · horário de atendimento {confirmar()}</p>
  <h1 class="display" id="hero-title" data-draw>Fale com a {stroke("Medvita")}</h1>
</div></section>
<section class="section" aria-labelledby="canais-title" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
  <h2 class="sr-only" id="canais-title">Canais</h2>
  <div class="channels">
    <a class="channel channel-art reveal" data-tilt href="{WA}" target="_blank" rel="noopener noreferrer">{img3d("telefone", cls="channel-img")}<small>WhatsApp e telefone</small><strong>{WA_SHOW}</strong><span>Instituições e profissionais</span>{NEW_TAB}</a>
    <a class="channel channel-art reveal" data-tilt style="--d:.06s" href="mailto:{EMAIL}">{img3d("envelope", cls="channel-img")}<small>E-mail</small><strong>{EMAIL}</strong><span>Propostas e editais</span></a>
    <a class="channel channel-art reveal" data-tilt style="--d:.12s" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{img3d("conversa", cls="channel-img")}<small>Instagram</small><strong>@medvita.multi</strong><span>Novidades da equipe</span>{NEW_TAB}</a>
  </div>
  <p class="muted contact-note">Dados pessoais (LGPD): {DPO_NOME}, <a href="mailto:{DPO_EMAIL}">{DPO_EMAIL}</a> {confirmar()}</p>
</div></section>
''')

# =====================================================================
# Privacidade e 404
# =====================================================================
page("privacidade.html",
 "Política de Privacidade | Medvita",
 "Como o site da Medvita trata dados pessoais: o que é coletado, para quê, por quanto tempo e como pedir acesso, correção ou exclusão.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Política de Privacidade</nav>
  <p class="kicker">Atualizada em {datetime.date.today().strftime("%d/%m/%Y")}</p>
  <h1 class="title" id="hero-title">Política de <span class="blue">Privacidade</span></h1>
</div></section>
<section class="section" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap prose">
<p>{confirmar("CONFIRMAR: texto para revisão jurídica antes do domínio oficial")}</p>
<h2>Quem trata os dados</h2>
<p>{RAZAO}, CNPJ {CNPJ}.</p>
<p>Encarregado pelo tratamento de dados pessoais: {DPO_NOME}, <a href="mailto:{DPO_EMAIL}">{DPO_EMAIL}</a>, telefone {DPO_TEL}.</p>
<h2>O que este site coleta</h2>
<p>Nada fica guardado no site. Os formulários só montam uma mensagem, que é enviada apenas se você decidir mandá-la pelo seu WhatsApp. A partir daí ela chega à Medvita como qualquer outra mensagem.</p>
<p>Os dados que você pode incluir são: nome, instituição, tipo de instituição, cidade, estado, profissão, registro no conselho, áreas e turnos. Não envie dados de pacientes nem documentos pelo formulário.</p>
<p>O site não usa cookies de publicidade nem ferramentas de análise de audiência. A hospedagem (GitHub Pages) pode registrar dados técnicos de acesso, como endereço IP, para segurança e funcionamento do serviço.</p>
<h2>Para que os dados são usados</h2>
<ul>
<li>Responder ao seu contato.</li>
<li>Para instituições: preparar propostas e prestar os serviços contratados.</li>
<li>Para profissionais: recrutamento e seleção, e organização das escalas.</li>
<li>Cumprir obrigações legais e regulatórias, inclusive com órgãos públicos e conselhos de classe.</li>
</ul>
<p>A Medvita não vende dados pessoais.</p>
<h2>Com quem os dados podem ser compartilhados</h2>
<p>Só quando necessário: com as instituições contratantes, para executar o contrato; com fornecedores de folha de pagamento, contabilidade, tecnologia e saúde ocupacional; e com autoridades, quando a lei exigir. Todos devem manter os dados em sigilo.</p>
<h2>Por quanto tempo</h2>
<p>Pelo tempo necessário para as finalidades acima e pelos prazos que a lei exige. Depois disso, os dados são eliminados ou anonimizados.</p>
<h2>Seus direitos</h2>
<p>Pela Lei Geral de Proteção de Dados (Lei 13.709/2018), você pode pedir a confirmação do tratamento, o acesso, a correção, a anonimização, o bloqueio, a portabilidade e a eliminação dos seus dados, além de revogar o consentimento. Escreva para <a href="mailto:{DPO_EMAIL}">{DPO_EMAIL}</a> com o assunto "Dados pessoais".</p>
<h2>Segurança</h2>
<p>Os dados recebidos são acessados apenas por pessoas autorizadas, na medida do necessário. Colaboradores, parceiros e fornecedores assinam termos de confidencialidade.</p>
<h2>Mudanças nesta política</h2>
<p>Esta política pode ser atualizada. A data no topo da página mostra a versão em vigor.</p>
</div></section>
''')

page("404.html",
 "Página não encontrada | Medvita",
 "Esta página não existe ou mudou de endereço.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title" style="min-height:60vh">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Erro 404</p>
    <h1 class="display" id="hero-title" data-draw>Página {stroke("não encontrada")}</h1>
    <div class="btn-row"><a class="btn btn-primary" href="index.html"><span>Início</span></a><a class="btn btn-outline" href="contato.html"><span>Contato</span></a></div>
  </div>
  <figure class="hero-cluster" aria-hidden="true">{float3d("lupa", "c-main", 0.3)}{float3d("pensamento", "c-a", 0.6, 0.7)}</figure>
</div></section>
''', noindex=True)

# ---------- sitemap e robots ----------
pages = ["index.html", "para-instituicoes.html", "trabalhe-conosco.html", "sobre.html", "contato.html", "privacidade.html"]
today = datetime.date.today().isoformat()
urls = "".join(f"<url><loc>{SITE_URL}/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod></url>" for p in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print("ok")
