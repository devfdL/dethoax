## Cara kerja

* input gambar

```python
if request.method == 'POST' and request.FILES['myfile']:
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    # menyimpan gambar ke direktori
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    img_dir = uploaded_file_url
    time.sleep(10)
    # mendapatkan lokasi gambar yang sudah di upload
    imgdr = img_dir[1:]
```

* gambar ke teks

```python
# memasukan dir gambar yang ingin di ubah ke teks
image = cv2.imread(imgdr)
while True:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # merubah format gambar ke .png
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    #the temporary file
    # proses merubah dari gambar ke teks
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(filename))

    # menghapus gambar yang sudah diubah ke teks
    os.remove(filename)

    # menulis teks yang didapat ke file txt
    f = open('text.txt','a')
    f.write(text)

    # menghentikan proses
    if len(text) > 1:
        break
```

* mencari berita di web

```python
# mencari berita 
f = open('text.txt', "r")
info = f.read()

# mencari judul berita
get_title = info.split('.')
global title
title = get_title[0]

# mencari berita yang sesuai judul di web
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


# menulis berita yang didapat ke file txt
with open('news.txt', "a") as news_file:
    for el in news_data:             
        news_file.write(el.text+"\n")
        time.sleep(1)
        break
driver.quit()
```

* proses cek kesamaan berita

```python
# mengambil teks berita yang di input
path_1 = 'text.txt'
f1=open(path_1, "r")
data1 =f1.read()
s = data1.split()


# mengambil teks berita yang di cari di web
path_2 = 'news.txt'
f2=open(path_2, "r")
data2 =f2.read()
f = data2.split()

ss= set(s)  
fs =set(f)

# menghitung perbedaan berita yang diinput dengan berita yang di dapat

# fungsi union (gabungan)
#fungsi intersection (irisan)

different = ss.union(fs) - ss.intersection(fs)
total = len(s) + len(f) 

score = len(different)/total*100
strscore = str(score)
print('Score by different: ' + str(score) + ' %')
```