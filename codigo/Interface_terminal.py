from investimento import Investimento, datetime
import psycopg2
from decimal import Decimal

conn = psycopg2.connect(
    host="containers-us-west-209.railway.app",
    port = 7199,
    database="railway",
    user="postgres",
    password="68N7rlanoyebMviVGHmi"
)

cur = conn.cursor()

def menu():
    return '\n[1]_ Criar investimento. [2]_ Modificar investimento. [3]_ Listar investimentos. [4]_ Deletar investimento. [5]_ Detalhar ativo.'

def legenda_investimento():
    return '____________________________________________________________________________________________________________________________\nID| CÓDIGO  |    DATA    | QUANTIDADE | VALOR DA UNIDADE |  TIPO  |  TAXA DE CORRETAGEM  | VALOR DA OPERAÇÃO | VALOR TOTAL |'

def linhas_horizontais():
    return '--+---------+------------+------------+------------------+--------+----------------------+-------------------+-------------+'

def listar_investimentos(lista):
    print(legenda_investimento())
    for n in range(len(lista)):
        print(linhas_horizontais())
        print(f' {n + 1}| {lista[n]}')

def listar_investimentos_com_banco(lista):
    cur.execute(f"SELECT * FROM investimento")
    lista_nao_convertida = cur.fetchall()
    for n in range(len(lista_nao_convertida)):
        objeto = Investimento(lista_nao_convertida[n][0], lista_nao_convertida[n][1], lista_nao_convertida[n][2], float(lista_nao_convertida[n][3]), lista_nao_convertida[n][4], float(lista_nao_convertida[n][5]))
        lista.append(objeto)
    lista.sort(key = lambda x: x.data)
    listar_investimentos(lista)
    del lista[:]
    del lista_nao_convertida[:]
    conn.commit()

def criar_investimento():
    codigo = digitos('codigo')
    data = digitos('data')
    quantidade = digitos ('quantidade')
    valor_unidade = digitos ('valor_unidade')
    tipo = digitos('tipo')
    taxa_de_corretagem = digitos('taxa_de_corretagem')

    # lista.append(Investimento(codigo, data, quantidade, valor_unidade, tipo, taxa_de_corretagem))

    cur.execute(f"INSERT INTO investimento (cod_investimento, data, quantidade, valor_unidade, tipo_investimento, taxa_de_corretagem) VALUES ('{codigo}', '{data}', {str(quantidade)}, {str(valor_unidade)}, '{tipo}', {str(taxa_de_corretagem)})")

    conn.commit()

def modificar_investimento():
    codigo = digitos('codigo')
    data = digitos('data')
    cur.execute(f"SELECT * FROM investimento WHERE cod_investimento = '{codigo}' and data = '{data}'")
    investimento = cur.fetchall()
    objeto = Investimento(investimento[0][0], investimento[0][1], investimento[0][2], float(investimento[0][3]), investimento[0][4], float(investimento[0][5]))
    print(legenda_investimento())
    print(linhas_horizontais())
    print(f'NA| {objeto}')
    print(opcoes_de_mudanca())
    escolha = digitos('escolha')
    if escolha == 1:
        nov_codigo = digitos('codigo')
        cur.execute(f"UPDATE investimento SET cod_investimento = '{nov_codigo}' WHERE cod_investimento = '{codigo}' and data = '{data}'")
    elif escolha == 2:
        nov_data = digitos('data')
        cur.execute(f"UPDATE investimento SET data = '{nov_data}' WHERE cod_investimento = '{codigo}' and data = '{data}'")
    elif escolha == 3:
        nov_quantidade = digitos('quantidade')
        cur.execute(f"UPDATE investimento SET quantidade = '{nov_quantidade}' WHERE cod_investimento = '{codigo}' and data = '{data}'")
    elif escolha == 4:
        nov_valor_unidade = digitos('valor_unidade')
        cur.execute(f"UPDATE investimento SET valor_unidade = '{nov_valor_unidade}' WHERE cod_investimento = '{codigo}' and data = '{data}'")
    elif escolha == 5:
        nov_tipo = digitos('tipo')
        cur.execute(f"UPDATE investimento SET tipo_investimento = '{nov_tipo}' WHERE cod_investimento = '{codigo}' and data = '{data}'")
    elif escolha == 6:
        nov_taxa_de_corretagem = digitos('taxa_de_corretagem')
        cur.execute(f"UPDATE investimento SET cod_investimento = '{nov_taxa_de_corretagem}' WHERE cod_investimento = '{codigo}' and data = '{data}'")

