================================================================================
ARTIGOS NOVOS — CSS, JS E IMAGENS (pasta assets)
================================================================================
Raiz: docs/articles/assets/

Regra: todo artigo novo em docs/articles/*.html referencia apenas artefactos
nesta árvore, com caminhos relativos ao ficheiro HTML (nunca URLs absolutas
locais para ficheiros fora de assets/).

  assets/css/     Folhas de estilo partilhadas ou por tema
  assets/js/      Scripts partilhados (tema, artigo)
  assets/img/     Imagens do blog (hero, corpo, favicon partilhado)

LIGAÇÕES TÍPICAS NO <head> E NO FIM DO <body>
---------------------------------------------
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/article.css">
  <link rel="stylesheet" href="assets/css/highlight.css">   <!-- se código -->
  <meta property="og:image" content="assets/img/YYYY_MM_DD_IMAGE_001.png">

  <script src="assets/js/main.js"></script>
  <script src="assets/js/article.js"></script>

CSS NOVO
--------
- Preferir estender assets/css/article.css ou main.css quando for poucas
  regras reutilizáveis (ex.: classes de série, componentes de diagrama).
- Se o artigo precisar de muita folha própria, criar um ficheiro em
  assets/css/ com nome estável (ex.: serie-foo.css) e ligá-lo só nos HTML
  que precisarem — não deixar CSS solto ao lado do .html do artigo.

JS NOVO
-------
- Colocar em assets/js/ e referenciar com href/src relativos como acima.
- Evitar blocos grandes de <script> inline; exceções mínimas (ex.: dados
  embutidos) devem ser mesmo exceção.

IMAGENS
-------
- Sempre em assets/img/. Convenções de nomes e séries: ver img/README.txt

VALIDAÇÃO
---------
- tools/validate_article_images.ps1 (imagens vs nomes dos HTML)

================================================================================
