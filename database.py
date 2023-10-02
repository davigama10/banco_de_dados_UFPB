import psycopg2 as db

class Connection:
    def __init__(self):
        self.config = {
            "DBProject": {
                "user": "postgres",
                "password": "12345678",
                "host": "localhost",
                "port": "5432",
                "database": "DBProject"
            }
        }
        self.conn = db.connect(**self.config["DBProject"])
        self.cur = self.conn.cursor()

    # Outros métodos relacionados à conexão com o banco de dados
