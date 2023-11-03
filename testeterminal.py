import psycopg2
from prettytable import PrettyTable
from decimal import Decimal
import os
from os import name, system
import PySimpleGUI as sg


class Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="dbproject",
            user="postgres",
            password="12345678",
            host="localhost"
        )
        self.cur = self.conn.cursor()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()

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

class ProdutoApp:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        try:
            conn = Connection()
            conn.execute("SELECT * FROM produto", ())
            rows = conn.cur.fetchall()
            
            # Create a PySimpleGUI table to display data
            data = [[j for j in i] for i in rows]
            header_list = ["cod_produto", "quant_estoque", "validade","fabricante", "valor", "marca","fabricado em mari", "categoria"]
            
            layout = [[sg.Table(values=data,
                                headings=header_list,
                                display_row_numbers=False,
                                auto_size_columns=True,
                                num_rows=min(25, len(data)))],
                    [sg.Button("OK")]]
            
            conn.close()
            return layout  # return the layout
        except Exception as e:
            sg.popup("Erro ao buscar dados:", str(e))
            return []  # return an empty layout in case of an error


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

            # Create a PySimpleGUI table to display data
            data = [[j for j in i] for i in rows]
            header_list = ["cod_produto", "quant_estoque", "validade","fabricante", "valor", "marca","fabricado em mari","categoria"]
            
            layout = [[sg.Table(values=data,
                                headings=header_list,
                                display_row_numbers=False,
                                auto_size_columns=True,
                                num_rows=min(25, len(data)))],
                      [sg.Button("OK")]]
            
            window = sg.Window('Produtos Encontrados', layout)
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'OK':
                    break
            window.close()

        except Exception as e:
            print("Erro ao buscar dados:", str(e))


def fazer_compra():
    conn = Connection()
    valor_total = 0  # Initialize valor_total
    carrinho = []  # List to store the products added to the cart

    try:
        while True:
            # Create a window with fields to enter product details
            layout = [[sg.Text('Código do Produto:'), sg.Input(key='-COD_PRODUTO-')],
                      [sg.Text('Quantidade:'), sg.Input(key='-QUANTIDADE-')],
                      [sg.Button('Adicionar ao Carrinho'), sg.Button('Finalizar Compra')]]

            window = sg.Window('Comprar Produto', layout)

            while True:
                event, values = window.read()

                if event == sg.WINDOW_CLOSED:
                    break
                elif event == 'Adicionar ao Carrinho':
                    # Add the product to the cart
                    cod_produto = values['-COD_PRODUTO-']
                    quantidade = values['-QUANTIDADE-']
                    carrinho.append((cod_produto, quantidade))
                    sg.popup('Produto adicionado ao carrinho!')

                    # Clear the input fields
                    window.Element('-COD_PRODUTO-').Update('')
                    window.Element('-QUANTIDADE-').Update('')
                elif event == 'Finalizar Compra':
                    # Finalize the purchase and display the purchased products
                    sg.popup('Compra finalizada! Você comprou os seguintes produtos:', '\n'.join(f'Produto: {prod}, Quantidade: {quant}' for prod, quant in carrinho))
                    
                    # Calculate the total value of the cart and update the quantity of each product in the database
                    for cod_produto, quantidade in carrinho:
                        conn.cur.execute("SELECT valor, quant_estoque FROM produto WHERE cod_produto = %s", (cod_produto,))
                        valor_produto, quant_estoque = conn.cur.fetchone()
                        valor_total += valor_produto * int(quantidade)
                        
                        # Update the quantity of the product in the database
                        new_quantity = quant_estoque - int(quantidade)
                        update_sql = "UPDATE produto SET quant_estoque = %s WHERE cod_produto = %s"
                        conn.execute(update_sql, (new_quantity, cod_produto))
                        conn.commit()

                    # Print the total value of the cart
                    sg.popup(f"O valor total do seu carrinho é: {valor_total}")
                    
                    # Ask if the customer is new or old
                    cliente_novo = sg.popup_get_text("Você é um cliente novo ou antigo? (n/a): ")
                    
                    cpf_cliente = None  # Initialize cpf_cliente with None

                    if cliente_novo.lower() == 'n':
                        # If it's a new customer, call the function to register a new customer
                        ClienteForm().submit()
                        cpf_cliente = sg.popup_get_text("Por favor, digite seu CPF: ")  # Ask for the CPF after the new customer registration

                    elif cliente_novo.lower() == 'a':
                        # If it's an old customer, ask for the CPF and register the purchase for that CPF
                        cpf_cliente = sg.popup_get_text("Por favor, digite seu CPF: ")

                    if cpf_cliente and conn.customer_exists(cpf_cliente):
                        sg.popup("Bem-vindo de volta!")
                        
                        # Check if the customer meets the criteria for a discount
                        conn.cur.execute("SELECT cidade, animefavorito, timefutebol FROM cliente WHERE cpf = %s", (cpf_cliente,))
                        cidade, animefavorito, timefutebol = conn.cur.fetchone()
                        
                        if cidade == "Souza" or animefavorito == "One Piece" or timefutebol == "Flamengo":
                            valor_total *= Decimal('0.9')  # Apply a 10% discount
                            sg.popup("Parabéns! Você ganhou um desconto de 10%. O valor total do seu pedido com desconto é: {:.2f}".format(valor_total))
                    else:
                        sg.popup("Parece que você é um novo cliente. Vamos fazer seu cadastro.")
                        
                        ClienteForm().submit()

                    break

            if event == sg.WINDOW_CLOSED or event == 'Finalizar Compra':
                break

    except Exception as e:
        sg.popup("Erro ao fazer a compra:", str(e))

    finally:
        conn.close()
        window.close()




