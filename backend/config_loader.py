#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carregador de configurações seguras do Aviator Bot
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Carregador de configurações seguras"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        
        # Prioridade: 1º Pen Drive E:\AVIATOR, 2º Pasta local AVIATOR
        self.external_aviator_folder = Path("E:/AVIATOR")
        self.local_aviator_folder = self.project_root / "AVIATOR"
        
        # Determinar qual pasta usar
        if self.external_aviator_folder.exists():
            self.aviator_folder = self.external_aviator_folder
            logger.info(f"Usando credenciais do pen drive: {self.aviator_folder}")
        else:
            self.aviator_folder = self.local_aviator_folder
            logger.info(f"Usando credenciais locais: {self.aviator_folder}")
            
        self.credentials_file = self.aviator_folder / "credentials.json"
        
    def ensure_aviator_folder(self) -> bool:
        """Garante que a pasta AVIATOR existe"""
        try:
            self.aviator_folder.mkdir(exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Erro ao criar pasta AVIATOR: {e}")
            return False
    
    def load_credentials(self) -> Optional[Dict[str, Any]]:
        """Carrega as credenciais do arquivo seguro"""
        try:
            if not self.credentials_file.exists():
                logger.warning(f"Arquivo de credenciais não encontrado: {self.credentials_file}")
                return None
                
            with open(self.credentials_file, 'r', encoding='utf-8') as f:
                credentials = json.load(f)
                
            # Validar se as credenciais foram configuradas
            if credentials.get('username') == 'seu_usuario_aqui':
                logger.warning("Credenciais não foram configuradas ainda")
                return None
                
            logger.info("Credenciais carregadas com sucesso")
            return credentials
            
        except Exception as e:
            logger.error(f"Erro ao carregar credenciais: {e}")
            return None
    
    def save_credentials(self, credentials: Dict[str, Any]) -> bool:
        """Salva as credenciais no arquivo seguro"""
        try:
            self.ensure_aviator_folder()
            
            with open(self.credentials_file, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, indent=2, ensure_ascii=False)
                
            logger.info("Credenciais salvas com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar credenciais: {e}")
            return False
    
    def get_bot_config(self) -> Dict[str, Any]:
        """Retorna configuração do bot"""
        credentials = self.load_credentials()
        if not credentials:
            return self._get_default_config()
            
        return credentials.get('bot_settings', self._get_default_config())
    
    def get_element_config(self) -> Dict[str, Any]:
        """Retorna configuração de elementos"""
        credentials = self.load_credentials()
        if not credentials:
            return self._get_default_elements()
            
        return credentials.get('elements', self._get_default_elements())
    
    def get_login_credentials(self) -> Optional[Dict[str, str]]:
        """Retorna credenciais de login"""
        credentials = self.load_credentials()
        if not credentials:
            return None
            
        username = credentials.get('username')
        password = credentials.get('password')
        
        if not username or not password or username == 'seu_usuario_aqui':
            return None
            
        return {
            'username': username,
            'password': password
        }
    
    def get_betting_strategy(self) -> Dict[str, Any]:
        """Retorna estratégia de apostas"""
        credentials = self.load_credentials()
        if not credentials:
            return self._get_default_strategy()
            
        return credentials.get('betting_strategy', self._get_default_strategy())
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Configuração padrão do bot"""
        return {
            "site_url": "https://1-wins.br.com/",
            "game_url": "https://1-wins.br.com/casino/game/aviator",
            "headless": False,
            "wait_timeout": 30,
            "strategy_threshold": 2.0,
            "history_size": 10,
            "min_strategy_checks": 4,
            "update_interval": 2,
            "max_retries": 3
        }
    
    def _get_default_elements(self) -> Dict[str, Any]:
        """Elementos padrão da página 1Win"""
        return {
            "cookies_button": "//button[contains(text(), 'Aceitar') or contains(text(), 'Accept')]",
            "username_field": "//input[@type='email' or @placeholder*='email' or @placeholder*='usuário']",
            "password_field": "//input[@type='password' or @placeholder*='senha']",
            "login_button": "//button[contains(text(), 'Entrar') or contains(text(), 'Login')]",
            "game_iframe": "game-iframe",
            "result_history": "game-history",
            "bet_input": "//input[@placeholder*='aposta' or @class*='bet-input']",
            "bet_button": "//button[contains(text(), 'Apostar') or contains(@class, 'bet-button')]",
            "cashout_button": "//button[contains(text(), 'Retirar') or contains(@class, 'cashout')]",
            "multiplier_display": "//*[contains(@class, 'multiplier') or contains(@class, 'coefficient')]",
            "balance_display": "//*[contains(@class, 'balance') or contains(text(), 'R$')]"
        }
    
    def _get_default_strategy(self) -> Dict[str, Any]:
        """Estratégia padrão de apostas"""
        return {
            "amount": 1.0,
            "strategy_type": "conservative",
            "auto_cashout": 2.0,
            "max_loss": 50.0,
            "max_win": 100.0,
            "stop_on_loss": True,
            "stop_on_win": True,
            "progressive_betting": False,
            "progression_factor": 1.5,
            "reset_on_win": True
        }
    
    def update_config(self, section: str, config: Dict[str, Any]) -> bool:
        """Atualiza uma seção específica da configuração"""
        try:
            credentials = self.load_credentials() or {}
            credentials[section] = config
            return self.save_credentials(credentials)
        except Exception as e:
            logger.error(f"Erro ao atualizar configuração {section}: {e}")
            return False
    
    def is_configured(self) -> bool:
        """Verifica se as credenciais foram configuradas"""
        credentials = self.load_credentials()
        if not credentials:
            return False
            
        username = credentials.get('username')
        return username and username != 'seu_usuario_aqui'

# Instância global
config_loader = ConfigLoader()