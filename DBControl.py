import psycopg2 as db
import csv

class Config:
    def __init__(self):
        self.config = {
            "dbproject": {
                "user": "postgres",
                "password": "12345678",
                "host": "localhost",
                "port": "5432",
                "database": "dbproject"
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        self.conn = db.connect(**self.config["dbproject"])
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

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
        self.cursor.execute(sql, params or ())
        return self.fetchall()

class Cliente(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO cliente (nome, cpf, sexo, email) VALUES (%s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM cliente WHERE cod_cliente = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM cliente WHERE cod_cliente = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE cliente SET nome = %s, cpf = %s, sexo = %s, email = %s WHERE cod_cliente = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_cliente"):
        sql =  "SELECT * FROM cliente WHERE cod_cliente = %s"
        if column == "nome":
            sql = "SELECT * FROM cliente WHERE nome LIKE %s"
        if column == "cpf":
            sql = "SELECT * FROM cliente WHERE cpf LIKE %s"
        if column == "sexo":
            sql = "SELECT * FROM cliente WHERE sexo = %s"
        if column == "email":
            sql = "SELECT * FROM cliente WHERE email LIKE %s"
        if column == "todos":
            sql = "SELECT * FROM cliente"
        data = self.query(sql, args)

        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome"], row["cpf"], row["sexo"], row["email"])
            print("Registros inseridos")
        except Exception as e:
            print("Erro ao inserir", e)

    def list_all(self):
        return self.query("SELECT * FROM cliente;")

class Funcionario(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO funcionario (nome, cpf, sexo, email, salario, funcao, comissoes) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM funcionario WHERE cod_funcionario = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM funcionario WHERE cod_funcionario = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE funcionario SET nome = %s, cpf = %s, sexo = %s, email = %s, salario = %s, funcao = %s, comissoes = %s WHERE cod_funcionario = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_funcionario"):
        sql =  "SELECT * FROM funcionario WHERE cod_funcionario = %s"
        if column == "nome":
            sql = "SELECT * FROM funcionario WHERE nome LIKE %s"
        if column == "cpf":
            sql = "SELECT * FROM funcionario WHERE cpf LIKE %s"
        if column == "sexo":
            sql = "SELECT * FROM funcionario WHERE sexo = %s"
        if column == "email":
            sql = "SELECT * FROM funcionario WHERE email LIKE %s"
        if column == "salario":
            sql = "SELECT * FROM funcionario WHERE salario LIKE %s"
        if column == "funcao":
            sql = "SELECT * FROM funcionario WHERE funcao LIKE %s"
        if column == "comissoes":
            sql = "SELECT * FROM funcionario WHERE comissoes LIKE %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome"], row["cpf"], row["sexo"], row["email"], row["salario"], row["funcao"], row["comissoes"])
            print("Registros inseridos")
        except Exception as e:
            print("Erro ao inserir", e)

    def list_all(self):
        return self.query("SELECT * FROM funcionario;")

class Produto(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO Produto (quant_estoque, validade, fabricante, valor, marca) VALUES (%s, %s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM Produto WHERE Cod_produto = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM Produto WHERE Cod_produto = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE Produto SET quant_estoque = %s, validade = %s, fabricante = %s, valor = %s, marca = %s WHERE cod_produto = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_produto"):
        sql =  "SELECT * FROM Produto WHERE Cod_produto = %s"
        if column == "quant_estoque":
            sql = "SELECT * FROM Produto WHERE quant_estoque = %s"
        if column == "validade":
            sql = "SELECT * FROM Produto WHERE validade LIKE %s"
        if column == "fabricante":
            sql = "SELECT * FROM Produto WHERE fabricante LIKE %s"
        if column == "valor":
            sql = "SELECT * FROM Produto WHERE valor LIKE %s"
        if column == "marca":
            sql = "SELECT * FROM Produto WHERE marca LIKE %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["quant_estoque"], row["validade"], row["fabricante"], row["valor"], row["marca"])
            print("Registros inseridos")
        except Exception as e:
            print("Erro ao inserir", e)

    def list_all(self):
        return self.query("SELECT * FROM Produto;")

class ItensVendas(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO itens_vendas (Cod_produto, tipo, quant_comp) VALUES (%s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM itens_vendas WHERE cod_itens = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM itens_vendas WHERE cod_itens = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE itens_vendas SET cod_produto = %s, tipo = %s, quant_comp = %s WHERE cod_itens = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_itens"):
        sql =  "SELECT * FROM itens_vendas WHERE cod_itens = %s"
        if column == "cod_produto":
            sql = "SELECT * FROM itens_vendas WHERE cod_produto = %s"
        if column == "tipo":
            sql = "SELECT * FROM itens_vendas WHERE tipo LIKE %s"
        if column == "quant_comp":
            sql = "SELECT * FROM itens_vendas WHERE quant_comp LIKE %s"

        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["cod_produto"], row["tipo"], row["quant_comp"])
            print("Registros inseridos")
        except Exception as e:
            print("Erro ao inserir", e)

    def list_all(self):
        return self.query("SELECT * FROM itens_vendas;")

class Vendas(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        sql = "INSERT INTO vendas (cod_itens, cod_funcionario, cod_cliente, cod_produto, num_mesa, valor_comissao, quant_produto, valor_compra, data_) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.execute(sql, args)
        self.commit()

    def delete(self, id):
        try:
            sql_s = f"SELECT * FROM vendas WHERE cod_vendas = {id}"
            if not self.query(sql_s):
                return "Registro não encontrado para deletar."
            sql_d = f"DELETE FROM vendas WHERE cod_vendas = {id}"
            self.execute(sql_d)
            self.commit()
            return "Registro deletado"
        except Exception as e:
            print("Erro ao deletar", e)

    def update(self, id, *args):
        try:
            sql = f"UPDATE vendas SET cod_itens = %s, cod_funcionario = %s, cod_cliente = %s, cod_produto = %s, num_mesa = %s, valor_comissao = %s, quant_produto =%s, valor_compra = %s, data_ =%s WHERE cod_vendas = {id}"
            self.execute(sql, args)
            self.commit()
            print("Registro atualizado")
        except Exception as e:
            print("Erro ao atualizar", e)

    def search(self, *args, column="cod_vendas"):
        sql =  "SELECT * FROM vendas WHERE cod_vendas = %s"
        if column == "cod_itens":
            sql = "SELECT * FROM vendas WHERE cod_itens = %s"
        if column == "cod_funcionario":
            sql = "SELECT * FROM vendas WHERE cod_funcionario = %s"
        if column == "cod_cliente":
            sql = "SELECT * FROM vendas WHERE cod_cliente = %s"
        if column == "cod_produto":
            sql = "SELECT * FROM vendas WHERE cod_produto = %s"
        if column == "num_mesa":
            sql = "SELECT * FROM vendas WHERE num_mesa = %s"
        if column == "valor_comissao":
            sql = "SELECT * FROM vendas WHERE valor_comissao LIKE %s"
        if column == "quant_produto":
            sql = "SELECT * FROM vendas WHERE quant_produto = %s"
        if column == "valor_compra":
            sql = "SELECT * FROM vendas WHERE valor_compra LIKE %s"
        if column == "data_":
            sql = "SELECT * FROM vendas WHERE data_ LIKE %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["cod_itens"], row["cod_funcionario"], row["cod_cliente"], row["cod_produto"], row["num_mesa"], row["valor_comissao"], row["quant_produto"], row["valor_compra"], row["data_"])
            print("Registros inseridos")
        except Exception as e:
            print("Erro ao inserir", e)

    def list_all(self):
        return self.query("SELECT * FROM vendas;")

def exibir_menu():
    print("Selecione uma opção:")
    print("1. Inserir")
    print("2. Atualizar")
    print("3. Excluir")
    print("4. Pesquisar por")
    print("5. Listar todos")
    print("6. Exibir um")
    print("7. Inserir CSV")
    print("0. Sair")

def menu_inserir(cliente):
    nome = input("Digite o nome: ")
    cpf = input("Digite o CPF: ")
    sexo = input("Digite o sexo: ")
    email = input("Digite o email: ")
    cliente.insert(nome, cpf, sexo, email)

def menu_atualizar(cliente):
    id_update = input("Digite o id que deseja atualizar: ")
    nome = input("Digite o novo nome: ")
    cpf = input("Digite o novo CPF: ")
    sexo = input("Digite o novo sexo: ")
    email = input("Digite o novo email: ")
    cliente.update(id_update, nome, cpf, sexo, email)

def menu_excluir(cliente):
    id_delete = input("Digite o id que deseja excluir: ")
    cliente.delete(id_delete)

def menu_pesquisar_por(cliente):
    print("1. Nome")
    print("2. CPF")
    print("3. Sexo")
    print("4. Email")
    valor_de_pesquisa = input("Selecione uma opção de pesquisa: ")
    if valor_de_pesquisa == "1":
        aux_pesquisa = input("Digite o nome que deseja pesquisar: ")
        resultado = cliente.search(aux_pesquisa, column="nome")
    elif valor_de_pesquisa == "2":
        aux_pesquisa = input("Digite o CPF que deseja pesquisar: ")
        resultado = cliente.search(aux_pesquisa, column="cpf")
    elif valor_de_pesquisa == "3":
        aux_pesquisa = input("Digite o sexo que deseja pesquisar: ")
        resultado = cliente.search(aux_pesquisa, column="sexo")
    elif valor_de_pesquisa == "4":
        aux_pesquisa = input("Digite o email que deseja pesquisar: ")
        resultado = cliente.search(aux_pesquisa, column="email")
    else:
        resultado = "Opção inválida."
    
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_listar_todos(cliente):
    resultado = cliente.list_all()
    if resultado:
        for row in resultado:
            print(row)
    else:
        print("Nenhum registro encontrado.")

def menu_exibir_um(cliente):
    valor_de_pesquisa = input("Digite o id que deseja exibir: ")
    resultado = cliente.search(valor_de_pesquisa)
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_inserir_csv(cliente):
    filename = input("Digite o nome do arquivo CSV para inserção: ")
    cliente.insert_csv(filename)

def menu_inserir_produto(produto):
    quant_estoque = input("Digite a quantidade em estoque: ")
    validade = input("Digite a validade: ")
    fabricante = input("Digite o fabricante: ")
    valor = input("Digite o valor: ")
    marca = input("Digite a marca: ")
    produto.insert(quant_estoque, validade, fabricante, valor, marca)

def menu_atualizar_produto(produto):
    id_update = input("Digite o id que deseja atualizar: ")
    quant_estoque = input("Digite a nova quantidade em estoque: ")
    validade = input("Digite a nova validade: ")
    fabricante = input("Digite o novo fabricante: ")
    valor = input("Digite o novo valor: ")
    marca = input("Digite a nova marca: ")
    produto.update(id_update, quant_estoque, validade, fabricante, valor, marca)

def menu_excluir_produto(produto):
    id_delete = input("Digite o id que deseja excluir: ")
    produto.delete(id_delete)

def menu_pesquisar_por_produto(produto):
    print("1. Quantidade em Estoque")
    print("2. Validade")
    print("3. Fabricante")
    print("4. Valor")
    print("5. Marca")
    valor_de_pesquisa = input("Selecione uma opção de pesquisa: ")
    if valor_de_pesquisa == "1":
        aux_pesquisa = input("Digite a quantidade em estoque que deseja pesquisar: ")
        resultado = produto.search(aux_pesquisa, column="quant_estoque")
    elif valor_de_pesquisa == "2":
        aux_pesquisa = input("Digite a validade que deseja pesquisar: ")
        resultado = produto.search(aux_pesquisa, column="validade")
    elif valor_de_pesquisa == "3":
        aux_pesquisa = input("Digite o fabricante que deseja pesquisar: ")
        resultado = produto.search(aux_pesquisa, column="fabricante")
    elif valor_de_pesquisa == "4":
        aux_pesquisa = input("Digite o valor que deseja pesquisar: ")
        resultado = produto.search(aux_pesquisa, column="valor")
    elif valor_de_pesquisa == "5":
        aux_pesquisa = input("Digite a marca que deseja pesquisar: ")
        resultado = produto.search(aux_pesquisa, column="marca")
    else:
        resultado = "Opção inválida."
    
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_listar_todos_produto(produto):
    resultado = produto.list_all()
    if resultado:
        for row in resultado:
            print(row)
    else:
        print("Nenhum registro encontrado.")

def menu_exibir_um_produto(produto):
    valor_de_pesquisa = input("Digite o id que deseja exibir: ")
    resultado = produto.search(valor_de_pesquisa)
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_inserir_itens_vendas(itens_vendas):
    cod_produto = input("Digite o código do produto: ")
    tipo = input("Digite o tipo: ")
    quant_comp = input("Digite a quantidade comprada: ")
    itens_vendas.insert(cod_produto, tipo, quant_comp)

def menu_atualizar_itens_vendas(itens_vendas):
    id_update = input("Digite o id que deseja atualizar: ")
    cod_produto = input("Digite o novo código do produto: ")
    tipo = input("Digite o novo tipo: ")
    quant_comp = input("Digite a nova quantidade comprada: ")
    itens_vendas.update(id_update, cod_produto, tipo, quant_comp)

def menu_excluir_itens_vendas(itens_vendas):
    id_delete = input("Digite o id que deseja excluir: ")
    itens_vendas.delete(id_delete)

def menu_pesquisar_por_itens_vendas(itens_vendas):
    print("1. Código do Produto")
    print("2. Tipo")
    print("3. Quantidade Comprada")
    valor_de_pesquisa = input("Selecione uma opção de pesquisa: ")
    if valor_de_pesquisa == "1":
        aux_pesquisa = input("Digite o código do produto que deseja pesquisar: ")
        resultado = itens_vendas.search(aux_pesquisa, column="cod_produto")
    elif valor_de_pesquisa == "2":
        aux_pesquisa = input("Digite o tipo que deseja pesquisar: ")
        resultado = itens_vendas.search(aux_pesquisa, column="tipo")
    elif valor_de_pesquisa == "3":
        aux_pesquisa = input("Digite a quantidade comprada que deseja pesquisar: ")
        resultado = itens_vendas.search(aux_pesquisa, column="quant_comp")
    else:
        resultado = "Opção inválida."
    
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_listar_todos_itens_vendas(itens_vendas):
    resultado = itens_vendas.list_all()
    if resultado:
        for row in resultado:
            print(row)
    else:
        print("Nenhum registro encontrado.")

def menu_exibir_um_itens_vendas(itens_vendas):
    valor_de_pesquisa = input("Digite o id que deseja exibir: ")
    resultado = itens_vendas.search(valor_de_pesquisa)
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_inserir_vendas(vendas):
    cod_itens = input("Digite o código dos itens: ")
    cod_funcionario = input("Digite o código do funcionário: ")
    cod_cliente = input("Digite o código do cliente: ")
    cod_produto = input("Digite o código do produto: ")
    num_mesa = input("Digite o número da mesa: ")
    valor_comissão = input("Digite o valor da comissao: ")
    quant_produto = input("Digite a quantidade de produtos: ")
    valor_compra = input("Digite o valor da compra: ")
    data_ = input("Digite a data: ")
    vendas.insert(cod_itens, cod_funcionario, cod_cliente, cod_produto, num_mesa, valor_comissão, quant_produto, valor_compra, data_)

def menu_atualizar_vendas(vendas):
    id_update = input("Digite o id que deseja atualizar: ")
    cod_itens = input("Digite o novo código dos itens: ")
    cod_funcionario = input("Digite o novo código do funcionário: ")
    cod_cliente = input("Digite o novo código do cliente: ")
    cod_produto = input("Digite o novo código do produto: ")
    num_mesa = input("Digite o novo número da mesa: ")
    valor_comissão = input("Digite o novo valor da comissao: ")
    quant_produto = input("Digite a nova quantidade de produtos: ")
    valor_compra = input("Digite o novo valor da compra: ")
    data_ = input("Digite a nova data: ")
    vendas.update(id_update, cod_itens, cod_funcionario, cod_cliente, cod_produto, num_mesa, valor_comissão, quant_produto, valor_compra, data_)

def menu_excluir_vendas(vendas):
    id_delete = input("Digite o id que deseja excluir: ")
    vendas.delete(id_delete)

def menu_pesquisar_por_vendas(vendas):
    print("1. Código dos Itens")
    print("2. Código do Funcionário")
    print("3. Código do Cliente")
    print("4. Código do Produto")
    print("5. Número da Mesa")
    print("6. Valor da Comissao")
    print("7. Quantidade de Produtos")
    print("8. Valor da Compra")
    print("9. Data")
    valor_de_pesquisa = input("Selecione uma opção de pesquisa: ")
    if valor_de_pesquisa == "1":
        aux_pesquisa = input("Digite o código dos itens que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="cod_itens")
    elif valor_de_pesquisa == "2":
        aux_pesquisa = input("Digite o código do funcionário que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="cod_funcionario")
    elif valor_de_pesquisa == "3":
        aux_pesquisa = input("Digite o código do cliente que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="cod_cliente")
    elif valor_de_pesquisa == "4":
        aux_pesquisa = input("Digite o código do produto que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="cod_produto")
    elif valor_de_pesquisa == "5":
        aux_pesquisa = input("Digite o número da mesa que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="num_mesa")
    elif valor_de_pesquisa == "6":
        aux_pesquisa = input("Digite o valor da comissao que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="valor_comissao")
    elif valor_de_pesquisa == "7":
        aux_pesquisa = input("Digite a quantidade de produtos que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="quant_produto")
    elif valor_de_pesquisa == "8":
        aux_pesquisa = input("Digite o valor da compra que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="valor_compra")
    elif valor_de_pesquisa == "9":
        aux_pesquisa = input("Digite a data que deseja pesquisar: ")
        resultado = vendas.search(aux_pesquisa, column="data_")
    else:
        resultado = "Opção inválida."
    
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def menu_listar_todos_vendas(vendas):
    resultado = vendas.list_all()
    if resultado:
        for row in resultado:
            print(row)
    else:
        print("Nenhum registro encontrado.")

def menu_exibir_um_vendas(vendas):
    valor_de_pesquisa = input("Digite o id que deseja exibir: ")
    resultado = vendas.search(valor_de_pesquisa)
    if resultado:
        if isinstance(resultado, str):
            print(resultado)
        else:
            for row in resultado:
                print(row)
    else:
        print("Nenhum resultado encontrado.")

def main():
    while True:
        print("\nEscolha a classe com a qual você deseja interagir:")
        print("1. Cliente")
        print("2. Funcionário")
        print("3. Produto")
        print("4. Itens de Vendas")
        print("5. Vendas")
        print("0. Sair")

        opcao = input("\nDigite o número da classe que deseja interagir (ou 0 para sair): ")

        if opcao == "0":
            print("Encerrando o programa.")
            break
        elif opcao == "1":
            cliente = Cliente()
            while True:
                exibir_menu()
                opcao_cliente = input("\nDigite o número da opção desejada: ")
                if opcao_cliente == "1":
                    menu_inserir(cliente)
                elif opcao_cliente == "2":
                    menu_atualizar(cliente)
                elif opcao_cliente == "3":
                    menu_excluir(cliente)
                elif opcao_cliente == "4":
                    menu_pesquisar_por(cliente)
                elif opcao_cliente == "5":
                    menu_listar_todos(cliente)
                elif opcao_cliente == "6":
                    menu_exibir_um(cliente)
                elif opcao_cliente == "7":
                    menu_inserir_csv(cliente)
                elif opcao_cliente == "0":
                    break
                else:
                    print("Opção inválida.")
        elif opcao == "2":
            funcionario = Funcionario()
            while True:
                exibir_menu()
                opcao_funcionario = input("\nDigite o número da opção desejada: ")
                if opcao_funcionario == "1":
                    menu_inserir(funcionario)
                elif opcao_funcionario == "2":
                    menu_atualizar(funcionario)
                elif opcao_funcionario == "3":
                    menu_excluir(funcionario)
                elif opcao_funcionario == "4":
                    menu_pesquisar_por(funcionario)
                elif opcao_funcionario == "5":
                    menu_listar_todos(funcionario)
                elif opcao_funcionario == "6":
                    menu_exibir_um(funcionario)
                elif opcao_funcionario == "7":
                    menu_inserir_csv(funcionario)
                elif opcao_funcionario == "0":
                    break
                else:
                    print("Opção inválida.")
        elif opcao == "3":
            produto = Produto()
            while True:
                exibir_menu()
                opcao_produto = input("\nDigite o número da opção desejada: ")
                if opcao_produto == "1":
                    menu_inserir_produto(produto)
                elif opcao_produto == "2":
                    menu_atualizar_produto(produto)
                elif opcao_produto == "3":
                    menu_excluir_produto(produto)
                elif opcao_produto == "4":
                    menu_pesquisar_por_produto(produto)
                elif opcao_produto == "5":
                    menu_listar_todos_produto(produto)
                elif opcao_produto == "6":
                    menu_exibir_um_produto(produto)
                elif opcao_produto == "7":
                    menu_inserir_csv(produto)
                elif opcao_produto == "0":
                    break
                else:
                    print("Opção inválida.")
        elif opcao == "4":
            itens_vendas = ItensVendas()
            while True:
                exibir_menu()
                opcao_itens_vendas = input("\nDigite o número da opção desejada: ")
                if opcao_itens_vendas == "1":
                    menu_inserir_itens_vendas(itens_vendas)
                elif opcao_itens_vendas == "2":
                    menu_atualizar_itens_vendas(itens_vendas)
                elif opcao_itens_vendas == "3":
                    menu_excluir_itens_vendas(itens_vendas)
                elif opcao_itens_vendas == "4":
                    menu_pesquisar_por_itens_vendas(itens_vendas)
                elif opcao_itens_vendas == "5":
                    menu_listar_todos_itens_vendas(itens_vendas)
                elif opcao_itens_vendas == "6":
                    menu_exibir_um_itens_vendas(itens_vendas)
                elif opcao_itens_vendas == "7":
                    menu_inserir_csv(itens_vendas)
                elif opcao_itens_vendas == "0":
                    break
                else:
                    print("Opção inválida.")
        elif opcao == "5":
            vendas = Vendas()
            while True:
                exibir_menu()
                opcao_vendas = input("\nDigite o número da opção desejada: ")
                if opcao_vendas == "1":
                    menu_inserir_vendas(vendas)
                elif opcao_vendas == "2":
                    menu_atualizar_vendas(vendas)
                elif opcao_vendas == "3":
                    menu_excluir_vendas(vendas)
                elif opcao_vendas == "4":
                    menu_pesquisar_por_vendas(vendas)
                elif opcao_vendas == "5":
                    menu_listar_todos_vendas(vendas)
                elif opcao_vendas == "6":
                    menu_exibir_um_vendas(vendas)
                elif opcao_vendas == "7":
                    menu_inserir_csv(vendas)
                elif opcao_vendas == "0":
                    break
                else:
                    print("Opção inválida.")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
