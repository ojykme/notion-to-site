import os
import re
import json
import shutil
import urllib.parse
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import sys
from templates import CSS_CONTENT, HTML_TEMPLATE, SIDEBAR_TEMPLATE

# 기본 설정
SOURCE_DIR = Path('notion')

# 파라미터 파싱
DEST_DIR_STR = 'web'
WITH_MENU = True

if '--no-menu' in sys.argv:
    WITH_MENU = False
    
for i, arg in enumerate(sys.argv):
    if arg == '--out' and i + 1 < len(sys.argv):
        DEST_DIR_STR = sys.argv[i+1]

DEST_DIR = Path(DEST_DIR_STR)

# 향후 S3/CDN 연동 시 이 값을 'https://cdn.example.com/' 등으로 변경하면 됩니다.
# 빈 문자열이면 로컬 상대 경로를 사용합니다.
BASE_DOMAIN = '' 

def remove_uuid_from_name(name):
    # 노션 UUID 제거
    name_without_ext, ext = os.path.splitext(name)
    cleaned_name = re.sub(r' [a-fA-F0-9]{32}$', '', name_without_ext)
    return cleaned_name + ext

def get_target_html_name(cleaned_md_name):
    """특정 마크다운 파일명을 index.html 등 원하는 이름으로 매핑합니다."""
    if cleaned_md_name == '플렉스지 사용자 가이드.md':
        return 'index.html'
    return cleaned_md_name[:-3] + '.html'

