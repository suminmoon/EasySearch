from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from .models import Post
import cv2

# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def upload(request):

    image = request.FILES.get('image')
    post = Post(image=image)
    post.save()

    key = Post.objects.all()
    dbimg = key[len(key) - 1].image
    db = str(dbimg)

    if __name__ == '__main__':
        im = cv2.imread('/images/' + db)  # 'C:\\python_ML\\data\\cat.jpg'

        # Select ROI
        showCrosshair = False
        fromCenter = False
        r = cv2.selectROI("Image", im, fromCenter, showCrosshair)
        # r = cv2.selectROI(im)

        # Crop image
        imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # imCrop = im[int(r[1]):int(r[1] + r[2])]

        # Display cropped image
        cv2.imshow("Image", imCrop)
        cv2.imwrite('C:\python_ML\data/search/uploading/sample.jpg', imCrop)  # "C:\\python_ML\\data\\dog.jpg"
        cv2.waitKey(0)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return render(request, 'pages/upload.html')


def detail(request):
    key = Post.objects.all()
    dbimg = key[len(key)-1].image
    return render(request, 'pages/detail.html')



