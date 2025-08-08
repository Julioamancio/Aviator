#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_env.py - Corrige dependências ausentes.
"""
import sys
import subprocess
import importlib

ESSENTIAL = [
    "customtkinter==5.2.0",
    "selenium==4.21.0",
    "webdriver-manager==4.0.1",
    "requests==2.31.0",
    "pillow==10.4.0",
    "numpy==1.26.4"
]

def run(cmd):
    print(f"[CMD] {' '.join(cmd)}")
    return subprocess.run(cmd, text=True)

def ensure(spec: str):
    pkg = spec.split("==")[0]
    try:
        importlib.import_module(pkg)
        print(f"[OK] {pkg} presente.")
    except ImportError:
        print(f"[Instalando] {spec}")
        run([sys.executable, "-m", "pip", "install", spec])

def full_reinstall():
    print("[FULL] Reinstalando todos pacotes.")
    for spec in ESSENTIAL:
        run([sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", spec])

def main():
    print("=" * 60)
    print(" FIX ENV - AVIATOR BOT ")
    print("=" * 60)
    print("Python:", sys.version)
    if "--full" in sys.argv:
        full_reinstall()
    else:
        run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
        for spec in ESSENTIAL:
            ensure(spec)
    print("Concluído.")
    print("=" * 60)

if __name__ == "__main__":
    main()