# def fazer_compra():
#     conn = Connection()
#     valor_total = 0  # Inicializa valor_total

#     try:
#         while True:
#             # Carrega os dados do produto da tabela de produtos
#             conn.execute("SELECT * FROM produto", ())
#             rows = conn.cur.fetchall()

#             # Cria uma PrettyTable para exibir os produtos disponíveis
#             table = PrettyTable()
#             table.field_names = ["cod_produto", "quant_estoque", "validade", "fabricante", "valor", "marca", "fabricado em mari", "categoria"]

#             for row in rows:
#                 table.add_row(row)

#             # Exibe a tabela de produtos
#             print("Produtos disponíveis:")
#             print(table)

#             # Pergunta ao usuário o código do produto e a quantidade desejada
#             cod_produto = int(input("Digite o código do produto que deseja comprar: "))
#             quant_estoque = int(input("Digite a quantidade desejada: "))

#             # Verifica se o produto escolhido e a quantidade estão disponíveis
#             for row in rows:
#                 if row[0] == cod_produto:
#                     if quant_estoque <= row[1]:
#                         print(f"Produto '{row[5]}' adicionado ao carrinho.")
                        
#                         # Calcula o valor total do pedido
#                         total_value = Decimal(row[4]) * quant_estoque
#                         valor_total += total_value  # Atualiza valor_total
#                         print(f"O valor total do seu pedido é: {valor_total}")  # Imprime valor_total
                        
#                         new_quantity = row[1] - quant_estoque
#                         update_sql = "UPDATE produto SET quant_estoque = %s WHERE cod_produto = %s"
#                         conn.execute(update_sql, (new_quantity, cod_produto))
#                         conn.commit()
                        
#                         break
#                     else:
#                         print("Quantidade insuficiente em estoque.")
#                         return

#             # Pergunta ao usuário se ele quer continuar comprando
#             continuar = input("Deseja continuar comprando? (s/n): ")
            
            
#             # Limpa a saída do console antes da próxima interação
#             os.system('cls' if os.name == 'nt' else 'clear')
            
#             if continuar.lower() != 's':
#                 break

