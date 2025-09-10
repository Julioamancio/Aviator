# Aviator Bot — Flask UI + Render

Aplicação Flask profissional com dashboard, controle do bot (start/stop), edição de configuração e visualização de logs. Preparado para deploy no Render.com.

Seus scripts/estratégias podem ser integrados editando `app/user_script.py` (ou apontando `bot.script_path` em Configuração) e implementando a função `run_step(config, ctx) -> dict`.

## Requisitos
- Python 3.10+ (Render usa 3.11 por padrão)

## Instalação local
```bash
python -m venv venv
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python run.py
# abra http://127.0.0.1:8000
```

## Estrutura
- `wsgi.py`: ponto de entrada para produção (Render)
- `run.py`: execução local com debug
- `app/`: pacote da aplicação
  - `__init__.py`: factory do Flask (+ logs)
  - `routes.py`: rotas e APIs
  - `config_manager.py`: persistência JSON em `config/config.json`
  - `bot_service.py`: serviço do bot em thread (start/stop, logs, status)
  - `user_script.py`: ponto para colar sua lógica
- `templates/` e `static/`: UI

## Como integrar seu script
Cole seu código em `app/user_script.py` e exponha:
```python
def run_step(config: dict, ctx: dict) -> dict:
    # sua lógica aqui
    return {"ok": True}
```
Ou aponte o caminho do arquivo na tela Configuração (campo "Caminho do Script").

## Deploy no Render.com
1) Crie um novo Web Service no Render apontando para este repositório.
2) Render detectará `render.yaml` e aplicará:
   - build: `pip install -r requirements.txt`
   - start: `gunicorn -w 1 -k gthread -b 0.0.0.0:$PORT wsgi:app`
3) Health check em `/health`.

Variáveis úteis (opcionais):
- `PYTHON_VERSION=3.11`

## Endpoints
- `GET /` Dashboard
- `POST /start` Inicia bot
- `POST /stop` Para bot
- `GET/POST /config` Edita config
- `GET /logs` Logs UI
- `GET /health` Health check
- `GET /api/status` JSON status
- `GET /api/logs` JSON logs

## Aviso
Esta UI não executa Selenium/GUI; para usar seu script original (Drive), cole a lógica em `app/user_script.py` ou ajuste `script_path`. Em ambientes como Render, rodar navegadores exige setup adicional (headless e binários), não incluído aqui.
