#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de WebSocket para comunicação em tempo real
"""

import json
import logging
from typing import List, Dict, Any
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Gerencia conexões WebSocket"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Aceita uma nova conexão WebSocket"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nova conexão WebSocket estabelecida. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove uma conexão WebSocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Conexão WebSocket removida. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Envia mensagem para uma conexão específica"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem pessoal: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Envia mensagem para todas as conexões ativas"""
        if not self.active_connections:
            return
        
        message_str = json.dumps(message, default=str)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Erro ao enviar broadcast: {e}")
                disconnected.append(connection)
        
        # Remove conexões que falharam
        for connection in disconnected:
            self.disconnect(connection)
    
    def get_connection_count(self) -> int:
        """Retorna o número de conexões ativas"""
        return len(self.active_connections)