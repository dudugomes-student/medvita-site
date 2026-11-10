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

# ---------- ícones de interface (traço, 24x24) ----------
I = {
    "wa": '<path d="M4 19.5 5.3 15.6A8 8 0 1 1 8.6 18.8Z"/><path d="M9 10.5h6M9 13.5h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "menu": '<path d="M4 8h16M4 16h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
}
def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg>'

NEW_TAB = '<span class="sr-only"> (abre em nova aba)</span>'
def wa_btn(label="Falar no WhatsApp", cls="btn btn-primary"):
    return f'<a class="{cls}" href="{WA}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>{label}</span>{NEW_TAB}</a>'

def arrow_link(href, label):
    return f'<a class="link-arrow" href="{href}">{label}{icon("arrow")}</a>'

# O único desenho do site: a linha contínua que forma o coração do logo.
# `pos` move o coração ao longo da linha (0 a 1).
def trace(pos=0.5, cls="hero-trace"):
    w = 1200
    x = round(36 + pos * (w - 72 - 70))
    d = (f"M4 104 H{x-30} C{x} 104 {x+26} 98 {x+35} 80 C{x+44} 61 {x+35} 38 {x+19} 35 "
         f"C{x+9} 33 {x+2} 41 {x} 48 C{x-3} 37 {x-14} 30 {x-26} 35 C{x-41} 42 {x-35} 64 {x-14} 81 "
         f"C{x} 92 {x+16} 101 {x+40} 104 H{w-4}")
    return (f'<svg class="trace {cls}" data-draw viewBox="0 0 {w} 110" preserveAspectRatio="{'xMin' if pos < .4 else 'xMax' if pos > .6 else 'xMid'}YMax slice" aria-hidden="true">'
            f'<path pathLength="1" d="{d}"/></svg>')

AREAS = [("Fisioterapia", "Fisioterapeutas", "CREFITO"),
         ("Enfermagem", "Enfermeiros", "COREN"),
         ("Psicologia", "Psicólogos", "CRP"),
         ("Nutrição", "Nutricionistas", "CRN")]

NAV = [("index.html", "Início"), ("para-instituicoes.html", "Para instituições"), ("trabalhe-conosco.html", "Trabalhe conosco"),
       ("sobre.html", "Sobre"), ("contato.html", "Contato")]

