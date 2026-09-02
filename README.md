# Christian Mulato Dev Blog

Este repositório contém a estrutura, acervo e esteira de publicações do blog pessoal e profissional de Christian Mulato ([personal.caracore.com.br](https://personal.caracore.com.br/)). O espaço é dedicado a ensaios de alta densidade técnica, reflexões de carreira, arquitetura de sistemas corporativos, soberania digital e trade-offs da engenharia de software real.

## Propósito e Linha Editorial

O blog equilibra análises técnicas rigorosas com reflexões do dia a dia da engenharia de software, adotando a abordagem de *Fiction-Based Technical Insights* e realismo de engenharia. A linha editorial foge de modismos efêmeros e dogmas corporativos para focar em:
* **Fundações de Engenharia:** Transações ACID, persistência relacional soberana, ciclo de vida de componentes, integridade de dados e arquitetura local.
* **Economia e FinOps:** Custos reais de infraestrutura, matemática de escala, impacto de taxas de juros globais e modelos de monetização por resultado.
* **Transição Tecnológica:** Automação cognitiva, sistemas headless, agentes autônomos locais (M2M) e o novo papel da interface humana focado em auditoria e relatórios.

---

## Visão Geral do Acervo

* **Total de Artigos:** 260 artigos publicados.
* **Período de Publicações:** De março de 2024 a março de 2029.
* **Séries Temáticas Ativas no Acervo:**
  * [A Evolução Cíclica da TI](https://personal.caracore.com.br/articles/2026_11_16_serie_evolucao_ciclica_ti_chamada.html): Trilogia de novembro de 2026 analisando a trajetória de três décadas — do aprendizado denso no servidor (JSF/JSP nos anos 2000) à hipertrofia do front-end e o colapso do CRUD humano na era dos agentes autônomos.
  * [Economia Programável e Soberania de Ativos](https://personal.caracore.com.br/articles/2029_01_04_serie_economia_programavel_chamada.html): Pós-graduação autodidata de 2029 focada na transição monetária do Drex/CBDC, tokenização de RWA, infraestrutura do BIS e BRICS Pay, e automação comercial com agentes autônomos de IA.
  * [Auditor de Sistemas](https://personal.caracore.com.br/articles/2028_01_18_serie_auditor_sistemas_chamada.html): Pós-graduação autodidata de 2028 para profissionais com mais de 8 anos de estrada, cobrindo governança de TI (COBIT/CRISC), perícia forense (ISO/IEC 27037) e compliance fiscal internacional.
  * [Blindagem de Sistemas](https://personal.caracore.com.br/articles/2027_11_11_serie_blindagem_sistemas_chamada.html): Pós-graduação prática em engenharia de riscos, resiliência de memória com Rust, mitigação na JVM, isolamento em kernel (eBPF) e soberania digital, acompanhada de 7 lições de apoio aos sábados.
  * [Do RPA ao Silício](https://personal.caracore.com.br/articles/2026_08_25_serie_do_rpa_ao_silicio_a_grande_transformacao_chamada.html): Crônica ficcional com fundo de verdade técnica sobre o futuro do desenvolvimento, automação cognitiva, sistemas operacionais e a geopolítica física do silício.
  * [A Ilusão Informatizada](https://personal.caracore.com.br/articles/2026_09_30_serie_ilusao_informatizada_index.html): Ensaios críticos sobre o avanço tecnológico acelerado, economia de tokens e o vácuo de responsabilidade.
  * [Recolocação Java](https://personal.caracore.com.br/articles/2026_08_10_serie_recolocacao_java_teste_pratico_index.html): Guias pragmáticos de carreira, contratação e testes práticos de arquitetura sob pressão.
  * [Além do Hype](https://personal.caracore.com.br/articles/2027_05_05_serie_alem_hype_monolitos_microservicos_index.html): Discussão matemática e financeira entre monolitos modulares e microsserviços.
  * [O Novo Tabuleiro do Mundo](https://personal.caracore.com.br/articles/2027_05_02_serie_novo_tabuleiro_index.html): A geopolítica de IA, data centers locais e soberania energética.
  * [As Redes Invisíveis](https://personal.caracore.com.br/articles/2027_02_12_serie_redes_invisiveis_index.html): Telecomunicações, bilhetagem de transporte e resiliência cibernética.
  * [Horizonte do Essencial](https://personal.caracore.com.br/articles/2026_06_05_serie_horizonte_essencial_chamada.html): Reflexões sobre hardware local, soberania de código e desenvolvimento sustentável.
  * [Protocolo de Lucerna](https://personal.caracore.com.br/articles/2026_04_20_serie_protocolo_lucerna_index.html): Histórias e análises de segurança em sistemas corporativos legados.
  * [O Mito da Eficiência](https://personal.caracore.com.br/articles/2026_12_15_serie_mito_eficiencia_ia_silicio_index.html): IA, silício e a busca racional por otimização real.
  * [A Ilusão da Interface](https://personal.caracore.com.br/articles/2027_10_07_serie_ilusao_da_interface_chamada.html): Crítica geopolítica e social sobre o petrodólar, as panelinhas locais e a economia da atenção.
  * [Brasil, SDK e Soberania](https://personal.caracore.com.br/articles/2026_02_15_serie_brasil_sdk_soberania_index.html): Análise de desenvolvimento nacional, regulação e soberania.
  * [Depois do debate](https://personal.caracore.com.br/articles/2026_10_06_serie_depois_do_debate_carreira_index.html): Reflexões sobre o futuro da carreira técnica na era dos LLMs.
  * [Do Silício ao Chão de Fábrica](https://personal.caracore.com.br/articles/2027_07_30_serie_do_silicio_ao_chao_de_fabrica_chamada.html): Geopolítica física, soberania de dados híbrida e telemetria offline-first na economia real produtiva.

---

## Padrões Arquiteturais e de Publicação

1. **Estrutura Estática e Leve:** Sem runtime dinâmico no servidor; páginas HTML5 semânticas com suporte a tema claro/escuro (`assets/css/main.css`, `assets/css/article.css`).
2. **Dicionário Verde em Quadro de Lousa (`.chalkboard`):** Todo artigo técnico ou ensaio deve incluir uma seção final com glossário de termos técnicos e de negócios explicados para leigos (`<div class="chalkboard"><dl><dt><strong>...</strong></dt><dd>...</dd></dl></div>`).
3. **Imagens Hero 16:9:** Fotografias cinematográficas e conceituais de engenharia, em formato paisagem 16:9, posicionadas no topo do artigo com `<figure>`, `<figcaption>` e metadados `og:image`.
4. **Navegação Encadeada:** Episódios de séries contêm cabeçalho com kicker da série e rodapé com links bidirecionais (*Anterior*, *Próximo*, *Índice da Série*).
5. **Automação do Feed RSS (`docs/feed.xml`):**
   ```powershell
   python update_feed.py
   ```
   Lê todos os artigos de `docs/articles/`, extrai o conteúdo semântico, valida URLs absolutas e gera o `feed.xml` com ordenação cronológica decrescente estrita (RFC-822).

6. **Publicação automática no LinkedIn:** O script [`linkedin_rss_auto.py`](./linkedin_rss_auto.py) identifica o arquivo de artigo adicionado ou alterado no commit atual, extrai o título do frontmatter YAML Markdown ou do HTML publicado e cria uma publicação de artigo pela API REST `https://api.linkedin.com/rest/posts`.

### Como funciona para leigos

Quando um novo artigo é enviado para o GitHub, o GitHub Actions inicia automaticamente o processo. O robô encontra o artigo alterado, prepara uma mensagem com título, resumo e link, e publica essa mensagem no perfil do LinkedIn. Nenhuma senha fica escrita no código: as informações sensíveis ficam guardadas de forma protegida no GitHub.

O processo é acionado apenas por alterações em `docs/articles/**` nas branches `master` ou `main`. Alterações no README, no feed ou em outros arquivos não geram uma publicação no LinkedIn.

### Configuração e manutenção para desenvolvedores

O workflow [`publish-linkedin.yml`](./.github/workflows/publish-linkedin.yml) instala Python e `requests`, fornece as configurações por variáveis de ambiente e executa [`linkedin_rss_auto.py`](./linkedin_rss_auto.py). A URL pública é formada por `BLOG_BASE_URL` e `PUBLIC_ARTICLES_PATH`; neste repositório, o padrão é `https://personal.caracore.com.br/articles/`.

No repositório GitHub, abra **Settings > Secrets and variables > Actions > New repository secret** e mantenha estes Secrets:

| Secret | Conteúdo | Renovação |
|---|---|---|
| `LINKEDIN_ACCESS_TOKEN` | Access token OAuth com o escopo `w_member_social`. | Renovar quando expirar, atualmente em aproximadamente 60 dias. |
| `PERSON_URN` | URN no formato `urn:li:person:SEU_ID`. | Normalmente não muda para o mesmo perfil. |

Na aplicação LinkedIn, os produtos **Share on LinkedIn** e **Sign In with LinkedIn using OpenID Connect** devem estar provisionados. A autorização utiliza `openid`, `profile` e `w_member_social`. O token não deve ser incluído no código, em commits, logs ou URLs.

#### Renovação do token

O access token mostrado no painel do LinkedIn tem validade limitada. Quando ele expirar:

1. Gere um novo token na ferramenta **OAuth 2.0** da aplicação LinkedIn, usando `openid`, `profile` e `w_member_social`.
2. No GitHub, acesse **Settings > Secrets and variables > Actions**, edite `LINKEDIN_ACCESS_TOKEN` e substitua o valor antigo.
3. Não altere `PERSON_URN`, salvo se a publicação passar para outro perfil.
4. Faça um novo push em `docs/articles/**` e confirme o resultado em **GitHub > Actions > Publicar artigo no LinkedIn**.

Uma execução concluída com sucesso indica que a API aceitou a publicação; a confirmação final deve ser feita no perfil do LinkedIn.

---

## Memória para IAs e Agentes

Para diretrizes detalhadas de colaboração autônoma, padrões de código e templates de novos artigos, consulte o arquivo [`AGENTS.md`](./AGENTS.md).
