def gerar_link_pagamento(plano):
    if plano == "destaque":
        return "https://pagamento.com/destaque"
    elif plano == "premium":
        return "https://pagamento.com/premium"
    else:
        return None
