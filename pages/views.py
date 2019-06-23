from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
import cv2
import os, io, re
from google.cloud import vision
from google.cloud.vision import types
from .models import Post
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests



@require_GET
def index(request):
    return render(request, 'pages/index.html')


@require_http_methods(['GET', 'POST'])
def upload(request):
    if request.method == "GET":
        return render(request, 'pages/upload.html')

    else:
        image = request.FILES.get('image')
        post = Post(image=image)
        post.save()

        return redirect('pages:detail')


def detail(request):
    p = Post.objects.all()
    dbimg = p[len(p)-1].image
    db = str(dbimg)
    im = cv2.imread('media/'+ db )
    im = cv2.resize(im, (900, 600))

    # # Select ROI
    showCrosshair = False
    fromCenter = False
    r = cv2.selectROI("Image", im, fromCenter, showCrosshair)


    # # Crop image
    imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]


    # # Display cropped image
    imCrop = cv2.resize(imCrop, (400,200)) #(가로,세로)
    cv2.imshow("Image", imCrop)
    cv2.imwrite('pages/static/pages/img/sample.jpg', imCrop)
    cv2.waitKey(0)
    #
    #media/cuttings/sample.jpg'

    cv2.destroyAllWindows()

    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(
        os.path.dirname(''),
        'pages/static/pages/img/sample.jpg')

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    my_list = list()

    for text in texts:
        aa = text.description
        my_list.append(aa)

    serial_no = my_list[0].replace('\n', '')

    context = {'serial_no': serial_no}

    return render(request, 'pages/detail.html', context)


