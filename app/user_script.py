"""
Integração do Usuário

Substitua a função `run_step` pelo conteúdo do seu script do Google Drive.
A função deve receber (config: dict, ctx: dict) e retornar um dict com o resultado da iteração.
"""
from __future__ import annotations
from typing import Any, Dict


def run_step(config: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    # Exemplo simplificado. Troque pela sua lógica.
    strat = config.get("strategy", {})
    thr = float(strat.get("threshold", 1.5))
    if thr > 1.2:
        action = "HOLD"
    else:
        action = "BUY"
    return {
        "action": action,
        "note": "Exemplo run_step; substitua pelo seu script.",
    }