def header(active):
    on = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{on if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="site-header">
  <div class="wrap header-bar">
    <a class="brand" href="index.html"><picture><source type="image/webp" srcset="assets/logo-80.webp 105w, assets/logo-160.webp 210w" sizes="92px"><img src="assets/logo-80.png" srcset="assets/logo-80.png 105w, assets/logo-160.png 210w" sizes="92px" width="105" height="80" alt="Med Vita Saúde: página inicial"></picture></a>
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
        <h2>Páginas</h2>
        <ul>
          <li><a href="para-instituicoes.html">Para instituições</a></li>
          <li><a href="trabalhe-conosco.html">Trabalhe conosco</a></li>
          <li><a href="sobre.html">Sobre a Medvita</a></li>
          <li><a href="privacidade.html">Política de Privacidade</a></li>
        </ul>
      </div>
      <div>
        <h2>Contato</h2>
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
  <a class="btn btn-line" href="para-instituicoes.html#pedido">Pedir equipe</a>
</nav>'''

def page(slug, title, desc, body, forms=False, noindex=False):
    url = f"{SITE_URL}/" if slug == "index.html" else f"{SITE_URL}/{slug}"
    js = '<script src="js/main.js" defer></script>' + ('<script src="js/forms.js" defer></script>' if forms else "")
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
<script>document.documentElement.classList.add('js')</script>
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
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="fonts/plus-jakarta-sans-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/medvita.css">
{ld}{js}
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
{header(slug)}
<main id="conteudo" tabindex="-1">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    (ROOT / slug).write_text(out, encoding="utf-8")

def form_result():
    return (f'<div class="form-result" data-form-result hidden><p role="status"></p>'
            f'<a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>Abrir no WhatsApp</span>{NEW_TAB}</a></div>')

def chips(label, values, name, group_cls=""):
    items = "".join(f'<label class="chip"><input type="checkbox" name="{name}" value="{v}" data-label="{label}"><span>{v}</span></label>' for v in values)
    return f'<fieldset class="full {group_cls}"><legend>{label}</legend><div class="chips">{items}</div></fieldset>'

def order_form(idp, title="Pedir equipe"):
    """Pedido de equipe para instituições. Sai pronto no WhatsApp."""
    return f'''<form class="order" id="{idp}" data-whatsapp-form="instituicao" data-number="{WA_NUMBER}" novalidate>
  <h2>{title}</h2>
  <p class="note">Marque o que precisa. A mensagem sai pronta no WhatsApp.</p>
  <div class="form-grid">
    {chips("Áreas", [a[0] for a in AREAS], "area", "picks")}
    {chips("Turnos", ["Dia", "Noite", "Fim de semana"], "turno")}
    <div class="field full"><label for="{idp}-tipo">Tipo de instituição</label><select id="{idp}-tipo" name="tipo" required data-label="Tipo de instituição"><option value="">Escolha</option><option>Prefeitura ou secretaria de saúde</option><option>Hospital</option><option>Clínica</option><option>Outra</option></select></div>
    <div class="field"><label for="{idp}-inst">Instituição</label><input id="{idp}-inst" name="instituicao" autocomplete="organization" required maxlength="160" data-label="Instituição"></div>
    <div class="field"><label for="{idp}-cidade">Cidade e estado</label><input id="{idp}-cidade" name="cidade" required maxlength="120" placeholder="Barueri (SP)" data-label="Cidade"></div>
    <div class="field full"><label for="{idp}-nome">Seu nome</label><input id="{idp}-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
  </div>
  <div class="form-foot"><button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Montar mensagem</span></button>
  <p>Sem dados de pacientes. Nada fica salvo no site.</p></div>
  {form_result()}
</form>'''

def areas_list():
    return '<ul class="areas">' + "".join(
        f'<li><strong>{t}</strong><span>{p} com registro ativo no conselho.</span><em>{c}</em></li>' for t, p, c in AREAS) + "</ul>"

UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()
uf_opts = "".join(f'<option value="{u}"{" selected" if u == "SP" else ""}>{u}</option>' for u in UFS)

# =====================================================================
# Início
# =====================================================================
page("index.html",
 "Medvita | Fisioterapia, enfermagem, psicologia e nutrição",
 "Fisioterapeutas, enfermeiros, psicólogos e nutricionistas para instituições públicas e privadas. Monte o pedido e envie pelo WhatsApp.",
 f'''<section class="hero" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div>
      <h1 class="h1" id="hero-title">Fisioterapeutas, enfermeiros, psicólogos e nutricionistas para a sua unidade.</h1>
      <p class="lede">A Medvita monta e acompanha equipes de saúde para prefeituras, hospitais e clínicas.</p>
      <div class="btn-row">{wa_btn()}<a class="btn btn-line" href="sobre.html">Conhecer a Medvita</a></div>
    </div>
    {order_form("pedido")}
  </div>
  <div class="wrap">{trace(0.22)}</div>
</section>

<section class="section" aria-labelledby="areas-title"><div class="wrap">
  <div class="section-head">
    <h2 class="h2" id="areas-title">Quatro áreas que trabalham juntas</h2>
    <p>Cada profissional atua na sua área e conversa com os outros sobre o mesmo paciente.</p>
  </div>
  {areas_list()}
</div></section>

<section class="section section-tint" aria-labelledby="jeito-title"><div class="wrap split">
  <h2 class="h2" id="jeito-title">O que a Medvita busca em cada atendimento</h2>
  <div>
    <p class="statement">Olhar a pessoa inteira, seguir o que a ciência mostra e manter o ambiente seguro e acolhedor.</p>
    <p class="muted" style="margin-top:20px">É a missão da empresa, resumida no lema do logo: qualidade e humanização.</p>
    {arrow_link("sobre.html", "Missão, visão e valores")}
  </div>
</div></section>

<section class="section" aria-labelledby="prof-title"><div class="wrap">
  <div class="callout">
    <div>
      <h2 class="h2" id="prof-title">Você é profissional de saúde?</h2>
      <p class="muted" style="margin-top:10px">Fisioterapeuta, enfermeiro, psicólogo ou nutricionista: deixe seu cadastro.</p>
    </div>
    <a class="btn btn-line" href="trabalhe-conosco.html">Fazer cadastro</a>
  </div>
</div></section>
''', forms=True)

# =====================================================================
# Para instituições
# =====================================================================
STEPS = [("Conversa", "Entender a unidade, a demanda e o prazo."), ("Proposta", "Áreas, turnos e escala por escrito."),
         ("Começo", "A equipe é apresentada à unidade."), ("Acompanhamento", "Ajustes ao longo do contrato.")]

page("para-instituicoes.html",
 "Para instituições de saúde | Medvita",
 "Prefeituras, secretarias, hospitais e clínicas: peça fisioterapeutas, enfermeiros, psicólogos e nutricionistas e envie o pedido pelo WhatsApp.",
 f'''<section class="page-top" aria-labelledby="hero-title"><div class="wrap">
  <p class="eyebrow">Para instituições públicas e privadas</p>
  <h1 class="h1" id="hero-title">Do pedido à equipe na unidade</h1>
  <p class="lede">Você diz o que precisa, a Medvita monta a equipe e acompanha o contrato.</p>
  {trace(0.78)}
</div></section>

<section class="section" aria-labelledby="como-title" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
  <h2 class="sr-only" id="como-title">Como funciona</h2>
  <p class="muted" style="margin-bottom:18px">Etapas {confirmar()}</p>
  <ol class="steps">{"".join(f"<li><h3 class='h3'>{t}</h3><p>{p}</p></li>" for t, p in STEPS)}</ol>
</div></section>

<section class="section section-tint" aria-labelledby="pedido-h"><div class="wrap split">
  <div>
    <h2 class="h2" id="pedido-h">Monte o pedido</h2>
    <p class="lede" style="margin-top:14px">Marque as áreas e os turnos. Os detalhes a gente acerta na conversa.</p>
    <p class="muted" style="margin-top:28px">Contratação por licitação? Envie o edital para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
  {order_form("pedido", "Pedido de equipe")}
</div></section>

<section class="section" aria-labelledby="areas-title"><div class="wrap">
  <div class="section-head"><h2 class="h2" id="areas-title">Quem vai para a sua unidade</h2><p>Todos com registro ativo no conselho da profissão.</p></div>
  {areas_list()}
</div></section>
''', forms=True)

# =====================================================================
# Trabalhe conosco
# =====================================================================
prof_opts = ('<option value="Fisioterapeuta">Fisioterapeuta</option><option value="Enfermeiro(a)">Enfermeiro(a)</option>'
             '<option value="Psicólogo(a)">Psicólogo(a)</option><option value="Nutricionista">Nutricionista</option>')

page("trabalhe-conosco.html",
 "Trabalhe conosco | Medvita",
 "Fisioterapeutas, enfermeiros, psicólogos e nutricionistas: deixe seu cadastro com a Medvita pelo WhatsApp.",
 f'''<section class="page-top" aria-labelledby="hero-title"><div class="wrap">
  <p class="eyebrow">Para profissionais de saúde {confirmar()}</p>
  <h1 class="h1" id="hero-title">Trabalhe com a Medvita</h1>
  <p class="lede">Fisioterapeutas, enfermeiros, psicólogos e nutricionistas com registro ativo.</p>
  {trace(0.5)}
</div></section>

<section class="section" aria-labelledby="cad-title" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap split">
  <div>
    <h2 class="h2" id="cad-title">Seu cadastro em um minuto</h2>
    <p class="lede" style="margin-top:14px">A mensagem sai pronta no seu WhatsApp. Documentos, só quando a equipe pedir.</p>
  </div>
  <form class="order" data-whatsapp-form="profissional" data-number="{WA_NUMBER}" novalidate>
    <div class="form-grid">
      <div class="field full"><label for="p-nome">Nome completo</label><input id="p-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <div class="field"><label for="p-prof">Profissão</label><select id="p-prof" name="profissao" required data-label="Profissão"><option value="">Escolha</option>{prof_opts}</select></div>
      <div class="field"><label for="p-reg">Registro no conselho</label><input id="p-reg" name="registro" required maxlength="24" placeholder="COREN-SP 123456" data-label="Registro"></div>
      <div class="field"><label for="p-cidade">Cidade onde mora</label><input id="p-cidade" name="cidade" autocomplete="address-level2" required maxlength="80" data-label="Cidade"></div>
      <div class="field"><label for="p-uf">Estado</label><select id="p-uf" name="uf" required data-label="Estado">{uf_opts}</select></div>
      {chips("Turnos", ["Dia", "Noite", "Fim de semana"], "turno")}
    </div>
    <div class="form-foot"><button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Montar mensagem</span></button>
    <p>Nada fica salvo no site. <a href="privacidade.html">Privacidade</a></p></div>
    {form_result()}
  </form>
</div></section>
''', forms=True)

# =====================================================================
# Sobre
# =====================================================================
VALORES = [("Qualidade", "Cuidado pensado para cada pessoa."),
           ("Empatia e respeito", "Dignidade e atenção ao que cada um precisa."),
           ("Atualização", "Métodos e práticas revistos sempre."),
           ("Trabalho em equipe", "As quatro áreas trabalham juntas."),
           ("Integridade", "Ética, transparência e honestidade.")]

page("sobre.html",
 "Sobre a Medvita | Serviços de saúde multiprofissionais",
 f"{RAZAO}: fisioterapia, enfermagem, psicologia e nutrição. Missão, visão, valores e dados da empresa.",
 f'''<section class="page-top" aria-labelledby="hero-title"><div class="wrap">
  <p class="eyebrow">Sobre</p>
  <h1 class="h1" id="hero-title">Uma empresa de saúde que junta quatro áreas</h1>
  <p class="lede">Fisioterapia, enfermagem, psicologia e nutrição, com o lema que está no logo: qualidade e humanização.</p>
  {trace(0.3)}
</div></section>

<section class="section" aria-labelledby="mv-title" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap split">
  <div><h2 class="h3" id="mv-title" style="color:var(--brand);margin-bottom:12px">Missão</h2>
  <p class="statement">Melhorar a qualidade de vida dos pacientes com atendimento multiprofissional, integral, acessível e baseado em evidências, num ambiente acolhedor.</p></div>
  <div><h2 class="h3" style="color:var(--brand);margin-bottom:12px">Visão</h2>
  <p class="statement">Unir conhecimento técnico e cuidado humano nos serviços de saúde e de apoio interdisciplinar.</p></div>
</div></section>

<section class="section section-tint" aria-labelledby="val-title"><div class="wrap">
  <h2 class="h2" id="val-title" style="margin-bottom:28px">Valores</h2>
  <ul class="values">{"".join(f'<li><strong>{t}</strong><span>{p}</span></li>' for t, p in VALORES)}</ul>
</div></section>

<section class="section" aria-labelledby="dados-title"><div class="wrap split">
  <h2 class="h2" id="dados-title">Dados da empresa</h2>
  <dl class="facts">
    <div><dt>Razão social</dt><dd>{RAZAO}</dd></div>
    <div><dt>CNPJ</dt><dd>{CNPJ}</dd></div>
    <div><dt>Responsável técnico</dt><dd>{confirmar("CONFIRMAR nome e registro")}</dd></div>
    <div><dt>Encarregado de dados</dt><dd>{DPO_NOME}</dd></div>
    <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
    <div><dt>Privacidade</dt><dd><a href="privacidade.html">Política de Privacidade</a></dd></div>
  </dl>
</div></section>
''')

# =====================================================================
# Contato
# =====================================================================
page("contato.html",
 "Contato | Medvita",
 f"WhatsApp {WA_SHOW}, e-mail {EMAIL} e Instagram @medvita.multi.",
 f'''<section class="page-top" aria-labelledby="hero-title"><div class="wrap">
  <h1 class="h1" id="hero-title">Fale com a Medvita</h1>
  <p class="lede">Horário de atendimento {confirmar()}</p>
  {trace(0.62)}
</div></section>
<section class="section" aria-labelledby="canais-title" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
  <h2 class="sr-only" id="canais-title">Canais</h2>
  <ul class="channels">
    <li><small>WhatsApp e telefone</small><a href="{WA}" target="_blank" rel="noopener noreferrer">{WA_SHOW}{NEW_TAB}</a></li>
    <li><small>E-mail, propostas e editais</small><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><small>Instagram</small><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@medvita.multi{NEW_TAB}</a></li>
  </ul>
  <p class="muted" style="margin-top:28px">Dados pessoais (LGPD): {DPO_NOME}, <a href="mailto:{DPO_EMAIL}">{DPO_EMAIL}</a> {confirmar()}</p>
</div></section>
''')

# =====================================================================
# Privacidade e 404
# =====================================================================
page("privacidade.html",
 "Política de Privacidade | Medvita",
 "Como o site da Medvita trata dados pessoais: o que é coletado, para quê, por quanto tempo e como pedir acesso, correção ou exclusão.",
 f'''<section class="page-top" aria-labelledby="hero-title"><div class="wrap">
  <p class="eyebrow">Atualizada em {datetime.date.today().strftime("%d/%m/%Y")}</p>
  <h1 class="h1" id="hero-title">Política de Privacidade</h1>
</div></section>
<section class="section" style="padding-top:clamp(28px,4vw,48px)"><div class="wrap prose">
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
 f'''<section class="page-top" aria-labelledby="hero-title" style="padding-bottom:var(--sec)"><div class="wrap">
  <p class="eyebrow">Erro 404</p>
  <h1 class="h1" id="hero-title">Esta página não existe</h1>
  <div class="btn-row"><a class="btn btn-primary" href="index.html">Ir para o início</a><a class="btn btn-line" href="contato.html">Contato</a></div>
  {trace(0.7)}
</div></section>
''', noindex=True)

# ---------- sitemap e robots ----------
pages = ["index.html", "para-instituicoes.html", "trabalhe-conosco.html", "sobre.html", "contato.html", "privacidade.html"]
today = datetime.date.today().isoformat()
urls = "".join(f"<url><loc>{SITE_URL}/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod></url>" for p in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print("ok")
