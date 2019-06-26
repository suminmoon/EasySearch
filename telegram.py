import os
import django
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

token = '636670076:AAFgJ7kM8IIqbZVQnQeIUdw2UkX3H5gWjZs'
api_url = f'https://api.telegram.org/bot{token}'
def telegram_crontab():
        
        telegramOBJ = Table.objects.all()
        print(telegramOBJ)

        for telegramobj in telegramOBJ:
            chat_id = telegramobj.userID
            text = telegramobj.productNO
            price = telegramobj.lowPRICE

            query = text

            naver_url = "https://search.shopping.naver.com/search/all.nhn?origQuery=15915ADY1M&pagingIndex=1&pagingSize=40&productSet=model&viewType=list&sort=price_asc&frm=NVSHMDL&query=" + query
            naver_url_obj = urlopen(naver_url)
            naver_bs = BeautifulSoup(naver_url_obj.read(), "html.parser")
            ##가격비교 팝업창
            naver_price_href = naver_bs.select_one(
                '#_search_list > div.search_list.basis > ul > li > div.info > a').get('href')
            ##01에서 받은 url

            naver_price_url = urlopen(naver_price_href)
            naver_price_bs = BeautifulSoup(naver_price_url.read(), "html.parser")
            ##가격비교
            naver_price = naver_price_bs.select_one(
                "#_mainSummaryPrice > table > tbody > tr:nth-of-type(1) > td.price > em > a").text
            naver_price = naver_price.split(' ')[1].replace(',', '')
            naver_url = naver_price_bs.select_one(
                "#_mainSummaryPrice > table > tbody > tr:nth-of-type(1) > td.price > em > a").get('href').replace(' ',
                                                                                                                  '')
            naver_mall = naver_price_bs.select_one(
                "#_mainSummaryPrice > table > tbody > tr:nth-of-type(1) > td.mall_area > div > span.mall > a > img").get(
                'alt')
            naver_img = naver_price_bs.select_one('#viewImage').get('src')

            if int(naver_price) <= int(price):
                t_price = naver_price
                requests.get(f'{api_url}/sendMessage?chat_id={chat_id}&text={t_price}')
                telegramobj.delete()
            else:
                t_price ="기다려"
                requests.get(f'{api_url}/sendMessage?chat_id={chat_id}&text={t_price}')



if __name__ == '__main__':
    path = os.path.dirname(__file__)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'form.settings'
    django.setup()
    from pages.models import Table
    telegram_crontab()