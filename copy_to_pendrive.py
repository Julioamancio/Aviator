#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Copiar Credenciais para Pen Drive - Aviator Bot
"""

import json
import shutil
from pathlib import Path

def main():
    print("="*60)
    print("    COPIAR CREDENCIAIS PARA PEN DRIVE - AVIATOR BOT")
    print("="*60)
    print()
    
    # Definir caminhos
    project_root = Path(__file__).parent
    local_aviator_folder = project_root / "AVIATOR"
    local_credentials_file = local_aviator_folder / "credentials.json"
    
    external_aviator_folder = Path("E:/AVIATOR")
    external_credentials_file = external_aviator_folder / "credentials.json"
    
    # Verificar se pen drive está disponível
    if not external_aviator_folder.parent.exists():
        print("❌ Pen drive E:\ não foi detectado!")
        print("📱 Conecte o pen drive na porta E:\ e tente novamente.")
        return False
    
    # Verificar se credenciais locais existem
    if not local_credentials_file.exists():
        print("❌ Arquivo de credenciais local não encontrado!")
        print(f"📁 Esperado em: {local_credentials_file}")
        print("🔧 Execute primeiro: python configure_credentials.py")
        return False
    
    print("✅ Pen drive E:\ detectado!")
    print(f"📁 Credenciais locais encontradas: {local_credentials_file}")
    print()
    
    # Mostrar informações das credenciais
    try:
        with open(local_credentials_file, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        username = credentials.get('username', 'Não configurado')
        if username == 'seu_usuario_aqui':
            username = 'Não configurado'
        
        print("📋 INFORMAÇÕES DAS CREDENCIAIS:")
        print("-" * 40)
        print(f"Usuário: {username}")
        print(f"Site: {credentials.get('site_config', {}).get('site_url', 'N/A')}")
        print(f"Estratégia: {credentials.get('betting_strategy', {}).get('strategy_type', 'N/A')}")
        print(f"Valor da aposta: R$ {credentials.get('betting_strategy', {}).get('amount', 0):.2f}")
        print()
        
    except Exception as e:
        print(f"⚠️ Erro ao ler credenciais: {e}")
        print("Continuando com a cópia...")
        print()
    
    # Verificar se já existe no pen drive
    if external_credentials_file.exists():
        print("⚠️ Já existem credenciais no pen drive!")
        print(f"📁 Localização: {external_credentials_file}")
        
        overwrite = input("Deseja sobrescrever as credenciais existentes? (s/N): ").lower().strip()
        if overwrite != 's':
            print("❌ Operação cancelada pelo usuário.")
            return False
        print()
    
    # Criar pasta no pen drive
    try:
        external_aviator_folder.mkdir(exist_ok=True, parents=True)
        print(f"📂 Pasta criada no pen drive: {external_aviator_folder}")
    except Exception as e:
        print(f"❌ Erro ao criar pasta no pen drive: {e}")
        return False
    
    # Copiar arquivo de credenciais
    try:
        shutil.copy2(local_credentials_file, external_credentials_file)
        print(f"✅ Credenciais copiadas com sucesso!")
        print(f"📁 De: {local_credentials_file}")
        print(f"📱 Para: {external_credentials_file}")
    except Exception as e:
        print(f"❌ Erro ao copiar credenciais: {e}")
        return False
    
    # Copiar README também
    local_readme = local_aviator_folder / "README.md"
    external_readme = external_aviator_folder / "README.md"
    
    if local_readme.exists():
        try:
            shutil.copy2(local_readme, external_readme)
            print(f"📖 README copiado: {external_readme}")
        except Exception as e:
            print(f"⚠️ Aviso: Erro ao copiar README: {e}")
    
    # Criar arquivo de informações no pen drive
    info_file = external_aviator_folder / "info.txt"
    try:
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write("AVIATOR BOT - CREDENCIAIS SEGURAS\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Data da cópia: {Path().cwd()}\n")
            f.write(f"Origem: {local_credentials_file}\n")
            f.write(f"Destino: {external_credentials_file}\n\n")
            f.write("IMPORTANTE:\n")
            f.write("- Mantenha este pen drive em local seguro\n")
            f.write("- Não compartilhe as credenciais\n")
            f.write("- Faça backup regularmente\n")
            f.write("- O bot usará automaticamente estas credenciais\n\n")
            f.write("Para usar:\n")
            f.write("1. Conecte o pen drive na porta E:\\\n")
            f.write("2. Execute o bot normalmente\n")
            f.write("3. O sistema detectará automaticamente as credenciais\n")
        
        print(f"📄 Arquivo de informações criado: {info_file}")
    except Exception as e:
        print(f"⚠️ Aviso: Erro ao criar arquivo de informações: {e}")
    
    print()
    print("🎉 CÓPIA CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print(f"📱 Credenciais no pen drive: {external_aviator_folder}")
    print("🔒 Mantenha o pen drive em local seguro")
    print("🚀 O bot usará automaticamente as credenciais do pen drive")
    print()
    print("💡 DICAS:")
    print("- Conecte o pen drive antes de iniciar o bot")
    print("- Se o pen drive não estiver conectado, o bot usará as credenciais locais")
    print("- Mantenha sempre um backup das credenciais")
    print("- Atualize as credenciais no pen drive quando necessário")
    print()
    
    return True

def verify_pendrive():
    """Verificar se o pen drive está conectado e tem as credenciais"""
    external_aviator_folder = Path("E:/AVIATOR")
    external_credentials_file = external_aviator_folder / "credentials.json"
    
    print("🔍 VERIFICAÇÃO DO PEN DRIVE")
    print("-" * 30)
    
    if not external_aviator_folder.parent.exists():
        print("❌ Pen drive E:\ não detectado")
        return False
    
    print("✅ Pen drive E:\ detectado")
    
    if not external_aviator_folder.exists():
        print("❌ Pasta AVIATOR não encontrada no pen drive")
        return False
    
    print("✅ Pasta AVIATOR encontrada")
    
    if not external_credentials_file.exists():
        print("❌ Arquivo de credenciais não encontrado no pen drive")
        return False
    
    print("✅ Arquivo de credenciais encontrado")
    
    try:
        with open(external_credentials_file, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        username = credentials.get('username', '')
        if username and username != 'seu_usuario_aqui':
            print(f"✅ Credenciais configuradas para: {username}")
            return True
        else:
            print("⚠️ Credenciais não configuradas no pen drive")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler credenciais: {e}")
        return False

if __name__ == "__main__":
    try:
        import sys
        
        if len(sys.argv) > 1 and sys.argv[1] == "--verify":
            verify_pendrive()
        else:
            main()
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")