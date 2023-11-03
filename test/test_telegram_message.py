# pip install beautifulsoup4
# pip install requests
# pip install python-telegram-bot
# pip install --upgrade python-telegram-bot

import asyncio
from telegram import Bot

async def send_telegram_message(token, chat_id, message):
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode='MarkdownV2')

async def main():
    # Configurações do bot do Telegram
    telegram_token = "TELEGRAM_TOKEN_BOT"  # Substitua pelo token do seu bot
    chat_id = "TELEGRAM_ID_CHAT"  # Substitua pelo ID do seu chat no Telegram

    # Lista de mensagens Markdown
    messages_to_send = [
        "Normal",
        "*Negrito*",
        "_Itálico_",
        "__Sublinhado__",
        "`Hello Word - Bloco de código`", # Bloco de código
        "[Google](http://www.google.com.br)", #Link
        # Adicione mais mensagens conforme necessário
    ]

    # Iterar sobre a lista de mensagens e enviá-las para o Telegram
    for message in messages_to_send:
        await send_telegram_message(telegram_token, chat_id, message)
        # Aguarde um curto período de tempo entre as mensagens, se desejar
        # await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())