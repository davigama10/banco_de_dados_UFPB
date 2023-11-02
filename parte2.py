import psycopg2
from prettytable import PrettyTable
from decimal import Decimal


class Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="projetoBD",
            user="postgres",
            password="2110",
            host="localhost"
        )
        self.cur = self.conn.cursor()

    def execute(self, sql, args):
        self.cur.execute(sql, args)

    def commit(self):
        self.conn.commit()

    def query(self, sql, args=None):
        if args is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, args)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
        
    def customer_exists(self, cpf):
        self.cur.execute("SELECT cpf FROM cliente WHERE cpf = %s", (cpf,))
        return self.cur.fetchone() is not None        

class ProdutoApp:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        try:
            conn = Connection()
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()
            
            # Create a PrettyTable instance
            table = PrettyTable()
            
            # Add column names (these should match your database)
            table.field_names = ["cod_produto", "quant_estoque", "validade","fabricante", "valor", "marca","fabricado em mari"]
            
            # Add rows to the table
            for row in rows:
                table.add_row(row)
            
            # Print the table
            print(table)
            
            conn.close()
        except Exception as e:
            print("Erro ao buscar dados:", str(e))

    def search(self, marca=None, preco_min=None, preco_max=None, categoria=None, fabricado_em_mari=None):
        try:
            conn = Connection()

            # Build the SQL query
            sql = "SELECT * FROM produto WHERE 1=1"
            params = []

            if marca is not None:
                sql += " AND marca = %s"
                params.append(marca)

            if preco_min is not None:
                sql += " AND preco >= %s"
                params.append(preco_min)

            if preco_max is not None:
                sql += " AND preco <= %s"
                params.append(preco_max)

            if categoria is not None:
                sql += " AND categoria = %s"
                params.append(categoria)

            if fabricado_em_mari is not None:
                sql += " AND fabricado_em_mari = %s"
                params.append(fabricado_em_mari)

            # Execute the query
            conn.execute(sql, tuple(params))
            
            rows = conn.cur.fetchall()

            # Create a PrettyTable instance
            table = PrettyTable()

            # Add column names (these should match your database)
            table.field_names = ["cod_produto", "quant_estoque", "validade","fabricante", "valor", "marca","fabricado em mari"]

            # Add rows to the table
            for row in rows:
                table.add_row(row)

            # Print the table
            print(table)

        except Exception as e:
            print("Erro ao buscar dados:", str(e))

def fazer_compra():
    conn = Connection()

    try:
        while True:
            # Load product data from the product table
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()

            # Create a PrettyTable to display available products
            table = PrettyTable()
            table.field_names = ["cod_produto", "quant_estoque", "validade", "fabricante", "valor", "marca", "fabricado em mari"]

            for row in rows:
                table.add_row(row)

            # Display the product table
            print("Produtos disponíveis:")
            print(table)

            # Ask the user for the product code and desired quantity
            cod_produto = int(input("Digite o código do produto que deseja comprar: "))
            quant_estoque = int(input("Digite a quantidade desejada: "))

            # Check if the chosen product and quantity are available
            for row in rows:
                if row[0] == cod_produto:
                    if quant_estoque <= row[1]:
                        print(f"Produto '{row[5]}' adicionado ao carrinho.")
                        
                        # Calculate total value of the order
                        total_value = Decimal(row[4]) * quant_estoque
                        print(f"O valor total do seu pedido é: {total_value}")
                        
                        new_quantity = row[1] - quant_estoque
                        update_sql = "UPDATE produto SET quant_estoque = %s WHERE cod_produto = %s"
                        conn.execute(update_sql, (new_quantity, cod_produto))
                        conn.commit()
                        
                        break
                    else:
                        print("Quantidade insuficiente em estoque.")
                        return

            # Perguntar ao usuário se ele quer continuar comprando
            continuar = input("Deseja continuar comprando? (s/n): ")
            if continuar.lower() != 's':
                break

        # Perguntar ao usuário se ele é um cliente antigo ou novo
        cliente_novo = input("Você é um cliente novo ou antigo? (n/a): ")
        
        if cliente_novo.lower() == 'n':
            # Se for um novo cliente, chamar a função para cadastrar um novo cliente
            ClienteForm().submit()
        
        
        elif cliente_novo.lower() == 'a':
            # Se for um cliente antigo, solicitar o CPF e registrar a compra para esse CPF
            cpf_cliente = input("Por favor, digite seu CPF: ")
            
        if conn.customer_exists(cpf_cliente):
            print("Bem-vindo de volta!")
        else:
            print("Parece que você é um novo cliente. Vamos fazer seu cadastro.")
            ClienteForm().submit()

    except Exception as e:
        print("Erro ao fazer a compra:", str(e))
    finally:
        conn.close()


