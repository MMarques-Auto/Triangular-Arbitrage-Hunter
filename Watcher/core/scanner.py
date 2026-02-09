import asyncio

async def scanner(binance):
    print("[CONEXÃO] Carregando mercados...")
    mercados = await binance.load_markets()
    print(f"[CONEXÃO] {len(mercados)} mercados carregados. Iniciando varredura.")

    # Mapeamento de Pares
    triangulos = []
    moedas_usdt = set()

    stables = [
         'EUR', 'GBP', 'AUD', 'BRL', 'TRY', 'RUB', 'NGN', 'ZAR', 'UAH', 'PLN', 'RON', 'ARS',
        'BIDR', 'IDRT', 'USDC', 'TUSD', 'USDP', 'FDUSD', 'DAI'
    ]
            
    for s, m in mercados.items():
        if m['spot'] and m['active'] and m['quote'] == 'USDT':
                    moedas_usdt.add(m['base'])

    for s, m in mercados.items():
        if m['spot'] and m['active']:
            base = m['base']
            quote = m['quote'] # A Ponte
            
            # FILTRO: Se a ponte NÃO for lixo, a gente opera.
            # Isso libera: ETH, BTC, BNB, mas também SOL, DOGE, MATIC, PEPE...
            if quote not in stables and base not in stables:
                
                if base in moedas_usdt and quote in moedas_usdt:
                    
                    par_compra = f"{base}/USDT"
                    par_meio   = s
                    par_venda  = f"{quote}/USDT"
                    
                    if par_compra in mercados and par_venda in mercados:
                        triangulos.append({
                            'id_unico': f"{base}-{quote}",
                            'moeda_base': base,
                            'moeda_quote': quote,
                            'par_meio': par_meio,
                            'par_compra': par_compra,
                            'par_venda': par_venda
                        })

    print(f"[SCANNER] {len(triangulos)} rotas sujas prontas para operação.")

    return triangulos