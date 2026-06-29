import os

def gerar_html(projeto, lista_pdfs, pasta_saida="paginas"):
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_html = os.path.join(pasta_saida, f"{projeto}.html")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{projeto}</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #1e1e1e;
                color: white;
                text-align: center;
            }}
            a {{
                display: block;
                margin: 10px;
                padding: 10px;
                background: #007acc;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                width: 300px;
                margin-left: auto;
                margin-right: auto;
            }}
            a:hover {{
                background: #005f99;
            }}
        </style>
    </head>
    <body>

        <h1>📚 {projeto}</h1>
        <h3>Manuais Disponíveis</h3>
    """

    for pdf in lista_pdfs:
        nome = pdf[1]
        caminho = pdf[2].replace("\\", "/")
        html += f'<a href="../{caminho}" target="_blank">{nome}</a>\n'

    html += """
    </body>
    </html>
    """

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html)

    return caminho_html