#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher simples para executar o Aviator Bot via venv.
"""
import os
import sys
import subprocess
from pathlib import Path

BASE = Path(__file__).parent
VENV = BASE / "venv"
PY = VENV / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")

def main():
    print("=== Launcher Aviator Bot ===")
    if not PY.exists():
        print("Venv não encontrado. Rode: python installer.py")
        input("Enter para sair...")
        return
    subprocess.run([str(PY), "main.py"])

if __name__ == "__main__":
    main()