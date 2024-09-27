import pandas as pd

def exportar_para_excel(file_path, dados):
    if not dados:
        print("Nenhum dado para exportar.")
        return
    
    pd.DataFrame(dados, columns=['nome', 'link', 'preco_pix']).to_excel(file_path, index=False)
    print(f"Dados exportados para {file_path} com sucesso!")
