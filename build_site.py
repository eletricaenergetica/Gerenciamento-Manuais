import os
import shutil

import database as db
import html_generator as htmlg

# ======================================================
# ALTERE APENAS ESTA LINHA COM O SEU GITHUB PAGES
# Exemplo:
# https://maurilio.github.io/manuais
# ======================================================

GITHUB_BASE_URL = "https://eletricaenergetica.github.io/Gerenciamento-Manuais-"


def gerar_site(projeto):

    dados = db.listar_manuais(projeto)

    if not dados:
        raise Exception("Nenhum manual encontrado para este projeto.")

    site_dir = "site"

    projeto_pdf_dir = os.path.join(site_dir, "pdfs", projeto)

    # Remove o site antigo
    if os.path.exists(site_dir):
        shutil.rmtree(site_dir)

    os.makedirs(projeto_pdf_dir, exist_ok=True)

    # Copia todos os PDFs
    for manual in dados:

        origem = manual[2]

        if os.path.exists(origem):
            shutil.copy(origem, projeto_pdf_dir)

    # Gera o HTML
    html_path = htmlg.gerar_html(
        projeto,
        dados,
        pasta_saida=site_dir
    )

    # Link público do GitHub Pages
    link = f"{GITHUB_BASE_URL}/{projeto}.html"

    return html_path, link


if __name__ == "__main__":
    gerar_site("Manuais")