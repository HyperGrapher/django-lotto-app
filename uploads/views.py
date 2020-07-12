from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import cv2
import pytesseract
from . import cv_methods
# from PIL import Image


# * if 'opencv-contrib-python-headless' is installed
# * No need other opencv package. Use it for production

"""
https://github.com/openpaperwork/pyocr/issues/93
when I use tesserocr, I feel tesserocr is more oriented
towards the original tesseract.
On the other hand, pyocr is intuitive,
however not as flexibel compare to tesseract.

Text Detection with OpenCV in Python | OCR using Tesseract (2020)
https://youtu.be/6DjFscX4I_c   -> DIGIT reading

Text recognition (OCR) with Tesseract and Python
https://youtu.be/JkzFjj2hjtw -> filtering vs..

# img = cv2.imread("/Users/burak..src/uploads/img.jpg")
# gray = get_grayscale(img)
# cv2.imshow("gray", gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
"""

pytesseract.pytesseract.tesseract_cmd = (
    r"/usr/local/Cellar/tesseract/4.1.1/bin/tesseract"
)

# digit reading -> image_to_string(img, config=conf)
conf = r"--oem 3 --psm 6 outputbase digits"


def upload(request):
    """
    HTML image upload for testing.
    NOTES:
    if the uploaded image has a duplicate name then
    FileSystemStorage adds a random str at the end of orginal name
    Consider generating UUID for file name.

    """
    context = {}
    if request.method == "POST":
        base = settings.BASE_DIR  # Project root dir "src"
        img = request.FILES["image"]
        fs = FileSystemStorage()
        uploaded = fs.save(img.name, img)  # returns unique name
        uppath = base + "/media/" + uploaded
        cvimg = cv2.imread(uppath)  # returns image
        # convert from BGR to RGB mode:
        # pytesseract assumes RGB format. Not required for grayscale
        # img_rgb = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        gray = cv_methods.get_grayscale(cvimg)  # returns image
        context["text"] = pytesseract.image_to_string(gray, lang="tur")
        cv2.imwrite(base + "/media/processed/saved.jpg", gray)  # returns bool
        # grayname = fs.save("saved.jpg", saved)  # returns unique name
        # print(f"saved image path: {grayname}")
        context["original"] = fs.url(uploaded)
        context["gray"] = fs.url("processed/saved.jpg")
    return render(request, "upload/upload.html", context)


def upload2(request):
    """
    HTML image upload for testing.
    NOTES:
    if the uploaded image has a duplicate name then
    FileSystemStorage adds a random str at the end of orginal name
    Consider generating UUID for file name.

    """
    context = {}
    if request.method == "POST":
        base = settings.BASE_DIR
        img = request.FILES["image"]
        fs = FileSystemStorage()
        uploaded = fs.save(img.name, img)  # returns unique name
        uppath = base + "/media/" + uploaded
        cvimg = cv2.imread(uppath)  # returns image
        gray = cv_methods.get_grayscale(cvimg)
        cv2.imwrite(base + "/media/processed/saved2.jpg", gray)  # returns bool
        # grayname = fs.save("saved.jpg", saved)  # returns unique name
        # print(f"saved image path: {grayname}")
        context["original"] = fs.url(uploaded)
        context["gray"] = fs.url("processed/saved2.jpg")
    return render(request, "upload/upload.html", context)


def index(request):
    return HttpResponse("Hello, world.")