#         cliente_novo = input("Você é um cliente novo ou antigo? (n/a): ")

#         cpf_cliente = None  # Inicializa cpf_cliente com None

#         if cliente_novo.lower() == 'n':
#             # Se for um novo cliente, chama a função para cadastrar um novo cliente
#             ClienteForm().submit()
#             cpf_cliente = input("Por favor, digite seu CPF: ")  # Pede o CPF após o cadastro do novo cliente

#         elif cliente_novo.lower() == 'a':
#             # Se for um cliente antigo, solicita o CPF e registra a compra para esse CPF
#             cpf_cliente = input("Por favor, digite seu CPF: ")

#         if cpf_cliente and conn.customer_exists(cpf_cliente):
#             print("Bem-vindo de volta!")
            
#             # Verifica se o cliente atende aos critérios para um desconto
#             conn.cur.execute("SELECT cidade, animefavorito, timefutebol FROM cliente WHERE cpf = %s", (cpf_cliente,))
#             cidade, animefavorito, timefutebol = conn.cur.fetchone()
            
#             # Declarações de impressão para depuração:
#             print("cidade:", cidade)
#             print("animefavorito:", animefavorito)
#             print("timefutebol:", timefutebol)
            
#             if cidade == "Souza" or animefavorito == "One Piece" or timefutebol == "Flamengo":
#                 valor_total *= Decimal('0.9')  # Aplica um desconto de 10%
#                 print("Parabéns! Você ganhou um desconto de 10%. O valor total do seu pedido com desconto é: {:.2f}".format(valor_total))
#         else:
#             print("Parece que você é um novo cliente. Vamos fazer seu cadastro.")
            
#             # Limpa a saída do console antes de cada interação
#             os.system('cls' if os.name == 'nt' else 'clear')
            
#             ClienteForm().submit()

#     except Exception as e:
#         print("Erro ao fazer a compra:", str(e))
#     finally:
#         conn.close()



