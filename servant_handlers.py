from pyrogram import MessageHandler, Filters
from telegram import Bot, ParseMode
from secrets import bot_token
import re
import requests
from bs4 import BeautifulSoup
from telegraph import utils as tutils, upload as tupload
from telegraph import Telegraph
import shutil

bot = Bot(bot_token)
telegraph = Telegraph()

telegraph.create_account(short_name='@Lor3m', author_name='@Lor3m')


def new_post(client, message):
    post = message.text
    link = re.findall(r'(https?://\S+)', post)[-1]

    parsed = requests.get(link).text

    page = BeautifulSoup(parsed,
                         features="html.parser")
    try:
        title = page.find('div', class_='bdaia-post-title').find('h1').next
    except AttributeError:
        title = page.find('h1', class_='post-title')
    content = page.find('div', class_='bdaia-post-content')
    image_url = re.findall(r'(https?://\S+)',
                           page.find('a', class_='bdaia-featured-img-cover')['style'])[-1].replace(');', '')
    response = requests.get(image_url, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    cover = tupload.upload_file('img.png')[0]
    cover_url = 'http://telegra.ph' + cover
    text = '<img src=\"{}\"></img>'.format(cover_url)

    for elem in content:
        if elem.name == 'div' or elem.name =='style' or 'script' in str(elem):
            pass
        elif elem.name == 'blockquote':
            if '<a>' in str(elem):
                quote = ''
                for p_ in elem:
                    quote += str(p_)
                twitter_link = elem.find_all('a')[-1]['href']
                text += '<p><blockquote>' + quote + '</blockquote></p>' + '<p><a href=\"{}\">Link to tweet</a></p>'.format(twitter_link)
            else:
                text += str(elem)
        elif 'iframe' in str(elem):
            url = elem.find('iframe')['src']
            text += '<p><a href=\"{}\">Link to video</a></p>'.format(url)
        elif elem.name =='h2':
            text += '<p><b>{}</b></p>'.format(elem.next)
        else:
            text += str(elem)

    nodes = tutils.html_to_nodes(text)

    tg_page = telegraph.create_page(content=nodes,
                                    title=title,
                                    author_name='@Lor3m',
                                    author_url='https://t.me/Lor3m')
    created_page = tg_page['url']

    bot.send_message(-1001347924999,
                     '{}\n\n{}'.format(title, created_page),
                     parse_mode=ParseMode.HTML,
                     )


new_post_handler = MessageHandler(new_post,
                                  Filters.chat('xakep_ru') & Filters.text)
