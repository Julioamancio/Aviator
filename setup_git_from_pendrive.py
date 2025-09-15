#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Configurar Git em Nova Máquina - Aviator Bot
"""

import json
import subprocess
import sys
from pathlib import Path

def run_command(command):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("="*60)
    print("    CONFIGURAR GIT EM NOVA MÁQUINA - AVIATOR BOT")
    print("="*60)
    print()
    
    # Verificar se pen drive está disponível
    pen_drive_path = Path("E:/AVIATOR")
    git_credentials_file = pen_drive_path / "git_credentials.json"
    
    if not pen_drive_path.exists():
        print("❌ Pen drive E:\\ não foi detectado!")
        print("📱 Conecte o pen drive na porta E:\\ e tente novamente.")
        return False
    
    if not git_credentials_file.exists():
        print("❌ Arquivo de credenciais do Git não encontrado no pen drive!")
        print(f"📁 Esperado em: {git_credentials_file}")
        return False
    
    print("✅ Pen drive E:\\ detectado!")
    print(f"📁 Credenciais do Git encontradas: {git_credentials_file}")
    print()
    
    # Carregar credenciais do Git
    try:
        with open(git_credentials_file, 'r', encoding='utf-8') as f:
            git_data = json.load(f)
        
        git_config = git_data.get('git_config', {})
        github_info = git_data.get('github_info', {})
        
        print("📋 INFORMAÇÕES DO GIT:")
        print("-" * 40)
        print(f"Nome: {git_config.get('user.name', 'N/A')}")
        print(f"Email: {git_config.get('user.email', 'N/A')}")
        print(f"Repositório: {github_info.get('repository', 'N/A')}")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao ler credenciais do Git: {e}")
        return False
    
    # Verificar se Git está instalado
    print("🔍 Verificando instalação do Git...")
    success, stdout, stderr = run_command("git --version")
    
    if not success:
        print("❌ Git não está instalado nesta máquina!")
        print("📥 Instale o Git primeiro:")
        print("   - Windows: https://git-scm.com/download/win")
        print("   - Linux: sudo apt install git")
        print("   - macOS: brew install git")
        return False
    
    print(f"✅ Git encontrado: {stdout.strip()}")
    print()
    
    # Configurar Git
    print("⚙️ CONFIGURANDO GIT...")
    print("-" * 40)
    
    # Configurar nome
    user_name = git_config.get('user.name')
    if user_name:
        print(f"📝 Configurando nome: {user_name}")
        success, stdout, stderr = run_command(f'git config --global user.name "{user_name}"')
        if success:
            print("✅ Nome configurado com sucesso")
        else:
            print(f"❌ Erro ao configurar nome: {stderr}")
    
    # Configurar email
    user_email = git_config.get('user.email')
    if user_email:
        print(f"📧 Configurando email: {user_email}")
        success, stdout, stderr = run_command(f'git config --global user.email "{user_email}"')
        if success:
            print("✅ Email configurado com sucesso")
        else:
            print(f"❌ Erro ao configurar email: {stderr}")
    
    print()
    
    # Verificar configuração
    print("🔍 VERIFICANDO CONFIGURAÇÃO...")
    print("-" * 40)
    
    success, stdout, stderr = run_command("git config --global user.name")
    if success:
        print(f"✅ Nome configurado: {stdout.strip()}")
    
    success, stdout, stderr = run_command("git config --global user.email")
    if success:
        print(f"✅ Email configurado: {stdout.strip()}")
    
    print()
    
    # Mostrar comandos úteis
    print("📋 COMANDOS ÚTEIS PARA USAR:")
    print("=" * 60)
    
    repository_url = github_info.get('repository')
    if repository_url:
        print(f"📥 Para clonar o repositório:")
        print(f"   git clone {repository_url}")
        print()
    
    print("📝 Comandos básicos do Git:")
    print("   git status              # Ver status dos arquivos")
    print("   git add .               # Adicionar todos os arquivos")
    print("   git commit -m \"msg\"     # Fazer commit")
    print("   git push                # Enviar para GitHub")
    print("   git pull                # Baixar do GitHub")
    print()
    
    print("🔧 Para configurar um projeto existente:")
    if repository_url:
        print(f"   git remote add origin {repository_url}")
        print("   git branch -M main")
        print("   git push -u origin main")
    print()
    
    # Perguntar se quer clonar o repositório
    if repository_url:
        clone_choice = input("Deseja clonar o repositório Aviator agora? (s/N): ").lower().strip()
        if clone_choice == 's':
            print("\n📥 Clonando repositório...")
            success, stdout, stderr = run_command(f"git clone {repository_url}")
            if success:
                print("✅ Repositório clonado com sucesso!")
                print(f"📁 Localização: ./Aviator")
                print("\n🚀 Próximos passos:")
                print("   1. cd Aviator")
                print("   2. python configure_credentials.py")
                print("   3. cd backend && python main.py")
            else:
                print(f"❌ Erro ao clonar: {stderr}")
    
    print()
    print("🎉 CONFIGURAÇÃO DO GIT CONCLUÍDA!")
    print("=" * 60)
    print("✅ Git configurado com suas credenciais")
    print("📱 Credenciais carregadas do pen drive")
    print("🚀 Pronto para usar Git e GitHub")
    print()
    print("💡 DICAS:")
    print("- Mantenha o pen drive seguro")
    print("- Use este script em qualquer máquina nova")
    print("- Suas credenciais ficam sempre sincronizadas")
    print()
    
    return True

def show_help():
    """Mostra ajuda sobre o script"""
    print("📖 AJUDA - Setup Git from Pen Drive")
    print("=" * 50)
    print("Este script configura o Git em uma nova máquina")
    print("usando as credenciais salvas no pen drive E:\\AVIATOR")
    print()
    print("📋 Pré-requisitos:")
    print("- Git instalado na máquina")
    print("- Pen drive conectado na porta E:\\")
    print("- Arquivo git_credentials.json no pen drive")
    print()
    print("🚀 Como usar:")
    print("   python setup_git_from_pendrive.py")
    print()
    print("🔧 O que o script faz:")
    print("- Verifica se Git está instalado")
    print("- Carrega credenciais do pen drive")
    print("- Configura user.name e user.email")
    print("- Oferece opção para clonar repositório")
    print("- Mostra comandos úteis")
    print()

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
            show_help()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")