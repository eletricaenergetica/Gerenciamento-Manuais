import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import shutil
import os

import database as db
import html_generator as htmlg
import qrcode_generator as qrg


db.criar_tabela()


class App:

    def __init__(self):
        self.janela = tb.Window(themename="darkly")
        self.janela.title("Gerenciamento de Manuais Industriais")
        self.janela.geometry("850x500")

        self.projeto = tb.StringVar()

        self.criar_interface()

        # ⚠️ proteção contra erro caso config não exista
        try:
            ultimo = db.pegar_ultimo_projeto()
            self.projeto.set(ultimo)
        except:
            self.projeto.set("")

        self.carregar_lista()

        self.janela.mainloop()

    # ---------------- INTERFACE ----------------
    def criar_interface(self):

        tb.Label(
            self.janela,
            text="📚 GERENCIAMENTO DE MANUAIS INDUSTRIAIS",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        frame_top = tb.Frame(self.janela)
        frame_top.pack(pady=5)

        tb.Label(frame_top, text="Projeto:").pack(side=LEFT)

        tb.Entry(
            frame_top,
            textvariable=self.projeto,
            width=40
        ).pack(side=LEFT, padx=5)

        tb.Button(
            frame_top,
            text="Carregar",
            bootstyle=PRIMARY,
            command=self.carregar_lista
        ).pack(side=LEFT)

        # ---------------- LISTA ----------------
        self.lista = tb.Treeview(
            self.janela,
            columns=("id", "nome", "caminho"),
            show="headings"
        )

        self.lista.heading("id", text="ID")
        self.lista.heading("nome", text="Nome")
        self.lista.heading("caminho", text="Arquivo")

        self.lista.column("id", width=50)
        self.lista.column("nome", width=200)
        self.lista.column("caminho", width=500)

        self.lista.pack(fill=BOTH, expand=True, pady=10)

        # ---------------- BOTÕES ----------------
        frame_btn = tb.Frame(self.janela)
        frame_btn.pack(pady=5)

        tb.Button(
            frame_btn,
            text="📄 Adicionar PDF",
            bootstyle=SUCCESS,
            command=self.adicionar_pdf
        ).pack(side=LEFT, padx=5)

        tb.Button(
            frame_btn,
            text="🗑 Remover",
            bootstyle=DANGER,
            command=self.remover
        ).pack(side=LEFT, padx=5)

        tb.Button(
            frame_btn,
            text="📄 Gerar QR + Publicar",
            bootstyle=PRIMARY,
            command=self.gerar_site_qr
        ).pack(side=LEFT, padx=5)

    # ---------------- CARREGAR ----------------
    def carregar_lista(self):

        for item in self.lista.get_children():
            self.lista.delete(item)

        projeto = self.projeto.get().strip()

        if not projeto:
            return

        dados = db.listar_manuais(projeto)

        for d in dados:
            self.lista.insert("", "end", values=d)

        try:
            db.salvar_ultimo_projeto(projeto)
        except:
            pass

    # ---------------- ADICIONAR PDF ----------------
    def adicionar_pdf(self):

        arquivo = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])

        if not arquivo:
            return

        projeto = self.projeto.get().strip()

        if not projeto:
            messagebox.showwarning("Aviso", "Digite o nome do projeto!")
            return

        pasta = f"pdfs/{projeto}"
        os.makedirs(pasta, exist_ok=True)

        nome = os.path.basename(arquivo)
        destino = os.path.join(pasta, nome)

        shutil.copy(arquivo, destino)

        db.inserir_manual(projeto, nome, destino)

        self.carregar_lista()

    # ---------------- REMOVER ----------------
    def remover(self):

        item = self.lista.selection()

        if not item:
            return

        dados = self.lista.item(item)["values"]

        if not dados:
            return

        id_manual = dados[0]

        db.deletar_manual(id_manual)

        self.carregar_lista()

    # ---------------- GERAR SITE + QR + GIT ----------------
    def gerar_site_qr(self):

        import build_site
        import git_publisher

        projeto = self.projeto.get().strip()

        if not projeto:
            messagebox.showwarning("Aviso", "Digite o nome do projeto!")
            return

        try:
            html_path, link = build_site.gerar_site(projeto)

            nome_qr = f"{projeto}.png"
            qr_path = qrg.gerar_qr(link, nome_qr)

            status_git = git_publisher.publicar_git()

            messagebox.showinfo(
                "✔ Processo concluído",
                f"Projeto: {projeto}\n\n"
                f"🌐 Link:\n{link}\n\n"
                f"📱 QR:\n{qr_path}\n\n"
                f"☁ Git:\n{status_git}"
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))


App()