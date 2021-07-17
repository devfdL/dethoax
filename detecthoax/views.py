from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def index(request):

    context ={
      'judul':'hoax detection',
      'webby':'Athalla rafly',
      'webname': 'hoax detecteren',
    }

    return render(request, 'index.html', context)


def Hoax(request):
    
    context ={
      'judul':'hoax detection',
      'webby':'Athalla rafly',
      'webname': 'hoax detecteren',
    }

    # upload gambar
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        img_dir = uploaded_file_url
        time.sleep(10)
        imgdr = img_dir[1:]
        #print(imgdr)
        # gambar ke teks
        image = cv2.imread(imgdr)
        while True:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)

            # load the image as a PIL/Pillow image, apply OCR, and then delete
            #the temporary file
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(Image.open(filename))
            os.remove(filename)
            print(text)

            f = open('text.txt','a')
            f.write(text)

            # show the output images
            #cv2.imshow("Image", image)
            #cv2.imshow("Output", gray)

            if len(text) > 1:
                break

        #cv2.destroyAllWindows()

        # mencari berita 
        f = open('text.txt', "r")
        info = f.read()

        # get title
        get_title = info.split('.')
        global title
        title = get_title[0]
        #print(title)

        driver = webdriver.Chrome("chromedriver.exe")
        driver.get("https://www.google.com/")
        time.sleep(1)
        text_input = driver.find_element_by_xpath("//input[@type='text']")
        text_input.clear()
        text_input.send_keys(title)
        time.sleep(3)
        get_news = driver.find_element_by_xpath("//div[@class='yuRUbf']").click()
        time.sleep(3)
        news_data = driver.find_elements_by_xpath("//body")
        time.sleep(2)

        # news = []

        with open('news.txt', "a") as news_file:
            for el in news_data:
                # news.append(el.text)                 
                news_file.write(el.text+"\n")
                time.sleep(1)
                break
        driver.quit()

        # cek kesamaan berita
        path_1 = 'text.txt'
        f1=open(path_1, "r")
        data1 =f1.read()
        s = data1.split()

        path_2 = 'news.txt'
        f2=open(path_2, "r")
        data2 =f2.read()
        f = data2.split()

        ss= set(s)  
        fs =set(f)

        #print(ss.intersection(fs)) 
        #print(ss.union(fs)) 
        different = ss.union(fs) - ss.intersection(fs)
        total = len(s) + len(f) 

        score = len(different)/total*100
        strscore = str(score)
        print('Score by different: ' + str(score) + ' %')
        f1.close()
        f2.close()
        os.remove('news.txt')
        os.remove('text.txt')

        str1 = " "

        return render(request, 'index.html', {
            'Score_by_different': strscore,
            'text_inp': data1,
            'result': data2,
            'judul':'hoax detecteren',
            'webby':'Athalla rafly',
            'webname': 'hoax detecteren',
        })
      

    return render(request, 'hoax.html', context)