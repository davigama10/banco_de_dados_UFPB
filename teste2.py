import psycopg2
from prettytable import PrettyTable
from decimal import Decimal
import os


class Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
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

    def funcionario_existe(self, cpf, senha):
        self.cur.execute("SELECT cpf FROM funcionario WHERE cpf = %s AND senha = %s", (cpf, senha))
        return self.cur.fetchone() is not None
    
    def get_sales_report(self, cod_funcionario, ano, mes):
        sql = f"""
            SELECT *
            FROM RelatorioVendasPorFuncionario
            WHERE cod_funcionario = %s
            AND ano = %s
            AND mes = %s;
        """
        self.cur.execute(sql, (cod_funcionario, ano, mes))
        return self.cur.fetchall()
    
    def gerar_relatorio_vendas(self, cod_funcionario, ano, mes):
        conn = Connection()
        relatorio = conn.get_sales_report(cod_funcionario, ano, mes)
        conn.close()
        return relatorio


class ProdutoApp:
    def __init__(self):
        self.load_data()
        
    def registrar_venda(self, cod_funcionario, cod_cliente, num_mesa, valor_compra, data):
        try:
            conn = Connection()
            
            valor_comissao = Decimal(valor_compra) * Decimal('0.1')  # 10% do valor total da compra

            sql = "INSERT INTO vendas (cod_funcionario, cod_cliente, num_mesa, valor_comissao, valor_compra, data_) VALUES (%s, %s, %s, %s, %s, %s);"
            conn.execute(sql, (cod_funcionario, cod_cliente, num_mesa, valor_comissao, valor_compra, data))

            conn.commit()
            conn.close()
            print("Venda registrada com sucesso!")

        except Exception as e:
            print("Erro ao registrar venda:", str(e))     
    
    def load_data(self):
        try:
            conn = Connection()
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()
            
            # Create a PrettyTable instance
            table = PrettyTable()
            
            # Add column names (these should match your database)
            table.field_names = ["cod_produto", "quant_estoque", "validade","fabricante", "valor", "marca","fabricado em mari", "categoria"]
            
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
            table.field_names = ["cod_produto", "quant_estoque", "validade","fabricante", "valor", "marca","fabricado em mari","categoria"]

            # Add rows to the table
            for row in rows:
                table.add_row(row)

            # Print the table
            print(table)

        except Exception as e:
            print("Erro ao buscar dados:", str(e))     
            
def get_cod_cliente(cpf_cliente):
    try:
        conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        cur = conn.cursor()

        sql = "SELECT cod_cliente FROM cliente WHERE cpf = %s"

        # Executar a consulta com o CPF desejado
        cur.execute(sql, (cpf_cliente,))

        # Atribuir o resultado a uma variável
        cod_cliente = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        return cod_cliente

    except Exception as e:
        print("Erro ao inserir forma de pagamento:", str(e))



