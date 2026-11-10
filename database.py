import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    
    # Criação da tabela de autores
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, 
        nacionalidade TEXT NOT NULL
    )
    """)
    
   
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ano TEXT,
        autorid INTEGER NOT NULL,
        FOREIGN KEY (autorid) 
            REFERENCES autores(id)
    )
    """)

    conexao.commit()
    conexao.close()

    print("Tabelas criadas com sucesso!")

if __name__=="__main__":
    criar_tabelas()