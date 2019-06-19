import os
import io
import re
import cv2
from google.cloud import vision
from google.cloud.vision import types
from django.shortcuts import render, redirect, get_object_or_404

def image(request):
    # Read image
    im = cv2.imread('/images/sample.jpg')  #'C:\\python_ML\\data\\cat.jpg'
    print(im)
    return render(request)

#     # Select ROI
#     showCrosshair = False
#     fromCenter = False
#     r = cv2.selectROI("Image", im, fromCenter, showCrosshair)
#     # r = cv2.selectROI(im)
#
#     # Crop image
#     imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#     # imCrop = im[int(r[1]):int(r[1] + r[2])]
#
#     # Display cropped image
#     cv2.imshow("Image", imCrop)
#     cv2.imwrite('C:\python_ML\data/search/uploading/sample.jpg', imCrop) #"C:\\python_ML\\data\\dog.jpg"
#     cv2.waitKey(0)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
#
#
#
# client = vision.ImageAnnotatorClient()
#
# # 내가 분석하려는 이미지 파일 경로를 잡는 코드 같음
# # (os.path.dirname('파일경로'), '이미지파일명')
# file_name = os.path.join(
#     os.path.dirname('C:'),
#     '/python_ML\data/search/uploading/sample.jpg')
#
# # 이미지 로드
# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()
#
# image = types.Image(content=content)
#
# # 이미지 파일에서 text를 감지
# response = client.text_detection(image=image)
# texts = response.text_annotations
#
# my_list = list()
# # 이미지에서 추출한 texts들 중 description만 뽑아내기
# for text in texts:
#     result = text.description
#     my_list.append(result)
#
# data = my_list[0]
# print(data)
#
#
#
