import pandas as pd
import os
from datetime import datetime

def confirmacao():
    input("""\n
------------------------------------------------------------------------------------
                Pressione qualquer tecla para continuar: """)

def ver_estoque():
    try:
        df = pd.read_csv("estoque.csv")
        print("\nESTOQUE:\n")
        for index, row in df.iterrows():
            print(f"{row['produto']}:\nQuantidade: {row['qntd_atual']} | Matéria-prima: {row['materia-prima']} | Massa (g): {row['massa']} | Ciclo (s): {row['ciclo']} | \nNº de cavidades: {row['n_cavidades']} | Venda mensal: {row['venda_mensal']} | Produção mensal: {row['producao_mensal']} | Data: {row['data']} |\n")
    except:
        print("Arquivo não existe, tente novamente.")
        
    confirmacao()
        
    return 0

def adicionar_produto():
    try:
        produto = str(input("Nome do produto: "))
        quantidade_atual = int(input("Quantidade atual do produto em estoque: "))
        materia_prima = str(input("Matéria-prima utilizada: "))
        massa = int(input("Massa por unidade (g): "))
        ciclo = int(input("Ciclo (s): "))
        n_cavidades = int(input("Número de cavidades: "))
        venda_mensal = int(input("Venda mensal (Estimativa): "))
        producao_mensal = int(input("Produção mensal: "))
        
        arquivo_csv = "estoque.csv"
        
        novo_item = {
        "produto": produto,
        "qntd_atual": quantidade_atual,
        "materia-prima": materia_prima,
        "massa": massa,
        "ciclo": ciclo,
        "n_cavidades": n_cavidades,
        "venda_mensal": venda_mensal,
        "producao_mensal": producao_mensal,
        "data": datetime.now().strftime("%d/%m/%Y")
        }

        df_novo = pd.DataFrame([novo_item])

        if not os.path.exists(arquivo_csv): 
            df_novo.to_csv(arquivo_csv, index=False)
        else:
            df_novo.to_csv(arquivo_csv, mode='a', header=False, index=False)
            novo_item = {"Produto"}
            print("Produto adicionado com sucesso!")
        # se não existir o arquivo, ele cria um novo com os cabeçalhos, caso contrário, apenas adiciona os novos valores no arquivo
            
    except Exception as e:
        print("ERRO: ", e)
    

def remover_produto():
    return 0

def atualizar_produto():
    df = pd.read_csv("estoque.csv")
    df_str = df.to_string()
    linha = "-" * len(df_str.split("\n")[0])
    
    print("\nProdutos em estoque:\n")
    print(*df["produto"].values, sep="\n")
    
    try:
        nome = input("\nDigite o nome do produto que deseja atualizar: ")
        resultado = df[df["produto"] == nome]
        resultado_str = resultado.to_string(index=False, header=True)
        print(f"\n{resultado_str}\n")
        coluna = input("Digite o nome da coluna que deseja mudar: ")
        
        if coluna in df.columns:
            novo_valor = input(f"Digite o valor desejado para a coluna {coluna}: ")
            df.loc[df["produto"] == nome, coluna] = novo_valor
            df.to_csv('estoque.csv', index=False)
            print("\nValor alterado com sucesso.\n")
            print(linha)
            print(df)
            print(linha)
            confirmacao()
            
    except Exception as e:
        print("ERRO: ", e)
    
    return 0

def exportar_excel():
    df = pd.read_csv('estoque.csv')
    
    df.to_excel("estoque.xlsx", index=False, engine="openpyxl")
    print("\nArquivo exportado com sucesso no arquivo 'estoque.xslx'.")
    confirmacao()
    
def simulacao_mensal():
    df = pd.read_csv("estoque.csv")
    for i in range (len(df)):
        resultado = df.iloc[i, 7] - df.iloc[i, 6] # Produção mensal - venda mensal
        df.iloc[i, 1] += resultado
        
    df.to_csv('estoque.csv', index=False)
    opc = input("\nSimulação mensal concluída, deseja ver o estoque atualizado? (S/N): ")
    if opc.capitalize() == 'S':
        ver_estoque()
    else:
        return


def main():    
    
    while(True):
        escolha = input(("""\n
----------------------------------
        Estoque Bela
----------------------------------
O que deseja fazer?

1. Adicionar produto
2. Remover produto
3. Atualizar produto
4. Ver estoque
5. Exportar como excel
6. Simulação mensal
7. Sair
----------------------------------
Opção: """))
        
        if(escolha == "1"):
            print("Opção escolhida: 1. Adicionar produto")
            adicionar_produto()
        elif(escolha == "2"):
            print("Opção escolhida: 2. Remover produto")
            remover_produto()
        elif(escolha == "3"):
            print("Opção escolhida: 3. Atualizar produto")
            atualizar_produto()
        elif(escolha == "4"):
            print("Opção escolhida: 4. Ver estoque")
            ver_estoque()
        elif(escolha == "5"):
            print("Opção escolhida: 5. Exportar como excel")
            exportar_excel()
        elif(escolha == "6"):
            print("Opção escolhida: 6. Simulação mensal")
            simulacao_mensal()
        elif(escolha == "7"):
            print("Opção escolhida: 7. Sair")
            break
        else:
            print("Valor inválido, tente novamente.")
            
            


main()