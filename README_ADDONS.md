# Recursos Avançados (v3.3)

Novos módulos:
- Validação remota de licença (license.remote_validation)
- Dashboard FastAPI (dashboard.enabled)
- Executor de ordens (order.mode = simulated/rest)
- Sistema de Plugins (pasta plugins/)
- Painel de Análise Avançada (histograma e heatmap)
- Analytics incremental

Endpoints Dashboard (padrão http://127.0.0.1:8008):
GET /status
GET /results
GET /plugins
POST /control {"action":"start"} ou {"action":"stop"}
POST /order {"side":"buy","amount":10}

Exemplo plugin: plugins/example_logger_plugin.py

Renovação de licença:
 - Ajuste activation_date ou use servidor remoto.

Para criar plugin:
```python
def register(api):
    api.on_signal(lambda results, desc, ctx: print("Sinal recebido", desc))
```