# Guia de Memória e Contexto para IAs — Christian Mulato Dev Blog (`AGENTS.md`)

> **Destinado a:** Todas as IAs, assistentes de código e agentes autônomos (Antigravity, Cursor, Copilot, Claude Code, Gemini).  
> **Repositório:** `caracore-personal`  
> **Domínio Oficial:** `https://personal.caracore.com.br/`  
> **Data de Atualização:** 02/09/2026
> **Total de Artigos:** 260 publicações (março de 2024 a março de 2029)  

---

## 1. Visão Geral e Identidade do Blog

O **Christian Mulato Dev Blog** é o espaço editorial e técnico de Christian Mulato (Engenheiro Construtor e Arquiteto de Software). O blog não é um agregador genérico de tutoriais, mas um acervo denso de:
* **Realismo de Engenharia & Fiction-Based Technical Insights:** Ensaios que conectam lições históricas da computação corporativa com a transição atual para IA, silício e economia programável.
* **Soberania Digital e Offline-First:** Foco em persistência local, robustez de dados, transações ACID, resiliência de memória e questionamento de dependências excessivas de nuvem.
* **FinOps e Eficiência de Negócio:** Análise crítica de custos de computação, tokens, juros globais, modelos de receita por resultado e sustentabilidade de carreira técnica.

---

## 2. Estrutura de Arquivos e Pastas

```
caracore-personal/
├── docs/
│   ├── index.html            # Página inicial (listagem de todos os artigos em ordem cronológica decrescente)
│   ├── ciclo-ativo.html      # Visualização exclusiva da janela do Ciclo Ativo oficial (2026-2029)
│   ├── feed.xml              # Feed RSS 2.0 completo com CDATA, enclosures e RFC-822 (gerado via script)
│   ├── CNAME                 # personal.caracore.com.br
│   ├── articles/
│   │   ├── YYYY_MM_DD_slug.html  # Todos os artigos publicados
│   │   └── assets/
│   │       ├── css/          # main.css, article.css, highlight.css
│   │       ├── js/           # main.js, article.js
│   │       └── img/          # Imagens hero (YYYY_MM_DD_IMAGE_001.png)
│   └── editorial/            # Páginas institucionais (linha editorial, manifesto, sobre o autor)
├── update_feed.py            # Script oficial em Python para regenerar docs/feed.xml
├── linkedin_rss_auto.py      # Publica o artigo alterado no commit na API REST do LinkedIn
├── README.md                 # Visão geral do repositório
├── .github/
│   └── workflows/
│       └── publish-linkedin.yml # Workflow de publicação automática no LinkedIn
└── AGENTS.md                 # Este documento de memória e regras para IAs
```

---

## 3. Padrão Obrigatório para Novos Artigos

Ao redigir e publicar novos artigos ou séries, toda IA **DEVE** seguir rigorosamente estes cinco passos:

### Passo 1: Nomenclatura e Cabeçalho do Artigo
* **Nome do arquivo:** `docs/articles/YYYY_MM_DD_nome_do_artigo.html`
* **Metadados:**
  - `<link rel="canonical" href="https://personal.caracore.com.br/articles/YYYY_MM_DD_nome_do_artigo.html" />`
  - `<meta property="og:url" content="https://personal.caracore.com.br/articles/YYYY_MM_DD_nome_do_artigo.html" />`
  - `<meta property="og:image" content="https://personal.caracore.com.br/articles/assets/img/YYYY_MM_DD_IMAGE_001.png" />`
  - `<meta name="author" content="Christian Mulato">`

### Passo 2: Imagem Hero 16:9 (Paisagem)
* **Padrão visual:** Foto/render editorial cinematográfico, estilo realista de alta sobriedade, iluminação técnica, sem rostos humanos identificáveis e sem marcas comerciais terceiras.
* **Markup:**
  ```html
  <figure class="hero-image-frame">
      <img src="assets/img/YYYY_MM_DD_IMAGE_001.png" alt="Descrição do tema" class="hero-image" />
      <figcaption class="hero-image-caption">Legenda descritiva com tom editorial e técnico.</figcaption>
  </figure>
  ```

### Passo 3: Dicionário Verde de Termos (`.chalkboard`) — **REGRA OBRIGATÓRIA**
Todo artigo técnico ou ensaio deve conter, antes da assinatura do autor, um quadro de lousa verde com termos técnicos e de negócios explicados em linguagem acessível para leigos e tomadores de decisão:

```html
<h2>Dicionário de Termos Técnicos e Negócios (para leigos)</h2>
<p>Conceitos fundamentais e jargões abordados no artigo explicados de forma simples e direta:</p>
<div class="chalkboard">
    <dl>
        <dt><strong>Termo Técnico ou Conceito</strong></dt>
        <dd>Explicação clara, sem jargões desnecessários, com foco no impacto de negócio e na compreensão de pessoas leigas.</dd>
        
        <dt><strong>Outro Conceito</strong></dt>
        <dd>Definição prática e contextualizada com o tema do artigo.</dd>
    </dl>
</div>
```

### Passo 4: Assinatura e Navegação no Rodapé
```html
<hr style="margin: 2.5rem 0 1.5rem 0;">
<p><em><strong>Nota:</strong> Descrição do tipo de ensaio (Fiction-Based Technical Insights & Engineering Realism).</em></p>

<div class="author-signature">
    <p><strong>Christian Mulato</strong><br>
    Engenheiro Construtor</p>
    <p>&copy; YYYY Christian Mulato. Todos os direitos reservados.</p>
</div>
```
E no `<footer class="site-footer">`:
* **Em séries:** Links para `Artigo anterior`, `Próximo episódio` e `Índice da série`.
* **Em artigos avulsos:** Link para a página inicial do blog.

