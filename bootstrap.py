#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bootstrap de dependências (uso emergencial fora do instalador).
"""
import sys
import subprocess

REQS = [
    "customtkinter==5.2.0",
    "selenium==4.21.0",
    "webdriver-manager==4.0.1",
    "requests==2.31.0",
    "pillow==10.4.0",
    "numpy==1.26.4"
]

def run(cmd):
    print("[CMD]", " ".join(cmd))
    return subprocess.run(cmd)

def main():
    print("=" * 50)
    print(" BOOTSTRAP AVIATOR BOT ")
    print("=" * 50)
    if sys.version_info < (3, 8):
        print("Python 3.8+ necessário.")
        return
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    for spec in REQS:
        run([sys.executable, "-m", "pip", "install", spec])
    print("Concluído.")

if __name__ == "__main__":
    main()