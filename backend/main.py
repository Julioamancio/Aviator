#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aviator Bot Backend API
FastAPI backend para controle e configuração do bot Aviator
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

from bot_controller import AviatorBotController
from models import (
    BotConfig, 
    BotStatus, 
    SessionStats, 
    BettingStrategy,
    ElementConfig,
    LoginCredentials
)
from websocket_manager import ConnectionManager

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Gerenciador de conexões WebSocket
manager = ConnectionManager()

# Controlador do bot
bot_controller = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    global bot_controller
    bot_controller = AviatorBotController()
    logger.info("Backend iniciado")
    yield
    if bot_controller:
        await bot_controller.cleanup()
    logger.info("Backend finalizado")

# Criar aplicação FastAPI
app = FastAPI(
    title="Aviator Bot API",
    description="API para controle e configuração do bot Aviator",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de request/response
class ConfigUpdateRequest(BaseModel):
    site_url: Optional[str] = None
    game_url: Optional[str] = None
    headless: Optional[bool] = None
    wait_timeout: Optional[int] = None
    strategy_threshold: Optional[float] = None
    history_size: Optional[int] = None
    min_strategy_checks: Optional[int] = None

class ElementUpdateRequest(BaseModel):
    cookies_button: Optional[str] = None
    username_field: Optional[str] = None
    password_field: Optional[str] = None
    login_button: Optional[str] = None
    game_iframe: Optional[str] = None
    result_history: Optional[str] = None
    bet_input: Optional[str] = None
    bet_button: Optional[str] = None
    cashout_button: Optional[str] = None

class CredentialsRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class BettingRequest(BaseModel):
    amount: float = Field(..., gt=0)
    strategy: str = Field(..., regex="^(conservative|moderate|aggressive|custom)$")
    auto_cashout: Optional[float] = None
    max_loss: Optional[float] = None
    max_win: Optional[float] = None

# Endpoints da API

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {"message": "Aviator Bot API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "bot_status": bot_controller.get_status() if bot_controller else "not_initialized"
    }

# Endpoints de configuração

@app.get("/config", response_model=BotConfig)
async def get_config():
    """Obter configuração atual do bot"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    return bot_controller.get_config()

@app.put("/config")
async def update_config(config: ConfigUpdateRequest):
    """Atualizar configuração do bot"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    try:
        updated_config = bot_controller.update_config(config.dict(exclude_unset=True))
        await manager.broadcast({"type": "config_updated", "data": updated_config.dict()})
        return {"message": "Configuração atualizada com sucesso", "config": updated_config}
    except Exception as e:
        logger.error(f"Erro ao atualizar configuração: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/elements", response_model=ElementConfig)
async def get_elements():
    """Obter configuração de elementos"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    return bot_controller.get_elements()

@app.put("/elements")
async def update_elements(elements: ElementUpdateRequest):
    """Atualizar configuração de elementos"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    try:
        updated_elements = bot_controller.update_elements(elements.dict(exclude_unset=True))
        await manager.broadcast({"type": "elements_updated", "data": updated_elements.dict()})
        return {"message": "Elementos atualizados com sucesso", "elements": updated_elements}
    except Exception as e:
        logger.error(f"Erro ao atualizar elementos: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints de credenciais

@app.post("/credentials")
async def set_credentials(credentials: CredentialsRequest):
    """Definir credenciais de login"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    try:
        bot_controller.set_credentials(credentials.username, credentials.password)
        return {"message": "Credenciais definidas com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao definir credenciais: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints de controle do bot

@app.post("/bot/start")
async def start_bot(background_tasks: BackgroundTasks):
    """Iniciar o bot"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    if bot_controller.is_running():
        raise HTTPException(status_code=400, detail="Bot já está em execução")
    
    try:
        background_tasks.add_task(run_bot_with_updates)
        return {"message": "Bot iniciado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao iniciar bot: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bot/stop")
async def stop_bot():
    """Parar o bot"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    try:
        await bot_controller.stop()
        await manager.broadcast({"type": "bot_stopped", "data": {"timestamp": datetime.now().isoformat()}})
        return {"message": "Bot parado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao parar bot: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bot/status", response_model=BotStatus)
async def get_bot_status():
    """Obter status do bot"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    return bot_controller.get_detailed_status()

@app.get("/bot/stats", response_model=SessionStats)
async def get_session_stats():
    """Obter estatísticas da sessão"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    return bot_controller.get_session_stats()

# Endpoints de apostas

@app.post("/betting/start")
async def start_betting(betting_config: BettingRequest):
    """Iniciar apostas automáticas"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    if not bot_controller.is_running():
        raise HTTPException(status_code=400, detail="Bot deve estar em execução para iniciar apostas")
    
    try:
        strategy = BettingStrategy(
            amount=betting_config.amount,
            strategy_type=betting_config.strategy,
            auto_cashout=betting_config.auto_cashout,
            max_loss=betting_config.max_loss,
            max_win=betting_config.max_win
        )
        bot_controller.start_betting(strategy)
        await manager.broadcast({"type": "betting_started", "data": strategy.dict()})
        return {"message": "Apostas automáticas iniciadas", "strategy": strategy}
    except Exception as e:
        logger.error(f"Erro ao iniciar apostas: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/betting/stop")
async def stop_betting():
    """Parar apostas automáticas"""
    if not bot_controller:
        raise HTTPException(status_code=500, detail="Bot controller not initialized")
    
    try:
        bot_controller.stop_betting()
        await manager.broadcast({"type": "betting_stopped", "data": {"timestamp": datetime.now().isoformat()}})
        return {"message": "Apostas automáticas paradas"}
    except Exception as e:
        logger.error(f"Erro ao parar apostas: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints de logs

@app.get("/logs")
async def get_logs(lines: int = 100):
    """Obter logs do sistema"""
    try:
        if os.path.exists('backend.log'):
            with open('backend.log', 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                return {"logs": [line.strip() for line in recent_lines]}
        return {"logs": []}
    except Exception as e:
        logger.error(f"Erro ao obter logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket para atualizações em tempo real

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para atualizações em tempo real"""
    await manager.connect(websocket)
    try:
        while True:
            # Manter conexão ativa
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Funções auxiliares

async def run_bot_with_updates():
    """Executa o bot e envia atualizações via WebSocket"""
    try:
        await bot_controller.start()
        
        # Loop para enviar atualizações periódicas
        while bot_controller.is_running():
            status = bot_controller.get_detailed_status()
            stats = bot_controller.get_session_stats()
            
            await manager.broadcast({
                "type": "status_update",
                "data": {
                    "status": status.dict(),
                    "stats": stats.dict(),
                    "timestamp": datetime.now().isoformat()
                }
            })
            
            await asyncio.sleep(2)  # Atualizar a cada 2 segundos
            
    except Exception as e:
        logger.error(f"Erro durante execução do bot: {e}")
        await manager.broadcast({
            "type": "error",
            "data": {
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )