from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfFileMerger
from wsgiref.util import FileWrapper
from pathlib import Path
from django.views.static import serve 
import mimetypes
import os
import shutil
import PyPDF2
import fpdf
from io import BytesIO,StringIO
import img2pdf
import pyrebase
import zipfile
from zipfile import ZipFile
import comtypes.client
import pythoncom
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from newspaper import Article
import re

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

def pdf_page(path):
    sd = str(BASE_DIR) +'\\'+ path
    print(sd)
    pdf = PdfFileReader(sd)
    return pdf.getNumPages()

def download1(request):
    filepath = request.POST.get("first","")
    download = 1
    filename = "part1.pdf"
    with open(filepath, 'rb') as f:
        pdf_contents = f.read()
    os.remove(filepath)
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', filename)
    return response

def download2(request):
    filepath = request.POST.get("second","")
    download = 1
    filename = "part2.pdf"
    with open(filepath, 'rb') as f:
        pdf_contents = f.read()
    os.remove(filepath)
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', filename)
    return response
       

def pdf_splitter(path,val1):
    fname = os.path.splitext(os.path.basename(path))[0]
    sd = str(BASE_DIR) + path
    pdf = PdfFileReader(sd)
    pdf_writer = PdfFileWriter()
    for page in range(val1,val2):
        pdf_writer.addPage(pdf.getPage(page))
    output_filename = '{}_page_{}.pdf'.format(fname, page+1)
    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)
    print('Created: {}'.format(output_filename))
    if(val1==0):
        file1 = str(BASE_DIR)+'\\'+output_filename
        return file1
    else:
        file2 = str(BASE_DIR)+'\\'+output_filename
        return file2
    
def home(request):
    return render(request,'webpages/home.html',{'title':'Home'})

def home1(request):
    return render(request,'webpages/home.html')

def about(request):
    return render(request,'webpages/about.html',{'title':'About'})

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def split1(request):
    context = {}
    val = int(request.POST["num1"])
    username = 'unlogged'
    if request.user.is_authenticated:
        username = request.user.username
    directory = 'media'+'\\'+username
    if request.method == 'POST':
        fs = FileSystemStorage(directory)
        uploaded_file = request.FILES['document']
        nam = uploaded_file.name
        nam = (nam.replace(" ", "_"))
        uploaded_file.name = nam
        name = fs.save(uploaded_file.name,uploaded_file)
        size = pdf_page(directory+'\\'+nam)
        if(val>=size):
           return render(request, 'webpages/split.html', {'alert_flag': True})
        '''config = {
            'apiKey': "AIzaSyA9uEa3RB3lQMHwY09OAkP6CH6BrhNskpQ",
            'authDomain': "praful-pdf.firebaseapp.com",
            'databaseURL': "https://praful-pdf.firebaseio.com",
            'projectId': "praful-pdf",
            'storageBucket': "praful-pdf.appspot.com",
            'messagingSenderId': "362849410817",
            'appId': "1:362849410817:web:a339b25414e33248ffc500",
            'measurementId': "G-D8LWGR78X5"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        path_on_cloud = "pdf/split/{}".format(nam)
        path_on_local =  str(BASE_DIR) + fs.url(name)
        storage.child(path_on_cloud).put(path_on_local)'''
        path = directory+'\\'+nam
        sd = str(BASE_DIR) +'\\'+ path
        pdf = PdfFileReader(sd)
        pdf_writer = PdfFileWriter()
        for page in range(0,val):
            pdf_writer.addPage(pdf.getPage(page))
        output_filename1 = '{}.pdf'.format('part1')
        with open(output_filename1, 'wb') as out:
            pdf_writer.write(out)
        output_filename2 = '{}.pdf'.format('part2')
        pdf_writer1 = PdfFileWriter()
        for page in range(val,size):
            pdf_writer1.addPage(pdf.getPage(page))
        with open(output_filename2, 'wb') as out:
            pdf_writer1.write(out)
        #os.remove(sd)
        file1 = str(BASE_DIR)+'\\'+output_filename1
        file2 = str(BASE_DIR)+'\\'+output_filename2
        zipObj = ZipFile('sample.zip', 'w')
        zipObj.write(output_filename1)
        zipObj.write(output_filename2)
        zipObj.close()
        os.remove(file1)
        os.remove(file2)
        file1 = str(BASE_DIR)+'\\'+'sample.zip'
        zip_file = open(file1, 'rb')
        response = HttpResponse(zip_file, content_type='application/force-download')
        zip_file.close()
        os.remove(file1)
        response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ',nam+'.zip')
        return response

def split(request):
    return render(request,'webpages/split.html',{'title':'Split'})

def merge(request):
    return render(request,'webpages/merge.html',{'title':'Merge'})

def merge1(request):
    username = 'unlogged'
    if request.user.is_authenticated:
        username = request.user.username
    directory = 'media'+'\\'+username
    fs = FileSystemStorage(directory)
    pdf_merger = PdfFileMerger()
    download = 1
    output_file = 'temp.pdf'
    for count, x in enumerate(request.FILES.getlist("files")):
        pdf_merger.append(x)
        uploaded_file = x
        nam = uploaded_file.name
        nam = (nam.replace(" ", "_"))
        uploaded_file.name = nam
        name = fs.save(uploaded_file.name,uploaded_file)
        '''config = {
            'apiKey': "AIzaSyA9uEa3RB3lQMHwY09OAkP6CH6BrhNskpQ",
            'authDomain': "praful-pdf.firebaseapp.com",
            'databaseURL': "https://praful-pdf.firebaseio.com",
            'projectId': "praful-pdf",
            'storageBucket': "praful-pdf.appspot.com",
            'messagingSenderId': "362849410817",
            'appId': "1:362849410817:web:a339b25414e33248ffc500",
            'measurementId': "G-D8LWGR78X5"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        #path_on_cloud = "pdf/merge/{}".format(nam)
        #path_on_local =  str(BASE_DIR) + fs.url(name)
        #storage.child(path_on_cloud).put(path_on_local)'''
    with open(output_file, 'wb') as fileobj:
        pdf_merger.write(fileobj)
    filepath = str(BASE_DIR)+'\\'+output_file
    filename = "result.pdf"
    with open(filepath, 'rb') as f:
        pdf_contents = f.read()
    os.remove(filepath)
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', filename)
    return response

def compress(request):
    return render(request,'webpages/compress.html',{'title':'Compress'})

def compress1(request):
    username = 'unlogged'
    if request.user.is_authenticated:
        username = request.user.username
    directory = 'media'+'\\'+username
    fs = FileSystemStorage(directory)
    uploaded_file = request.FILES['document']
    download = 1
    nam = uploaded_file.name
    nam = (nam.replace(" ", "_"))
    uploaded_file.name = nam
    name = fs.save(uploaded_file.name,uploaded_file)
    '''config = {
            'apiKey': "AIzaSyA9uEa3RB3lQMHwY09OAkP6CH6BrhNskpQ",
            'authDomain': "praful-pdf.firebaseapp.com",
            'databaseURL': "https://praful-pdf.firebaseio.com",
            'projectId': "praful-pdf",
            'storageBucket': "praful-pdf.appspot.com",
            'messagingSenderId': "362849410817",
            'appId': "1:362849410817:web:a339b25414e33248ffc500",
            'measurementId': "G-D8LWGR78X5"
        }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    path_on_cloud = "pdf/compress/{}".format(nam)
    path_on_local =  str(BASE_DIR) + fs.url(name)
    storage.child(path_on_cloud).put(path_on_local)'''
    writer = PdfFileWriter()
    filename = "result.pdf"
    sd = str(BASE_DIR) +'\\'+ directory+'\\'+nam
    reader = PdfFileReader(sd)
    for i in range(reader.numPages):
        page = reader.getPage(i)
        page.compressContentStreams()
        writer.addPage(page)
    with open('filepath', 'wb') as f:
        writer.write(f)
    with open('filepath', 'rb') as f:
        pdf_contents = f.read()
    os.remove('filepath')
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', filename)
    return response

def encrypt(request):
    return render(request,'webpages/encrypt.html',{'title':'Encrypt'})

def encrypt1(request):
    val = request.POST["pswd"]
    username = 'unlogged'
    if request.user.is_authenticated:
        username = request.user.username
    directory = 'media'+'\\'+username
    fs = FileSystemStorage(directory)
    uploaded_file = request.FILES['document']
    download=1
    nam = uploaded_file.name
    nam = (nam.replace(" ", "_"))
    uploaded_file.name = nam
    name = fs.save(uploaded_file.name,uploaded_file)
    '''config = {
            'apiKey': "AIzaSyA9uEa3RB3lQMHwY09OAkP6CH6BrhNskpQ",
            'authDomain': "praful-pdf.firebaseapp.com",
            'databaseURL': "https://praful-pdf.firebaseio.com",
            'projectId': "praful-pdf",
            'storageBucket': "praful-pdf.appspot.com",
            'messagingSenderId': "362849410817",
            'appId': "1:362849410817:web:a339b25414e33248ffc500",
            'measurementId': "G-D8LWGR78X5"
        }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    path_on_cloud = "pdf/encrypt/{}".format(nam)
    path_on_local =  str(BASE_DIR) + fs.url(name)
    storage.child(path_on_cloud).put(path_on_local)'''
    sd = str(BASE_DIR) +'\\'+ directory+'\\'+nam
    pdf = PdfFileReader(sd)
    output_pdf = PdfFileWriter()
    output_pdf.appendPagesFromReader(pdf)
    output_pdf.encrypt(val)
    filename = "result.pdf"
    with open("filepath", "wb") as out_file:
        output_pdf.write(out_file)
    with open("filepath", 'rb') as f:
        pdf_contents = f.read()
    os.remove('filepath')
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', filename)
    return response

