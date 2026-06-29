import qrcode

def gerar_qr(link, nome_saida="qrcode.png"):
    img = qrcode.make(link)
    img.save(nome_saida)
    return nome_saida