def result(request, serial_no):
    try:
        ##네이버(가격비교)
        naver_url = f"https://search.shopping.naver.com/search/all.nhn?origQuery={serial_no}&pagingIndex=1&pagingSize=40&productSet=model&viewType=list&sort=price_asc&frm=NVSHMDL&query={serial_no}"
        naver_url_obj = urlopen(naver_url)
        naver_bs = BeautifulSoup(naver_url_obj.read(), "html.parser")
        ##가격비교 팝업창
        naver_price_href = naver_bs.select_one('#_search_list > div.search_list.basis > ul > li > div.info > a').get('href')
        ##01에서 받은 url

        naver_price_url = urlopen(naver_price_href)
        naver_price_bs = BeautifulSoup(naver_price_url.read(), "html.parser")

        try:
            ##가격비교
            naver_price = naver_price_bs.select_one(
                "#_mainSummaryPrice > table > tbody > tr:nth-of-type(1) > td.price > em > a").text
            naver_price = naver_price.split(' ')[-1].replace(',', '')
            naver_url = naver_price_bs.select_one(
                "#_mainSummaryPrice > table > tbody > tr:nth-of-type(1) > td.price > em > a").get('href')
            naver_mall = naver_price_bs.select_one(
                "#_mainSummaryPrice > table > tbody > tr:nth-of-type(1) > td.mall_area > div > span.mall > a > img").get('alt')
            naver_img = naver_price_bs.select_one('#viewImage').get('src')

        except Exception:
            naver_price = 1000000000000
            naver_mall = "상품이 없습니다."
            naver_url = "상품이 없습니다."
            naver_img = "상품이 없습니다."

        ##네이버(일반상품)

        try:
            naver_all_url = f'https://search.shopping.naver.com/search/all.nhn?origQuery={serial_no}&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query={serial_no}'
            naver_all_obj = urlopen(naver_all_url)
            naver_all_bs = BeautifulSoup(naver_all_obj.read(), "html.parser")

            naver_all_price = naver_all_bs.select_one(
                "#_search_list > div.search_list.basis > ul > li:nth-of-type(1) > div.info > span.price > em > span").text.replace(
                ',', '')
            naver_all_url = naver_all_bs.select_one(
                "#_search_list > div.search_list.basis > ul > li:nth-of-type(1) > div.info > a").get('href')

            naver_all_mall = naver_all_bs.select_one(
                "#_search_list > div.search_list.basis > ul > li:nth-of-type(1) > div.info_mall > p > a.mall_img > img").get(
                'alt')
            naver_all_img = naver_all_bs.select_one(
                '#_search_list > div.search_list.basis > ul > li:nth-of-type(1) > div.img_area > a > img').get(
                'data-original')

        except Exception:
            naver_all_price =100000000000
            naver_all_mall = "상품이 없습니다."
            naver_all_url = "상품이 없습니다."
            naver_all_img = "상품이 없습니다."


        # 가격비교 vs 일반상품
        if int(naver_price) <= int(naver_all_price):
            naver_total_price = naver_price
            naver_total_mall = naver_mall
            naver_total_url = naver_url
            naver_total_image = naver_img
        else:
            naver_total_price = naver_all_price
            naver_total_mall = naver_all_mall
            naver_total_url = naver_all_url
            naver_total_image = naver_all_img

        context_naver = {'naver_total_mall': naver_total_mall, 'naver_total_image': naver_total_image,
                   'naver_total_price': naver_total_price, 'naver_total_url': naver_total_url}


    except Exception:
        context_naver = {'naver_error': '네이버'}

        #########################################################################################
    try:
        ##에누리(가격비교)
        enuri_url = f"http://www.enuri.com/lsv2016/ajax/getSearchGoods_ajax.jsp?key=minprice3&keyword={serial_no}"
        enuri_res = requests.get(enuri_url)
        enuri_result = enuri_res.json()

        try:
            enuri_product = enuri_result.get('srpModelList')[0]
            enuri_strImgUrl = enuri_product.get('strImgUrl')
            enuri_strModelName = enuri_product.get('strModelName')
            enuri_modelno = enuri_product.get('intModelNo')
            enuri_strCa_code = enuri_product.get('strCa_code')

            enuri_url_detail = f"http://www.enuri.com/lsv2016/ajax/detail/detailShoplist_ajax.jsp" \
                f"?&modelno={enuri_modelno}&list_type=1&list_cnt=8&cate={enuri_strCa_code}"
            enuri_res_detail = requests.get(enuri_url_detail)
            enuri_result_detail = enuri_res_detail.json()

            enuri_product_detail = enuri_result_detail.get('price_list')[0]
            enuri_price = enuri_product_detail.get('price')
            enuri_shop_name = enuri_product_detail.get('shop_name')
            enuri_shop_code = enuri_product_detail.get('shop_code')
            enuri_pl_no = enuri_product_detail.get('pl_no')
            enuri_url_minprice = f"http://www.enuri.com/move/Redirect.jsp?cmd=move_link&vcode={enuri_shop_code}" \
                f"&modelno={enuri_modelno}&pl_no={enuri_pl_no}&cate={enuri_strCa_code}" \
                f"&urltype=0&coupon=0&porder=0"

        except Exception:
            enuri_price = 1000000000000
            enuri_shop_name = "상품이 없습니다."
            enuri_url_minprice = "상품이 없습니다."
            enuri_strImgUrl = "상품이 없습니다."

        ##에누리(일반상품)
        try:
            enuri_ilban_product = enuri_result.get('srpPlnoList')[0]
            ilban_img = enuri_ilban_product.get('imgurl')
            ilban_name = enuri_ilban_product.get('org_goodsnm')
            ilban_price = enuri_ilban_product.get('lngPrice')
            ilban_shop_name = enuri_ilban_product.get('shop_name')
            ilban_url = enuri_ilban_product.get('url')
        except Exception:
            ilban_price = 1000000000000
            ilban_shop_name = "상품이 없습니다."
            ilban_url = "상품이 없습니다."
            ilban_img = "상품이 없습니다."

        # 가격비교 vs 일반상품
        if int(enuri_price) <= int(ilban_price):
            enuri_total_price = enuri_price
            enuri_total_mall = enuri_shop_name
            enuri_total_url = enuri_url_minprice
            enuri_total_image = enuri_strImgUrl
        else:
            enuri_total_price = ilban_price
            enuri_total_mall = ilban_shop_name
            enuri_total_url = ilban_url
            enuri_total_image = ilban_img

        context_enuri = {'enuri_total_image': enuri_total_image, 'enuri_total_mall': enuri_total_mall,
        'enuri_total_price': enuri_total_price, 'enuri_total_url': enuri_total_url}

    except Exception:
        context_enuri={'enuri_error': '에누리'}

        ############################################################################################

    try:
        # ##다나와(가격비교)
        danawa_urls = 'http://search.danawa.com/ajax/getProductList.ajax.php'
        try:
            data1 = {
                # 'serial_no': serial_no,
                'query': serial_no,
                'sort': 'priceASC',
                'volumeType': 'vmvs',
                'limit': 90
            }
            headers1 = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                'Referer': 'http://search.danawa.com/dsearch.php'
            }
            req = requests.post(danawa_urls, data=data1, headers=headers1)
            danawa_bs = BeautifulSoup(req.text, 'html.parser')
            danawa_price_url = danawa_bs.select_one('.prod_name > a').get('href')

            headers2 = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            }

            danawa_req = requests.post(danawa_price_url, headers=headers2)

            danawa_price_bs = BeautifulSoup(danawa_req.text, 'html.parser')

            if 'popup' in danawa_price_url:

                danawa_mall = danawa_price_bs.select_one(
                    '#danawa_pop_content > div.similar_prod > div.info_area > div.mall_a > div > img').get(
                    'alt')
                danawa_price = danawa_price_bs.select_one(
                    '#danawa_pop_content > div.similar_prod > div.info_area > div.price_a > span.low_price > em').text.replace(
                ',', '')
                danawa_url = danawa_price_bs.select_one('#danawa_pop_content > div.similar_prod > div.thumb_area > a').get(
                    'href')
                danawa_image = danawa_price_bs.select_one(
                    '#danawa_pop_content > div.similar_prod > div.thumb_area > a > img').get('src')

            else:

                danawa_mall = danawa_price_bs.select_one(
                    '#blog_content > div.summary_info > div.detail_summary > div.summary_left > div.lowest_area > div.lowest_list > table > tbody > tr.lowest > td.mall > div > a > img').get(
                    'alt')
                danawa_price = danawa_price_bs.select_one(
                    '#blog_content > div.summary_info > div.detail_summary > div.summary_left > div.lowest_area > div.lowest_list > table > tbody > tr.lowest > td.price > a > span.txt_prc > em').text.replace(
                    ',', '')
                danawa_url = danawa_price_bs.select_one(
                    '#blog_content > div.summary_info > div.detail_summary > div.summary_left > div.lowest_area > div.lowest_list > table > tbody > tr.lowest > td.mall > div > a').get(
                    'href')
                danawa_image = danawa_price_bs.select_one('#baseImage').get('src')

        except Exception:
            danawa_price = 1000000000000
            danawa_url = "상품이 없습니다"
            danawa_image = "상품이 없습니다"
            danawa_mall = "상품이 없습니다"
        ##다나와(일반상품)

        try:
            data2 = {
                'query': serial_no,
                'sort': 'priceASC',
                'volumeType': 'va',
                'limit': 90
            }
            headers3 = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                'Referer': 'http://search.danawa.com/dsearch.php'
            }
            danawa_all_req = requests.post(danawa_urls, data=data2, headers=headers3)
            danawa_all_bs = BeautifulSoup(danawa_all_req.text, 'html.parser')

            image = danawa_all_bs.select_one('.product_list > li:nth-of-type(1) > div > div > a > img ').get('data-original')
            price = danawa_all_bs.select_one(
                '.product_list > li:nth-of-type(1) > div > div:nth-of-type(3) > ul > li > a > p:nth-of-type(2) > strong').text.replace(
                ',', '')
            url = danawa_all_bs.select_one('.product_list > li:nth-of-type(1) > div > div:nth-of-type(2) > p > a').get('href')
            mall = danawa_all_bs.select_one(
                '.product_list > li:nth-of-type(1) > div > div:nth-of-type(3) > ul > li > a > p:nth-of-type(1)> img ').get(
                'alt')

        except Exception:
            price = 100000000000
            url = "상품이 없습니다"
            mall = "상품이 없습니다"
            image = "상품이 없습니다"

        # 가격비교 vs 일반상품
        if int(danawa_price) <= int(price):
            danawa_total_price = danawa_price
            danawa_total_mall = danawa_mall
            danawa_total_url = danawa_url
            danawa_total_image = danawa_image
        else:
            danawa_total_price = price
            danawa_total_mall = mall
            danawa_total_url = url
            danawa_total_image = image

        context_danawa ={'danawa_total_image': danawa_total_image, 'danawa_total_mall': danawa_total_mall,
               'danawa_total_price': danawa_total_price, 'danawa_total_url': danawa_total_url, }

    except Exception:
        context_danawa = {'danawa_error': '다나와'}

    context_naver.update(context_enuri)
    context_naver.update(context_danawa)
    return render(request, 'pages/result.html', context_naver)







