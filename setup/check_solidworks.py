"""Diagnostics: is SOLIDWORKS installed/registered and reachable over COM?"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging; logging.disable(logging.CRITICAL)
from solidworks_mcp.utils.sw_finder import SolidWorksFinder

info = SolidWorksFinder.get_install_info()
print("  SLDWORKS.exe :", info["exe_path"] or "NOT FOUND")
print("  file version :", info["version"])
for k, v in info["templates"].items():
    print(f"  {k:9} tpl :", v)

import winreg
try:
    cur = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, r"SldWorks.Application\CurVer")
    print("  COM ProgID   :", cur, "(SldWorks.Application.34 = SOLIDWORKS 2026)")
except OSError:
    print("  COM ProgID   : SldWorks.Application NOT registered")

import win32com.client
try:
    sw = win32com.client.GetActiveObject("SldWorks.Application")
    print("  running SW   : revision", sw.RevisionNumber, "- COM connection OK")
except Exception:
    print("  running SW   : not running (start SOLIDWORKS 2026 before using the MCP tools)")