class ClienteForm:
    def submit(self):
        layout = [[sg.Text('Nome:'), sg.Input(key='-NOME-')],
                  [sg.Text('CPF:'), sg.Input(key='-CPF-')],
                  [sg.Text('Sexo:'), sg.Input(key='-SEXO-')],
                  [sg.Text('Email:'), sg.Input(key='-EMAIL-')],
                  [sg.Text('Cidade:'), sg.Input(key='-CIDADE-')],
                  [sg.Text('Time de Futebol:'), sg.Input(key='-TIMEFUTEBOL-')],
                  [sg.Text('Anime Favorito:'), sg.Input(key='-ANIMEFAVORITO-')],
                  [sg.Button('Submit')]]

        window = sg.Window('Cliente Form', layout)

        event, values = window.read()
        if event == 'Submit':
            self.insert_cliente(values['-NOME-'], values['-CPF-'], values['-SEXO-'], values['-EMAIL-'], values['-CIDADE-'], values['-TIMEFUTEBOL-'], values['-ANIMEFAVORITO-'])

        window.close()

    def insert_cliente(self, nome, cpf, sexo, email, cidade, timefutebol, animefavorito):
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
        layout = [[sg.Text('Escolha uma opção de pagamento:')],
                  [sg.Radio('Cartão', "RADIO1", default=True, key='-CARTAO-')],
                  [sg.Radio('Boleto', "RADIO1", key='-BOLETO-')],
                  [sg.Radio('Pix', "RADIO1", key='-PIX-')],
                  [sg.Radio('Berries', "RADIO1", key='-BERRIES-')],
                  [sg.Button('Submit')]]

        window = sg.Window('Forma de Pagamento', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Submit':
                break

        window.close()

        tipo = None
        if values['-CARTAO-']:
            tipo = 1
        elif values['-BOLETO-']:
            tipo = 2
        elif values['-PIX-']:
            tipo = 3
        elif values['-BERRIES-']:
            tipo = 4

        status = sg.popup_get_text('Digite o status do pagamento:')

        if tipo is not None and status is not None:
            self.insert_forma_pagamento(tipo, status)
        else:
            sg.popup("Forma de pagamento inválida.")

    def insert_forma_pagamento(self, tipo, status):
        try:
            conn = Connection()
            
            sql = "INSERT INTO FormaPagamento (tipo, status) VALUES (%s, %s);"
            conn.execute(sql, (tipo, status))
            
            conn.commit()
            conn.close()
            sg.popup("Forma de pagamento inserida com sucesso!")

        except Exception as e:
            sg.popup("Erro ao inserir forma de pagamento:", str(e))

class ProdutoForm:
    def submit(self):
        layout = [[sg.Text('Nome do Produto:'), sg.Input(key='-MARCA-')],
                  [sg.Text('Preço do Produto:'), sg.Input(key='-VALOR-', size=(10,1))],
                  [sg.Text('Quantidade em Estoque:'), sg.Input(key='-QUANT_ESTOQUE-', size=(10,1))],
                  [sg.Text('Data de Validade (DD-MM-AAAA):'), sg.Input(key='-VALIDADE-', size=(10,1))],
                  [sg.Text('Fabricado em Mari? (Sim/Não):'), sg.Input(key='-FABRICADO_EM_MARI-', size=(10,1))],
                  [sg.Button('Submit')]]

        window = sg.Window('Produto Form', layout)

        event, values = window.read()
        if event == 'Submit':
            self.insert_produto(values['-MARCA-'], float(values['-VALOR-']), int(values['-QUANT_ESTOQUE-']), values['-VALIDADE-'], values['-FABRICADO_EM_MARI-'])

        window.close()

    def insert_produto(self, marca, valor, quant_estoque, validade, fabricado_em_mari):
        try:
            conn = Connection()
            
            sql = "INSERT INTO Produto (marca, valor, quant_estoque, validade, fabricado_em_mari) VALUES (%s, %s, %s, %s, %s);"
            conn.execute(sql,(marca,float(valor),int(quant_estoque),validade,fabricado_em_mari=='Sim'))
            
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
            # Create a layout for the menu tab
        menu_layout = [[sg.Text("Digite 1 para realizar uma compra")],
                       [sg.Text("Digite 2 para ver se um produto esta no estoque")],
                       [sg.Text("Digite 3 para entrar como funcionário")],
                       [sg.Text("Digite 4 para cadastrar Produto")],
                       [sg.Text("Digite 0 para sair")],
                       [sg.Input(key='-IN-')],
                       [sg.Button('Ok'), sg.Button('Sair')]]

        # Create a layout for the products tab
        produto_layout = self.app.load_data()  # Load product data here

        # Create a layout for the tabs
        layout = [[sg.TabGroup([[sg.Tab('Menu', menu_layout), sg.Tab('Produtos', produto_layout)]])]]

        window = sg.Window('Menu', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Sair':
                break

            if event == 'Ok':
                opcao = int(values['-IN-'])

                if opcao == 1:
                    fazer_compra()  # First, select items to purchase
                    # self.cliente_form.submit()  # Then, register the customer
                    self.forma_pagamento_form.submit()
                    
                elif opcao == 3:
                    cpf_funcionario = sg.popup_get_text('Por favor, digite seu CPF:')
                    senha_funcionario = sg.popup_get_text('Por favor, digite sua senha:')
                    conn = Connection()
                    if conn.funcionario_existe(cpf_funcionario, senha_funcionario):
                        relatorio = gerar_relatorio_vendas()
                        sg.popup_scrolled("Relatório de vendas:", "\n".join(str(linha) for linha in relatorio))
                    else:
                        sg.popup("CPF ou senha inválidos.")
                elif opcao == 4:
                    self.produto_form.submit()
                    print("cadastro de Produto:")
                else:
                    sg.popup("Opção inválida. Tente novamente.")

        window.close()
        pass


if __name__ == "__main__":
    menu = Menu()
    menu.run()

    
