import tkinter as tk
import webbrowser
import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from tkinter import messagebox

def confirmacao():
    input("""\n
------------------------------------------------------------------------------------
                Pressione qualquer tecla para continuar: """)

def ver_estoque():
    try:
        df = pd.read_csv("estoque.csv")
        print("\nESTOQUE:\n")
        for index, row in df.iterrows():
            print(f"{row['produto']}:\nQuantidade: {row['qntd_atual']} | Matéria-prima: {row['materia_prima']} | Massa (g): {row['massa']} | Ciclo (s): {row['ciclo']} | \nNº de cavidades: {row['n_cavidades']} | Venda mensal: {row['venda_mensal']} | Produção mensal: {row['producao_mensal']} | Data: {row['data']} |\n")
    except:
        print("Arquivo não existe, tente novamente.")
        
    confirmacao()
        
    return 0

def adicionar_produto():
    try:
        janela_input = tk.Toplevel()
        janela_input.title("Adicionar Produto")
        janela_input.geometry("400x500")
        janela_input.configure(bg='#000000')
        
        janela_input.update_idletasks()
        width = janela_input.winfo_width()
        height = janela_input.winfo_height()
        x = (janela_input.winfo_screenwidth() // 2) - (width // 2)
        y = (janela_input.winfo_screenheight() // 2) - (height // 2)
        janela_input.geometry(f'{width}x{height}+{x}+{y}')
        
    
        campos = {}
        entries = {}
        
        campos_info = [
            ("produto", "Nome do produto:", str),
            ("quantidade_atual", "Quantidade atual:", int),
            ("materia_prima", "Matéria-prima:", str),
            ("massa", "Massa (g):", int),
            ("ciclo", "Ciclo (s):", int),
            ("n_cavidades", "Número de cavidades:", int),
            ("venda_mensal", "Venda mensal:", int),
            ("producao_mensal", "Produção mensal:", int)
        ]
        
        for key, label_text, _ in campos_info:
            frame = tk.Frame(janela_input, bg='#f0f0f0')
            frame.pack(pady=5)
            
            label = tk.Label(frame, text=label_text, bg='#f0f0f0', font=('Arial', 10))
            label.pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(frame, font=('Arial', 10))
            entry.pack(side=tk.LEFT, padx=5)
            entries[key] = entry
        
        def salvar():
            try:
                for key, _, tipo in campos_info:
                    valor = entries[key].get().strip()
                    if tipo == int:
                        campos[key] = int(valor)
                    else:
                        campos[key] = valor
                
                # Criar novo item
                novo_item = {
                    "produto": campos["produto"],
                    "qntd_atual": campos["quantidade_atual"],
                    "materia_prima": campos["materia_prima"],
                    "massa": campos["massa"],
                    "ciclo": campos["ciclo"],
                    "n_cavidades": campos["n_cavidades"],
                    "venda_mensal": campos["venda_mensal"],
                    "producao_mensal": campos["producao_mensal"],
                    "data": datetime.now().strftime("%d/%m/%Y")
                }
                
                arquivo_csv = "estoque.csv"
                df_novo = pd.DataFrame([novo_item])
                
                if not os.path.exists(arquivo_csv):
                    df_novo.to_csv(arquivo_csv, index=False)
                else:
                    df_novo.to_csv(arquivo_csv, mode='a', header=False, index=False)
                
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                janela_input.destroy()
                
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para os campos numéricos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o produto: {str(e)}")
        
        # Botões de ação
        frame_botoes = tk.Frame(janela_input, bg='#f0f0f0')
        frame_botoes.pack(pady=20)
        
        btn_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar,
                              width=10, font=('Arial', 10),
                              bg='#4CAF50', fg='white')
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_input.destroy,
                                width=10, font=('Arial', 10),
                                bg='#f44336', fg='white')
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar janela de input: {str(e)}")

def remover_produto():
    df = pd.read_csv("estoque.csv")
    
    while True:
        print("\nProdutos em estoque:")
        print(*df["produto"].values, sep="\n")
        print("\n")
        
        prod_remover = input("Digite o nome do produto que deseja remover do estoque (ou digite 'sair' para cancelar a operação): ").strip().lower()
        
        if prod_remover == "sair":
            print("Operação cancelada.")
            return
        
        if prod_remover in df["produto"].str.lower().values:
            opc = input(f"Deseja realmente excluir o produto {prod_remover} (S/N)? ".strip().lower())
            if(opc == "s"):
                df = df[df["produto"].str.lower() != prod_remover]  
                df.to_csv("estoque.csv", index=False)
                print("\n✅ Produto removido com sucesso!\n")
                opc = input("Deseja ver o estoque atualizado (S/N)? \n")
                if(opc.capitalize() == "S"):
                    ver_estoque()
                    return
                else:
                    return
            else:
                print("Operação cancelada.")
                return
        else:
            print("❌ Produto não encontrado, tente novamente.")
            

