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

    # # Select ROI
    showCrosshair = False
    fromCenter = False
    r = cv2.selectROI("Image", im, fromCenter, showCrosshair)
    # r = cv2.selectROI(im)
    #
    # # Crop image
    imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    # imCrop = im[int(r[1]):int(r[1] + r[2])]
    #
    # # Display cropped image
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
        result = text.description
        my_list.append(result)

    serial_no = my_list[0].replace('\n', '')

    context = {'serial_no': serial_no}

    return render(request, 'pages/detail.html', context)


def result(request, serial_no):
    # query = serial_no
    # 8006790  # 버버리 코트
    # SF199SK  # 페레가모 선글라스
    url = f"http://www.enuri.com/lsv2016/ajax/getSearchGoods_ajax.jsp?key=minprice3&keyword={serial_no}"
    res = requests.get(url)
    result = res.json()

    ### 가격비교 최저가
    product = result.get('srpModelList')[0]
    strImgUrl = product.get('strImgUrl')  # 이미지
    strModelName = product.get('strModelName')  # 상품 이름
    # print(product.get('lngMinPrice'))  # 상품 가격
    modelno = product.get('intModelNo')  # 가격비교 상세 사이트 이동을 위한 model NO
    strCa_code = product.get('strCa_code')  # 가격비교 상세 사이트 이동을 위한 category code

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

    # print("가격비교 최저가")
    # print(f"이미지: {strImgUrl}")
    # print(f"상품 이름: {strModelName}")
    # print(f"상품 가격: {price}")
    # print(f"쇼핑몰: {shop_name}")
    # print(f"최저가 url: {url_minprice}")
    context = {'price':price, 'shop_name':shop_name, 'shop_code':shop_code, 'pl_no':pl_no, 'url_minprice':url_minprice}
    return render(request, 'pages/result.html', context)


