#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-instala dependências ausentes (opcional, importar no main se quiser).
"""
import sys
import subprocess

PKGS = [
    ("customtkinter", "5.2.0"),
    ("selenium", "4.21.0"),
    ("webdriver-manager", "4.0.1"),
    ("requests", "2.31.0"),
    ("pillow", "10.4.0"),
    ("numpy", "1.26.4")
]

def ensure_package(mod: str, ver: str):
    try:
        __import__(mod)
    except ImportError:
        spec = f"{mod}=={ver}"
        print(f"[AUTO] Instalando {spec}")
        subprocess.run([sys.executable, "-m", "pip", "install", spec])

def bootstrap():
    for mod, ver in PKGS:
        ensure_package(mod, ver)

if __name__ == "__main__":
    bootstrap()