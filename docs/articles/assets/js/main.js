// Main.js - Funcionalidades para a página principal do blog
// Christian Mulato Dev Blog - Sistema de Temas Dark/Light

document.addEventListener('DOMContentLoaded', function() {
    
    // Classe para gerenciar o tema
    class ThemeManager {
        constructor() {
            this.themeToggle = document.getElementById('themeToggle');
            this.themeIcon = document.getElementById('themeIcon');
            this.init();
        }
        
        init() {
            // Detecta tema salvo ou preferência do sistema
            const savedTheme = localStorage.getItem('theme');
            const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            const currentTheme = savedTheme || systemTheme;
            
            this.setTheme(currentTheme);
            this.updateIcon(currentTheme);
            
            // Event listeners
            if (this.themeToggle) {
                this.themeToggle.addEventListener('click', () => this.toggleTheme());
            }
            
            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!localStorage.getItem('theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                    this.updateIcon(e.matches ? 'dark' : 'light');
                }
            });
        }
        
        toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            this.setTheme(newTheme);
            this.updateIcon(newTheme);
            localStorage.setItem('theme', newTheme);
        }
        
        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
        }
        
        updateIcon(theme) {
            if (this.themeIcon) {
                this.themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
            }
            if (this.themeToggle) {
                this.themeToggle.setAttribute('aria-label', 
                    theme === 'light' ? 'Ativar tema escuro' : 'Ativar tema claro');
            }
        }
    }
    
    // Filtros de artigos
    function initializeFilters() {
        // Utilitário para gerar slugs sem acentos/símbolos
        const slugify = (str) => {
            if (!str) return '';
            return str
                .toString()
                .toLowerCase()
                .normalize('NFD')
                .replace(/\p{Diacritic}+/gu, '') // remove acentos
                .replace(/&/g, ' e ')
                .replace(/[^a-z0-9\s-]/g, '')
                .trim()
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-');
        };
        const categoryFilter = document.getElementById('categoryFilter');
        const searchInput = document.getElementById('searchInput');
        const articles = document.querySelectorAll('.article-card');
        
        // Filtro por categoria
        if (categoryFilter) {
            categoryFilter.addEventListener('change', function() {
                const selectedCategory = slugify(this.value);
                filterArticles(selectedCategory, searchInput ? searchInput.value.toLowerCase() : '');
            });
        }
        
        // Busca por texto
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                const selectedCategory = categoryFilter ? slugify(categoryFilter.value) : '';
                filterArticles(selectedCategory, searchTerm);
            });
        }
        
        function filterArticles(category, searchTerm) {
            articles.forEach(article => {
                const categoryEl = article.querySelector('.category');
                const articleCategory = categoryEl ? categoryEl.textContent.toLowerCase() : '';
                const articleSlug = article.dataset.categorySlug || slugify(articleCategory);
                const titleElement = article.querySelector('.article-title');
                const descriptionElement = article.querySelector('.article-description');
                const articleTitle = titleElement ? titleElement.textContent.toLowerCase() : '';
                const articleDescription = descriptionElement ? descriptionElement.textContent.toLowerCase() : '';
                
                const matchesCategory = !category || category === 'todas' || articleSlug.includes(category);
                const matchesSearch = !searchTerm || 
                    articleTitle.includes(searchTerm) || 
                    articleDescription.includes(searchTerm);
                
                if (matchesCategory && matchesSearch) {
                    article.style.display = 'block';
                    article.style.animation = 'fadeIn 0.3s ease-in-out';
                } else {
                    article.style.display = 'none';
                }
            });
            
            // Mostrar/ocultar seções vazias
            document.querySelectorAll('.month-section').forEach(section => {
                const visibleArticles = [...section.querySelectorAll('.article-card')]
                    .filter(article => article.style.display !== 'none');
                section.style.display = visibleArticles.length ? 'block' : 'none';
            });

            document.querySelectorAll('.featured-grid, .showcase-grid').forEach(section => {
                const visibleArticles = [...section.querySelectorAll('.article-card')]
                    .filter(article => article.style.display !== 'none');
                section.closest('.editorial-section').style.display = visibleArticles.length ? '' : 'none';
            });
        }

        document.querySelectorAll('[data-series-filter]').forEach(button => {
            button.addEventListener('click', () => {
                if (categoryFilter) {
                    categoryFilter.value = button.dataset.seriesFilter;
                    categoryFilter.dispatchEvent(new Event('change'));
                }
                document.querySelector('#arquivo').scrollIntoView({ behavior: 'smooth' });
            });
        });
    }

    function initializeEditorialCards() {
        const archive = document.querySelector('#arquivo');
        if (!archive) return;
        const sourceCards = [...archive.querySelectorAll('.article-card')];
        const coverFallbacks = {
            '2026_02_15': '2026_02_22_IMAGE_001',
            '2026_04_20': '2026_05_05_IMAGE_001',
            '2026_06_05': '2026_08_05_IMAGE_002',
            '2026_06_15': '2026_08_05_IMAGE_001',
            '2026_08_25': '2026_09_05_IMAGE_001',
            '2026_12_15': '2026_12_22_IMAGE_001',
            '2027_07_30': '2027_08_05_IMAGE_001'
        };
        const seriesClasses = [
            'economia-programavel',
            'horizonte-essencial',
            'rpa-silicio',
            'alem-hype',
            'blindagem',
            'lucerna'
        ];
        const attachCoverFallback = (cover, card) => {
            cover.addEventListener('error', function handleCoverError() {
                if (cover.dataset.fallback !== 'used') {
                    cover.dataset.fallback = 'used';
                    cover.src = cover.src.replace(/\.webp$/, '.png');
                    return;
                }
                cover.removeEventListener('error', handleCoverError);
                cover.remove();
                card.classList.add('article-card--no-cover');
            });
        };

        const prepareCard = (card) => {
            const articleLink = card.querySelector('.article-title a');
            const category = card.querySelector('.category');
            const categorySlug = card.dataset.categorySlug || '';
            const dateMatch = articleLink && articleLink.getAttribute('href').match(/(\d{4}_\d{2}_\d{2})/);

            seriesClasses.forEach(series => {
                if (categorySlug.includes(series)) card.classList.add(`series-${series}`);
            });

            if (!articleLink || !dateMatch || card.querySelector('.article-cover')) return;

            const title = articleLink.textContent.trim();
            const cover = document.createElement('img');
            cover.className = 'article-cover';
            const coverFile = coverFallbacks[dateMatch[1]] || `${dateMatch[1]}_IMAGE_001`;
            cover.src = `articles/assets/img/${coverFile}.webp`;
            cover.alt = title;
            cover.loading = 'lazy';
            cover.decoding = 'async';
            cover.width = 960;
            cover.height = 540;
            const coverFrame = document.createElement('div');
            coverFrame.className = 'article-cover-frame';
            coverFrame.appendChild(cover);
            const articleMeta = card.querySelector('.article-meta');
            if (articleMeta) coverFrame.appendChild(articleMeta);
            attachCoverFallback(cover, card);
            card.prepend(coverFrame);

            if (category) category.title = category.textContent.trim();
        };

        const featuredGrid = document.querySelector('#featuredGrid');
        const latestGrid = document.querySelector('#latestGrid');
        const popularGrid = document.querySelector('#popularGrid');
        const cloneCards = (target, cards, className) => {
            cards.forEach((card, index) => {
                prepareCard(card);
                const clone = card.cloneNode(true);
                clone.classList.add(className);
                const cloneCover = clone.querySelector('.article-cover');
                if (cloneCover) attachCoverFallback(cloneCover, clone);
                if (index === 0) {
                    clone.classList.add('is-leading');
                    const leadingCover = clone.querySelector('.article-cover');
                    if (className === 'featured-card' && leadingCover) {
                        leadingCover.loading = 'eager';
                        leadingCover.fetchPriority = 'high';
                    }
                }
                target.appendChild(clone);
            });
        };

        const publicationDate = (card) => {
            const link = card.querySelector('.article-title a');
            const match = link && link.getAttribute('href').match(/(\d{4})_(\d{2})_(\d{2})/);
            return match ? `${match[1]}-${match[2]}-${match[3]}` : null;
        };
        const todayParts = new Intl.DateTimeFormat('en-CA', {
            timeZone: 'America/Sao_Paulo',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        }).formatToParts(new Date());
        const datePart = (type) => todayParts.find(part => part.type === type).value;
        const today = `${datePart('year')}-${datePart('month')}-${datePart('day')}`;
        const publishedCards = sourceCards
            .filter(card => publicationDate(card) && publicationDate(card) <= today)
            .sort((a, b) => publicationDate(b).localeCompare(publicationDate(a)));

        cloneCards(featuredGrid, publishedCards.slice(0, 3), 'featured-card');
        cloneCards(latestGrid, publishedCards.slice(0, 6), 'latest-card');

        const editorialSeries = ['horizonte-essencial', 'rpa-silicio', 'alem-hype'];
        const popularCards = editorialSeries
            .map(series => sourceCards.find(card => (card.dataset.categorySlug || '').includes(series))
                || sourceCards.find(card => card.classList.contains(`series-${series}`)))
            .filter(Boolean);
        cloneCards(popularGrid, popularCards, 'popular-card');

        let nextCard = 0;
        const prepareArchiveBatch = () => {
            sourceCards.slice(nextCard, nextCard + 12).forEach(prepareCard);
            nextCard += 12;
            if (nextCard < sourceCards.length) setTimeout(prepareArchiveBatch, 16);
        };
        setTimeout(prepareArchiveBatch, 0);
    }
    
    // Smooth scroll para navegação interna
    function initializeSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Estatísticas dinâmicas
    function updateStats() {
        const totalArticles = document.querySelectorAll('#arquivo .article-card').length;
        const statElement = document.querySelector('.stat');
        if (statElement) {
            statElement.textContent = `${totalArticles} artigos no acervo`;
        }
    }
    
    // Inicializar tudo
    new ThemeManager();
    initializeEditorialCards();
    initializeFilters();
    initializeSmoothScroll();
    updateStats();
    
    const articleCount = document.querySelectorAll('#arquivo .article-card').length;
    if (articleCount > 0) {
        console.log('🚀 Main.js carregado com sucesso!');
        console.log(`📊 Artigos carregados: ${articleCount}`);
    }
});

// Adicionar estilos para animações
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .article-card {
        transition: all 0.3s ease;
    }
    
`;
document.head.appendChild(style);

if (window.location.protocol !== 'file:' &&
    ['personal.caracore.com.br', 'www.caracore.com.br', 'caracore.com.br'].indexOf(window.location.hostname) !== -1 &&
    !document.querySelector('script[data-caracore-ga4]')) {
    const analyticsScript = document.createElement('script');
    analyticsScript.src = new URL('analytics.js', document.currentScript.src).href;
    document.head.appendChild(analyticsScript);
}
