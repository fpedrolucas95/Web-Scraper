# Web Scraper de Preços

**Web Scraper de Preços** é uma aplicação Python para realizar pesquisas de produtos no site das Casas Bahia, salvar os resultados em um banco de dados MySQL e exportar os dados para um arquivo Excel.

## Funcionalidades

- Pesquisar produtos com base em palavras-chave fornecidas.
- Definir a quantidade de produtos a ser pesquisada.
- Armazenar os resultados das pesquisas em um banco de dados MySQL.
- Exportar os resultados da pesquisa atual ou todo o banco de dados para um arquivo Excel.

## Como Usar

1. Para realizar uma pesquisa e salvar os resultados no banco de dados:
   ```bash
   python main.py --pesquisar "termo de pesquisa" --quantidade 10
   ```
   Onde `--pesquisar` define os termos de pesquisa e `--quantidade` define o número de produtos a ser pesquisado (padrão: 10).

2. Para exportar os resultados da pesquisa atual para um arquivo Excel:
   ```bash
   python main.py --pesquisar "termo de pesquisa" --quantidade 10 --exportar nome_do_arquivo
   ```
   Onde `--exportar` define o nome do arquivo Excel onde os resultados da sessão atual serão salvos.

3. Para exportar todos os produtos já armazenados no banco de dados:
   ```bash
   python main.py --exportar-tudo nome_do_arquivo
   ```
   Onde `--exportar-tudo` define o nome do arquivo Excel onde todos os produtos do banco de dados serão salvos.
   
## Requisitos

- Python 3.8 ou superior
- MySQL
- Bibliotecas Python:
  - `mysql-connector-python`
  - `pandas`
  - `webdriver-manager`
  - `selenium`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/fpedrolucas95/Web-Scraper.git
   ```
2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Configure o MySQL:
   - Crie um banco de dados chamado `produtos_database`.
   - Defina as credenciais de conexão ao MySQL no arquivo `database.py`.

4. Execute o aplicativo:
   ```bash
   python main.py --pesquisar "notebook" --quantidade 5
   ```

## Estrutura do Projeto

```
├── main.py                # Arquivo principal para rodar o scraper
├── web_scraper.py          # Lógica de scraping para coleta de produtos
├── exporter.py             # Função para exportar os dados para Excel
├── database.py             # Conexão e interações com o banco de dados MySQL
├── requirements.txt        # Dependências do projeto
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é licenciado sob a GNU General Public License v3.0 (GPL-3.0). Isso garante a você as seguintes liberdades:

- Utilizar o software para qualquer propósito.
- Modificar o software conforme suas necessidades.
- Compartilhar o software com outras pessoas.
- Distribuir suas próprias modificações.

Para mais detalhes, consulte o arquivo [LICENSE](https://github.com/usuario/consulta-cnpj/blob/main/LICENSE) no repositório do projeto.
