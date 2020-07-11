from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import os
from django.conf import settings
import cv2
from . import cv_methods
import numpy as np
# * if 'opencv-contrib-python-headless' is installed
# * No need other opencv package. Use it for production

"""
https://github.com/openpaperwork/pyocr/issues/93
when I use tesserocr, I feel tesserocr is more oriented towards the original tesseract. 
On the other hand, pyocr is intuitive, however not as flexibel compare to tesseract.
"""


class Home(TemplateView):
    template_name: "home.html"


def upload(request):
    """
    HTML image upload for testing. 
    NOTES:
    if the uploaded image has a duplicate name then 
    FileSystemStorage adds a random str at the end of orginal name
    Consider generating UUID for file name. 

    # img = cv2.imread("/Users/burak/Projects/Ticari/lottoapp-200713/backend/src/uploads/img.jpg")
    # gray = get_grayscale(img)
    # cv2.imshow("gray", gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    """
    context = {}
    if request.method == "POST":
        img = request.FILES["image"]
        fs = FileSystemStorage()
        uploaded = fs.save(img.name, img)  # returns unique name
        imgcv = cv2.imread(settings.BASE_DIR + "/media/" + uploaded)
        uppath = settings.BASE_DIR + "/media/" + uploaded
        cvimg = cv2.imread(uppath)
        gray = cv_methods.get_grayscale(cvimg)
        boolsaved = cv2.imwrite(settings.BASE_DIR + "/media/_savevee.jpg" , gray)
        # grayname = fs.save("saved.jpg", saved)  # returns unique name
        # print(f"saved image path: {grayname}")
        context["original"] = fs.url(uploaded) 
        context["gray"] = fs.url("_savevee.jpg") 
    return render(request, "upload/upload.html", context)


def index(request):
    return HttpResponse("Hello, world.")
