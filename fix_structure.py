#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_structure.py
Normaliza a estrutura para que o import 'from src.gui.main_app import AviatorGUI' funcione.

Uso:
    python fix_structure.py
Depois:
    python verify_modules.py
    python main.py
"""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).parent.resolve()
SRC_ROOT = ROOT / "src"
AVIATOR = ROOT / "AviatorBot"
AVIATOR_SRC = AVIATOR / "src"

NEEDED_SUBDIRS = ["gui", "core", "utils", "components"]

def ensure_init(path: Path):
    if path.is_dir():
        init_file = path / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# package\n", encoding="utf-8")

def copy_if_missing(src_dir: Path, dst_dir: Path):
    if not src_dir.exists():
        return
    for sub in NEEDED_SUBDIRS:
        s = src_dir / sub
        d = dst_dir / sub
        if s.exists():
            d.mkdir(parents=True, exist_ok=True)
            # Copiar arquivos .py (não sobrescreve se já existe com conteúdo)
            for py in s.glob("*.py"):
                target = d / py.name
                if not target.exists():
                    shutil.copy2(py, target)

def main():
    print("=" * 60)
    print(" NORMALIZANDO ESTRUTURA (fix_structure.py) ")
    print("=" * 60)
    print(f"Raiz: {ROOT}")
    # Criar ./src se não existe
    if not SRC_ROOT.exists():
        SRC_ROOT.mkdir()
        print("Criado diretório ./src")
    # Copiar de AviatorBot/src se existir
    if AVIATOR_SRC.exists():
        print("Detectado AviatorBot/src – copiando subpastas principais...")
        copy_if_missing(AVIATOR_SRC, SRC_ROOT)
    else:
        print("AviatorBot/src não encontrado (ok se você já está com src direto).")

    # Garantir subpastas
    for sd in NEEDED_SUBDIRS:
        (SRC_ROOT / sd).mkdir(parents=True, exist_ok=True)

    # Garantir __init__.py
    ensure_init(SRC_ROOT)
    for sd in NEEDED_SUBDIRS:
        ensure_init(SRC_ROOT / sd)

    # Conferir main_app
    main_app = SRC_ROOT / "gui" / "main_app.py"
    if main_app.exists():
        print("OK: src/gui/main_app.py encontrado.")
    else:
        print("ATENÇÃO: src/gui/main_app.py não existe. Vou criar um esqueleto mínimo.")
        main_app.write_text(
            "# Placeholder main_app.py - substitua pelo arquivo completo fornecido.\n"
            "class AviatorGUI:\n"
            "    def run(self):\n"
            "        print('Placeholder - substitua pelo arquivo completo.')\n",
            encoding="utf-8"
        )
    print("\nEstrutura final verificada.")
    print("Execute agora: python verify_modules.py")
    print("=" * 60)

if __name__ == "__main__":
    main()