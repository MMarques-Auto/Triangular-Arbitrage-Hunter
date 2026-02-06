import ccxt
import pandas as pd

binance = ccxt.binance()

mercados = binance.load_markets()
moedas_usdt = []
capital = 1
oportunidades = 0

for i in mercados:
    market = mercados[i]
    if (market['spot']) and (market['active']):
        base = market['base']
        quote = market['quote']
        if (quote == 'USDT'):
            moedas_usdt.append(base)

print(f"Moedas com emparelhamento em USDT: {len(moedas_usdt)}")

triangulos = []

for i in mercados:
    market = mercados[i]
    if (market['spot']) and (market['active']):
        base = market['base']
        quote = market['quote']
        if (base in moedas_usdt) and (quote in moedas_usdt):
            ficha = {
           'par_meio': i,
           'moeda_base': base,
           'moeda_quote': quote,
           'par_compra': quote + '/USDT',
           'par_venda': base + '/USDT',
            }
            triangulos.append(ficha)

tickers = binance.fetch_tickers()

for i in triangulos:
    preco_ask_1 = tickers[i['par_compra']]['ask']
    preco_ask_2 = tickers[i['par_meio']]['ask']
    preco_bid_3 = tickers[i['par_venda']]['bid']
    passo1 = capital/preco_ask_1
    passo2 = passo1/preco_ask_2
    passo3 = passo2*preco_bid_3
    lucro = (passo3 - 1) * 100
    if lucro > 0.1:
        print(f"[ALERTA] Oportunidade em {i['par_meio']}! Lucro: {lucro:.4f}%")
        oportunidades += 1

print(f"Varredura concluída. Encontramos {oportunidades} oportunidades positivas.")