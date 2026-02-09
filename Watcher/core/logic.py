def calc(capital, p1, p2, p3, taxa=0.001):

    if p1 == 0 or p2 == 0 or p3 == 0:
        return {'lucro_pct': -100, 'lucro_valor': 0, 'valido': False}
    
    qtd_f1 = (capital/p1) * (1-taxa)

    qtd_f2 = (qtd_f1 * p2) * (1-taxa)

    capital_final = (qtd_f2 * p3) * (1-taxa)

    lucro = capital_final - capital
    lucro_pct = (lucro/capital) * 100

    return {
        'entrada': capital,
        'saida': capital_final,
        'lucro': lucro,
        'lucro_pct': lucro_pct,
        'valido': lucro > 0
    }