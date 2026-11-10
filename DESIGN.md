# Design — Medvita

Direção: clínico e direto. Papel branco, texto em tinta roxa escura, réguas finas no lugar de cartões, um só desenho: o traço contínuo que forma o coração do logo.

Fonte da verdade: tokens em `css/medvita.css` (`:root`).

| Token | Valor | Uso |
| --- | --- | --- |
| `--ink` | #2A2140 | títulos, texto, rodapé |
| `--muted` | #5A5178 | apoio |
| `--brand` | #62229C | roxo do logo: botão principal, traço, links, destaques pontuais |
| `--brand-deep` | #4A1779 | hover, links |
| `--tint` | #F3EFF9 | fundo de faixa (cor sólida, sem degradê) |
| `--rule` | #E2DBEE | réguas e bordas |
| `--r-s` / `--r-m` / `--r-l` | 4 / 8 / 14 px | campo e caixa de escolha / botão secundário / painel |

Regras
- Fonte: Plus Jakarta Sans auto-hospedada (500 a 800), a mesma dos posts. Títulos em 800, em frase normal (sem maiúsculas).
- Desenho: só o traço do logo (`trace()` no build), que se desenha uma vez ao aparecer. Nada de emoji, ícone 3D, estetoscópio, cruz ou jaleco fora do logo.
- Movimento: só o traço. Respeita `prefers-reduced-motion`.
- Pílula só no botão principal. Botão secundário com contorno e canto de 8 px.
- Listas com régua no lugar de grade de cartões. Variar a forma de cada seção.
- Textos: sem "médico" e "serviços médicos", sem superlativos, promessas ou números sem prova. Proibidos também: soluções estratégicas, otimizar, excelência, inovação, garantir, líder, referência.
- Checagem: `python3 devibe_scan.py .` (unslop-ui) deve ficar sem achados altos.
