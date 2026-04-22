# -*- coding: utf-8 -*-
"""
3D Wikipedia Knowledge Explorer - Backend API + Frontend
Single FastAPI server that serves both the API and static files
"""

import sys
import io
import os
import re

# Force UTF-8 encoding for stdout/stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Set
from urllib.parse import unquote
from collections import deque
import uvicorn

# Import libzim
import libzim
from bs4 import BeautifulSoup
import zhconv


def to_simplified(text: str) -> str:
    """Convert Traditional Chinese to Simplified Chinese"""
    if not text:
        return text
    return zhconv.convert(text, 'zh-cn')

# Directory where this script lives
# When running as PyInstaller bundle, use _MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global archive instance
archive: Optional[libzim.Archive] = None

app = FastAPI(title="3D Wiki Explorer API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ArticleNode(BaseModel):
    title: str
    titleEncoded: str
    path: str
    is_redirect: bool


class KnowledgeGraph(BaseModel):
    root: ArticleNode
    nodes: List[ArticleNode]
    edges: List[tuple]  # (from_idx, to_idx)


def init_archive(zim_path: str):
    global archive
    print(f"Loading ZIM archive: {zim_path}")
    archive = libzim.Archive(zim_path)
    print(f"Loaded! Entry count: {archive.entry_count}")


def get_article_title(entry) -> str:
    """Extract decoded title from entry"""
    title = entry.title
    # Handle URL encoding
    if '%' in title:
        title = unquote(title)
    return title


def extract_links(content: bytes) -> Set[str]:
    """Extract internal Wikipedia links from article content"""
    soup = BeautifulSoup(content, 'html.parser')
    links = set()
    
    for a in soup.find_all('a', href=True):
        href = a.get('href', '')
        # Skip external, anchors, scripts
        if not href.startswith(('http', '#', './', 'javascript:')):
            decoded = unquote(href)
            # Skip special pages
            if ':' not in decoded and not decoded.startswith('-'):
                links.add(decoded)
    
    return links


def get_article_content(title: str) -> Optional[bytes]:
    """Get article content by title"""
    if not archive:
        return None
    
    try:
        entry = archive.get_entry_by_title(title)
        if entry.is_redirect:
            entry = entry.get_redirect_entry()
        
        item = entry.get_item()
        return bytes(item.content)
    except Exception as e:
        print(f"Error getting article {title}: {e}")
        return None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main index.html page"""
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-cache"})


@app.get("/three.min.js")
async def serve_threejs():
    return FileResponse(os.path.join(BASE_DIR, "three.min.js"), media_type="application/javascript", headers={"Cache-Control": "no-cache"})


@app.get("/OrbitControls.js")
async def serve_orbitcontrols():
    return FileResponse(os.path.join(BASE_DIR, "OrbitControls.js"), media_type="application/javascript", headers={"Cache-Control": "no-cache"})


@app.get("/api/status")
async def api_status():
    return {"message": "3D Wiki Explorer API", "status": "running"}


@app.get("/archive-info")
async def get_archive_info():
    """Get basic archive information"""
    if not archive:
        raise HTTPException(status_code=500, detail="Archive not loaded")
    
    return {
        "title": archive.get_metadata('Title'),
        "date": archive.get_metadata('Date'),
        "language": archive.get_metadata('Language'),
        "entry_count": archive.entry_count,
        "article_count": archive.article_count,
    }


@app.post("/search")
async def search_articles(body: dict):
    """Search articles by title prefix"""
    if not archive:
        raise HTTPException(status_code=500, detail="Archive not loaded")
    
    query = body.get('query', '')
    limit = body.get('limit', 20)
    
    results = []
    visited = set()
    
    # Start from main entry and traverse
    try:
        # Try exact match first
        if archive.has_entry_by_title(query):
            entry = archive.get_entry_by_title(query)
            results.append({
                "title": to_simplified(get_article_title(entry)),
                "titleEncoded": entry.title,
            })
            visited.add(entry.title)
    except:
        pass
    
    # BFS search through entries (limited)
    # This is a simplified search - in production would use title index
    max_check = 10000
    checked = 0
    
    try:
        # Try random entries as starting points
        for _ in range(min(50, archive.article_count // 100)):
            try:
                entry = archive.get_random_entry()
                if entry.title not in visited and not entry.is_redirect:
                    title = get_article_title(entry)
                    if query.lower() in title.lower():
                        results.append({
                            "title": to_simplified(title),
                            "titleEncoded": entry.title,
                        })
                        visited.add(entry.title)
                        if len(results) >= limit:
                            break
            except:
                pass
    except Exception as e:
        print(f"Search error: {e}")
    
    return {"results": results[:limit], "query": query}


@app.post("/explore")
async def explore_article(body: dict):
    """
    Explore an article and build a knowledge graph
    depth: how many levels of links to follow
    max_nodes: maximum number of nodes to include
    """
    title = body.get('title', '')
    depth = body.get('depth', 1)
    max_nodes = body.get('max_nodes', 50)
    
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if not archive:
        raise HTTPException(status_code=500, detail="Archive not loaded")
    
    nodes = []
    edges = []
    node_map = {}
    
    # Add root node
    try:
        entry = archive.get_entry_by_title(title)
        if entry.is_redirect:
            entry = entry.get_redirect_entry()
        
        root_title = get_article_title(entry)
        root_encoded = entry.title
        root_path = entry.path
        
        root_idx = 0
        nodes.append({
            "title": to_simplified(root_title),
            "titleEncoded": root_encoded,
            "path": root_path,
            "is_redirect": False,
            "depth": 0
        })
        node_map[root_encoded] = 0
        
        # BFS to build graph
        queue = deque([(root_encoded, depth)])
        visited = {root_encoded}
        
        while queue and len(nodes) < max_nodes:
            current_encoded, current_depth = queue.popleft()
            
            if current_depth <= 0:
                continue
            
            try:
                entry = archive.get_entry_by_title(current_encoded)
                if entry.is_redirect:
                    entry = entry.get_redirect_entry()
                
                content = get_article_content(get_article_title(entry))
                if content:
                    links = extract_links(content)
                    
                    for link in links:
                        if link in visited or len(nodes) >= max_nodes:
                            continue
                        
                        visited.add(link)
                        
                        # Check if linked article exists
                        if not archive.has_entry_by_title(link):
                            continue
                        
                        link_entry = archive.get_entry_by_title(link)
                        
                        # Add node
                        idx = len(nodes)
                        nodes.append({
                            "title": to_simplified(get_article_title(link_entry)),
                            "titleEncoded": link_entry.title,
                            "path": link_entry.path,
                            "is_redirect": link_entry.is_redirect,
                            "depth": depth - current_depth + 1
                        })
                        node_map[link] = idx
                        
                        # Add edge
                        edges.append([node_map[current_encoded], idx])
                        
                        # Queue for next level
                        if current_depth > 1:
                            queue.append((link, current_depth - 1))
                
            except Exception as e:
                print(f"Error exploring {current_encoded}: {e}")
                continue
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Article not found: {e}")
    
    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }


@app.post("/thumbnails")
async def get_thumbnails(body: dict):
    """Batch fetch first-image thumbnails for a list of article titles."""
    titles = body.get('titles', [])
    if not titles or not archive:
        return {"thumbnails": {}}
    
    result = {}
    for title in titles[:20]:  # Cap at 20 to avoid slowness
        try:
            content = get_article_content(title)
            if not content:
                continue
            soup = BeautifulSoup(content, 'html.parser')
            content_div = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'class': 'mw-parser-output'})
            if not content_div:
                continue
            for img in content_div.find_all('img'):
                src = img.get('src', '')
                if not src or src.startswith('http'):
                    continue
                w = int(img.get('data-file-width', img.get('width', '0')) or '0')
                h = int(img.get('data-file-height', img.get('height', '0')) or '0')
                if w < 80 or h < 80:
                    continue
                if '.svg' in src.lower():
                    continue
                norm_src = src.lstrip('./')
                result[title] = f"/image?path={norm_src}"
                break  # First suitable image only
        except Exception:
            continue
    
    return {"thumbnails": result}


@app.get("/image")
async def serve_image(path: str = ""):
    """Serve an image from the ZIM archive by its path"""
    if not archive:
        raise HTTPException(status_code=500, detail="Archive not loaded")
    
    if not path:
        raise HTTPException(status_code=400, detail="Path is required")
    
    # Normalize path - remove leading ./ if present
    norm_path = path.lstrip('./')
    
    try:
        if not archive.has_entry_by_path(norm_path):
            # Try with ./ prefix
            if not archive.has_entry_by_path('./' + norm_path):
                raise HTTPException(status_code=404, detail=f"Image not found: {norm_path}")
            norm_path = './' + norm_path
        
        entry = archive.get_entry_by_path(norm_path)
        item = entry.get_item()
        img_content = bytes(item.content)
        
        # Determine content type from extension
        ext = norm_path.rsplit('.', 1)[-1].lower() if '.' in norm_path else ''
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'svg': 'image/svg+xml',
            'webp': 'image/webp',
            'ico': 'image/x-icon',
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        
        from fastapi.responses import Response
        return Response(
            content=img_content,
            media_type=content_type,
            headers={"Cache-Control": "public, max-age=86400"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Image error: {e}")


@app.post("/article-content")
async def get_content(body: dict):
    """Get article content with summary and related links"""
    title = body.get('title', '')
    
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if not archive:
        raise HTTPException(status_code=500, detail="Archive not loaded")
    
    try:
        entry = archive.get_entry_by_title(title)
        if entry.is_redirect:
            entry = entry.get_redirect_entry()
        
        item = entry.get_item()
        content = bytes(item.content)
        
        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove non-content elements
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'table', 'sup']):
            tag.decompose()
        
        title_text = to_simplified(get_article_title(entry))
        
        # Extract main content
        content_div = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'class': 'mw-parser-output'})
        
        # Extract first significant image (skip tiny icons/spacers)
        image_url = None
        all_images = []
        if content_div:
            for img in content_div.find_all('img'):
                src = img.get('src', '')
                if not src or src.startswith('http'):
                    continue
                width = int(img.get('data-file-width', img.get('width', '0')) or '0')
                height = int(img.get('data-file-height', img.get('height', '0')) or '0')
                # Skip tiny images (icons, spacers)
                if width < 80 or height < 80:
                    continue
                # Skip SVG icons (usually small UI elements)
                is_svg = '.svg' in src.lower()
                # Normalize path for our /image endpoint
                norm_src = src.lstrip('./')
                area = width * height
                img_entry = {
                    "url": f"/image?path={norm_src}",
                    "width": width,
                    "height": height,
                    "alt": img.get('alt', ''),
                    "area": area,
                    "is_svg": is_svg,
                }
                all_images.append(img_entry)
            
            # Pick best main image: prefer non-SVG, larger area
            best = None
            for img in all_images:
                score = img['area']
                if not img['is_svg']:
                    score *= 3  # Boost non-SVG images
                if width >= 200 and height >= 150:
                    score *= 2  # Boost decent-sized images
                img['score'] = score
                if best is None or score > best['score']:
                    best = img
            
            if best:
                image_url = best['url']
            
            # Clean up helper fields from output
            for img in all_images:
                img.pop('score', None)
                img.pop('area', None)
                img.pop('is_svg', None)
        
        if content_div:
            # Full text (first 20 paragraphs for a longer summary)
            paragraphs = []
            paragraphs_html = []
            for p in content_div.find_all('p')[:20]:
                text = p.get_text(strip=True)
                if text and len(text) > 20:
                    paragraphs.append(text)
                    # Convert paragraph to string, then replace wiki links
                    p_str = str(p)
                    # Find all <a> tags and replace internal wiki links
                    def replace_wiki_link(m):
                        full_match = m.group(0)
                        href = m.group(1)
                        link_text = m.group(2)
                        # Decode URL
                        decoded = unquote(href)
                        if ':' in decoded or decoded.startswith('-'):
                            return full_match
                        if archive.has_entry_by_title(decoded):
                            return f'<a class="wiki-link" data-target="{decoded}">{to_simplified(link_text)}</a>'
                        return full_match
                    p_str = re.sub(
                        r'<a[^>]*href="([^"#]+)"[^>]*>([^<]+)</a>',
                        replace_wiki_link,
                        p_str
                    )
                    # Remove outer <p> tag
                    p_html = re.sub(r'^<p[^>]*>', '', p_str)
                    p_html = re.sub(r'</p>$', '', p_html)
                    paragraphs_html.append(p_html)
            summary = '\n\n'.join(paragraphs)
            summary_html = '\n\n'.join(paragraphs_html)
            
            # Full article text (all paragraphs) — plain + HTML with wiki links
            full_content_text = ''
            full_content_html = ''
            for p in content_div.find_all('p'):
                text = p.get_text(strip=True)
                if text and len(text) > 10:
                    full_content_text += text + '\n\n'
                    # Convert paragraph to string, then replace wiki links
                    p_str = str(p)
                    def replace_wiki_link(m):
                        full_match = m.group(0)
                        href = m.group(1)
                        link_text = m.group(2)
                        decoded = unquote(href)
                        if ':' in decoded or decoded.startswith('-'):
                            return full_match
                        if archive.has_entry_by_title(decoded):
                            return f'<a class="wiki-link" data-target="{decoded}">{to_simplified(link_text)}</a>'
                        return full_match
                    p_str = re.sub(
                        r'<a[^>]*href="([^"#]+)"[^>]*>([^<]+)</a>',
                        replace_wiki_link,
                        p_str
                    )
                    # Remove outer <p> tag
                    p_html = re.sub(r'^<p[^>]*>', '', p_str)
                    p_html = re.sub(r'</p>$', '', p_html)
                    full_content_html += f'<p>{p_html}</p>'
            
            # Extract related links (all internal links from content)
            related_links = []
            seen = set()
            for idx, a in enumerate(content_div.find_all('a', href=True)):
                href = a.get('href', '')
                if href.startswith(('http', '#', './', 'javascript:')):
                    continue
                decoded = unquote(href)
                # Skip special pages, duplicates, and self-references
                if ':' in decoded or decoded.startswith('-') or decoded in seen or decoded == title:
                    continue
                link_text = to_simplified(a.get_text(strip=True))
                if not link_text or len(link_text) < 2:
                    continue
                # Skip very short or numeric links
                if len(link_text) <= 2 and not link_text.encode('utf-8').isalpha():
                    continue
                seen.add(decoded)
                # Check if article exists in archive
                if archive.has_entry_by_title(decoded):
                    # Score: earlier + longer title = more relevant
                    score = (100 - min(idx, 100)) + len(link_text) * 2
                    related_links.append({
                        "title": link_text,
                        "target": decoded,
                        "score": score,
                    })
            
            # Sort by relevance score and take top results
            related_links.sort(key=lambda x: x.get('score', 0), reverse=True)
            # Remove score from output
            for link in related_links:
                link.pop('score', None)
        else:
            summary = soup.get_text()[:5000]
            full_content_text = summary
            full_content_html = ''
            summary_html = ''
            related_links = []
        
        return {
            "title": title_text,
            "summary": to_simplified(summary[:5000]),
            "summary_html": summary_html[:8000],
            "full_content": to_simplified(full_content_text[:50000]),
            "full_content_html": to_simplified(full_content_html[:50000]),
            "related_links": related_links[:9],
            "image": image_url,
            "images": all_images[:5],
            "content_length": len(content)
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Article not found: {e}")


@app.get("/browse-zim")
async def browse_zim():
    """Open native file dialog to select a ZIM file, return full path"""
    import threading
    result = {"path": "", "error": ""}
    
    def _open_dialog():
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            path = filedialog.askopenfilename(
                parent=root,
                title='选择 ZIM 文件',
                filetypes=[('ZIM 文件', '*.zim'), ('所有文件', '*.*')],
            )
            root.destroy()
            result["path"] = path
        except Exception as e:
            result["error"] = str(e)
    
    # Run dialog in a thread so it doesn't block the event loop
    t = threading.Thread(target=_open_dialog)
    t.start()
    t.join(timeout=120)  # Wait up to 2 min for user to pick a file
    
    if result["error"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return {"path": result["path"]}


@app.post("/reload-zim")
async def reload_zim(body: dict):
    """Reload the ZIM archive from a new file path"""
    global archive
    zim_path = body.get('zim_path', '')
    if not zim_path:
        raise HTTPException(status_code=400, detail="zim_path is required")
    if not os.path.exists(zim_path):
        raise HTTPException(status_code=400, detail=f"File not found: {zim_path}")
    if not zim_path.lower().endswith('.zim'):
        raise HTTPException(status_code=400, detail="File extension must be .zim")
    try:
        init_archive(zim_path)
        return {
            "message": "ZIM archive loaded successfully",
            "article_count": archive.article_count if archive else 0,
            "date": archive.get_metadata('Date') if archive else '',
            "language": archive.get_metadata('Language') if archive else '',
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load ZIM: {e}")


def main():
    print("Starting API server at http://localhost:8765")
    print("Use the '载入ZIM文件' button in the UI to load a ZIM archive.")
    uvicorn.run(app, host="0.0.0.0", port=8765)


if __name__ == "__main__":
    main()
