#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image
from PIL import ImageOps

import os

maindir = ''

app = QApplication([])
win = QWidget()

win.setWindowTitle('редактор "Easy Editor"')
win.resize(1080, 720)

btn_folder = QPushButton('Открыть папку')
img_list = QListWidget()
lb_image = QLabel('Картинка')

btn_left = QPushButton('Влево')
btn_right = QPushButton('Вправо')
btn_flip = QPushButton('Отзеркалить')
btn_sharp = QPushButton('Резкость')
btn_graysc = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton('Сбросить')

row = QHBoxLayout() #общий лэйаут
col1 = QVBoxLayout() #кнопка "открыть папку" и список
col1.addWidget(btn_folder)
col1.addWidget(img_list)
col2 = QVBoxLayout() #картинка и кнопки редактирования
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout() #кнопки редактирования
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_graysc)
row_tools.addWidget(btn_save)
row_tools.addWidget(btn_reset)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"


    def loadImage(self, dir, filename):
        #при загрузке запоминаем путь и имя файла 
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)


    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        #сохраняет копию файла в подпапке
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)


    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)


#функции
def openDir():
    global maindir
    maindir = QFileDialog.getExistingDirectory()

def filter(files, extensions = ['.png']):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showImageList():
    openDir()
    filenames = filter(os.listdir(maindir), ['.jpg','.jpeg','.png','.swg', '.bmp', '.gif'])
    img_list.clear()
    for name in filenames:
        img_list.addItem(name)

def showChosenImage():
    if img_list.currentRow() >= 0:
        filename = img_list.currentItem().text()
        image_path = os.path.join(maindir, filename)
        scaled_pix = QPixmap(image_path).scaled(lb_image.width(), lb_image.height(), Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pix)




workimage = ImageProcessor() #текущая рабочая картинка для работы
img_list.currentRowChanged.connect(showChosenImage)


btn_graysc.clicked.connect(workimage.do_bw)
btn_folder.clicked.connect(showImageList)
btn_flip.clicked.connect(workimage.mirror)
btn_save.clicked.connect(workimage.saveImage)

win.show()


app.exec()
