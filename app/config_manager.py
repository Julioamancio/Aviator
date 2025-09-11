import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG: Dict[str, Any] = {
    "app": {
        "title": "Aviator Bot",
        "host": "127.0.0.1",
        "port": 8000
    },
    "platform": {
        "login_url": "https://estrelabet.com/ptb/bet/main",
        "game_url": "https://estrelabet.com/ptb/games/detail/casino/normal/7787",
        "cookie_button_xpath": "//*[@id='cookies-bottom-modal']/div/div[1]/a",
        "iframe_id": "gm-frm",
        "results_selector": ".result-history"
    },
    "strategy": {
        "name": "threshold",
        "threshold": 1.5,
        "risk_percent": 2.0,
        "max_consecutive_losses": 3
    },
    "license": {
        "activation_date": "2025-01-01",
        "note": "Ajuste conforme necessário"
    },
    "bot": {
        "engine": "selenium",
        "interval_seconds": 2
    }
}


class ConfigManager:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path("config/config.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.save(DEFAULT_CONFIG)

    def load(self) -> Dict[str, Any]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_CONFIG.copy()

    def save(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Helpers práticos
    def get(self, key: str, default: Any = None) -> Any:
        data = self.load()
        return data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        data = self.load()
        data[key] = value
        self.save(data)