def image(request):
    return render(request,"webpages/image.html",{"title":"Image"})

def image1(request):
    val = ''
    val = request.POST["num1"]
    if(val==''):
        val = 'convert'
    output_file='temp.pdf'
    username = 'unlogged'
    if request.user.is_authenticated:
        username = request.user.username
    directory = 'media'+'\\'+'djangos_images'
    directory_user = 'media'+'\\'+username
    fs = FileSystemStorage(directory)
    download = 1
    filename = 'result.pdf'
    filepath = str(BASE_DIR)+'\\'+output_file
    dirname = str(BASE_DIR)+'\\'+'media'+'\\'+'djangos_images'
    '''config = {
            'apiKey': "AIzaSyA9uEa3RB3lQMHwY09OAkP6CH6BrhNskpQ",
            'authDomain': "praful-pdf.firebaseapp.com",
            'databaseURL': "https://praful-pdf.firebaseio.com",
            'projectId': "praful-pdf",
            'storageBucket': "praful-pdf.appspot.com",
            'messagingSenderId': "362849410817",
            'appId': "1:362849410817:web:a339b25414e33248ffc500",
            'measurementId': "G-D8LWGR78X5"
        }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()'''
    for count, x in enumerate(request.FILES.getlist("files")):
        uploaded_file = x
        name = fs.save(uploaded_file.name,uploaded_file)
        #path_on_cloud = "pdf/image/{}".format(name)
        #path_on_local =  str(BASE_DIR) + fs.url(name)
        #storage.child(path_on_cloud).put(path_on_local)
        uploaded_file.name = '{}.jpeg'.format(count)
    with open("filepath","wb") as f:
        imgs=[]
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                continue
            imgs.append(path)
        f.write(img2pdf.convert(imgs))
    with open("filepath", 'rb') as f:
        pdf_contents = f.read()
    for fname in os.listdir(dirname):
        os.remove(dirname+'\\'+fname)
    if(username!='unlogged'):
        shutil.copy("filepath",directory_user+'\\'+val+'.pdf')
    os.remove("filepath")
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', val+'.pdf')
    return response

def web(request):
    return render(request,'webpages/web.html',{'title':'HTML'})

def web1(request):
    val = request.POST["num1"]
    name = request.POST["name"]
    '''uploaded_file = request.FILES['document']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name,uploaded_file)
    template = get_template("webpages/html_convert.html")
    context = Context({'pagesize':'A4'})
    html = template.render({'pagesize':'A4'})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html), dest=result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else: 
        return HttpResponse('Errors')'''
    username = 'unlogged'
    if request.user.is_authenticated:
        username = request.user.username
    directory_user = 'media'+'\\'+username
    article = Article(val)
    article.download()
    article.parse()
    strs = article.text
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    ct=1
    font_dir = str(BASE_DIR)+'\\'+'static'+'\\'+'arial-unicode-ms.ttf'
    pdf.add_font('ArialUnicode',fname=font_dir,uni=True)
    pdf.set_font("ArialUnicode", size=12) # font and textsize
    pdf.cell(200, 10, txt=article.title, ln=1, align="C")
    for x in strs.splitlines():
        a = [line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', x)]
        for b in a:
            pdf.add_font('ArialUnicode',fname=font_dir,uni=True)
            ct+=1
            pdf.set_font("ArialUnicode", size=12) # font and textsize
            pdf.cell(200, 10, txt=b, ln=1, align="L")
            if(ct%24==0):
                pdf.add_page()
    pdf.output("test.pdf")
    filename = 'parsed.pdf'
    with open("test.pdf", 'rb') as f:
        pdf_contents = f.read()
    if(username!='unlogged'):
        shutil.copy("test.pdf",directory_user+'\\'+name+'.pdf')
    os.remove('test.pdf')
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    download=1
    response['Content-Disposition'] = "%sfilename=%s" % ('attachment; ' if download else '', filename)
    return response