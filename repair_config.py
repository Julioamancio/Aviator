#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recria/garante o arquivo config/default_config.json.
Uso:
    python repair_config.py
"""

from pathlib import Path
import json
from src.utils.config_manager import _DEFAULT_CONFIG  # usa o mesmo default

CONFIG_PATH = Path("config/default_config.json")

def main():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        print(f"[INFO] Já existe: {CONFIG_PATH} (será sobrescrito)")
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(_DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    print(f"[OK] Arquivo recriado: {CONFIG_PATH}")

if __name__ == "__main__":
    main()