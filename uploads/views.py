from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

class Home(TemplateView):
    template_name: 'home.html'

def upload(request):
    '''
    HTML image upload for testing. 
    NOTES:
    if the uploaded image has a duplicate name then 
    FileSystemStorage adds a random str at the end of orginal name
    '''
    context = {}
    print("NEW REQUEST")
    if request.method == 'POST':
        img = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(img.name, img)
        context['url'] = fs.url(name)
        print(f"File name: {img.name} and file size: {img.size}")
        print(f"File storage name:{fs.url(name)}")
    return render(request, 'upload/upload.html', context)

def index(request):
    return HttpResponse("Hello, world.")


