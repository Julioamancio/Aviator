#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico de ambiente.
"""
import sys, site, os, platform, importlib.util

def main():
    print("===== DIAGNÓSTICO AMBIENTE AVIATOR BOT =====")
    print("Python:", sys.version)
    print("Executável:", sys.executable)
    print("Plataforma:", platform.platform())
    print("\nCWD:", os.getcwd())
    print("\nsys.path:")
    for p in sys.path:
        print(" -", p)
    print("\nsite.getsitepackages():")
    try:
        for p in site.getsitepackages():
            print(" *", p)
    except Exception:
        pass
    print("\ncustomtkinter disponível?", importlib.util.find_spec("customtkinter") is not None)
    print("============================================")

if __name__ == "__main__":
    main()