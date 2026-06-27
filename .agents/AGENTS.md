# Christian Mulato Dev Blog - Memory & Guidelines for AI Agents

Este documento serve para contextualizar qualquer agente ou modelo de IA sobre a estrutura, convenções de estilo e regras de publicação do blog pessoal de Christian Mulato.

---

## 📂 Visão Geral do Projeto

* **Workspace Root:** `D:/onedrive/dev/caracore-personal`
* **Diretório de Distribuição (Github Pages):** `docs/`
* **Artigos e Séries:** `docs/articles/`
* **Assets de Imagem:** `docs/articles/assets/img/`
* **Estilos CSS:** `docs/articles/assets/css/` (arquivos `main.css`, `article.css`, `highlight.css`)

---

## Status Atual (Ciclo Ativo: jun/2026 a mai/2029)

* **Total de Artigos Publicados:** 179 artigos
* **Total de Séries com Índice Próprio:** 10 séries
* **Período do Acervo:** março de 2024 a junho de 2027 (datas futuras em 2027 são usadas para agendamento de séries editoriais)

---

## 📅 Regras de Publicação e Datas

1. **Intervalo entre Publicações:** Mínimo de **10 dias** entre artigos da mesma série ou postagens subsequentes para espaçamento editorial.
2. **Restrição de Início de Mês:** **Proibido publicar artigos nos primeiros 5 dias de qualquer mês**. Esse período é reservado exclusivamente para publicações no LinkedIn do autor.
3. **Página de Índice/Chamada:** Deve ser publicada exatamente **10 dias antes do Episódio 1** e conter resenhas ou descrições detalhadas de todos os episódios programados.
4. **Alinhamento Cronológico:** Todas as novas postagens devem ser cadastradas em ordem cronológica inversa (mais recentes primeiro) no grid de `docs/index.html` e no RSS Feed em `docs/feed.xml`.

---

## 🖼️ Convenção de Nomenclatura e Formato de Imagens

Todas as imagens de destaque de artigos seguem o padrão registrado no [README de Imagens](file:///D:/onedrive/dev/caracore-personal/docs/articles/assets/img/README.html):
* **Padrão de Nome:** `YYYY_MM_DD_IMAGE_NNN.png`
  * `YYYY_MM_DD` correspondendo exatamente à data no nome do arquivo HTML do artigo.
  * `NNN` = `001` para imagem de destaque/capa, `002+` para imagens complementares.
* **Proporção Física:** Sempre **16:9 (Landscape/Paisagem)**, tipicamente 1920×1080 px ou 1024×576 px.
* **Uso Semântico:** As imagens principais no início de cada artigo devem ser declaradas utilizando a estrutura `<figure>` para garantir centralização:
  ```html
  <figure class="hero-image-frame">
      <img src="assets/img/YYYY_MM_DD_IMAGE_001.png" alt="[Descrição]" class="hero-image" />
      <figcaption class="hero-image-caption">[Legenda Centralizada]</figcaption>
  </figure>
  ```

---

## 🎨 Identidade Visual e Estilo de Layout

1. **Tipografia:** Fonte principal `Inter` para leitura, `Fira Code` para blocos de código e dados técnicos.
2. **Suporte Dark/Light:** O blog possui um botão de alternância de tema global (`#themeToggle`). Todos os elementos de estilo customizados devem respeitar as variáveis de cores claras/escuras definidas em [article.css](file:///D:/onedrive/dev/caracore-personal/docs/articles/assets/css/article.css).
3. **Quadro Verde de Giz (Chalkboard):** Usado para glossários técnicos, termos complexos, tabelas ASCII ou citações de destaque. Deve ser construído com:
  ```html
  <div class="chalkboard">
      <!-- Tabelas, definições (<dl>/<dt>/<dd>) ou parágrafos com estilo emulado de giz -->
  </div>
  ```
4. **Encadeamento Linear:** Cada episódio de uma série deve conter um gancho de transição e um link ativo (`<a>`) na última linha apontando para o próximo episódio da série.
