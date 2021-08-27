# Asyncio is a library to write concurrent code using the async/await syntax.
import asyncio

# Telepot helps you build applications for Telegram Bot API.
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

#“Pretty-print” structures in a form which can be used as input to the interpreter.
from pprint import pprint

#Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup

# Requests is a HTTP library for the Python programming language.
import requests

# Insert images into Jupyter Notebook
from IPython.display import Image



# async creates a coroutine function
async def handle(msg):

    # making chat_id be accesible outside of the code
    global chat_id

    # set variables / https://www.programcreek.com/python/example/105815/telepot.glance
    content_type, chat_type, chat_id = telepot.glance(msg)

    #print variables
    print(content_type, chat_type, chat_id)

    pprint(msg)

    username = msg['chat']['first_name']

    # Check that the content type is text and it is not "/start"
    if content_type == 'text':
        if msg['text'] != '/start':
            text = msg['text']

            # remove all white space characters—spaces, tabs, new lines
            text = text.strip()

            # coroutine await/async - function is paused
            await getMeaning(text.lower())



async def getMeaning(text):

    # URL formation
    url = 'https://www.urbandictionary.com/define.php?term=' + text

    # gather page response via requests
    page = requests.get(url)

    # creation of BaeutifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # pprint(soup) (Figure 1)

    try:
        try:

            # get definition - we are searching div category (Figure 2)
            definition = soup.find('div', {"class" : 'meaning'}).text

            await bot.sendMessage(chat_id, definition)

        except:
            await bot.sendMessage(chat_id, 'Meaning not found!')
    except:
        await bot.sendMessage(chat_id, 'Something went wrong...')

# Initialisation

TOKEN = '1983335411:AAEEtYwPUzBxm1wykQ-BHsM3vnSoNHkh_84'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

# Keep it running
loop.run_forever()
