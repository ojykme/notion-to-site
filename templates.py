CSS_CONTENT = """@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
    /* 기존 변수 개선 및 추가 */
    --bg-color: #ffffff;
    --sidebar-bg: #fbfbfd;
    --text-primary: #1d1d1f;
    --text-secondary: #6e6e73;
    --accent-color: #0071e3;
    --accent-hover: #0077ed;
    --border-color: #e8e8ed;
    --callout-bg: #f5f5f7;
    --font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --sidebar-width: 280px;
    
    /* 추가된 디자인 시스템 */
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.12);
    --transition-fast: 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}

body {
    font-family: var(--font-family);
    line-height: 1.68;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    margin: 0;
    padding: 0;
    background-color: var(--bg-color);
    -webkit-font-smoothing: antialiased;
}

/* Layout */
.app-container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: var(--sidebar-width);
    background-color: var(--sidebar-bg);
    border-right: 1px solid var(--border-color);
    padding: 2.5rem 1.25rem;
    box-sizing: border-box;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.site-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 2rem;
    padding-left: 0.5rem;
    color: var(--text-primary);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Search Box Premium Upgrade */
.search-container {
    position: relative;
    margin-bottom: 2rem;
}
.search-input {
    width: 100%;
    padding: 0.7rem 1rem 0.7rem 2.4rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    background-color: #f5f5f7;
    box-sizing: border-box;
    outline: none;
    transition: all var(--transition-fast);
    font-family: var(--font-family);
}
.search-input:focus {
    border-color: var(--accent-color);
    background-color: #fff;
    box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
}
.search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.9rem;
    color: var(--text-secondary);
    pointer-events: none;
}
.search-results {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    z-index: 100;
    max-height: 320px;
    overflow-y: auto;
    display: none;
}
.search-results.active {
    display: block;
    animation: fadeIn 0.2s ease-out;
}
.search-result-item {
    padding: 0.9rem 1.2rem;
    border-bottom: 1px solid var(--border-color);
    text-decoration: none;
    display: block;
    color: var(--text-primary);
    transition: background-color var(--transition-fast);
}
.search-result-item:last-child {
    border-bottom: none;
}
.search-result-item:hover {
    background-color: rgba(0, 0, 0, 0.03);
}
.search-result-title {
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
}
.search-result-excerpt {
    font-size: 0.85rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Navigation & Sidebar Item Links */
.nav-links {
    list-style: none;
    padding: 0;
    margin: 0;
    flex-grow: 1;
}
.nav-links li {
    margin-bottom: 0.25rem;
}
.nav-links a {
    display: block;
    padding: 0.5rem 0.75rem;
    color: #424245;
    text-decoration: none;
    border-radius: var(--radius-sm);
    font-size: 0.92rem;
    font-weight: 500;
    transition: all var(--transition-fast);
}
.nav-links a:hover {
    background-color: rgba(0,0,0,0.04);
    color: var(--text-primary);
}
.nav-links a.active {
    background-color: var(--accent-color);
    color: #fff;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
}

/* GitBook Style Collapsible Folders */
details {
    margin-bottom: 0.25rem;
}
details summary {
    cursor: pointer;
    padding: 0.5rem 0.75rem;
    font-weight: 600;
    font-size: 0.92rem;
    color: var(--text-primary);
    border-radius: var(--radius-sm);
    user-select: none;
    transition: background-color var(--transition-fast);
    list-style: none; 
    display: flex;
    align-items: center;
}
details summary::-webkit-details-marker {
    display: none;
}
details summary:hover {
    background-color: rgba(0,0,0,0.04);
}
details summary::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-right: 2px solid var(--text-secondary);
    border-bottom: 2px solid var(--text-secondary);
    transform: rotate(-45deg);
    margin-right: 0.75rem;
    margin-left: 0.2rem;
    transition: transform var(--transition-fast) ease;
}
details[open] > summary::before {
    transform: rotate(45deg);
    margin-bottom: 2px;
}

ul.nested-nav {
    list-style: none;
    padding-left: 0.75rem;
    margin: 0.25rem 0 0.5rem 0.75rem;
    border-left: 1px dashed var(--border-color);
}

/* Main Content Area */
.main-content {
    flex-grow: 1;
    margin-left: var(--sidebar-width);
    padding: 5rem 4rem;
    box-sizing: border-box;
    background-color: var(--bg-color);
}
.no-sidebar .sidebar {
    display: none;
}
.no-sidebar .main-content {
    margin-left: 0;
}
.content-wrapper {
    max-width: 760px;
    margin: 0 auto;
    animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Typography & Markdown Elements */
h1 {
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 2.5rem;
    color: #000;
    line-height: 1.25;
}
h2 {
    font-size: 1.75rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-top: 3.5rem;
    margin-bottom: 1.2rem;
    color: #111;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.5rem;
}
h3 {
    font-size: 1.35rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    color: #222;
}
p {
    font-size: 1.05rem;
    color: #333336;
    margin-bottom: 1.6rem;
    word-break: keep-all;
}
a {
    color: var(--accent-color);
    text-decoration: none;
    font-weight: 500;
    border-bottom: 1px dashed transparent;
    transition: border-color var(--transition-fast);
}
a:hover {
    border-bottom-color: var(--accent-color);
}

/* Notion Style Callouts & Blockquotes */
aside {
    background-color: var(--callout-bg);
    border-left: 4px solid var(--text-secondary);
    border-radius: var(--radius-md);
    padding: 1.25rem 1.5rem;
    margin: 2rem 0;
}
aside h3 {
    margin-top: 0;
    font-size: 1.1rem;
}
aside p {
    font-size: 0.95rem;
    margin-bottom: 0;
}

.callout {
    border-left: 4px solid var(--accent-color);
    margin: 2rem 0;
    padding: 1rem 1.5rem;
    background-color: rgba(0, 113, 227, 0.04);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
.callout p {
    margin: 0;
    color: #0056b3;
    font-weight: 500;
    font-size: 1.02rem;
}

img {
    max-width: 100%;
    height: auto;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    margin: 2.5rem 0;
    display: block;
}

/* Elegant Table Design */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 2.5rem 0;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    overflow: hidden;
}
th, td {
    padding: 14px 18px;
    text-align: left;
    font-size: 0.95rem;
}
th {
    background-color: #f5f5f7;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border-color);
}
td {
    border-bottom: 1px solid var(--border-color);
    color: #333;
}
tr:last-child td {
    border-bottom: none;
}

/* Responsive */
@media (max-width: 960px) {
    .main-content {
        padding: 4rem 2rem;
    }
}
@media (max-width: 768px) {
    .app-container {
        flex-direction: column;
    }
    .sidebar {
        width: 100%;
        position: relative;
        height: auto;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
        padding: 1.5rem;
    }
    .main-content {
        margin-left: 0;
        padding: 3rem 1.5rem;
    }
    h1 { font-size: 2rem; }
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 플렉스지 사용자 가이드</title>
    <link rel="stylesheet" href="{css_path}style.css">
</head>
<body class="{body_class}">
    <div class="app-container">
        {sidebar_html}
        <!-- Main Content -->
        <main class="main-content">
            <div class="content-wrapper">
                {content}
            </div>
        </main>
    </div>

    <!-- Search Logic -->
    <script>
        const rootPath = '{css_path}';
        let searchData = [];

        // Fetch search index
        fetch(rootPath + 'search_index.json')
            .then(res => res.json())
            .then(data => {{
                searchData = data;
            }})
            .catch(err => console.error('Search index load error:', err));

        const searchInput = document.getElementById('search-input');
        const searchResults = document.getElementById('search-results');

        searchInput.addEventListener('input', (e) => {{
            const query = e.target.value.trim().toLowerCase();
            if (query.length < 1) {{
                searchResults.classList.remove('active');
                return;
            }}
            
            if (searchData.length > 0) {{
                // Vanilla JS Search
                const results = searchData.filter(item => {{
                    return item.title.toLowerCase().includes(query) || 
                           item.content.toLowerCase().includes(query);
                }});
                
                searchResults.innerHTML = '';
                
                if(results.length > 0) {{
                    results.slice(0, 8).forEach(item => {{
                        const a = document.createElement('a');
                        a.href = rootPath + item.url;
                        a.className = 'search-result-item';
                        
                        const contentLower = item.content.toLowerCase();
                        const matchIndex = contentLower.indexOf(query);
                        let excerpt = "";
                        
                        if (matchIndex !== -1) {{
                            const start = Math.max(0, matchIndex - 20);
                            const end = Math.min(item.content.length, matchIndex + query.length + 40);
                            excerpt = "..." + item.content.substring(start, end).replace(/\\n/g, ' ') + "...";
                            
                            // Highlight query
                            const regex = new RegExp(`(${{query}})`, 'gi');
                            excerpt = excerpt.replace(regex, '<strong style="color:var(--accent-color);">$1</strong>');
                        }} else {{
                            excerpt = item.content.substring(0, 60).replace(/\\n/g, ' ') + '...';
                        }}
                        
                        a.innerHTML = `
                            <div class="search-result-title">${{item.title}}</div>
                            <div class="search-result-excerpt">${{excerpt}}</div>
                        `;
                        searchResults.appendChild(a);
                    }});
                    searchResults.classList.add('active');
                }} else {{
                    searchResults.innerHTML = '<div class="search-result-item"><div class="search-result-title">결과가 없습니다.</div></div>';
                    searchResults.classList.add('active');
                }}
            }}
        }});

        // Close search results when clicking outside
        document.addEventListener('click', (e) => {{
            if (!e.target.closest('.search-container')) {{
                searchResults.classList.remove('active');
            }}
        }});
        
        // ESC 누르면 검색창 닫기
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                searchResults.classList.remove('active');
            }}
        }});
        
        // Restore folder open states from localStorage
        const openFolders = JSON.parse(localStorage.getItem('flexg_open_folders') || '[]');
        document.querySelectorAll('details[data-folder]').forEach(details => {{
            const folderId = details.getAttribute('data-folder');
            if (openFolders.includes(folderId)) {{
                details.setAttribute('open', '');
            }}
            
            // Listen for toggle to save state
            details.addEventListener('toggle', (e) => {{
                let currentOpen = JSON.parse(localStorage.getItem('flexg_open_folders') || '[]');
                if (details.open) {{
                    if (!currentOpen.includes(folderId)) currentOpen.push(folderId);
                }} else {{
                    currentOpen = currentOpen.filter(id => id !== folderId);
                }}
                localStorage.setItem('flexg_open_folders', JSON.stringify(currentOpen));
            }});
        }});

        // Automatically open the folder containing the active page
        document.querySelectorAll('.nav-links a.active').forEach(link => {{
            let parent = link.parentElement;
            while (parent && !parent.classList.contains('sidebar')) {{
                if (parent.tagName === 'DETAILS') {{
                    parent.setAttribute('open', '');
                    // Also save to localStorage so it stays open
                    const folderId = parent.getAttribute('data-folder');
                    let currentOpen = JSON.parse(localStorage.getItem('flexg_open_folders') || '[]');
                    if (folderId && !currentOpen.includes(folderId)) {{
                        currentOpen.push(folderId);
                        localStorage.setItem('flexg_open_folders', JSON.stringify(currentOpen));
                    }}
                }}
                parent = parent.parentElement;
            }}
        }});
    </script>
</body>
</html>
"""

SIDEBAR_TEMPLATE = """
        <!-- Sidebar / TOC -->
        <nav class="sidebar">
            <a href="{css_path}index.html" class="site-title">📚 가이드 문서</a>
            
            <div class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" id="search-input" class="search-input" placeholder="문서 검색...">
                <div id="search-results" class="search-results"></div>
            </div>

            <ul class="nav-links">
                {toc_html}
            </ul>
        </nav>
"""
