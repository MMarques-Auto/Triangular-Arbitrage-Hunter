import asyncio
import time

from core import exchange, scanner, logic
from utils import alerts
import config
import core.database as db

async def main():

    print("--- Iniciando Bot ---")

    binance = exchange.get_binance_connection()
    triangulos = await scanner.scanner(binance)

    print(f"Monitorando {len(triangulos)} rotas | R${config.capital_atual}")
    alerts.enviar_telegram(f"🚀🚀 Bot iniciado | R${config.capital_atual} 🚀🚀")

    db.get_connection()
    db.init_db()

    while True:
        try:
            tickers = await binance.fetch_tickers()
            for t in triangulos:
                par_compra = t['par_compra']
                par_meio = t['par_meio']
                par_venda = t['par_venda']

                if par_compra not in tickers or par_meio not in tickers or par_venda not in tickers:
                    continue

                try:
                    p1 = float(tickers[par_compra]['ask']) # type: ignore
                    p2 = float(tickers[par_meio]['ask']) # type: ignore
                    p3 = float(tickers[par_venda]['bid']) # type: ignore
                except:
                    continue

                resultado = logic.calc(config.capital_atual, p1, p2, p3)

                # FILTRO 1: Lucro Mínimo (> 0.3%)
                if resultado['valido'] is True and 5.0 > resultado['lucro_pct'] > 0.3:
                    
                    print(f"🔍 Auditando preços reais: {t['moeda_base']} -> {t['moeda_quote']} (Ticker: {resultado['lucro_pct']:.2f}%)")
                    
                    # 1. Pega Preço Real da Entrada
                    p1_real = await exchange.obter_preco_medio(binance, par_compra, 'buy', config.capital_atual)
                    
                    if p1_real:
                        # 2. Pega Preço Real do Meio (Usando p3 do ticker como base de conversão)
                        p2_real = await exchange.obter_preco_medio(binance, par_meio, 'sell', config.capital_atual, p3)
                        
                        if p2_real:
                            # 3. Pega Preço Real da Saída
                            p3_real = await exchange.obter_preco_medio(binance, par_venda, 'sell', config.capital_atual)
                            
                            if p3_real:
                                # AGORA A HORA DA VERDADE: Recalcula com os preços do Order Book
                                resultado_real = logic.calc(config.capital_atual, p1_real, p2_real, p3_real)
                                
                                # Só aceita se AINDA DER LUCRO depois de ver o preço real
                                if resultado_real['valido'] is True and resultado_real['lucro_pct'] > 0.0:
                                    
                                    msg = (
                                        f"💎 OPORTUNIDADE REAL CONFIRMADA (Auditada)!\n"
                                        f"Rota: {t['moeda_base']} -> {t['moeda_quote']}\n"
                                        f"Lucro Ticker: {resultado['lucro_pct']:.2f}%\n"
                                        f"Lucro REAL: {resultado_real['lucro_pct']:.2f}% (Est. ${resultado_real['lucro_valor']:.2f})"
                                    )
                                    print(msg)
                                    db.save(t,resultado['lucro_pct'], resultado_real, "REAL", "Confirmed Profit")
                                    alerts.enviar_telegram(msg)

                                else:
                                    print(f"📉 Alarme Falso: Lucro sumiu no Order Book ({resultado_real['lucro_pct']:.2f}%)")
                                    db.save(t, resultado['lucro_pct'], resultado_real, "FALSO", "Slippage no Order Book")
                            
                            else:
                                print(f"❌ Sem liquidez na Saída ({par_venda})")
                        else:
                            print(f"❌ Sem liquidez no Meio ({par_meio})")
                    else:
                        print(f"❌ Sem liquidez na Entrada ({par_compra})")
        except Exception as e:
            print(f"Erro no Loop: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        msg_final = ("Robô parado pelo usuário")
        print(msg_final)
        alerts.enviar_telegram(msg_final)