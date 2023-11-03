# pip install beautifulsoup4
# pip install requests
# pip install python-telegram-bot
# pip install --upgrade python-telegram-bot

from bs4 import BeautifulSoup
import requests
from telegram import Bot

# Função para obter informações do produto a partir de uma URL
def get_product_info(url):
    # Defina os headers para simular uma requisição de navegador
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537,36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
    
    # Faça uma requisição HTTP para a URL especificada
    site = requests.get(url, headers=headers)
    
    # Crie um objeto BeautifulSoup para analisar o conteúdo HTML da página
    soup = BeautifulSoup(site.content, 'html.parser')
    
    # Extraia o título e o preço da página
    title = soup.find('h1', class_='sc-89bddf0f-6 dVrDvy').get_text()
    price = soup.find('h4', class_='sc-5492faee-2 hAMMrD finalPrice').get_text().strip()
    
    # Formate o preço removendo caracteres não numéricos e substituindo ',' por '.'
    num_price = price[3:8].replace('.', '').replace(',', '.')
    
    # Retorne uma tupla contendo o título e o preço como um número de ponto flutuante
    return title, float(num_price)

# Função para monitorar vários produtos a partir de uma lista de URLs
def monitor_products(urls):
    # Inicialize uma lista vazia para armazenar as informações do produto
    product_info = []
    
    # Itere sobre cada URL na lista
    for url in urls:
        # Chame a função get_product_info para obter as informações do produto
        title, price = get_product_info(url)
        
        # Adicione as informações à lista de informações do produto
        product_info.append((title, price))
    
    # Retorne a lista completa de informações do produto
    return product_info

# Bloco principal para executar o código quando este script é executado diretamente
if __name__ == "__main__":
    # Lista de URLs dos produtos a serem monitorados
    product_urls = [
        "https://www.kabum.com.br/produto/469132/", # Exemplo
        "https://www.kabum.com.br/link_1",
        "https://www.kabum.com.br/link_2",
        "https://www.kabum.com.br/link_3",
        "https://www.kabum.com.br/link_4",
        "https://www.kabum.com.br/link_5",
    ]

# Chame a função monitor_products para obter informações sobre os produtos
product_info_list = monitor_products(product_urls)

# Exiba as informações formatadas na tela
for title, price in product_info_list:
    print(f"R$ {price} = {title}")