def extract_text_for_search(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def process_html_content(html_content, relative_depth=0):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. a 태그 (링크) 수정
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http://') or href.startswith('https://') or href.startswith('mailto:'):
            continue
        
        decoded_href = urllib.parse.unquote(href)
        cleaned_href = remove_uuid_from_name(decoded_href)
        
        # 파일명 매핑 (플렉스지 사용자 가이드.md -> index.html)
        if cleaned_href.endswith('.md'):
            # 경로가 포함되어 있을 수 있으므로 파일명만 추출해서 변환 확인
            parts = cleaned_href.split('/')
            parts[-1] = get_target_html_name(parts[-1])
            cleaned_href = '/'.join(parts)
        
        a['href'] = urllib.parse.quote(cleaned_href)

    # 2. img 태그 (이미지) 수정
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith('http://') or src.startswith('https://') or src.startswith('data:'):
            continue
            
        decoded_src = urllib.parse.unquote(src)
        cleaned_src = remove_uuid_from_name(decoded_src)
        
        if BASE_DOMAIN:
            img['src'] = f"{BASE_DOMAIN.rstrip('/')}/{urllib.parse.quote(cleaned_src)}"
        else:
            img['src'] = urllib.parse.quote(cleaned_src)
            
    return str(soup)

def build_toc_tree(md_files_info):
    tree = {'files': [], 'children': {}}
    for info in md_files_info:
        parts = info['dest_dir'].parts
        
        current = tree
        for part in parts:
            if not part:
                continue
            if part not in current['children']:
                current['children'][part] = {'files': [], 'children': {}}
            current = current['children'][part]
        current['files'].append(info)
    return tree

def render_toc_tree(node, current_url_path=""):
    html = ""
    # Render files in current level
    # Sort files: index.html first, then alphabetically
    files = sorted(node['files'], key=lambda x: (0 if x['target_html_name'] == 'index.html' else 1, x['title']))
    
    for info in files:
        active_class = ' class="active"' if info['url_path'] == current_url_path else ''
        html += f'<li><a href="{{css_path}}{info["url_path"]}"{active_class}>{info["title"]}</a></li>\n'
        
    # Render children (folders)
    for folder_name in sorted(node['children'].keys()):
        child_node = node['children'][folder_name]
        
        html += f'<li>\n'
        html += f'<details open>\n'
        html += f'<summary>{folder_name}</summary>\n'
        html += f'<ul class="nested-nav">\n'
        html += render_toc_tree(child_node, current_url_path)
        html += f'</ul>\n'
        html += f'</details>\n'
        html += f'</li>\n'
        
    return html

def build():
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True)
    
    with open(DEST_DIR / 'style.css', 'w', encoding='utf-8') as f:
        f.write(CSS_CONTENT)

    # Pass 1: 모든 마크다운 파일을 수집하여 목차(TOC)와 검색 인덱스 준비
    md_files_info = []
    search_index = []
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        rel_root = Path(root).relative_to(SOURCE_DIR)
        clean_rel_parts = [remove_uuid_from_name(part) for part in rel_root.parts]
        clean_rel_root = Path(*clean_rel_parts)
        
        for file in files:
            source_file = Path(root) / file
            cleaned_file_name = remove_uuid_from_name(file)
            
            if file.endswith('.md'):
                target_html_name = get_target_html_name(cleaned_file_name)
                dest_url_path = (clean_rel_root / target_html_name).as_posix()
                
                # 파일 읽기 및 마크다운 파싱 (검색 인덱스용)
                with open(source_file, 'r', encoding='utf-8') as f:
                    md_text = f.read()
                
                html_snippet = markdown.markdown(
                    md_text.replace('<aside>', '<aside markdown="1">'), 
                    extensions=['tables', 'fenced_code', 'nl2br', 'md_in_html']
                )
                
                plain_text = extract_text_for_search(html_snippet)
                title = cleaned_file_name[:-3]
                
                search_index.append({
                    "title": title,
                    "url": dest_url_path,
                    "content": plain_text
                })
                
                md_files_info.append({
                    "source": source_file,
                    "title": title,
                    "dest_dir": clean_rel_root,
                    "target_html_name": target_html_name,
                    "html_snippet": html_snippet,
                    "url_path": dest_url_path
                })
    
    # search_index.json 생성
    with open(DEST_DIR / 'search_index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

    # Pass 2: HTML 파일 생성 및 에셋 복사
    for root, dirs, files in os.walk(SOURCE_DIR):
        rel_root = Path(root).relative_to(SOURCE_DIR)
        clean_rel_parts = [remove_uuid_from_name(part) for part in rel_root.parts]
        clean_rel_root = Path(*clean_rel_parts)
        
        current_dest_dir = DEST_DIR / clean_rel_root
        current_dest_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            if not file.endswith('.md'):
                source_file = Path(root) / file
                cleaned_file_name = remove_uuid_from_name(file)
                shutil.copy2(source_file, current_dest_dir / cleaned_file_name)

    # TOC (목차) Tree 생성
    toc_tree = build_toc_tree(md_files_info)

    # HTML 렌더링
    for info in md_files_info:
        relative_depth = len(info['dest_dir'].parts)
        if relative_depth > 0 and info['dest_dir'].parts[0] == '':
            relative_depth = 0
            
        css_path = '../' * relative_depth if not BASE_DOMAIN else BASE_DOMAIN
        if BASE_DOMAIN and not BASE_DOMAIN.endswith('/'):
            css_path += '/'
            
        processed_html_snippet = process_html_content(info['html_snippet'], relative_depth)
        
        # 현재 파일에 해당하는 TOC 렌더링 (자신을 active로 표시)
        current_toc_html = render_toc_tree(toc_tree, info['url_path']) if WITH_MENU else ""
        
        sidebar_html = SIDEBAR_TEMPLATE.format(
            css_path=css_path, 
            toc_html=current_toc_html.replace('{css_path}', css_path)
        ) if WITH_MENU else ""
        
        body_class = "" if WITH_MENU else "no-sidebar"
        
        final_html = HTML_TEMPLATE.format(
            title=info['title'],
            content=processed_html_snippet,
            sidebar_html=sidebar_html,
            body_class=body_class,
            css_path=css_path
        )
        
        dest_file = DEST_DIR / info['dest_dir'] / info['target_html_name']
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Converted: {dest_file}")

if __name__ == '__main__':
    build()
    print("웹사이트 생성 완료!")
