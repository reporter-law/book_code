import pytesseract#tesserocr 变成了pytesseract
from PIL import Image
import glob,os
path = r"C:\Users\lenovo\Desktop\图片处理\pdf"
for file in glob.glob(os.path.join(path, "*.jpg")):
    images = Image.open(file)
    #images = images.convert('L')
    text = pytesseract.image_to_string(images)
    if text:
        print(text)
#image_to_text(images)#已经没有了
'''验证失败'''
#灰度化
def simple(file):
    images = Image.open(file)
    #images = images.convert('L')
    text = pytesseract.image_to_string(images)
    print(text)
    return text


def two_number(image):
    # images.show()
    image = Image.open(image)
    print(pytesseract.image_to_string(image))
    # 二值化
    threshold = 40
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = images.point(table, '1')
    result = pytesseract.image_to_string(image)
    print('ok')
    return result
two_number("J:\pyinstaller\Python3.8版本项目\github项目\自动化\checkcode.png")