def deletar_investimento():
    codigo = digitos('codigo')
    data = digitos('data')
    cur.execute(f"SELECT * FROM investimento WHERE cod_investimento = '{codigo}' and data = '{data}'")
    investimento = cur.fetchall()
    objeto = Investimento(investimento[0][0], investimento[0][1], investimento[0][2], float(investimento[0][3]), investimento[0][4], float(investimento[0][5]))
    print(legenda_investimento())
    print(linhas_horizontais())
    print(f'NA| {objeto}')
    cur.execute(f"DELETE FROM investimento WHERE cod_investimento = '{codigo}' and data = '{data}'")

def opcoes_de_mudanca():
    return '\n[1]_ Código. [2]_ Data [3]_ Quantidade. [4]_ Valor Unidade. [5]_ Tipo. [6]_ Taxa de Corretagem.'

def main():

    lista = []


    while True:
        lista.sort(key = lambda x: x.data)

        print(menu())
        
        escolha = digitos('escolha')

        if escolha == 1:
            criar_investimento()
        elif escolha == 2:
            modificar_investimento()
        elif escolha == 3:
            listar_investimentos_com_banco(lista)
        elif escolha == 4:
            deletar_investimento()
        elif escolha == 5:
            pass

def digitos(info):

    # SISTEMA DE ENTRADA PARA O CÓDIGO DO INVESTIMENTO:
    if info == 'codigo':
        while True:
            try:
                codigo = input('\nDigite o código do investimento: ').upper()
                if not codigo[:3].isalpha() or not codigo[4:].isnumeric() and len(codigo) < 5 or len(codigo) > 5:
                    raise Exception
                return codigo
            except:
                print('\nCódigo inválido. Tente novamente!')

    # SISTEMA DE ENTRADA PARA A DATA DO INVESTIMENTO:
    elif info == 'data':
        while True:
            try:
                data = input('\nDigite a data do investimento: ')
                data_convertida = datetime.datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                return data_convertida
            except:
                print('\nData inválida. Tente novamente!')

    # SISTEMA DE ENTRADA PARA A QUANTIDADE DO INVESTIMENTO:
    elif info == 'quantidade':
        while True:
            try:
                quantidade = int(input('\nDigite a quantidade do investimento: '))
                if quantidade < 1:
                    raise Exception
                return quantidade
            except:
                print('\nQuantidade inválida. Tente novamente!')

    # SISTEMA DE ENTRADA PARA O VALOR DA UNIDADE DO INVESTIMENTO:
    elif info == 'valor_unidade':
        while True:
            try:
                valor_unidade = float(input('\nDigite o valor da unidade do investimento: '))
                if valor_unidade <= 0:
                    raise Exception
                return valor_unidade
            except:
                print('\nValor inválido. Tente novamente!')

    # SISTEMA DE ENTRADA PARA O TIPO DO INVESTIMENTO:
    elif info == 'tipo':
        while True:
            try:
                tipo = input('\nDigite o tipo do investimento: ').upper().strip()
                if tipo != 'COMPRA' and tipo != 'VENDA':
                    raise Exception
                return tipo
            except:
                print('\nTipo inválido. Tente novamente!')

    # SISTEMA DE ENTRADA PARA A TAXA DE CORRETAGEM DO INVESTIMENTO:
    elif info == 'taxa_de_corretagem':
        while True:
            try:
                taxa_de_corretagem = float(input('\nDigite a taxa de corretagem do investimento: '))
                if taxa_de_corretagem <= 0:
                    raise Exception
                return taxa_de_corretagem
            except:
                print('\nValor da taxa inválido. Tente novamente!')

    # SISTEMA DE ENTRADA PARA A ESCOLHA DO MENU:
    elif info == 'escolha':
        while True:
            try:
                escolha = int(input('\nDigite sua escolha: '))
                if escolha < 1 or escolha > 6:
                    raise Exception
                return escolha
            except:
                print('\nEscolha inválida. Tente novamente!')

if __name__ == '__main__':
    main()