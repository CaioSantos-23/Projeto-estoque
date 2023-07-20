import pandas as pd
import tkinter as tk
from tkinter import messagebox

class Produto:
    def __init__(self, codigo_barras, quantidade_em_estoque, quantidade_minima):
        self.codigo_barras = codigo_barras
        self.quantidade_em_estoque = quantidade_em_estoque
        self.quantidade_minima = quantidade_minima
        self.entrada_de_estoque = 0
        self.saida_de_estoque = 0

    def atualizar_estoque(self, quantidade):
        if quantidade >= 0:
            self.quantidade_em_estoque += quantidade
            self.entrada_de_estoque += quantidade
        else:
            self.quantidade_em_estoque += quantidade
            self.saida_de_estoque += abs(quantidade)

        if self.quantidade_em_estoque <= self.quantidade_minima:
            print("Estoque baixo para o produto:", self.produto)

    def __str__(self):
        return f"Codigo de Barras: {self.codigo_barras}, Quantidade em Estoque: {self.quantidade_em_estoque}"

class Estoque:
    def __init__(self, file_path):
        self.file_path = file_path
        self.produtos = self.carregar_estoque()

    def carregar_estoque(self):
        estoque_data = pd.read_excel(self.file_path)
        produtos = []
        for index, row in estoque_data.iterrows():
            produto = Produto(row['Codigo_de_Barras'], row['Quantidade_em_Estoque'], row['Quantidade_Minima'])
            produto.entrada_de_estoque = row.get('Entrada_de_Estoque', 0)
            produto.saida_de_estoque = row.get('Saida_de_Estoque', 0)
            produtos.append(produto)
        return produtos

    def salvar_estoque(self):
        data = {
            'Codigo_de_Barras': [produto.codigo_barras for produto in self.produtos],
            'Quantidade_em_Estoque': [produto.quantidade_em_estoque for produto in self.produtos],
            'Quantidade_Minima': [produto.quantidade_minima for produto in self.produtos],
            'Entrada_de_Estoque': [produto.entrada_de_estoque for produto in self.produtos],
            'Saida_de_Estoque': [produto.saida_de_estoque for produto in self.produtos],
        }
        estoque_df = pd.DataFrame(data)
        estoque_df.to_excel(self.file_path, index=False)

    def atualizar_produto(self, codigo_barras, quantidade):
        for produto in self.produtos:
            if produto.codigo_barras == codigo_barras:
                produto.atualizar_estoque(quantidade)
                break

    def verificar_estoque(self, codigo_barras=None):
        produtos_abaixo_minimo = []
        for produto in self.produtos:
            if produto.quantidade_em_estoque <= produto.quantidade_minima:
                produtos_abaixo_minimo.append(produto)
        
        if codigo_barras:
            for produto in produtos_abaixo_minimo:
                if produto.codigo_barras == codigo_barras:
                    return produto
            return None
        else:
            return produtos_abaixo_minimo

    def gerar_planilha_estoque_minimo(self):
        produtos_abaixo_minimo = self.verificar_estoque()
        if produtos_abaixo_minimo:
            data = {
                'Codigo_de_Barras': [produto.codigo_barras for produto in produtos_abaixo_minimo],
                'Quantidade_em_Estoque': [produto.quantidade_em_estoque for produto in produtos_abaixo_minimo],
                'Quantidade_Minima': [produto.quantidade_minima for produto in produtos_abaixo_minimo],
                'Entrada_de_Estoque': [produto.entrada_de_estoque for produto in produtos_abaixo_minimo],
                'Saida_de_Estoque': [produto.saida_de_estoque for produto in produtos_abaixo_minimo],
            }
            estoque_minimo_df = pd.DataFrame(data)
            estoque_minimo_df.to_excel('Estoque_Minimo.xlsx', index=False)
            messagebox.showinfo("Planilha Estoque Mínimo", "Planilha Estoque_Minimo.xlsx gerada com sucesso!")
        else:
            messagebox.showinfo("Planilha Estoque Mínimo", "Todos os produtos estão acima do estoque mínimo!")

class InterfaceUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque")
        self.root.geometry("500x400")

        # Título
        self.label_titulo = tk.Label(root, text="Controle de Estoque", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=10)

        # Frame para os campos de entrada
        self.frame_entrada = tk.Frame(root)
        self.frame_entrada.pack(padx=20, pady=10)

        # Campos de entrada
        self.label_codigo = tk.Label(self.frame_entrada, text="Código de Barras:", font=("Arial", 12))
        self.label_codigo.grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entry_codigo.grid(row=0, column=1, padx=10)

        self.label_quantidade = tk.Label(self.frame_entrada, text="Quantidade:", font=("Arial", 12))
        self.label_quantidade.grid(row=1, column=0, sticky=tk.W)
        self.entry_quantidade = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entry_quantidade.grid(row=1, column=1, padx=10)

        # Botões
        self.button_atualizar = tk.Button(root, text="Atualizar Estoque", font=("Arial", 12), command=self.atualizar_estoque)
        self.button_atualizar.pack(pady=10)

        self.button_verificar = tk.Button(root, text="Verificar Estoque", font=("Arial", 12), command=self.verificar_estoque_individual)
        self.button_verificar.pack(pady=10)

        self.button_verificar_minimo = tk.Button(root, text="Verificar Estoque Mínimo", font=("Arial", 12), command=self.verificar_estoque_minimo)
        self.button_verificar_minimo.pack(pady=10)

        self.button_gerar_planilha_minimo = tk.Button(root, text="Gerar Planilha Estoque Mínimo", font=("Arial", 12), command=self.gerar_planilha_estoque_minimo)
        self.button_gerar_planilha_minimo.pack(pady=10)

        self.file_path = 'C:\\Users\\Raian Satyro\\OneDrive\\Documentos\\Dev\\python\\estoqueOggi\\Projeto-estoque\\Estoque_com_codigo_de_barras.xlsx'
        self.estoque = Estoque(self.file_path)

    def atualizar_estoque(self):
        codigo_barras = self.entry_codigo.get()
        quantidade = int(self.entry_quantidade.get())
        self.estoque.atualizar_produto(codigo_barras, quantidade)
        self.estoque.salvar_estoque()
        messagebox.showinfo("Atualização de Estoque", "Estoque atualizado com sucesso!")

    def verificar_estoque_individual(self):
        codigo_barras = self.entry_codigo.get()
        produto = self.estoque.verificar_estoque(codigo_barras)
        if produto:
            messagebox.showinfo("Verificar Estoque", str(produto))
        else:
            messagebox.showinfo("Verificar Estoque", "Produto não encontrado no estoque!")

    def verificar_estoque_minimo(self):
        produtos_abaixo_minimo = self.estoque.verificar_estoque()
        if produtos_abaixo_minimo:
            mensagem = "Produtos abaixo do estoque mínimo:\n\n"
            for produto in produtos_abaixo_minimo:
                mensagem += str(produto) + "\n\n"
            messagebox.showinfo("Estoque Mínimo", mensagem)
        else:
            messagebox.showinfo("Estoque Mínimo", "Todos os produtos estão acima do estoque mínimo!")

    def gerar_planilha_estoque_minimo(self):
        self.estoque.gerar_planilha_estoque_minimo()

if __name__ == "__main__":
    root = tk.Tk()
    interface = InterfaceUsuario(root)
    root.mainloop()