from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
import cv2
import os, io, re
from google.cloud import vision
from google.cloud.vision import types
from .models import Post
# Create your views here.


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

    text = my_list[0].replace('\n', '')

    context = {'text': text}

    return render(request, 'pages/detail.html', context)


def result(request):
    return render(request, 'pages/result.html')