class ClienteForm:
    def submit(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        sexo = input("Sexo: ")
        email = input("Email: ")
        cidade = input("Cidade: ")
        timefutebol = input("Time de Futebol: ")
        animefavorito = input("Anime Favorito: ")

        insert_cliente(nome, cpf, sexo, email, cidade, timefutebol, animefavorito)
        
        return {
            'nome': nome,
            'cpf': cpf,
            'sexo': sexo,
            'email': email,
            'cidade': cidade,
            'timefutebol': timefutebol,
            'animefavorito': animefavorito,
        }

def insert_cliente(nome, cpf, sexo, email, cidade, timefutebol, animefavorito):
    try:
        conn = Connection()
        
        sql = "INSERT INTO cliente (nome, cpf, sexo, email, cidade, timefutebol, animefavorito) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        conn.execute(sql, (nome, cpf, sexo, email, cidade, timefutebol, animefavorito))

        conn.commit()
        conn.close()
        print("Cliente inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir cliente:", str(e))   


class FormaPagamentoForm:
    def submit(self):
                                                # Payment type menu
        print("Digite 1 para Cartão")
        print("Digite 2 para Boleto")
        print("Digite 3 para Pix")
        print("Digite 4 para Berries")

        tipo = int(input("Escolha uma opção de pagamento: "))
        if tipo not in [1, 2, 3, 4]:
                        print("Forma de pagamento inválida.")
                        return
                    
        status = input("Digite o status do pagamento: ")
        # print("Forma de pagamento inserida com sucesso!")
        
        insert_forma_pagamento(tipo, status)

def insert_forma_pagamento(tipo, status):
    try:

        conn = Connection()
        
        sql = "INSERT INTO FormaPagamento (tipo, status) VALUES (%s, %s);"
        conn.execute(sql, (tipo, status))
        
        conn.commit()
        conn.close()
        print("Forma de pagamento inserida com sucesso!")

    except Exception as e:
        print("Erro ao inserir forma de pagamento:", str(e))

class ProdutoForm:
    def submit(self):
        marca = input("Nome do Produto: ")
        valor = float(input("Preço do Produto: "))
        quant_estoque = int(input("Quantidade em Estoque: "))
        validade = input("Data de Validade (DD-MM-AAAA): ")
        fabricado_em_mari = input("Fabricado em Mari? (Sim/Não): ")

        insert_produto(marca, valor, quant_estoque, validade, fabricado_em_mari)

def insert_produto(marca, valor, quant_estoque, validade, fabricado_em_mari):
    try:
        conn = Connection()
        
        sql = "INSERT INTO Produto (marca, valor, quant_estoque, validade, fabricado_em_mari) VALUES (%s, %s, %s, %s, %s);"
        conn.execute(sql, (marca, valor, quant_estoque, validade, fabricado_em_mari == 'Sim'))
        
        conn.commit()
        conn.close()
        print("Produto inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir produto:", str(e))

class Vendedor:
    def __init__(self, cpf):
        self.cpf = cpf
        self.conn = Connection()

    def get_vendas(self):
        sql = "SELECT * FROM venda WHERE cpf_vendedor = %s;"
        return self.conn.query(sql, (self.cpf,))
        
    def close(self):
        self.conn.close()

def gerar_relatorio_vendas():
    conn = Connection()
    sql = "SELECT cpf_vendedor, COUNT(*), SUM(valor) FROM venda GROUP BY cpf_vendedor;"
    relatorio = conn.query(sql)
    conn.close()
    return relatorio    

class Menu:
    def __init__(self):
        self.app = ProdutoApp()
        self.cliente_form = ClienteForm()
        self.forma_pagamento_form = FormaPagamentoForm()
        self.produto_form = ProdutoForm()

    def run(self):
        while True:
            print("Digite 1 para realizar uma compra")
            print("Digite 2 para ver se um produto esta no estoque")
            print("Digite 3 para cadastrar Produto")
            print("Digite 4 para fazer um relatorio do funcionario")
            print("Digite 0 para sair")
            
            opcao = int(input("Escolha uma opção: "))
            
            if opcao == 1:
                fazer_compra()  # Primeiro, selecione os itens para comprar
                # self.cliente_form.submit()  # Em seguida, faça o cadastro do cliente
                self.forma_pagamento_form.submit()
            elif opcao == 2:
                cod_produto = int(input("Digite o código do produto que deseja verificar: "))
                conn = Connection()
                sql = "SELECT quant_estoque FROM produto WHERE cod_produto = %s;"
                quant_estoque = conn.query(sql, (cod_produto,))
                if quant_estoque is not None:
                    print(f"O produto com código {cod_produto} tem {quant_estoque} unidades em estoque.")
                else:
                    print("Produto não encontrado.")
                conn.close()
            elif opcao == 3:
                self.produto_form.submit()
                print("cadastro de Produto:")
            elif opcao == 4:
                relatorio = gerar_relatorio_vendas()
                print("Relatório de vendas:")
                for linha in relatorio:
                    print(linha)
            elif opcao == 0:
                break
            else:
                print("Opção inválida. Tente novamente.")



if __name__ == "__main__":
    menu = Menu()
    menu.run()

    

