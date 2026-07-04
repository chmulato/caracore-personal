# Christian Mulato Dev Blog - Memory & Guidelines for AI Agents

Este documento serve para contextualizar qualquer agente ou modelo de IA sobre a estrutura, convenções de estilo, regras de publicação e padrões de layout do blog pessoal de Christian Mulato.

---

## 📂 Visão Geral do Projeto

* **Workspace Root:** `D:/onedrive/dev/caracore-personal`
* **Diretório de Distribuição (Github Pages):** `docs/`
* **Artigos e Séries:** `docs/articles/`
* **Assets de Imagem:** `docs/articles/assets/img/`
* **Estilos CSS:** `docs/articles/assets/css/` (arquivos `main.css`, `article.css`, `highlight.css`)

---

## 📈 Status Atual (Ciclo Ativo: jun/2026 a mai/2029)

* **Total de Artigos Publicados:** 191 artigos
* **Total de Séries com Índice Próprio:** 11 séries
* **Período do Acervo:** março de 2024 a setembro de 2027 (datas futuras em 2027 são usadas para agendamento de séries editoriais)
* **Lista de Séries Ativas:**
  1. **Além do Hype** (Index + 5 Episódios) — Arquitetura de software, matemática de escala e FinOps.
  2. **O Novo Tabuleiro do Mundo** (Index + 6 Episódios + Epílogo) — IA como commodity física e matriz energética.
  3. **As Redes Invisíveis** (Index + 5 Episódios + Epílogo) — Telecomunicações e transporte metropolitano.
  4. **Horizonte do Essencial** (Chamada + 5 Episódios + Epílogo) — Hardware local e soberania digital.
  5. **Recolocação Java** (Index + 7 Episódios) — Carreiras e testes práticos de arquitetura.
  6. **Protocolo de Lucerna** (Index + 6 Episódios + Epílogo) — Crônicas de segurança e legado corporativo.
  7. **O Mito da Eficiência** (Index + 5 Episódios) — IA e limitações do silício.
  8. **A Ilusão Informatizada** (Index + 4 Episódios + Epílogo) — Crítica ao avanço tecnológico.
  9. **Brasil, SDK e Soberania** (Index + 7 Episódios) — Regulação e desenvolvimento de SDKs nacionais.
  10. **Depois do debate** (Index + 3 Episódios) — O futuro do programador na era dos LLMs.
  11. **Do Silício ao Chão de Fábrica** (Index + 8 Episódios) — Geopolítica física, soberania de dados híbrida e telemetria offline-first na economia real produtiva do país.
  12. **A Ilusão da Interface** (Index + 3 Episódios + 1 Apêndice) — Crítica geopolítica e social sobre o petrodólar, as panelinhas locais, a economia da atenção dos algoritmos e o desdobramento da linguagem de controle para leitores adultos e jovens.

---

## 📅 Regras de Publicação, Datas e Colisões

1. **Intervalo entre Publicações:** Mínimo de **10 dias** entre artigos da mesma série ou postagens subsequentes para espaçamento editorial.
2. **Restrição de Início de Mês:** **Proibido publicar artigos nos primeiros 5 dias de qualquer mês**. Esse período é reservado para redes sociais do autor.
3. **Página de Índice/Chamada:** Deve ser publicada exatamente **10 dias antes do Episódio 1** e conter a grade descritiva de todos os episódios programados.
4. **Isolamento de Linha do Tempo (Prevenção de Colisões):** Séries publicadas concorrentemente no mesmo mês devem rodar em dias diferentes da semana para evitar colisões físicas de imagens ou arquivos. A série *"Além do Hype"* foi deslocada de quartas para **quintas-feiras** para coexistir sem conflito com a série *"O Novo Tabuleiro do Mundo"*, que ocupa as quartas-feiras.

---

## 🖼️ Convenção de Imagens

Todas as imagens de destaque de artigos seguem o padrão registrado no [README de Imagens](docs/articles/assets/img/README.html):
* **Padrão de Nome:** `YYYY_MM_DD_IMAGE_NNN.png`
  * `YYYY_MM_DD` correspondendo exatamente à data no nome do arquivo HTML do artigo.
  * `NNN` = `001` para imagem de destaque/capa, `002+` para imagens complementares (ex: diagramas de arquitetura, mapas).
* **Proporção Física:** Sempre **16:9 (Landscape/Paisagem)**, tipicamente 1920×1080 px ou 1024×576 px.
* **Uso Semântico (Imagem Destaque):** As imagens principais no início de cada artigo devem ser declaradas utilizando a estrutura `<figure>` para garantir centralização:
  ```html
  <figure class="hero-image-frame">
      <img src="assets/img/YYYY_MM_DD_IMAGE_001.png" alt="[Descrição]" class="hero-image" />
      <figcaption class="hero-image-caption">[Legenda Centralizada]</figcaption>
  </figure>
  ```
* **Uso Semântico (Imagens Complementares/Diagramas):** Devem ser inseridas usando o container padrão nativo do blog (sem classes customizadas ad-hoc ou estilos CSS inline):
  ```html
  <div class="image-container">
      <img src="assets/img/YYYY_MM_DD_IMAGE_NNN.png" alt="[Descrição]" />
      <p class="image-caption">[Legenda em itálico]</p>
  </div>
  ```

---

## 🎨 Layout e Estrutura de Páginas HTML

