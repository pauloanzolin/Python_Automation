# Necessary Instalations on Python (Windows or Linux)
# pip install beautifulsoup4
# pip install requests
# pip install python-telegram-bot
# pip install --upgrade python-telegram-bot

# crontab -e
# 0 * * * * /usr/bin/python3 /home/avila/scrip_python/Monitor_kabum.py (Hora a hora)
# 0 12 * * * /usr/bin/python3 /home/avila/scrip_python/Monitor_kabum.py (Meio dia)

from bs4 import BeautifulSoup
import requests
import asyncio
import re
from telegram import Bot
from urllib.parse import urlparse, quote

# Função para obter informações do produto a partir de uma URL
def get_product_info(url):
    # Defina os headers para simular uma requisição de navegador
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537,36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    # Faça uma requisição HTTP para a URL especificada
    site = requests.get(url, headers=headers)

    # Crie um objeto BeautifulSoup para analisar o conteúdo HTML da página
    soup = BeautifulSoup(site.content, 'html.parser')

    # Extraia o título e o preço da página
    title_element = soup.find('h1', class_='sc-89bddf0f-6 dVrDvy')
    price_element = soup.find('h4', class_='sc-5492faee-2 hAMMrD finalPrice')
    
    # Verifique se os elementos foram encontrados antes de acessar os métodos
    title = title_element.get_text().strip() if title_element else "N/A"

    # Trate os casos em que o preço não é encontrado
    num_price = None
    if price_element:
        price = price_element.get_text().strip()
        num_price = float(price[3:9].replace('.', '').replace(',', '.')) if price[3:9] else None


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
        product_info.append((title, price, url))

    # Retorne a lista completa de informações do produto
    return product_info

async def send_telegram_message(token, chat_id, message):
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Configurações do bot do Telegram
telegram_token = "TELEGRAM_BOT_TOKEN"  # Substitua pelo token do seu bot
chat_id = "TELEGRAM_CHAT_ID"  # Substitua pelo ID do seu chat no Telegram


# Bloco principal para executar o código quando este script é executado diretamente
async def main():
    # Lista de URLs dos produtos a serem monitorados
    product_urls = [
        "https://www.kabum.com.br/link_example_1", #Substitua os links 
        "https://www.kabum.com.br/link_example_2",
        "https://www.kabum.com.br/link_example_3",
        "https://www.kabum.com.br/link_example_4",
        "https://www.kabum.com.br/link_example_5",
        "https://www.kabum.com.br/link_example_6"
    ]

    # Chame a função monitor_products para obter informações sobre os produtos
    product_info_list = monitor_products(product_urls)

    # Exiba as informações formatadas na tela
    message = "\n▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲\nLista de produtos Kabum\n"
    for title, price, url in product_info_list:
        print(f"\nR$ {price} = {title}\nLink: {url}\n---------------------------")


    # Crie uma mensagem formatada com as informações dos produtos
    message = "\n▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲\nLista de produtos Kabum\n\n"
    for title, price, url in product_info_list:
        parsed_url = urlparse(url)
        escaped_path = quote(parsed_url.path, safe="/")
        full_escaped_url = f"{parsed_url.scheme}://{parsed_url.netloc}{escaped_path}"
        message += f"*R$ {price}*\n[{title}]({full_escaped_url})\n--------------------------------\n"

    # Chame a função send_telegram_message para enviar a mensagem para o Telegram
    await send_telegram_message(telegram_token, chat_id, message)

if __name__ == "__main__":
    asyncio.run(main())