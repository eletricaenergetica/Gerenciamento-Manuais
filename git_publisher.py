import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def executar(comando, pasta):
    """
    Executa um comando Git e retorna a saída.
    """
    resultado = subprocess.run(
        comando,
        cwd=pasta,
        capture_output=True,
        text=True,
        encoding="utf-8"  # Garante compatibilidade de caracteres em qualquer SO
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            f"Erro ao executar:\n"
            f"{' '.join(comando)}\n\n"
            f"{resultado.stderr.strip()}"
        )

    return resultado.stdout.strip()


def localizar_repositorio():
    """
    Localiza automaticamente a pasta que contém o diretório .git.
    """
    pasta = Path(__file__).resolve().parent

    while pasta != pasta.parent:
        if (pasta / ".git").exists():
            return pasta
        pasta = pasta.parent

    raise RuntimeError("Repositório Git não encontrado.")


def publicar_git():
    """
    Publica automaticamente as alterações no GitHub.
    """
    repo = localizar_repositorio()

    logging.info(f"Repositório encontrado em:\n{repo}")

    # Verifica se o Git está disponível
    executar(["git", "--version"], repo)

    # Adiciona todos os arquivos
    executar(["git", "add", "."], repo)

    # Verifica se existe algo para publicar (faz strip para limpar espaços/quebras)
    status = executar(["git", "status", "--porcelain"], repo).strip()

    if not status:
        return "Nenhuma alteração encontrada."

    mensagem = datetime.now().strftime(
        "Atualização automática %d/%m/%Y %H:%M"
    )

    # Commit
    executar(["git", "commit", "-m", mensagem], repo)

    # Push para a branch configurada (master ou main)
    executar(["git", "push"], repo)

    return "Publicação realizada com sucesso!"


if __name__ == "__main__":
    try:
        print(publicar_git())
    except Exception as erro:
        logging.error(erro)
