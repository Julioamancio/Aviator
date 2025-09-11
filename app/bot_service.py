import importlib.util
import logging
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from .config_manager import ConfigManager


log = logging.getLogger("BotService")


def _load_user_callable(script_path: Path) -> Optional[Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]]:
    if not script_path.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("user_script", script_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        fn = getattr(module, "run_step", None)
        if callable(fn):
            return fn  # type: ignore[return-value]
        return None
    except Exception as e:
        log.exception("Falha carregando script do usuário: %s", e)
        return None


@dataclass
class BotState:
    running: bool = False
    started_at: float = 0.0
    iterations: int = 0
    last_result: Dict[str, Any] = field(default_factory=dict)
    logs: deque[str] = field(default_factory=lambda: deque(maxlen=300))


class BotService:
    def __init__(self, cfg: ConfigManager, user_id: int) -> None:
        self.cfg = cfg
        self.user_id = user_id
        self.state = BotState()
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    # Public API
    def start(self) -> bool:
        if self.state.running:
            return False
        self._stop.clear()
        self.state.running = True
        self.state.started_at = time.time()
        # Choose loop by engine
        try:
            engine = self.cfg.load().get("bot", {}).get("engine", "selenium")
        except Exception:
            engine = "selenium"
        target = self._run_loop_selenium if engine == "selenium" else self._run_loop
        self._thread = threading.Thread(target=target, name="BotThread", daemon=True)
        self._thread.start()
        self._emit("Bot iniciado.")
        return True

    def stop(self) -> bool:
        if not self.state.running:
            return False
        self._stop.set()
        t = self._thread
        if t and t.is_alive():
            t.join(timeout=10)
        self.state.running = False
        self._emit("Bot parado.")
        return True

    def status(self) -> Dict[str, Any]:
        data = self.cfg.load()
        return {
            "running": self.state.running,
            "started_at": self.state.started_at,
            "uptime_sec": (time.time() - self.state.started_at) if self.state.running else 0,
            "iterations": self.state.iterations,
            "last_result": self.state.last_result,
            "config": data,
        }

    def tail_logs(self, n: int = 200) -> list[str]:
        return list(self.state.logs)[-n:]

    # Internal
    def _emit(self, msg: str) -> None:
        log.info(msg)
        self.state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def _run_loop_selenium(self) -> None:
        data = self.cfg.load()
        bot_cfg = data.get("bot", {})
        interval = float(bot_cfg.get("interval_seconds", 2))
        try:
            from .selenium_bot import run_selenium_bot

            def set_result(res: Dict[str, Any]) -> None:
                self.state.last_result = res or {}

            run_selenium_bot(self.cfg, self.user_id, self._stop, self._emit, set_result)
        except Exception as e:
            self._emit(f"Selenium loop error: {e}")
        finally:
            self._emit("Loop finalizado.")

    def _run_loop(self) -> None:
        data = self.cfg.load()
        bot_cfg = data.get("bot", {})
        script_path = Path(bot_cfg.get("script_path", "app/user_script.py"))
        interval = float(bot_cfg.get("interval_seconds", 2))
        user_fn = _load_user_callable(script_path)
        if not user_fn:
            self._emit(f"Script do usuário não encontrado ou inválido: {script_path}")
            self._emit("Usando estratégia placeholder interna.")

        ctx: Dict[str, Any] = {
            "start_time": time.time(),
            "notes": "ctx compartilhado para o script"
        }
        try:
            while not self._stop.is_set():
                self.state.iterations += 1
                try:
                    if user_fn:
                        result = user_fn(data, ctx)
                    else:
                        result = self._placeholder_step(data, ctx)
                    self.state.last_result = result or {}
                    self._emit(f"Step #{self.state.iterations} -> {result}")
                except Exception as step_err:
                    self._emit(f"Erro no step: {step_err}")
                    log.exception("Erro step")
                # Sleep respecting stop event
                self._stop.wait(interval)
        finally:
            self._emit("Loop finalizado.")

    @staticmethod
    def _placeholder_step(config: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        strat = config.get("strategy", {})
        thr = float(strat.get("threshold", 1.5))
        risk = float(strat.get("risk_percent", 2.0))
        # Apenas um resultado simulado
        return {
            "action": "HOLD" if thr >= 1.0 else "BUY",
            "risk": risk,
            "score": round(thr * 0.66, 3),
        }


class BotManager:
    """Gerencia instâncias de BotService por usuário."""

    def __init__(self, cfg: ConfigManager) -> None:
        self.cfg = cfg
        self._services: dict[int, BotService] = {}
        self._lock = threading.Lock()

    def get_service(self, user_id: int) -> BotService:
        with self._lock:
            svc = self._services.get(user_id)
            if not svc:
                svc = BotService(self.cfg, user_id)
                self._services[user_id] = svc
            return svc
