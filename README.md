# Site da Medvita

Site estático (HTML, CSS e JavaScript, sem dependências no navegador) da MED VITA SERVIÇOS DE SAÚDE LTDA, para o GitHub Pages.

## Páginas

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Início: pedido de equipe no topo, as quatro áreas, missão em uma frase, chamada para profissionais |
| `para-instituicoes.html` | Etapas, pedido de equipe pelo WhatsApp, licitações |
| `trabalhe-conosco.html` | Cadastro de fisioterapeutas, enfermeiros, psicólogos e nutricionistas pelo WhatsApp |
| `sobre.html` | Missão, visão, valores e dados da empresa |
| `contato.html` | WhatsApp, e-mail e Instagram |
| `privacidade.html` | Política de privacidade deste site |
| `404.html` | Página não encontrada |

## Como editar

Edite o `build.py` e rode `python3 build.py`. Não edite os `.html` direto.

- **Contato:** `WA_NUMBER`, `WA_SHOW`, `EMAIL` no topo do `build.py` e `WHATSAPP` em `js/forms.js`.
- **Domínio próprio:** troque `SITE_URL`, rode o build e crie o arquivo `CNAME`.
- **Marcas [CONFIRMAR]:** são geradas pela função `confirmar()`. Quando a informação chegar, troque a chamada pelo texto certo.

## Pendências antes do domínio oficial ([CONFIRMAR] no site)

- Nome e registro do responsável técnico (rodapé e Sobre).
- Se o (11) 92626-4855 atende WhatsApp. Todos os botões apontam para ele.
- Se o e-mail de contato continua `licitacoes@medvitamulti.com.br`.
- E-mail do encarregado de dados: a política antiga traz `equilibriummulti@gmail.com`.
- Se a Medvita recruta profissionais (página Trabalhe conosco).
- As etapas de "Como funciona" e o horário de atendimento.
- O público: o site foi escrito para instituições públicas e privadas, como diz a política de privacidade antiga ("mão de obra terceirizada para empresas públicas e privadas"). Se a Medvita também atende pacientes direto, a página inicial muda.
- Revisão jurídica da política de privacidade.

## Créditos

Fonte Plus Jakarta Sans (OFL). Logo oficial da Med Vita Saúde, tirado do site antigo. O traço com o coração foi desenhado à mão em SVG, a partir do logo (função `trace` no `build.py`).
