import requests
import config

def enviar_telegram(mensagem):

    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[ALERTA] Token ou Chat ID não configurados")
        return
    
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload, timeout=3)
    except Exception as e:
        print(f"[ERRO TELEGRAM] Falha ao enviar: {e}")