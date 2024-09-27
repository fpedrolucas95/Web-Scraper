import argparse
from web_scraper import realizar_pesquisa
from exportar import exportar_para_excel
from database import DatabaseConnection

def processar_pesquisa_e_insercao(palavras_chave, quantidade, db):
    termo_pesquisa = ' '.join(palavras_chave)
    print(f"Iniciando a pesquisa de preços por '{termo_pesquisa}'...")
    
    resultados = realizar_pesquisa(termo_pesquisa, quantidade)
    
    if resultados:
        for resultado in resultados:
            db.inserir_produto({
                'nome': resultado['nome'],
                'link': resultado.get('link', ''),
                'preco': resultado.get('preco_pix', 'Não informado')
            })
        print(f"Pesquisa concluída! {len(resultados)} produtos foram salvos no banco de dados.")
    else:
        print("Nenhum produto encontrado na pesquisa.")
    
    return resultados

def exportar_resultados_sessao(nome_arquivo, resultados):
    if resultados:
        file_path = f"{nome_arquivo}.xlsx"
        exportar_para_excel(file_path, resultados)
        print(f"Dados da sessão exportados para {file_path} com sucesso!")
    else:
        print("Nenhum dado foi encontrado para exportar nesta sessão.")

def exportar_todos_os_dados(db, nome_arquivo):
    produtos = db.load_data()
    if produtos:
        file_path = f"{nome_arquivo}.xlsx"
        exportar_para_excel(file_path, produtos)
        print(f"Todos os dados do banco de dados exportados para {file_path} com sucesso!")
    else:
        print("Nenhum produto encontrado no banco de dados.")

def main():
    parser = argparse.ArgumentParser(description="Ferramenta de pesquisa e exportação de preços")
    parser.add_argument('--pesquisar', nargs='+', help="Palavra-chave para pesquisar produtos no site")
    parser.add_argument('--quantidade', type=int, default=10, help="Quantidade de produtos a pesquisar")
    parser.add_argument('--exportar', help="Nome do arquivo para exportar os resultados da sessão atual")
    parser.add_argument('--exportar-tudo', help="Nome do arquivo para exportar todos os resultados do banco de dados")
    args = parser.parse_args()

    db = DatabaseConnection()
    db.criar_tabela()

    if args.pesquisar:
        resultados = processar_pesquisa_e_insercao(args.pesquisar, args.quantidade, db)
    else:
        resultados = []

    if args.exportar:
        exportar_resultados_sessao(args.exportar, resultados)

    if args.exportar_tudo:
        exportar_todos_os_dados(db, args.exportar_tudo)

    db.close()

if __name__ == '__main__':
    main()
