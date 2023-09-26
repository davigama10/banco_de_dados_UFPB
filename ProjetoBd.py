import psycopg2 as pg

class Config:
    
    def __init__(self):
        
        self.config = {
            "postgres" :{
                "user": "postegres",
                "password" : "2110",
                "host" : "localhost",
                "port" : "5432",
                "database" : "ProjetoBar"
            }
        }
    
    
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.commit()
            self.connection.close()
    
    
    
    class Connection(Config):
        def __init__(self):
            Config.__init__(self)
            try:
                self.conn = db.connect(**self.config["postgres"])
                self.cur = self.conn.cursor()
            except Exception as e:
              print("Erro na conexão", e)
              exit(1)
              
              
              @property
              def connection(self):
                  return self.conn
              
              @property
              def cursor(self):
                  return self.cur
              
              def commit(self):
                  self.connection.commit() 
              
              
              def fetchall(self):
                  return self.cursor.fetchall()
              
              def execute(self, sql, params=None):
                  self.cursor.execute(sql, params or ())
                                    
            
            def query(self, sql, params=None):          
                self.cursor.execute(sql, params or())
                return self.fetchall()
            
            
            class Bar(Connection):
                def __init__(self):
                  connection.__init__(self)  
                  
                  def insert(self, *args):
                      try:
                          
                        self.execute("INSERT INTO Produto (Quant_estoque,Validade,Fabricante,Valor,Marca) VALUES (%s, %s,%s,%s,%s)", args)
                        
                        self.commit()
                      
                      except Exception as e:
                          print("Erro ao inserir" , e)
                          
                         
                          
                  if __name__ == "__main__":
                      Bar = Bar()
                      Bar.insert("40","09/25","Thais_gaudencio","19.89","Cachaca Sao Paulo")     