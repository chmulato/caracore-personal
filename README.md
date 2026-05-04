# Personal (Dev Blog)

Blog pessoal (Christian Mulato Dev Blog) no site matriz (caracore.com.br). Todo o conteúdo usa **links de referência relativos** para funcionar em qualquer base URL.

## Status atual do blog

- Artigos existentes em `docs/articles/*.html` com marcação `<article>`: **129**
- Ciclo ativo: **Junho 2026 - Maio 2029**
- Histórico preservado antes de: **04/06/2026**
- Séries com índice próprio: **Brasil SDK**, **Depois do debate**, **Protocolo de Lucerna**, **Recolocação Java**
- Convenção de imagens (página HTML): `docs/articles/assets/img/README.html`

## Convenção de links relativos

- **A partir de `personal/`** (index.html):
  - CSS: `articles/assets/css/main.css`
  - Um artigo: `articles/<nome>.html`

- **A partir de `personal/articles/`** (cada artigo):
  - Voltar ao início: `../index.html`
  - CSS: `assets/css/main.css`, `assets/css/article.css`, `assets/css/highlight.css`
  - Imagens: `assets/img/<arquivo>`
  - JS: `assets/js/main.js`
  - Link para outro artigo (mesma pasta): `nome_do_artigo.html`

Não usar caminhos absolutos do site (ex.: `/personal/...`) para navegação interna; usar apenas relativos. Links externos (LinkedIn, GitHub, etc.) permanecem absolutos. Canonical e og:url/og:image, quando usados, devem apontar para a URL canônica do matriz (https://personal.caracore.com.br//...).
