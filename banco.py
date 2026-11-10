from database import conectar_banco, criar_tabelas

criar_tabelas()
conexao = conectar_banco()

autores = [
    ("Machado de Assis", "Brasileira"),
    ("Ana Furtado", "Brasileira"),
    ("Mc Poze do Rodo", "Brasileira"),
]

for nome, nacionalidade in autores:
    conexao.execute("""
        INSERT INTO autores (nome, nacionalidade)
        SELECT ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM autores WHERE nome = ?)
    """, (nome, nacionalidade, nome))

livros = [
    ("As andorinhas", 1899, "Machado de Assis"),
    ("Caverna do Dragão", 1500, "Ana Furtado"),
    ("Us curinga do flamengo", 1200, "Mc Poze do Rodo"),
]

for titulo, ano, autor in livros:
    conexao.execute("""
        INSERT INTO livros (titulo, ano, autorid)
        SELECT ?, ?, id
        FROM autores
        WHERE nome = ?
        AND NOT EXISTS (SELECT 1 FROM livros WHERE titulo = ?)
    """, (titulo, ano, autor, titulo))

conexao.commit()
conexao.close()

print("Banco populado com sucesso xD")