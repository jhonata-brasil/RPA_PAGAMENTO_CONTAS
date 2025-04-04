import sqlite3

def connect_db_sqlite(logger):
    try:
        conn = sqlite3.connect('database/db_rpa_m2bot.db')
        
        return conn
    except Exception as e:
        logger.error(f'Erro ao realizar conexão com o banco de dados.')

def create_table_params_filters(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS filename_processed (
        
        id INTEGER PRIMARY KEY, 
        filename TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    
    '''
    
    conn.execute(create_table_query)
    
def insert_filename_in_db(conn, filename, logger):
    try:
        insert_query = '''
        INSERT INTO filename_processed (filename) VALUES (?)
        '''
        params_tuple = (filename,)
        
        conn.execute(insert_query, params_tuple)
        logger.info(f'Inserindo {filename}')
        conn.commit()
        logger.info(f'{filename} inserido na Base de dados.')
    except Exception as e:
        logger.error(f'  :::Erro ao inserir na base de dados: {e}')
    
def select_filename_in_db(conn, filename, logger):
    try:
        cursor = conn.execute("SELECT * FROM filename_processed WHERE filename = ?", (filename,))
        resultado = cursor.fetchone()        
        
        return resultado
    except Exception as e:
        logger.error(f'  :::Erro ao buscar arquivo na base de dados {e}')
    
    
    
    