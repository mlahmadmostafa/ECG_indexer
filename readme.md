

# 🛠️ Engineering Development Tool Catalog

A lightweight, offline-capable tool that converts a simple CSV spreadsheet into a beautiful, searchable HTML dashboard.

This project is designed for engineering teams or individuals to maintain a central index of development tools, installed paths, tutorials, and documentation without needing a complex database or web server.

## 📂 Project Structure

*   **`build_catalog.py`**: The generator script. It reads your data and builds the website.
*   **`tools.csv`**: Your database. Add your tools, paths, and links here.
*   **`index.html`**: The final output. A standalone file you can open in any browser.

## 🚀 Quick Start

### 1. Prerequisites
Run it from EXE file.

### 2. Prepare your Data
Edit the `tools.csv` file. You can open it in Excel, Notepad, or VS Code.
Ensure you keep the header row exactly as is:

```csv
tool name,tool description,tool path,tutorial,notes,keywords
```

**Example Row:**
```csv
Docker,Container platform,/usr/bin/docker,https://docker.com,Must run as root,devops,containers
```

### 3. Generate the Catalog
Open your terminal or command prompt in the project folder and run:

```bash
python build_catalog.py
```

You should see the message:
> ✅ Success! Generated 'index.html' with data from 'tools.csv'.

### 4. View the Result
Open the newly created **`index.html`** file in Chrome, Edge, or Firefox.
*   **No internet required:** The CSV data is embedded directly into the HTML.
*   **No server required:** Double-click the file to open it.

## 📊 CSV Column Guide

| Column Header | Description |
| :--- | :--- |
| **tool name** | The main title of the tool (e.g., "VS Code"). |
| **tool description** | A short summary of what the tool does. |
| **tool path** | The file system path (e.g., `C:\Program Files\...` or `/usr/bin/...`). |
| **tutorial** | A URL to documentation. If it starts with `http`, it becomes a clickable link. |
| **notes** | specific warnings, versions, or tips (highlighted in yellow). |
| **keywords** | Comma-separated tags for better search (e.g., `git, vcs, source`). |

## 🎨 Customization

To change the look and feel (colors, fonts, or layout), open `build_catalog.py` and modify the **CSS** inside the `html_template` variable.

## ❓ Troubleshooting

**"No tools found matching your search"**
*   Check if `tools.csv` exists in the same folder.
*   Make sure you re-ran `python build_catalog.py` after saving your CSV changes.

**Encoding Errors**
*   Ensure your CSV is saved with **UTF-8** encoding. Excel sometimes saves as CSV (Macintosh) or ANSI. Using VS Code or Notepad++ to save the CSV ensures correct encoding.

