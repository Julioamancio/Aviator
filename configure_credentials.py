#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Configuração Segura de Credenciais - Aviator Bot
"""

import json
import os
import getpass
from pathlib import Path

def main():
    print("="*60)
    print("    CONFIGURAÇÃO SEGURA DE CREDENCIAIS - AVIATOR BOT")
    print("="*60)
    print()
    
    # Definir caminhos - Prioridade: 1º Pen Drive E:\AVIATOR, 2º Pasta local AVIATOR
    project_root = Path(__file__).parent
    external_aviator_folder = Path("E:/AVIATOR")
    local_aviator_folder = project_root / "AVIATOR"
    
    # Verificar se pen drive está disponível
    pen_drive_available = external_aviator_folder.parent.exists()
    
    if pen_drive_available:
        print("📱 Pen drive E:\ detectado!")
        use_pen_drive = input("Deseja usar o pen drive E:\\AVIATOR para as credenciais? (S/n): ").lower().strip()
        if use_pen_drive != 'n':
            aviator_folder = external_aviator_folder
            print(f"✅ Usando pen drive: {aviator_folder}")
        else:
            aviator_folder = local_aviator_folder
            print(f"📁 Usando pasta local: {aviator_folder}")
    else:
        aviator_folder = local_aviator_folder
        print(f"📁 Pen drive não detectado. Usando pasta local: {aviator_folder}")
    
    credentials_file = aviator_folder / "credentials.json"
    
    # Criar pasta AVIATOR se não existir
    try:
        aviator_folder.mkdir(exist_ok=True, parents=True)
        print(f"📂 Pasta criada/verificada: {aviator_folder}")
    except Exception as e:
        print(f"❌ Erro ao criar pasta {aviator_folder}: {e}")
        print("🔄 Tentando usar pasta local como fallback...")
        aviator_folder = local_aviator_folder
        credentials_file = aviator_folder / "credentials.json"
        aviator_folder.mkdir(exist_ok=True, parents=True)
    
    # Carregar configuração existente ou criar nova
    if credentials_file.exists():
        print("📁 Arquivo de credenciais encontrado. Carregando configuração atual...")
        with open(credentials_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        print("📝 Criando nova configuração de credenciais...")
        config = {
            "username": "",
            "password": "",
            "site_config": {
                "site_url": "https://1-wins.br.com/",
                "game_url": "https://1-wins.br.com/casino/game/aviator"
            },
            "bot_settings": {
                "headless": False,
                "wait_timeout": 30,
                "strategy_threshold": 2.0,
                "history_size": 10,
                "min_strategy_checks": 4,
                "update_interval": 2,
                "max_retries": 3
            },
            "elements": {
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
            },
            "betting_strategy": {
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
        }
    
    print()
    print("🔐 CONFIGURAÇÃO DE CREDENCIAIS")
    print("-" * 40)
    
    # Configurar credenciais
    current_username = config.get('username', '')
    if current_username and current_username != 'seu_usuario_aqui':
        print(f"Usuário atual: {current_username}")
        change = input("Deseja alterar o usuário? (s/N): ").lower().strip()
        if change == 's':
            username = input("Digite seu nome de usuário: ").strip()
            config['username'] = username
    else:
        username = input("Digite seu nome de usuário: ").strip()
        config['username'] = username
    
    # Senha (sempre pergunta por segurança)
    print("\n🔑 Digite sua senha (não será exibida):")
    password = getpass.getpass("Senha: ")
    if password.strip():
        config['password'] = password.strip()
    
    print()
    print("⚙️ CONFIGURAÇÕES DO BOT")
    print("-" * 40)
    
    # Configurações básicas
    print(f"URL do Site: {config['site_config']['site_url']}")
    change_url = input("Deseja alterar a URL do site? (s/N): ").lower().strip()
    if change_url == 's':
        new_url = input("Nova URL do site: ").strip()
        if new_url:
            config['site_config']['site_url'] = new_url
    
    print(f"\nURL do Jogo: {config['site_config']['game_url']}")
    change_game_url = input("Deseja alterar a URL do jogo? (s/N): ").lower().strip()
    if change_game_url == 's':
        new_game_url = input("Nova URL do jogo: ").strip()
        if new_game_url:
            config['site_config']['game_url'] = new_game_url
    
    # Modo headless
    current_headless = config['bot_settings']['headless']
    print(f"\nModo Headless (sem interface): {'Sim' if current_headless else 'Não'}")
    change_headless = input("Deseja alterar? (s/N): ").lower().strip()
    if change_headless == 's':
        headless_choice = input("Ativar modo headless? (s/N): ").lower().strip()
        config['bot_settings']['headless'] = headless_choice == 's'
    
    print()
    print("🎰 ESTRATÉGIA DE APOSTAS")
    print("-" * 40)
    
    # Estratégia de apostas
    strategy = config['betting_strategy']
    print(f"Valor da aposta: R$ {strategy['amount']:.2f}")
    change_amount = input("Deseja alterar? (s/N): ").lower().strip()
    if change_amount == 's':
        try:
            new_amount = float(input("Novo valor da aposta (R$): "))
            if new_amount > 0:
                strategy['amount'] = new_amount
        except ValueError:
            print("Valor inválido, mantendo o atual.")
    
    print(f"\nCashout automático: {strategy['auto_cashout']:.1f}x")
    change_cashout = input("Deseja alterar? (s/N): ").lower().strip()
    if change_cashout == 's':
        try:
            new_cashout = float(input("Novo multiplicador para cashout: "))
            if new_cashout >= 1.1:
                strategy['auto_cashout'] = new_cashout
        except ValueError:
            print("Valor inválido, mantendo o atual.")
    
    print(f"\nPerda máxima: R$ {strategy['max_loss']:.2f}")
    change_max_loss = input("Deseja alterar? (s/N): ").lower().strip()
    if change_max_loss == 's':
        try:
            new_max_loss = float(input("Nova perda máxima (R$): "))
            if new_max_loss > 0:
                strategy['max_loss'] = new_max_loss
        except ValueError:
            print("Valor inválido, mantendo o atual.")
    
    # Adicionar informações de segurança
    config['_security_info'] = {
        "location": "AVIATOR/credentials.json",
        "purpose": "Credenciais e configurações seguras fora do controle de versão",
        "protected_by": ".gitignore",
        "last_updated": "2025-01-15"
    }
    
    config['_instructions'] = {
        "pt": "Este arquivo contém suas credenciais reais e está protegido pelo .gitignore",
        "en": "This file contains your real credentials and is protected by .gitignore",
        "warning": "NUNCA compartilhe este arquivo ou faça commit dele no Git!"
    }
    
    # Salvar configuração
    try:
        with open(credentials_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print()
        print("✅ CONFIGURAÇÃO SALVA COM SUCESSO!")
        print("="*60)
        print(f"📁 Arquivo salvo em: {credentials_file}")
        print("🔒 Arquivo protegido pelo .gitignore (não será enviado ao Git)")
        print("🚀 Agora você pode executar o bot com suas configurações!")
        print()
        print("Para iniciar o bot:")
        print("1. Backend: cd backend && python main.py")
        print("2. Frontend: cd frontend && npm start")
        print("3. Acesse: http://localhost:3000")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao salvar configuração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")