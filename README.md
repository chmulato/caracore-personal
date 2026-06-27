# Personal (Dev Blog)

Blog pessoal (Christian Mulato Dev Blog) no site matriz (caracore.com.br). Todo o conteúdo usa **links de referência relativos** para funcionar em qualquer base URL.

## Status atual do blog

- Artigos existentes em `docs/articles/*.html` com marcação `<article class="post">`: **179**
- Ciclo ativo: **Junho 2026 - Maio 2029**
- Séries com índice próprio: **Brasil SDK**, **Depois do debate**, **A Ilusão Informatizada**, **O Mito da Eficiência**, **Protocolo de Lucerna**, **Recolocação Java**, **As Redes Invisíveis**, **O Novo Tabuleiro do Mundo**, **Além do Hype**
- Série com chamada (sem `_index`): **Horizonte do Essencial** (`2026_06_05_serie_horizonte_essencial_chamada.html`)
- **Junho 2026:** 11 artigos no índice (avulso 02/06 + avulso 14/06 + avulso 19/06 + avulso 27/06 + chamada Horizonte + episódios Lucerna, Horizonte e Brasil SDK)
- **Último avulso publicado (jun/2026):** [A Normose da Engenharia Financeira...](docs/articles/2026_06_27_a_normose_da_engenharia_financeira_e_o_retrato_de_veblen.html), [Os Erros Invisíveis na Arquitetura...](docs/articles/2026_06_19_os_erros_invisiveis_na_arquitetura_que_ninguem_te_conta.html), [O Espelho da Linha de Frente...](docs/articles/2026_06_14_o_espelho_da_linha_de_frente_Ilusoes_digitais_e_o_cerco_a_economia_invisivel.html) e [Do AutoCAD à Inteligência Artificial…](docs/articles/2026_06_02_do_autocad_a_inteligencia_artificial_o_programador_esta_se_tornando_um_novo_tipo_de_projetista.html) — continuação de [Da Prancheta ao Prompt](docs/articles/2025_07_03_da_prancheta_ao_prompt_o_futuro_da_criacao_de_softwares_com_inteligencia_artificial.html) (jul/2025)
- Convenção de imagens: `docs/articles/assets/img/README.html`
- Memória Cursor do workspace: `.cursor/rules/blog-personal-workspace.mdc`

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

Não usar caminhos absolutos do site (ex.: `/personal/...`) para navegação interna; usar apenas relativos. Links externos (LinkedIn, GitHub, etc.) permanecem absolutos. Canonical e og:url/og:image, quando usados, devem apontar para a URL canônica do matriz (`https://personal.caracore.com.br/...`).

## Ao publicar série ou artigo novo

Atualizar em conjunto: HTML do artigo, `docs/index.html` (cartões + filtro + contador), `docs/feed.xml`, `docs/articles/assets/img/README.html`, este README e `.cursor/rules/blog-personal-workspace.mdc`.