def fazer_compra():
    conn = Connection()
    valor_total = 0  # Inicializa valor_total

    try:
        while True:
            # Carrega os dados do produto da tabela de produtos
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()

            # Cria uma PrettyTable para exibir os produtos disponíveis
            table = PrettyTable()
            table.field_names = ["cod_produto", "quant_estoque", "validade", "fabricante", "valor", "marca", "fabricado em mari", "categoria"]

            for row in rows:
                table.add_row(row)

            # Exibe a tabela de produtos
            print("Produtos disponíveis:")
            print(table)

            # Pergunta ao usuário o código do produto e a quantidade desejada
            cod_produto = int(input("Digite o código do produto que deseja comprar: "))
            quant_estoque = int(input("Digite a quantidade desejada: "))

            # Verifica se o produto escolhido e a quantidade estão disponíveis
            for row in rows:
                if row[0] == cod_produto:
                    if quant_estoque <= row[1]:
                        print(f"Produto '{row[5]}' adicionado ao carrinho.")
                        
                        # Calcula o valor total do pedido
                        total_value = Decimal(row[4]) * quant_estoque
                        valor_total += total_value  # Atualiza valor_total
                        print(f"O valor total do seu pedido é: {valor_total}")  # Imprime valor_total
                        
                        new_quantity = row[1] - quant_estoque
                        update_sql = "UPDATE produto SET quant_estoque = %s WHERE cod_produto = %s"
                        conn.execute(update_sql, (new_quantity, cod_produto))
                        conn.commit()
                        
                        break
                    else:
                        print("Quantidade insuficiente em estoque.")
                        return

            # Pergunta ao usuário se ele quer continuar comprando
            continuar = input("Deseja continuar comprando? (s/n): ")
                        
            # Limpa a saída do console antes da próxima interação
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if continuar.lower() != 's':
                break

        cliente_novo = input("Você é um cliente novo ou antigo? (n/a): ")

        cpf_cliente = None  # Inicializa cpf_cliente com None

        if cliente_novo.lower() == 'n':
            # Se for um novo cliente, chama a função para cadastrar um novo cliente
            ClienteForm().submit()
            cpf_cliente = input("Por favor, digite seu CPF: ")  # Pede o CPF após o cadastro do novo cliente

        elif cliente_novo.lower() == 'a':
            # Se for um cliente antigo, solicita o CPF e registra a compra para esse CPF
            cpf_cliente = input("Por favor, digite seu CPF: ")

        if cpf_cliente and conn.customer_exists(cpf_cliente):
            print("Bem-vindo de volta!")
            
            # Verifica se o cliente atende aos critérios para um desconto
            conn.cur.execute("SELECT cidade, animefavorito, timefutebol FROM cliente WHERE cpf = %s", (cpf_cliente,))
            cidade, animefavorito, timefutebol = conn.cur.fetchone()
            
            # Declarações de impressão para depuração:
            print("cidade:", cidade)
            print("animefavorito:", animefavorito)
            print("timefutebol:", timefutebol)
            
            if cidade == "Souza" or animefavorito == "One Piece" or timefutebol == "Flamengo":
                valor_total *= Decimal('0.9')  # Aplica um desconto de 10%
                print("Parabéns! Você ganhou um desconto de 10%. O valor total do seu pedido com desconto é: {:.2f}".format(valor_total))
        else:
            print("Parece que você é um novo cliente. Vamos fazer seu cadastro.")
            ClienteForm().submit()
            
        cod_funcionario = input("Digite o código do funcionário: ")
        num_mesa = input("Digite o número da mesa: ")
        data_compra = input("Digite a data da compra (DD-MM-AAAA): ")

        

        aux = get_cod_cliente(cpf_cliente)
        print(aux)

        ProdutoApp().registrar_venda(cod_funcionario, int(aux[0]), num_mesa, valor_total, data_compra)
        
        # Limpa a saída do console antes de cada interação
        os.system('cls' if os.name == 'nt' else 'clear')
            
        

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
        conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        cur = conn.cursor()
        
        sql = "INSERT INTO formapagamento (tipo, status) VALUES (%s, %s);"
        cur.execute(sql, (tipo, status))
        
        conn.commit()
        cur.close()
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

    def gerar_relatorio_vendas(self):
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
            print("Digite 3 para entrar como funcionário")
            print("Digite 4 para cadastrar Produto")
            print("Digite 0 para sair")
            
            opcao = int(input("Escolha uma opção: "))
            
             # Limpa a saída do console antes de cada interação
            os.system('cls' if os.name == 'nt' else 'clear')
            
            
            if opcao == 1:
                fazer_compra()  # Primeiro, selecione os itens para comprar
                # self.cliente_form.submit()  # Em seguida, faça o cadastro do cliente
                self.forma_pagamento_form.submit()
            elif opcao == 2:
                conn = Connection()
                print("Digite 1 para buscar por marca")
                print("Digite 2 para buscar por faixa de preço")
                print("Digite 3 para buscar por categoria")
                print("Digite 4 para saber se o produto foi fabricado em mari")
                
                opcao_busca = int(input("Escolha uma opção de busca: "))
                
                            # Limpa a saída do console antes de cada interação
                os.system('cls' if os.name == 'nt' else 'clear')
                
                if opcao_busca == 1:
                    marca = input("Digite a marca do produto que deseja verificar: ")
                    sql = "SELECT * FROM produto WHERE marca = %s;"
                    produtos = conn.query(sql, (marca,))
                    if produtos:
                        for produto in produtos:
                            print(f"O produto '{produto[5]}' da marca {marca} tem {produto[1]} unidades em estoque.")
                    else:
                        print("Produto não encontrado.")
                        
                elif opcao_busca == 2:
                    preco_min = float(input("Digite o preço mínimo: "))
                    preco_max = float(input("Digite o preço máximo: "))
                    sql = "SELECT * FROM produto WHERE valor BETWEEN %s AND %s;"
                    produtos = conn.query(sql, (preco_min, preco_max))
                    if produtos:
                        for produto in produtos:
                            print(f"O produto '{produto[5]}' com preço entre {preco_min} e {preco_max} tem {produto[1]} unidades em estoque.")
                    else:
                        print("Produto não encontrado.")
                elif opcao_busca == 4:
                    fabricado_em_mari = input("O produto foi fabricado em Mari? (Sim/Não): ")
                    self.app.search(fabricado_em_mari=fabricado_em_mari == 'Sim')

            elif opcao == 3:
                cpf_funcionario = input("Por favor, digite seu CPF: ")
                senha_funcionario = input("Por favor, digite sua senha: ")
                conn = Connection()
                if conn.funcionario_existe(cpf_funcionario, senha_funcionario):
                    while True:
                        print("Digite 1 para ver seu relatório")
                        print("Digite 2 para ver os produtos no estoque")
                        print("Digite 3 para voltar ao menu do cliente")
                        print("Digite 0 para sair")

                        opcao_funcionario = int(input("Escolha uma opção: "))
                        
                        # Limpa a saída do console antes de cada interação
                        os.system('cls' if os.name == 'nt' else 'clear')
                            

                        if opcao_funcionario == 1:
                            ano = input("ano: ")
                            mes = input("mes: ")
                            relatorio = conn.gerar_relatorio_vendas(cpf_funcionario, ano, mes)
                            print("relatorio mensal:")
                            for linha in relatorio:
                                print(linha)
                        elif opcao_funcionario == 2:
                            conn = Connection()
                            print("Digite 1 para buscar por marca")
                            print("Digite 2 para buscar por faixa de preço")
                            print("Digite 3 para buscar por categoria")
                            print("Digite 4 para saber se o produto foi fabricado em mari")
                            print("Digite 5 para buscar produtos com menos de 5 unidades disponíveis")
                            
                            
                            opcao_busca = int(input("Escolha uma opção de busca: "))
                            
                             # Limpa a saída do console antes de cada interação
                            os.system('cls' if os.name == 'nt' else 'clear')
                            
                            if opcao_busca == 1:
                                marca = input("Digite a marca do produto que deseja verificar: ")
                                sql = "SELECT * FROM produto WHERE marca = %s;"
                                produtos = conn.query(sql, (marca,))
                                if produtos:
                                    for produto in produtos:
                                        print(f"O produto '{produto[5]}' da marca {marca} tem {produto[1]} unidades em estoque.")
                                else:
                                    print("Produto não encontrado.")
                                    
                            elif opcao_busca == 2:
                                preco_min = float(input("Digite o preço mínimo: "))
                                preco_max = float(input("Digite o preço máximo: "))
                                sql = "SELECT * FROM produto WHERE valor BETWEEN %s AND %s;"
                                produtos = conn.query(sql, (preco_min, preco_max))
                                if produtos:
                                    for produto in produtos:
                                        print(f"O produto '{produto[5]}' com preço entre {preco_min} e {preco_max} tem {produto[1]} unidades em estoque.")
                                else:
                                    print("Produto não encontrado.")
                                    
                            elif opcao_busca == 3:
                                categoria = input("Digite a categoria do produto que deseja verificar: ")
                                sql = "SELECT * FROM produto WHERE categoria = %s;"
                                produtos = conn.query(sql, (categoria,))
                                if produtos:
                                    for produto in produtos:
                                        print(f"O produto '{produto[5]}' da categoria {categoria} tem {produto[1]} unidades em estoque.")
                                else:
                                    print("Produto não encontrado.")
                            elif opcao_busca == 4:
                                fabricado_em_mari = input("O produto foi fabricado em Mari? (Sim/Não): ")
                                self.app.search(fabricado_em_mari=fabricado_em_mari == 'Sim')
                            elif opcao_busca == 5:  # Nova condição
                                sql = "SELECT * FROM produto WHERE quant_estoque < %s;"
                                produtos = conn.query(sql, (5,))
                                if produtos:
                                    for produto in produtos:
                                        print(f"O produto '{produto[5]}' tem apenas {produto[1]} unidades em estoque.")
                                else:
                                    print("Não há produtos com menos de 5 unidades disponíveis.")
                                    
                            else:
                                print("Opção inválida. Tente novamente.")
                            
                            conn.close()
                        elif opcao_funcionario == 3:
                            break
                        elif opcao_funcionario == 0:
                            return
                        else:
                            print("Opção inválida. Tente novamente.")
                else:
                    print("CPF ou senha inválidos.")
            elif opcao == 4:
                self.produto_form.submit()
                print("cadastro de Produto:")
            elif opcao == 0:
                break
            else:
                print("Opção inválida. Tente novamente.")
                           


if __name__ == "__main__":
    menu = Menu()
    menu.run()

    