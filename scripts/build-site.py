#!/usr/bin/env python3
import os
import re
import json
import yaml
import zipfile
import shutil
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(REPO_ROOT, "dist")
GITHUB_BASE = "https://github.com/sherpa-md/sherpa-kits/blob/main"

def parse_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match: return None, None, None
    try:
        data = yaml.safe_load(match.group(1))
        return data, match.group(2), content
    except:
        return None, None, None

def build():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)
    
    sherpas = []
    
    # Discovery
    for root, dirs, files in os.walk(REPO_ROOT):
        if '.git' in root or 'dist' in root: continue
        for file in files:
            if file.endswith('.sherpa.md'):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, REPO_ROOT)
                fm, body, raw_content = parse_frontmatter(path)
                if fm and fm.get('confidentiality') == 'public':
                    sherpas.append({
                        'id': fm.get('id', rel_path),
                        'title': fm.get('title', 'Untitled'),
                        'description': fm.get('domain', ''),
                        'version': str(fm.get('version', '1.0')),
                        'rel_path': rel_path,
                        'content': fm,
                        'raw': raw_content
                    })
    
    # Save md files to dist for download/preview
    md_dir = os.path.join(DIST_DIR, "md")
    os.makedirs(md_dir, exist_ok=True)
    for s in sherpas:
        dest = os.path.join(md_dir, os.path.basename(s['rel_path']))
        shutil.copy2(os.path.join(REPO_ROOT, s['rel_path']), dest)
        s['download_url'] = f"md/{os.path.basename(s['rel_path'])}"
    
    # Bundle.zip
    bundle_path = os.path.join(DIST_DIR, "bundle.zip")
    with zipfile.ZipFile(bundle_path, 'w') as zf:
        for s in sherpas:
            zf.write(os.path.join(REPO_ROOT, s['rel_path']), arcname=s['rel_path'])
            
    # index.json
    with open(os.path.join(DIST_DIR, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump([s['content'] for s in sherpas], f, indent=2)
        
    # llms.txt
    with open(os.path.join(DIST_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write("# SherpaMD Catalog\n\nThis catalog contains public SherpaMD files.\n\n")
        for s in sherpas:
            f.write(f"- [{s['title']}]({s['download_url']}): {s['description']}\n")
            
    # sitemap.xml
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for s in sherpas:
        url = ET.SubElement(root, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = f"https://sherpamd.org/kits/{s['id']}"
    tree = ET.ElementTree(root)
    tree.write(os.path.join(DIST_DIR, 'sitemap.xml'), encoding='utf-8', xml_declaration=True)
    
    # index.html
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SherpaMD Catalog</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #f4f4f5; margin: 0; padding: 20px; color: #333; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .search-bar { width: 100%; padding: 10px; margin-bottom: 20px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; flex-direction: column;}
        .card-title { font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
        .card-desc { font-size: 0.9em; color: #666; margin-bottom: 15px; flex-grow: 1; }
        .actions { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
        button, .btn { padding: 5px 10px; font-size: 0.85em; cursor: pointer; border: none; border-radius: 4px; background: #007bff; color: white; text-decoration: none; }
        button:hover, .btn:hover { background: #0056b3; }
        .rating { color: #ccc; cursor: pointer; display: flex; gap: 2px; }
        .star.active { color: #f59e0b; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); padding: 20px; box-sizing: border-box;}
        .modal-content { background: white; width: 100%; max-width: 800px; margin: 0 auto; padding: 20px; border-radius: 8px; max-height: 90vh; overflow-y: auto; text-align: left; }
        .close { float: right; cursor: pointer; font-size: 1.5em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>SherpaMD Kits</h1>
        <div>
            <a href="bundle.zip" class="btn">All-Sherpas Bundle</a>
            <a href="site.zip" class="btn">Static Site ZIP</a>
            <a href="index.json" class="btn">index.json</a>
            <a href="llms.txt" class="btn">llms.txt</a>
        </div>
    </div>
    
    <div>
        <p><strong>Portable Backend Contract for Ratings:</strong> Send a POST request to <code>/api/ratings</code> with JSON body <code>{"id": "sherpa-id", "rating": 1-5}</code>. This catalog is static, but integrating this UI with a real backend simply requires implementing this endpoint.</p>
    </div>

    <input type="text" id="search" class="search-bar" placeholder="Search Sherpas...">
    
    <div id="grid" class="grid"></div>

    <div id="modal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <pre id="modal-body" style="white-space: pre-wrap; font-family: monospace;"></pre>
        </div>
    </div>

    <script>
        const sherpas = JSON_DATA_HERE;
        const GITHUB_BASE = "GITHUB_BASE_HERE";
        const grid = document.getElementById('grid');
        
        function renderCards(data) {
            grid.innerHTML = '';
            data.forEach(s => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div class="card-title">${s.title}</div>
                    <div class="card-desc">${s.description} (v${s.version})</div>
                    <div class="actions">
                        <button onclick="preview('${s.id}')">Preview</button>
                        <button onclick="copyToAI('${s.id}')">Copy 'Use with AI'</button>
                        <a href="${s.download_url}" class="btn" download>Download .md</a>
                        <a href="${GITHUB_BASE}/${s.rel_path}" class="btn" target="_blank">GitHub source</a>
                    </div>
                    <div class="rating" data-id="${s.id}">
                        ${[1,2,3,4,5].map(i => `<span class="star" data-val="${i}" onclick="rate('${s.id}', ${i})">★</span>`).join('')}
                    </div>
                `;
                grid.appendChild(card);
            });
        }
        
        window.preview = (id) => {
            const s = sherpas.find(x => x.id === id);
            document.getElementById('modal-body').textContent = s.raw;
            document.getElementById('modal').style.display = 'block';
        };
        
        window.closeModal = () => {
            document.getElementById('modal').style.display = 'none';
        };
        
        window.copyToAI = (id) => {
            const s = sherpas.find(x => x.id === id);
            navigator.clipboard.writeText(s.raw).then(() => alert('Copied to clipboard!')).catch(e => {
                // fallback if clipboard api fails
                const textArea = document.createElement("textarea");
                textArea.value = s.raw;
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                try {
                  document.execCommand('copy');
                  alert('Copied to clipboard!');
                } catch (err) {
                  alert('Failed to copy');
                }
                document.body.removeChild(textArea);
            });
        };
        
        window.rate = (id, val) => {
            fetch('/api/ratings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id, rating: val})
            }).then(res => {
                console.log('Rated', id, val);
                const ratingDiv = document.querySelector(`.rating[data-id="${id}"]`);
                ratingDiv.querySelectorAll('.star').forEach(el => {
                    el.classList.toggle('active', parseInt(el.dataset.val) <= val);
                });
            }).catch(e => {
                console.error('Rating failed (expected if no backend)', e);
                // visually update anyway for demo
                const ratingDiv = document.querySelector(`.rating[data-id="${id}"]`);
                ratingDiv.querySelectorAll('.star').forEach(el => {
                    el.classList.toggle('active', parseInt(el.dataset.val) <= val);
                });
            });
        };
        
        document.getElementById('search').addEventListener('input', (e) => {
            const q = e.target.value.toLowerCase();
            renderCards(sherpas.filter(s => s.title.toLowerCase().includes(q) || s.description.toLowerCase().includes(q) || s.raw.toLowerCase().includes(q)));
        });
        
        renderCards(sherpas);
    </script>
</body>
</html>
    """
    
    html = html.replace("JSON_DATA_HERE", json.dumps([{
        'id': s['id'], 'title': s['title'], 'description': s['description'], 
        'version': s['version'], 'download_url': s['download_url'], 
        'rel_path': s['rel_path'], 'raw': s['raw']
    } for s in sherpas]).replace("</script>", "<\\/script>"))
    html = html.replace("GITHUB_BASE_HERE", GITHUB_BASE)
    
    with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
        
    # site.zip
    site_zip_path = os.path.join(DIST_DIR, "site.zip")
    with zipfile.ZipFile(site_zip_path, 'w') as zf:
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                if file != "site.zip":
                    path = os.path.join(root, file)
                    rel_path = os.path.relpath(path, DIST_DIR)
                    zf.write(path, arcname=rel_path)
                    
    print(f"Discovered: {len(sherpas)}, Built: {len(sherpas)}, Downloadable: {len(sherpas)}")

if __name__ == "__main__":
    build()
