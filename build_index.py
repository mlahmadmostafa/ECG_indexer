import os

# Configuration
INPUT_CSV = 'tools.csv'
OUTPUT_HTML = 'index.html'

def create_catalog():
    # 1. Read the CSV Data
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Error: Could not find '{INPUT_CSV}' in this folder.")
        return

    try:
        with open(INPUT_CSV, 'r', encoding='utf-8') as f:
            csv_content = f.read()
            # Escape backticks to prevent breaking the JS template literal
            csv_content = csv_content.replace('`', '\\`')
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # 2. Define the HTML Template
    # We inject the csv_content into the variable `const csvData` below.
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Catalog</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            text-align: center; color: #333; margin-bottom: 30px;
            background: white; padding: 30px; border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1 {{ font-size: 2.5em; margin-bottom: 15px; color: #667eea; }}
        .subtitle {{ font-size: 1.1em; color: #666; margin-bottom: 20px; }}
        .contact-section {{ margin-top: 20px; padding-top: 20px; border-top: 2px solid #e0e0e0; }}
        .contact-link {{
            display: inline-flex; align-items: center; gap: 10px;
            background: #667eea; color: white; padding: 12px 24px;
            border-radius: 8px; text-decoration: none; font-weight: 600;
            transition: background 0.3s, transform 0.2s;
        }}
        .contact-link:hover {{ background: #5568d3; transform: translateY(-2px); }}
        .contact-message {{ color: #666; margin-bottom: 12px; font-size: 1em; }}
        
        .search-section {{
            background: white; border-radius: 12px; padding: 20px;
            margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .search-bar {{
            width: 100%; padding: 15px 20px; font-size: 1.1em;
            border: 2px solid #e0e0e0; border-radius: 8px; transition: border-color 0.3s;
        }}
        .search-bar:focus {{ outline: none; border-color: #667eea; }}
        
        .tools-grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px; margin-bottom: 30px;
        }}
        .tool-card {{
            background: white; border-radius: 12px; padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
            animation: fadeIn 0.5s;
        }}
        .tool-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .tool-name {{ font-size: 1.5em; color: #667eea; margin-bottom: 10px; font-weight: bold; }}
        .tool-description {{ color: #555; margin-bottom: 15px; line-height: 1.6; }}
        .tool-path {{
            background: #f5f5f5; padding: 10px; border-radius: 6px;
            font-family: 'Courier New', monospace; font-size: 0.9em;
            margin-bottom: 15px; word-break: break-all; color: #333;
        }}
        .tool-tutorial {{ margin-bottom: 15px; color: #666; }}
        .tool-notes {{
            margin-bottom: 15px; padding: 10px; background: #fff8e1;
            border-left: 4px solid #ffc107; border-radius: 4px; font-size: 0.95em;
        }}
        .keywords {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .keyword {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 5px 12px; border-radius: 15px;
            font-size: 0.85em; font-weight: 500;
        }}
        .no-results {{
            text-align: center; color: #666; font-size: 1.3em;
            padding: 40px; background: white; border-radius: 12px;
        }}
        .label {{
            font-weight: 600; color: #333; margin-bottom: 5px;
            font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Engineering Development Index</h1>
            <p class="subtitle">Comprehensive tool catalog for engineering development</p>
            <div class="contact-section">
                <p class="contact-message">Have questions or suggestions?</p>
                <a href="mailto:ED@ecgsa.com" class="contact-link">
                    ✉️ Communicate with us - ED@ecgsa.com
                </a>
            </div>
        </header>

        <div class="search-section" id="searchSection">
            <input type="text" 
                   class="search-bar" 
                   id="searchBar" 
                   placeholder="🔍 Search tools by name, description, keywords, or any metadata...">
        </div>

        <div class="tools-grid" id="toolsGrid"></div>
    </div>

    <script>
        // ============================================
        // INJECTED DATA FROM PYTHON
        // ============================================
        const csvData = `{csv_content}`;
        // ============================================

        let toolsData = [];

        window.addEventListener('load', function() {{
            Papa.parse(csvData, {{
                header: true,
                skipEmptyLines: true,
                complete: function(results) {{
                    toolsData = results.data;
                    displayTools(toolsData);
                }}
            }});
        }});

        document.getElementById('searchBar').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const filtered = toolsData.filter(tool => {{
                return (
                    (tool['tool name'] || '').toLowerCase().includes(searchTerm) ||
                    (tool['tool description'] || '').toLowerCase().includes(searchTerm) ||
                    (tool['tool path'] || '').toLowerCase().includes(searchTerm) ||
                    (tool['tutorial'] || '').toLowerCase().includes(searchTerm) ||
                    (tool['notes'] || '').toLowerCase().includes(searchTerm) ||
                    (tool['keywords'] || '').toLowerCase().includes(searchTerm)
                );
            }});
            displayTools(filtered);
        }});

        function displayTools(tools) {{
            const grid = document.getElementById('toolsGrid');
            
            if (tools.length === 0) {{
                grid.innerHTML = '<div class="no-results">No tools found matching your search</div>';
                return;
            }}

            grid.innerHTML = tools.map(tool => {{
                const keywords = (tool['keywords'] || '').split(',').map(k => k.trim()).filter(k => k);
                
                return `
                    <div class="tool-card">
                        <div class="tool-name">${{tool['tool name'] || 'Unnamed Tool'}}</div>
                        
                        ${{tool['tool description'] ? `
                            <div class="tool-description">${{tool['tool description']}}</div>
                        ` : ''}}
                        
                        ${{tool['tool path'] ? `
                            <div>
                                <div class="label">Path</div>
                                <div class="tool-path">${{tool['tool path']}}</div>
                            </div>
                        ` : ''}}
                        
                        ${{tool['tutorial'] ? `
                            <div class="tool-tutorial">
                                <div class="label">Tutorial</div>
                                ${{formatLink(tool['tutorial'])}}
                            </div>
                        ` : ''}}
                        
                        ${{tool['notes'] ? `
                            <div class="tool-notes">
                                <div class="label">Notes</div>
                                ${{tool['notes']}}
                            </div>
                        ` : ''}}
                        
                        ${{keywords.length > 0 ? `
                            <div>
                                <div class="label">Keywords</div>
                                <div class="keywords">
                                    ${{keywords.map(k => `<span class="keyword">${{k}}</span>`).join('')}}
                                </div>
                            </div>
                        ` : ''}}
                    </div>
                `;
            }}).join('');
        }}

        function formatLink(text) {{
            if (text && (text.startsWith('http://') || text.startsWith('https://'))) {{
                return `<a href="${{text}}" target="_blank" style="color:#667eea; text-decoration:underline;">${{text}}</a>`;
            }}
            return text;
        }}
    </script>
</body>
</html>
"""

    # 3. Write the Final HTML
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✅ Success! Generated '{OUTPUT_HTML}' with data from '{INPUT_CSV}'.")
    print("👉 You can now open 'index.html' directly in your browser.")

if __name__ == "__main__":
    create_catalog()