### Passo 5: Atualização dos Índices e Regeneração do Feed
1. **`docs/index.html`:** Adicionar o card na respectiva seção mensal, respeitando a **ordem cronológica decrescente**.
2. **`docs/ciclo-ativo.html`:** Adicionar o link do artigo no mês correspondente do Ciclo Ativo.
3. **Regenerar o Feed RSS:** Executar o script oficial utilizando o Python centralizado do workspace:
   ```powershell
   & "D:\dev\.venv\Scripts\python.exe" "D:\dev\caracore-personal\update_feed.py"
   ```

---

## 4. Séries Temáticas Registradas no Acervo

| Período | Série | Foco Temático |
|---|---|---|
| **Nov/2026** | **A Evolução Cíclica da TI** | Trilogia do servidor clássico (JSF/JSP) ao fim do CRUD e à web para agentes autônomos. |
| **Jan-Mar/2029** | **Economia Programável** | Pós-graduação de 2029: Drex, CBDCs, tokenização de ativos reais (RWA), BIS e BRICS Pay. |
| **Jan-Mar/2028** | **Auditor de Sistemas** | Pós-graduação de 2028: Governança de TI (COBIT/CRISC), perícia forense (ISO 27037) e compliance fiscal. |
| **Nov-Dez/2027** | **Blindagem de Sistemas** | Pós-graduação de 2027: Engenharia de riscos, resiliência de memória com Rust, mitigação na JVM e eBPF. |
| **Out-Nov/2027** | **A Ilusão da Interface** | Crítica sobre petrodólar, desindustrialização e economia da atenção. |
| **Jul-Set/2027** | **Do Silício ao Chão de Fábrica** | Soberania de dados híbrida e telemetria offline-first na indústria real. |
| **Mai-Jun/2027** | **Além do Hype** | Análise matemática e financeira entre monolitos modulares e microsserviços. |
| **Mai-Jul/2027** | **O Novo Tabuleiro do Mundo** | Geopolítica de IA, data centers locais e soberania energética. |
| **Set-Nov/2026** | **Do RPA ao Silício** | Automação cognitiva, sistemas operacionais e geopolítica do silício. |
| **Out-Dez/2026** | **A Ilusão Informatizada** | Crítica sobre tokens, excesso de conteúdo e vácuo de responsabilidade. |
| **Ago-Set/2026** | **Recolocação Java** | Testes práticos de arquitetura e decisões de engenharia sob pressão. |
| **Jun-Ago/2026** | **Horizonte do Essencial** | Hardware local, sustentabilidade de código e limites de escala. |
| **Abr-Jul/2026** | **Protocolo de Lucerna** | Segurança corporativa em legados e conformidade técnica. |

---

## 5. Estado Operacional Atual (02/09/2026)

- Aplicação LinkedIn: **Christian Mulato's Blog**.
- Produtos LinkedIn provisionados: **Share on LinkedIn** e **Sign In with LinkedIn using OpenID Connect**.
- Escopos autorizados: `openid`, `profile` e `w_member_social`.
- Secrets de repositório configurados no GitHub: `LINKEDIN_ACCESS_TOKEN` e `PERSON_URN`. Nunca registrar seus valores nesta memória, em commits ou em logs.
- Workflow validado com sucesso na branch `master`, no commit `d093885`, com duração aproximada de 33 segundos.
- O `LINKEDIN_ACCESS_TOKEN` tem validade limitada, atualmente indicada pelo LinkedIn como aproximadamente 2 meses. Quando expirar, gerar novo token e substituir somente o Secret no GitHub.
- O `PERSON_URN` normalmente permanece estável para o mesmo perfil; só deve ser alterado se a identidade autora mudar.
- Para diagnóstico, consultar **GitHub > Actions > Publicar artigo no LinkedIn**. Não fazer chamadas reais à API em testes locais sem necessidade.

## 6. Automação de Publicação no LinkedIn

1. O workflow `.github/workflows/publish-linkedin.yml` é acionado por `push` nas branches `master` ou `main`, somente quando houver alteração em `docs/articles/**`.
2. O script `linkedin_rss_auto.py` usa `GITHUB_BEFORE` e `GITHUB_SHA` para identificar arquivos adicionados ou modificados no push atual.
3. O script aceita Markdown com frontmatter YAML e também os artigos HTML existentes. Para Markdown, a extensão `.md` é convertida para `.html` na URL pública.
4. A publicação usa `POST https://api.linkedin.com/rest/posts`, o escopo `w_member_social` e uma chave de idempotência derivada do commit e da URL.
5. Os parâmetros públicos padrão são `BLOG_BASE_URL=https://personal.caracore.com.br`, `POSTS_DIRECTORY=docs/articles` e `PUBLIC_ARTICLES_PATH=articles`.

## 7. Checklist de Verificação para IAs

Antes de finalizar qualquer tarefa no blog, valide os itens:
- [ ] O artigo possui data no formato `YYYY_MM_DD_*.html`.
- [ ] A imagem 16:9 está associada em `assets/img/` e referenciada nas tags `og:image` e `<figure>`.
- [ ] O **Dicionário Verde (`.chalkboard`)** está presente com termos e definições para pessoas leigas.
- [ ] O rodapé contém links funcionais de navegação bidirecional e link para o índice.
- [ ] O `docs/index.html` e `docs/ciclo-ativo.html` foram atualizados na ordem cronológica decrescente.
- [ ] O `python update_feed.py` foi executado e `docs/feed.xml` foi atualizado com sucesso.
