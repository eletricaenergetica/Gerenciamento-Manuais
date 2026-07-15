import os
import qrcode


def gerar_qr(link: str, nome_saida: str = "qrcode.png", pasta: str = "qrcodes") -> str:
    """
    Gera um QR Code apontando para um link (URL).
    """

    if not link:
        raise ValueError("Link inválido para geração do QR Code.")

    os.makedirs(pasta, exist_ok=True)

    # Garante que o arquivo tenha a extensão .png
    if not nome_saida.lower().endswith(".png"):
        nome_saida += ".png"

    caminho_saida = os.path.join(pasta, nome_saida)

    # Definimos version=1 e fit=True para autoajuste correto do tamanho dos dados
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(caminho_saida)

    return caminho_saida
