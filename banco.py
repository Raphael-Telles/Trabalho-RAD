import sqlite3

# Função para conectar ao banco de dados e criar a tabela se não existir
def conectar():
    con = sqlite3.connect("alunos.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nota1 REAL NOT NULL,
            nota2 REAL NOT NULL,
            media REAL
        )
    """)
    con.commit()
    return con, cur

# Funções CRUD
def adicionar_aluno(cur, nome, nota1, nota2):
    media = (nota1 + nota2) / 2
    cur.execute("INSERT INTO alunos (nome, nota1, nota2, media) VALUES (?, ?, ?, ?)", (nome, nota1, nota2, media))

def listar_alunos(cur, filtro=""):
    if filtro:
        cur.execute("SELECT id, nome, nota1, nota2, (nota1 + nota2) / 2 AS media FROM alunos WHERE nome LIKE ?", ('%' + filtro + '%',))
    else:
        cur.execute("SELECT id, nome, nota1, nota2, (nota1 + nota2) / 2 AS media FROM alunos")
    return cur.fetchall()

def excluir_aluno(cur, aluno_id):
    cur.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))

def editar_aluno(cur, aluno_id, nome, nota1, nota2):
    media = (nota1 + nota2) / 2
    cur.execute("UPDATE alunos SET nome=?, nota1=?, nota2=?, media=? WHERE id=?", (nome, nota1, nota2, media, aluno_id))
