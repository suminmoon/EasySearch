from django.test import TestCase
#beautifulsoup4 : html parsing library
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

query = "8006790"
# 8006790  # 버버리 코트
# SF199SK  # 페레가모 선글라스
url = f"http://www.enuri.com/lsv2016/ajax/getSearchGoods_ajax.jsp?key=minprice3&keyword={query}"
res = requests.get(url)
result = res.json()


### 가격비교 최저가
product = result.get('srpModelList')[0]
strImgUrl = product.get('strImgUrl')  # 이미지
strModelName = product.get('strModelName')  # 상품 이름
# print(product.get('lngMinPrice'))  # 상품 가격
modelno = product.get('intModelNo')  # 가격비교 상세 사이트 이동을 위한 model NO
strCa_code = product.get('strCa_code') # 가격비교 상세 사이트 이동을 위한 category code

# 가격비교 상세 사이트 이동
url_detail = f"http://www.enuri.com/lsv2016/ajax/detail/detailShoplist_ajax.jsp" \
    f"?&modelno={modelno}&list_type=1&list_cnt=8&cate={strCa_code}"
res_detail = requests.get(url_detail)
result_detail = res_detail.json()

product_detail = result_detail.get('price_list')[0]
price = product_detail.get('price')  # 가격비교 상세 사이트에서의 상품 가격
shop_name = product_detail.get('shop_name')  # 최저가 쇼핑몰 이름
shop_code = product_detail.get('shop_code')  # 최저 쇼핑몰 url 이동을 위한 shop_code
pl_no = product_detail.get('pl_no')  # 최저 쇼핑몰 url 이동을 위한 pl_no
url_minprice = f"http://www.enuri.com/move/Redirect.jsp?cmd=move_link&vcode={shop_code}" \
    f"&modelno={modelno}&pl_no={pl_no}&cate={strCa_code}" \
    f"&urltype=0&coupon=0&porder=0"  # 최저가 url

print("가격비교 최저가")
print(f"이미지: {strImgUrl}")
print(f"상품 이름: {strModelName}")
print(f"상품 가격: {price}")
print(f"쇼핑몰: {shop_name}")
print(f"최저가 url: {url_minprice}")


print('='*100)

### 일반상품 최저가
product = result.get('srpPlnoList')[0]

ilban_img = product.get('imgurl')  # 이미지
ilban_name = product.get('org_goodsnm')  # 상품 이름
ilban_price = product.get('lngPrice')  # 상품 가격
ilban_shop_name = product.get('shop_name')  # 최저가 쇼핑몰 이름
ilban_url = product.get('url')  # 최저가 url

print("일반상품 최저가")
print(f"이미지: {ilban_img}")
print(f"상품 이름: {ilban_name}")
print(f"상품 가격: {ilban_price}")
print(f"쇼핑몰: {ilban_shop_name}")
print(f"최저가 url: {ilban_url}")
