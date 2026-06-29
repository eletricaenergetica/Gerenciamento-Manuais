from git import Repo
from datetime import datetime
import os


def publicar_git():

    # Repositório Git na pasta do projeto
    repo = Repo(os.getcwd())

    # Adiciona todos os arquivos
    repo.git.add(A=True)

    # Só faz commit se houver alterações
    if repo.is_dirty(untracked_files=True):

        mensagem = f"Atualização automática - {datetime.now():%d/%m/%Y %H:%M}"

        repo.index.commit(mensagem)

        origin = repo.remote("origin")
        origin.push()

        return "Publicação realizada com sucesso!"

    return "Nenhuma alteração para publicar."