#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installer / Updater - Aviator Bot v3.4
Inclui:
 - Ajuste de tipos para Pylance
 - Suporte a dependências ML, FastAPI, JWT
 - Estrutura modular
"""

import os, sys, subprocess, json, shutil, venv, stat, textwrap, base64
from pathlib import Path
from datetime import datetime

APP_NAME = "Aviator Bot v3.4"
BASE_DIR = Path.cwd()
PROJ_DIR = BASE_DIR / "AviatorBot"
VENV_DIR = PROJ_DIR / "venv"
REQ_FILE = PROJ_DIR / "requirements.txt"

PY_MIN = (3, 9)

DEPENDENCIES = [
    "customtkinter==5.2.0",
    "selenium==4.21.0",
    "webdriver-manager==4.0.1",
    "requests==2.31.0",
    "pillow==10.4.0",
    "numpy==1.26.4",
    "psutil==5.9.8",
    "urllib3<3",
    "matplotlib==3.9.0",
    "fastapi==0.111.0",
    "uvicorn==0.30.1",
    "scikit-learn==1.4.2",
    "python-jose==3.3.0",
    "pandas==2.2.2"
]

ICON_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAACBklEQVR4nO2ZMU8CQRCHv9oU"
    "iMACQi4QFDEmZuzBESjABkI2IlowBCYgGVlkEdhILCQi6FDak3DrbZr37L173bknLrK7M2eq"
    "6v1qOkHJycnJycnIx5mjb+AG2AF2Es8r8A3YCt0C1wHdgmv18Afk3gFfgIHIiATjwJvAy8wD"
    "Vng7KYwB08A6eBqu7ZTrDBV6ByJpANhaQBaW+Vymz0VqAO0i6X9ohCAhcWJCUA2AxeN1IH3a"
    "6pRUCidJfG7udyknJImcXiUgAcgGD++3BzV1LFgBs2Wq/dA1+U4Oaoyf8glJ8MELSCvMEfF9"
    "FEJL/IMC0gJfgTHQ9tJrnMtV61uYzDsSScnZfTZC74DiTZBIiSf3GtfAVySSZgW+QLZyUS0L"
    "2F5SOPwf3cPXLztItYOcueWnnyR2pk9vYO3DiCUnJycnJyczPYy14AUwFfvkWpFThQugROBD"
    "+BX4F/gT32zJHT0/Za1gLeQVFdfbGqrQko3zPpTEpSgCkXJ2YUJ0pSfmb9lC8Ai8AL8AK8Bx"
    "3BrJX1j7gPYdWubsXnZG4ADY6ZP3qBbD5izJdBt2hm5+BUA3uA3uAZuAz+B6uITGMAKWwAAA"
    "AElFTkSuQmCC"
)

DEFAULT_CONFIG = {}  # O instalador não sobrescreve config existente (use arquivo enviado anteriormente).

def banner():
    print("=" * 80)
    print(APP_NAME.center(80))
    print("Installer / Updater".center(80))
    print("=" * 80)

def parse_args():
    args = sys.argv[1:]
    return {
        "run": "--run" in args,
        "only-run": "--only-run" in args,
        "force": "--force" in args,
        "upgrade": "--upgrade" in args
    }

def check_python():
    if sys.version_info < PY_MIN:
        print(f"[ERRO] Python {PY_MIN[0]}.{PY_MIN[1]}+ requerido.")
        sys.exit(1)

def create_dirs():
    for d in [
        "config/profiles",
        "license",
        "logs",
        "exports",
        "screenshots",
        "assets/icons",
        "models",
        "plugins",
        "src/gui",
        "src/core",
        "src/utils"
    ]:
        (PROJ_DIR / d).mkdir(parents=True, exist_ok=True)

def write_requirements():
    REQ_FILE.write_text(
        "# Auto-generated requirements\n" + "\n".join(DEPENDENCIES) + "\n",
        encoding="utf-8"
    )

def create_venv(force=False):
    if VENV_DIR.exists() and force:
        shutil.rmtree(VENV_DIR)
    if VENV_DIR.exists():
        return
    print("[INFO] Criando venv...")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)

def venv_python():
    return VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")

def install_deps(upgrade=False):
    print("[INFO] Instalando dependências...")
    cmd_base = [str(venv_python()), "-m", "pip"]
    subprocess.run(cmd_base + ["install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    args = ["install", "-r", str(REQ_FILE)]
    if upgrade:
        args.insert(1, "--upgrade")
    subprocess.run(cmd_base + args, check=True)

def write_icon():
    icon_png = base64.b64decode(ICON_PNG_B64)
    ip = PROJ_DIR / "assets/icons/app_icon.png"
    if not ip.exists():
        ip.write_bytes(icon_png)

def write_init():
    for p in ["src", "src/gui", "src/core", "src/utils"]:
        f = PROJ_DIR / p / "__init__.py"
        if not f.exists():
            f.write_text("# package\n", encoding="utf-8")

def safe_json_write(path: Path, data: dict):
    if path.exists():
        return
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def write_default_config():
    cfg = PROJ_DIR / "config/default_config.json"
    if not cfg.exists() and DEFAULT_CONFIG:
        safe_json_write(cfg, DEFAULT_CONFIG)

def write_license():
    lic = PROJ_DIR / "license/activation.json"
    if not lic.exists():
        lic_data = {
            "activation_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "license_key": "DEMO-30-DIAS",
            "notes": "Renove alterando activation_date ou use validação remota"
        }
        safe_json_write(lic, lic_data)

def finalize_message():
    print("\n[OK] Instalação / atualização concluída.")
    print("Para executar:")
    print(f"  cd {PROJ_DIR}")
    print(f"  {('venv\\\\Scripts\\\\python.exe' if os.name=='nt' else './venv/bin/python')} main.py")

def run_app():
    print("[INFO] Executando aplicação...")
    subprocess.run([str(venv_python()), "main.py"])

def main():
    banner()
    opts = parse_args()
    check_python()
    create_dirs()
    write_requirements()
    create_venv(force=bool(opts.get("force", False)))
    install_deps(upgrade=bool(opts.get("upgrade", False)))
    write_icon()
    write_init()
    write_default_config()
    write_license()
    finalize_message()
    if opts.get("run") or opts.get("only-run"):
        run_app()

if __name__ == "__main__":
    main()