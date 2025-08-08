#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica se a estrutura final está correta.
Uso:
    python verify_modules.py
"""

from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).parent.resolve()

targets = [
    ROOT / "src" / "gui" / "main_app.py",
    ROOT / "src" / "core" / "aviator_bot.py",
    ROOT / "src" / "core" / "browser_manager.py",
    ROOT / "src" / "core" / "strategy.py",
    ROOT / "src" / "utils" / "config_manager.py",
]

def check_file(p: Path):
    return p.exists() and p.is_file()

def check_import(module_name: str):
    try:
        importlib.import_module(module_name)
        return True, ""
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print(" VERIFICANDO ESTRUTURA E IMPORTS ")
    print("=" * 60)
    all_ok = True

    for t in targets:
        ok = check_file(t)
        print(f"[{'OK' if ok else 'FALTA'}] {t.relative_to(ROOT)}")
        if not ok:
            all_ok = False

    # Ajustar sys.path para testar import
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    print("\nTestando import: src.gui.main_app")
    ok_imp, err = check_import("src.gui.main_app")
    print(" ->", "OK" if ok_imp else f"ERRO: {err}")
    all_ok = all_ok and ok_imp

    print("\nResumo final:", "SUCESSO" if all_ok else "PENDÊNCIAS")
    if not all_ok:
        print("Ajuste os arquivos faltantes antes de rodar main.py.")
    print("=" * 60)

if __name__ == "__main__":
    main()