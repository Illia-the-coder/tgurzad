from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiohttp
from newspaper import Article
from googletrans import Translator
from aiogram.types import InlineKeyboardMarkup
from requests_html import HTML
from datetime import datetime, timedelta
import asyncio
from asyncio import sleep

translator = Translator()
def translate_from_pl(text):

    translated_text = translator.translate(text.split('\n')[-1], src='pl', dest='uk').text

    return translated_text

API_TOKEN = '6837792932:AAF2oj0NGZ5CWyLtJ_IEfkWMyKSiIV52T0o'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
translator = Translator()


tg_chanells = {
    "Wroclaw": "@Wroclaw_Urzad",
    "Bydgoszcz": "@Bydgoszcz_Urzad",
    "Lublin": "@Lublin_Urzad",
    "Lodz": "@Lodzki_Urzad",
    "Gorzow Wielkopolski": "@Gorzow_Urzad",
    "Krakow": "@Krakow_Urzad",
    "Warsaw": "@Warszawa_Urzad",
    "Opole": "@Opole_Urzad",
    "Rzeszow": "@Rzeszow_Urzad",
    "Bialystok": "@Bialystok_Urzad",
    "Gdansk": "@Gdansk_Urzad",
    "Katowice": "@Katowice_Urzad",
    "Kielce": "@Kielce_Urzad",
    "Olsztyn": "@Olsztyn_Urzad",
    "Poznan": "@Poznanski_Urzad",
    "Szczecin": "@szczecin_Urzad"
}

polish_cities_websites = {
    "Wroclaw": "https://www.duw.pl/pl/dla-mediow/aktualnosci",
    # "Bydgoszcz": "https://cudzoziemiec.bydgoszcz.pl/en/news/",
    "Lublin": "https://www.gov.pl/web/uw-lubelski/wiadomosci",
    "Lodz": "https://www.gov.pl/web/uw-lodzki/wiadomosci",
    "Krakow": "https://www.krakow.pl/aktualnosci/1584,26,0,kategoria,aktualnosci.html",
    "Gorzow Wielkopolski": "https://um.gorzow.pl/",
    "Warsaw": "https://www.gov.pl/web/uw-mazowiecki/wiadomosci2",
    "Opole": "https://www.gov.pl/web/uw-opolski/aktualnosci-wiadomosci",
    "Rzeszow": "https://rzeszow.uw.gov.pl/aktualnosci",
    "Bialystok": "https://www.gov.pl/web/uw-podlaski/wiadomosci",
    "Gdansk": "https://www.gdansk.uw.gov.pl/aktualnosci",
    "Katowice": "https://www.katowice.uw.gov.pl/aktualnosci",
    "Kielce": "https://www.kielce.uw.gov.pl",
    "Olsztyn": "https://www.gov.pl/web/uw-warminsko-mazurski/aktualnosci",
    "Poznan": "https://www.poznan.pl/mim/info/news/",
    "Szczecin": "https://www.gov.pl/web/uw-zachodniopomorski/aktualnosci"
}

selectors = {
    # "Bydgoszcz":'#sectionBlog > div.sectionBlogBoxes > a',
    "Wroclaw": '#sub_right > div > div.left > div.okno > ul > li.box',
    "Krakow": 'body > div.main > article > div > div > section > div.events__list > div',
    "Lublin": 'article>div>ul>li', 
    "Lodz": 'article>div>ul>li', 
    "Gorzow Wielkopolski": '#js__news_home > div > div > div.news_home__list > div', 
    "Warsaw": 'article>div>ul>li', 
    "Opole": 'article>div>ul>li', 
    "Rzeszow": '#content > div.ds-table-collapse.grid > div > div.gridcell.ds-table-cell', 
    "Bialystok": 'article>div>ul>li', 
    "Gdansk": 'div > div.item-body', 
    "Katowice": 'body > div.wrapper > div.bg-color-white > div > div > div.col-md-9 > div', 
    "Kielce": 'article>div>ul>li', 
    "Olsztyn": 'article>div>ul>li', 
    "Szczecin": 'article>div>ul>li', 
    "Poznan":'body > section.content-container > div > div.body-container > article',

    'date': {
        "Poznan":'time',
        "Wroclaw": 'div.wiecejData > div',
        "Lublin": 'div.event > span', 
        "Krakow": 'div.item__text>p',
        "Lodz": 'div.event > span', 
        "Gorzow Wielkopolski": 'time', 
        "Warsaw": 'div.event > span', 
        "Opole": 'div.event > span', 
        "Rzeszow": 'div.ds-table.postmeta > div.ds-table-cell.time > span', 
        "Bialystok": 'div.event > span', 
        "Gdansk": 'div.date-created', 
        "Katowice": 'ul > li', 
        "Kielce": 'div.data', 
        "Olsztyn": 'div.event > span',
        "Szczecin": 'div.event > span',
        },
    'title': {
        "Poznan":'h2',
        "Wroclaw": 'strong > a',
        "Krakow": 'h3',
        "Lublin": 'div > div.title', 
        "Lodz": 'div > div.title', 
        "Gorzow Wielkopolski": 'div.news__name', 
        "Warsaw": 'div > div.title', 
        "Opole": 'div > div.title', 
        "Rzeszow": 'h2', 
        "Bialystok": 'div > div.title', 
        "Gdansk": 'h3 > a, h4 > a', 
        "Katowice": 'h2', 
        "Kielce": 'strong > a', 
        "Olsztyn": 'div > div.title',
        "Szczecin": 'div > div.title',
        }
    }

