import os
import html
import urllib.parse


def gerar_html(projeto, lista_pdfs, pasta_saida="."):
    """
    Gera o arquivo index.html contendo a lista de manuais do projeto,
    agora com design moderno em Grid responsivo, barra de busca e assinatura do autor.
    """

    if not lista_pdfs:
        raise Exception("Nenhum manual encontrado para gerar o HTML.")

    os.makedirs(pasta_saida, exist_ok=True)

    # O GitHub Pages procura automaticamente por index.html
    caminho_html = os.path.join(pasta_saida, "index.html")

    # Ordena os PDFs pelo nome (índice 1 da tupla) de forma case-insensitive
    lista_pdfs = sorted(lista_pdfs, key=lambda x: x[1].lower())

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{html.escape(projeto)}</title>

<style>
/* Configurações Gerais */
body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    background: #121212;
    color: #e0e0e0;
    margin: 0;
    padding: 20px;
    text-align: center;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 10px;
}}

h1 {{
    color: #00BFFF;
    margin-bottom: 5px;
    font-size: 2.2rem;
}}

/* Estilo da Assinatura do Autor */
.autor {{
    font-size: 0.95rem;
    color: #888; /* Cinza discreto para não brigar com o título principal */
    margin-top: -5px;
    margin-bottom: 15px;
    font-style: italic;
}}

.subtitle {{
    color: #888;
    margin-top: 5px;
    margin-bottom: 25px;
    font-size: 1.1rem;
}}

/* Barra de Busca */
.search-container {{
    margin-bottom: 30px;
}}

.search-input {{
    width: 100%;
    max-width: 500px;
    padding: 12px 20px;
    font-size: 16px;
    background: #1e1e1e;
    border: 2px solid #333;
    border-radius: 30px;
    color: white;
    outline: none;
    transition: all 0.3s ease;
}}

.search-input:focus {{
    border-color: #00BFFF;
    box-shadow: 0 0 10px rgba(0, 191, 255, 0.3);
}}

/* Grid de Cards */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 10px 0;
}}

/* Card Modernizado */
.card {{
    background: #1e1e1e;
    border: 1px solid #2d2d2d;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 191, 255, 0.15);
    border-color: #3d3d3d;
}}

.card h3 {{
    margin: 0 0 15px 0;
    font-size: 1.1rem;
    color: #ffffff;
    word-break: break-word;
    font-weight: 600;
}}

/* Botão do Card */
a {{
    display: block;
    padding: 10px;
    background: #0d6efd;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
    font-size: 0.95rem;
    transition: background 0.2s ease;
}}

a:hover {{
    background: #0b5ed7;
}}

footer {{
    margin-top: 60px;
    color: #555;
    font-size: 12px;
    border-top: 1px solid #222;
    padding-top: 15px;
}}
</style>

</head>

<body>

<div class="container">

    <h1>📚 {html.escape(projeto)}</h1>
    <div class="autor">Desenvolvido por Maurílio</div>
    <div class="subtitle" id="contador">{len(lista_pdfs)} Manual(is) disponível(is)</div>

    <div class="search-container">
        <input type="text" id="busca" class="search-input" placeholder="Pesquise por um manual...">
    </div>

    <div class="grid-container" id="lista-manuais">
"""

    for pdf in lista_pdfs:
        nome_completo = html.escape(pdf[1])
        
        # Remove visualmente a extensão ".pdf" para o título ficar mais limpo
        if nome_completo.lower().endswith(".pdf"):
            nome_exibicao = nome_completo[:-4]
        else:
            nome_exibicao = nome_completo
            
        arquivo_pdf = os.path.basename(pdf[2])

        # Sanitiza o link para evitar problemas com espaços ou acentos na URL
        projeto_url = urllib.parse.quote(projeto)
        arquivo_url = urllib.parse.quote(arquivo_pdf)
        link_pdf = f"pdfs/{projeto_url}/{arquivo_url}"

        html_content += f"""
        <div class="card" data-nome="{nome_completo.lower()}">
            <h3>{nome_exibicao}</h3>
            <a href="{link_pdf}" target="_blank">
                📖 Abrir Manual
            </a>
        </div>"""

    html_content += """
    </div>

    <footer>
        Gerado automaticamente pelo Sistema de Gerenciamento de Manuais.
    </footer>

</div>

<script>
document.getElementById('busca').addEventListener('input', function(e) {
    const termo = e.target.value.toLowerCase().trim();
    const cards = document.querySelectorAll('.card');
    let visiveis = 0;

    cards.forEach(card => {
        const nomeManual = card.getAttribute('data-nome');
        if (nomeManual.includes(termo)) {
            card.style.display = '';
            visiveis++;
        } else {
            card.style.display = 'none';
        }
    });

    // Atualiza o contador de manuais dinamicamente
    const contador = document.getElementById('contador');
    if (termo === '') {
        contador.textContent = cards.length + " Manual(is) disponível(is)";
    } else {
        contador.textContent = visiveis + " de " + cards.length + " encontrado(s)";
    }
});
</script>

</body>
</html>
"""

    with open(caminho_html, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_content)

    return caminho_html