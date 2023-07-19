import pandas as pd

# Carregar o arquivo do estoque
estoque = pd.read_excel('D:\\Caio\\Projeto Oggi\\Estoque_com_codigo_de_barras.xlsx')  # Substitua 'estoque.xlsx' pelo nome do seu arquivo

def atualizar_estoque(codigo_barras, quantidade):
    global estoque
    
    # Procurar o produto pelo codigo de barras
    produto = estoque.loc[estoque['Codigo_de_Barras'] == codigo_barras]
    
    if len(produto) == 0:
        print("Codigo de barras nao encontrado.")
        return
    
    # Atualizar a quantidade em estoque
    estoque.loc[estoque['Codigo_de_Barras'] == codigo_barras, 'Quantidade_em_Estoque'] += quantidade
    
    # Verificar se a quantidade esta abaixo do minimo
    if estoque.loc[estoque['Codigo_de_Barras'] == codigo_barras, 'Quantidade_em_Estoque'].item() <= produto['Quantidade_Minima'].item():
        print("Estoque baixo para o produto:", produto['Produto'].item())

    # Salvar as alteracoes no arquivo
    estoque.to_excel('Estoque_com_codigo_de_barras.xlsx', index=False)  # Substitua 'estoque.xlsx' pelo nome do seu arquivo

# Exemplo de uso
codigo_barras = input("Digite o codigo de barras: ")
quantidade = int(input("Digite a quantidade: "))

atualizar_estoque(codigo_barras, quantidade)
