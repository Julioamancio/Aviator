#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).parent
checks = [
    root / "src" / "gui" / "main_app.py",
    root / "AviatorBot" / "src" / "gui" / "main_app.py"
]
print("Verificando possíveis localizações:")
for c in checks:
    print(f"[{'OK' if c.exists() else 'FALTA'}] {c}")