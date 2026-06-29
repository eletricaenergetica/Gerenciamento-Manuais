import sqlite3

DB_NAME = "manuais.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manuais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        projeto TEXT,
        nome TEXT,
        caminho TEXT
    )
    """)

    conn.commit()
    conn.close()


def inserir_manual(projeto, nome, caminho):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO manuais (projeto, nome, caminho)
    VALUES (?, ?, ?)
    """, (projeto.strip(), nome, caminho))

    conn.commit()
    conn.close()


# ==============================
# 🔥 CORREÇÃO PRINCIPAL AQUI
# ==============================
def listar_manuais(projeto=None):
    conn = conectar()
    cursor = conn.cursor()

    if projeto:
        cursor.execute("""
        SELECT id, nome, caminho 
        FROM manuais 
        WHERE LOWER(projeto)=LOWER(?)
        """, (projeto.strip(),))
    else:
        cursor.execute("""
        SELECT id, nome, caminho 
        FROM manuais
        """)

    dados = cursor.fetchall()
    conn.close()
    return dados


def deletar_manual(id_manual):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM manuais WHERE id=?", (id_manual,))

    conn.commit()
    conn.close()


# ==========================
# CONFIG
# ==========================
def pegar_ultimo_projeto():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY,
        ultimo_projeto TEXT
    )
    """)

    cursor.execute("SELECT ultimo_projeto FROM config WHERE id=1")
    resultado = cursor.fetchone()

    conn.close()

    return resultado[0] if resultado else ""