1. **Rodapé de Página e Copyright:** Cada arquivo HTML de artigo ou chamada deve terminar com o bloco de direitos autorais perfeitamente contido na tag de rodapé do site (`site-footer`). O ano no copyright deve corresponder exatamente ao ano de publicação do arquivo (ex: `2026` ou `2027`):
  ```html
  <footer class="site-footer">
      <div class="container">
          <!-- Links de navegação anteriores/próximos se aplicável -->
          <p>&copy; 2027 Christian Mulato. Todos os direitos reservados.</p>
      </div>
  </footer>
  ```
2. **Quadros Verdes de Giz (Chalkboard):** Usados para tabelas ASCII, checklists de maturidade técnica, diagramas e glossários de termos. Deve ser construído com:
  ```html
  <div class="chalkboard">
      <!-- Tabelas, checklists, definições ou parágrafos com estilo emulado de giz -->
  </div>
  ```
3. **Glossários Técnicos Alfabetizados (A-Z):** O glossário localizado ao final de cada artigo dentro do `.chalkboard` deve ter seus termos organizados em **ordem alfabética estrita**.
4. **Contexto Histórico para Leis de Computação:** Leis fundamentais e metodologias citadas nos glossários (ex: leis de Amdahl, Conway, Gunther/USL, Brewer/CAP, Fowler/Strangler Fig) devem obrigatoriamente trazer seu contexto histórico com a autoria e data exata de criação (quem/quando/onde).
5. **Navegação Linear:** Cada episódio de uma série deve conter um gancho de transição e um link ativo no encerramento apontando para o próximo episódio. O episódio final (Epílogo) deve apontar de volta ao Índice da Série.

---

## ✍️ Tom Editorial e Assinatura

1. **Estilo Narrativo**: Tom sênior, sóbrio e técnico. Jargões de negócios modernos e siglas corporativas (como "cognitivo", "mindset", etc.) devem ser evitados no corpo principal, priorizando a adoção de termos clássicos e eruditos consagrados do português tradicional (ex: preferir "intelectivo", "intelectual" ou "mental"). Siglas e leis específicas devem ser isoladas estritamente na lousa de glossário ao final do artigo.
2. **Destaques e Ênfase no Texto**: Não use asteriscos de markdown (`**`) para aplicar negrito em arquivos HTML. Use sempre a tag HTML nativa clássica `<strong>`.
3. **Ironia e Mentoria (Ajuste de Rota 2027)**: O blog adota uma postura irônica e sarcástica em relação à tecnocracia, à burocracia do "teatro ágil" corporativo e à economia especulativa de fumaça (Faria Lima). Contudo, essa acidez deve ser direcionada apenas a níveis sistêmicos e estruturais. O relacionamento com novos desenvolvedores em início de carreira deve ser sempre de **mentoria e proteção**, blindando o time das armadilhas da pressa de mercado.
4. **Emojis**: É proibido o uso de emojis decorativos ou infantilizados nos títulos de cabeçalho, kichers, ou no corpo dos artigos para assegurar o tom maduro do blog.
5. **Assinatura do Autor**: Sempre inserida de forma padronizada no fechamento do artigo dentro da classe `post-footer`.
   * **Assinatura Técnica (Christian Mulato):** Usada para artigos práticos de engenharia, código e carreira:
     ```html
     <footer class="post-footer">
         <div class="author-info">
             <img src="assets/img/foto_chri.jpg" alt="Christian Mulato" class="author-avatar">
             <div class="author-details">
                 <strong>Christian Mulato</strong>
                 <p>Arquiteto de Software e Engenheiro de Sistemas</p>
             </div>
         </div>
     </footer>
     ```
   * **Assinatura Crítica/Geopolítica (Cidadão Global):** Usada para ensaios de realpolitik, crítica cultural, regulação de algoritmos e análises globais (como a série *"A Ilusão da Interface"*):
     ```html
     <footer class="post-footer">
         <div class="author-info">
             <img src="assets/img/foto_chri.jpg" alt="Cidadão Global" class="author-avatar">
             <div class="author-details">
                 <strong>Cidadão Global</strong>
             </div>
         </div>
     </footer>
     ```

---

## 🌐 Evitando Câmaras de Eco (Diretrizes de Evolução)

Para garantir que o blog continue crescendo de forma saudável e intelectualmente rica quando novos agentes ou modelos de IA colaborarem com ele:

1. **Evitar Regurgitação de Hypes:** Novos agentes não devem simplesmente repetir termos da moda ou discursos simplificados de senso comum sobre tecnologia, regulação ou política. Cada post deve buscar decodificar o *backend* (regras de incentivo econômico, física do hardware, infraestrutura de poder).
2. **Contraste de Visões:** Ao abordar temas complexos, o blog deve apresentar a justaposição de visões (como as perspectivas do Adulto e do Jovem, ou o embate entre o pragmatismo da engenharia física e as promessas da simulação digital).
3. **Maturidade Crítica vs. Niilismo:** Embora a acidez e o ceticismo com relação a lobbies e mercados especulativos sejam bem-vindos, a postura final deve ser sempre de incentivo ao estudo dos fundamentos e da soberania individual, e não de desesperança vazia.
4. **Respeito ao Legado:** Novos textos devem dialogar com o acervo existente, citando conceitos ou leis discutidas em posts e séries anteriores, criando uma teia lógica conectada em vez de pensamentos fragmentados.
