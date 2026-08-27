# Twitter/X Data Miner & Streamer (API v2)

Aplicação unificada em Python para extração de dados da plataforma X (Twitter) utilizando a biblioteca Tweepy e a API v2 oficial.

## 📌 Recursos

- **Modo Search**: Busca REST por tweets recentes dos últimos 7 dias.
- **Modo Stream**: Conexão persistente para captura contínua em tempo real e armazenamento em formato JSON.
- **Segurança**: Variáveis de ambiente isoladas via `dotenv` mantendo tokens privados protegidos fora do versionamento.

## 🚀 Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure suas credenciais:
Crie um arquivo `.env` baseado no `.env.example` e adicione seu `BEARER_TOKEN`.

3. Execute no modo desejado:

```bash
# Para buscar os últimos tweets (busca pontual):
python app.py --mode search --tag #python

# Para escutar tweets ao vivo (streaming):
python app.py --mode stream --tag #python
```