def atualizar_produto():
    df = pd.read_csv("estoque.csv")
    df_str = df.to_string()
    linha = "-" * len(df_str.split("\n")[0])
    
    print("\nProdutos em estoque:\n")
    print(*df["produto"].values, sep="\n")
    
    while True:
        nome = input("\nDigite o nome do produto que deseja atualizar (ou 'sair' para cancelar a operação): ").strip().lower()
        if nome == 'sair':
            print("\n❌ Operação cancelada.")
            return
        
        if nome in df["produto"].str.lower().values:
            resultado = df[df["produto"].str.lower() == nome]
            resultado_str = resultado.to_string(index=False, header=True)
            print(f"\n{resultado_str}\n")
            coluna = input("Digite o nome da coluna que deseja mudar: ").strip().lower()
            
            if coluna in df.columns:
                novo_valor = int(input(f"Digite o valor desejado para a coluna {coluna}: "))
                df.loc[df["produto"].str.lower() == nome, coluna] = novo_valor
                df.to_csv('estoque.csv', index=False)
                print("\nValor alterado com sucesso.\n")
                print(linha)
                print(df)
                print(linha)
                confirmacao()
                break
            else:
                print("❌ Coluna não reconhecida, tente novamente!")
        else:
            print("❌ Nome de produto não reconhecido, tente novamente.")
            

def exportar_excel():
    df = pd.read_csv('estoque.csv')
    
    df.to_excel("estoque.xlsx", index=False, engine="openpyxl")
    print("\nArquivo exportado com sucesso no arquivo 'estoque.xslx'.")
    confirmacao()
    
def simulacao_mensal():
    df = pd.read_csv("estoque.csv")
    for i in range (len(df)):
        df["qntd_atual"] += df["producao_mensal"] - df["venda_mensal"] # Produção mensal - venda mensal
        
    df.to_csv('estoque.csv', index=False)
    opc = input("\nSimulação mensal concluída, deseja ver o estoque atualizado? (S/N): ")
    if opc.capitalize() == 'S':
        ver_estoque()
    else:
        return

def exportar_pdf():
    df = pd.read_csv("estoque.csv")
    
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=11)
    
    pdf.cell(200, 10, "Dados do estoque", ln=True)
    pdf.set_font("Arial", size=9)
    
    for coluna in df.columns:
        pdf.set_text_color(0, 0, 255)
        pdf.cell(30, 10, coluna, border=1)
    
    pdf.ln()
    
    for _, linha in df.iterrows():
        for item in linha:
            pdf.set_text_color(0, 0, 0)
            pdf.cell(30, 10, str(item), border=1)
        pdf.ln()

    arquivo = "estoque.pdf"

    pdf.output(arquivo)
    webbrowser.open("file://" + os.path.abspath(arquivo))
    
def main():    
    try:
        janela = tk.Tk()
        janela.title("Controle de estoque")
        janela.geometry("300x600")
        
        janela.update_idletasks()
        width = janela.winfo_width()
        height = janela.winfo_height()
        x = (janela.winfo_screenwidth() // 2) - (width // 2)
        y = (janela.winfo_screenheight() // 2) - (height // 2)
        janela.geometry(f'{width}x{height}+{x}+{y}')
        
        janela.configure(bg='#f0f0f0')
        
        label = tk.Label(janela, text="Controle de estoque", font=('Arial', 14, 'bold'), bg='#f0f0f0')
        label.pack(pady=20)
        
        frame = tk.Frame(janela, bg='#f0f0f0')
        frame.pack(expand=True)
        
        botoes = [
            ("Adicionar produto", adicionar_produto),
            ("Remover produto", remover_produto),
            ("Atualizar produto", atualizar_produto),
            ("Ver estoque", ver_estoque),
            ("Exportar como excel", exportar_excel),
            ("Simular mensal", simulacao_mensal),
            ("Exportar como pdf", exportar_pdf),
            ("Sair", janela.quit)
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(frame, text=texto, command=comando, 
                          width=20, height=2, font=('Arial', 10),
                          bg='#4CAF50', fg='black',
                          relief=tk.RAISED, borderwidth=1)
            btn.pack(pady=5)
        
        janela.mainloop()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar a aplicação: {str(e)}")
        print(f"Erro detalhado: {str(e)}")

if __name__ == "__main__":
    main()