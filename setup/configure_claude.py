"""Register this MCP server in Claude Desktop's config (merges, keeps other servers, makes a backup)."""
import glob, json, os, shutil, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
SERVER = os.path.join(ROOT, "solidworks_mcp_server.py")

appdata = os.environ.get("APPDATA", "")
localapp = os.environ.get("LOCALAPPDATA", "")
dirs = [os.path.join(appdata, "Claude")]
# Microsoft Store / MSIX install keeps a virtualised copy of AppData
dirs += glob.glob(os.path.join(localapp, "Packages", "Claude_*", "LocalCache", "Roaming", "Claude"))

entry = {"command": PY, "args": [SERVER], "env": {"PYTHONIOENCODING": "utf-8"}}
for d in dirs:
    os.makedirs(d, exist_ok=True)
    cfg = os.path.join(d, "claude_desktop_config.json")
    data = {}
    if os.path.exists(cfg):
        shutil.copy2(cfg, cfg + time.strftime(".bak-%Y%m%d-%H%M%S"))
        with open(cfg, encoding="utf-8-sig") as f:
            txt = f.read().strip()
        data = json.loads(txt) if txt else {}
    data.setdefault("mcpServers", {})["solidworks"] = entry
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("  updated:", cfg)