date_format = {
    "Poznan":'%Y-%m-%d',
    "Wroclaw": '%d.%m.%Y',
    "Krakow": '%Y-%m-%d',
    "Lublin": '%d.%m.%Y',
    "Lodz": '%d.%m.%Y',
    "Gorzow Wielkopolski": '%d-%m-%Y',
    "Warsaw": '%d.%m.%Y',
    "Opole": '%d.%m.%Y',
    "Rzeszow": '%d.%m.%Y',
    "Bialystok": '%d.%m.%Y',
    "Gdansk": '%d.%m.%Y',
    "Katowice": '%d.%m.%Y',
    "Kielce": '%d.%m.%Y',
    "Olsztyn": '%d.%m.%Y',
    "Szczecin": '%d.%m.%Y',
    }


def replace_month_name_with_number(date_str):
    months_pl_to_num = {
        "stycznia": ".01.", "styczeń": ".01.",
        "lutego": ".02.", "luty": ".02.",
        "marca": ".03.", "marzec": ".03.",
        "kwietnia": ".04.", "kwiecień": ".04.",
        "maja": ".05.", "maj": ".05.",
        "czerwca": ".06.", "czerwiec": ".06.",
        "lipca": ".07.", "lipiec": ".07.",
        "sierpnia": ".08.", "sierpień": ".08.",
        "września": ".09.", "wrzesień": ".09.",
        "października": ".10.", "październik": ".10.",
        "listopada": ".11.", "listopad": ".11.",
        "grudnia": ".12.", "grudzień": ".12."
    }

    for pl, num in months_pl_to_num.items():
        date_str = date_str.replace(pl, num).replace('Data publikacji: ','').replace(' ', '')
    if len(date_str) !=10:
        date_str = [x for x in date_str.split(',') if '.' in x][0]
    return date_str

def parse_date(date_text, format_str):
    return datetime.strptime(replace_month_name_with_number(date_text), format_str).date()

async def get_links_with_dates(url, city, selectors, date_format, session,days):
    async with session.get(url) as response:
        html_text = await response.text()
        
    time_limit = datetime.now().date() - timedelta(days=days)
    date_link_pairs = []    
    r = HTML(html=html_text, url=url)   
    date_elements = r.find(selectors[city])
    
    for element in date_elements:
        if len(element.absolute_links):
            date_text = element.find(selectors['date'][city])[0].text
            title = element.find(selectors['title'][city])[0].text
            parsed_date = parse_date(date_text, date_format[city])
            if parsed_date >= time_limit:
                if city == 'Wroclaw':
                    link = list(
                        [x for x in element.find('strong')[0].absolute_links if (x.split('/')[-1].split('.')[-1] == 'html' or x.split('/')[-1].split('.')[-1] == x.split('/')[-1])])[0]
                else:
                    link = list([x for x in element.absolute_links if (x.split('/')[-1].split('.')[-1] == 'html' or x.split('/')[-1].split('.')[-1] == x.split('/')[-1])])[0]  
                async with session.get(link) as response:
                    html = await response.text()
                    article = Article(url)
                    article.download(input_html=html)
                    article.parse()
                    src = article.top_image
                    text = article.text
                date_link_pairs.append({'title': title, 'link': link,  'image': src, 'text': text}) 
                  
    return date_link_pairs

# Function to fetch latest news
async def fetch_latest_news(url,city,days=1):
    articles_data = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await get_links_with_dates(url,city,selectors, date_format, session,days)

async def send_message_to_tg_channel(city, chat_id, send_channel=False):
    news = await fetch_latest_news(polish_cities_websites[city], city, 0)
    n = 0
    for article in news:
        message_text = f"""<b>{translate_from_pl(article['title'])}</b>\n\n<i>{translate_from_pl(article['text'][:230])}...</i>\n\n<a href='{article['link']}'>▪️Читати повністю…</a>\n\n{tg_chanells[city]}"""
        try:
            if tg_chanells[city] != '' and send_channel:
                await bot.send_photo(tg_chanells[city], article['image'], caption=message_text, parse_mode=types.ParseMode.HTML)
            n += 1    
        except Exception as e:
            print(f"Error sending message: {e}")
    return  f"<b>{city}</b>: {n}/{len(news)}\n"

async def daily_parsing_task():
    chat_id = '1245273083'  # Replace with the actual chat ID or logic to determine it
    stat = ''
    for city in polish_cities_websites.keys():
        stat += await send_message_to_tg_channel(city, chat_id, send_channel=True)
    await bot.send_message(chat_id, stat, parse_mode=types.ParseMode.HTML)

async def schedule_daily_task(task):
    while True:
        now = datetime.now()
        target_time = now.replace(hour=18, minute=30, second=0, microsecond=0)

        if now > target_time:
            target_time += timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        print(f"Next run in {wait_seconds} seconds")
        await sleep(wait_seconds)

        await task()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=3)
    await message.answer("Hello! I'm a bot that can help you with the latest news. Use /parse to start parsing.", reply_markup=markup)
    print(message.chat.id)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_daily_task(daily_parsing_task))
    executor.start_polling(dp, skip_updates=True)
