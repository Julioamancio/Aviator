#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Launcher v3.3
 - Logging + Rotação
 - Licença local + remota
 - Carregamento robusto GUI
"""

import sys
import logging
from pathlib import Path
import importlib.util

from src.utils.config_manager import ConfigManager
from src.utils.logging_setup import setup_logging
from src.utils.license_manager import LicenseManager


def _import_gui():
    try:
        from src.gui.main_app import AviatorGUI
        return AviatorGUI
    except Exception as e:
        logging.error("Falha ao importar GUI: %s", e)
        return None

def main():
    cfg = ConfigManager()
    setup_logging(cfg.as_dict(), console_level=logging.INFO)
    log = logging.getLogger("Launcher")

    lic_cfg = cfg.get("license", default={}) or {}
    remote_cfg = lic_cfg.get("remote_validation", {}) or {}
    lm = LicenseManager(
        grace_days=lic_cfg.get("grace_days", 30),
        allow_run_if_missing=lic_cfg.get("allow_run_if_missing", True),
        remote_cfg=remote_cfg
    )
    log.info(lm.summary())
    if not lm.is_local_valid():
        log.error("LICENÇA LOCAL EXPIRADA. Ajuste activation_date.")
        input("Enter para sair...")
        return
    if remote_cfg.get("enabled", False):
        if not lm.remote_validate():
            status = lm.remote_status()
            log.error("Falha licença remota: %s", status[1] if status else "sem detalhe")
            if not remote_cfg.get("fail_open", True):
                input("Enter para sair...")
                return
        else:
            log.info("Licença remota OK: %s", (lm.remote_status() or ("", ""))[1])

    GuiClass = _import_gui()
    if not GuiClass:
        input("Enter para sair...")
        return

    app = GuiClass()
    app.run()

if __name__ == "__main__":
    main()