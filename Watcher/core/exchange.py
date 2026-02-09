import config
import ccxt.async_support as ccxt
import certifi

def get_binance_connection():

    print("[Exchange] Iniciando conexão com a Binance...")

    binance = ccxt.binance({
#        'apiKey': config.BINANCE_API_KEY,
#        'secret': config.BINANCE_SECRET_KEY,
        'enableRateLimit': True,
        'timeout': 30000,
        'options': {'defaultType': 'spot'},
    })

    return binance

async def obter_preco_medio(binance, par, lado, capital_necessario, preco_para_usdt=1.0):

    try:
        orderbook = await binance.fetch_order_book(par, limit=10)
        fila = orderbook['asks'] if lado == 'buy' else orderbook['bids']
        
        volume_acumulado = 0.0
        custo_acumulado = 0.0
        qtd_total_necessaria = 0.0
        volume_usdt_encontrado = 0.0
        
        for preco, qtd in fila:
            valor_desta_ordem_usdt = (preco * qtd) * preco_para_usdt
            volume_usdt_encontrado += valor_desta_ordem_usdt
            
            # Se achamos liquidez suficiente para cobrir os $100
            if volume_usdt_encontrado >= capital_necessario:
                return preco # Retorna o preço real de execução desta faixa
                
        return None

    except Exception as e:
        print(f"[ERRO LIQUIDEZ] Falha em {par}: {e}")
        return None