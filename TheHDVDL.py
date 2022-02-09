import sys
from PyQt5.QtWidgets import QApplication,QTabWidget, \
    QWidget, QComboBox, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QPen
from PyQt5 import uic
from PyQt5.QtCore import Qt
import cv2
from glob import glob
import numpy as np
from image_process import *
from data_process import *
import os
import random

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)

        # Display image
        self.label_show_image = self.findChild(QLabel, 'label_show_image')
        self.label_show_card = self.findChild(QLabel, 'show_card')
        self.w_display = 1280
        self.h_display = 720
        #Load background button
        self.list_image_background = []
        self.load_background_button = self.findChild(QPushButton, 'background_button')
        self.number_background = self.findChild(QLabel, 'number_background')
        self.load_background_button.clicked.connect(self.load_file_background)
        #Back Next button for background
        self.index_background = 0
        self.next_background_button = self.findChild(QPushButton, 'pushButton_6')
        self.next_background_button.clicked.connect(self.next_background)
        self.number_show_image = self.findChild(QLabel, 'number_show_image')

        self.back_background_button = self.findChild(QPushButton, 'back_button')
        self.back_background_button.clicked.connect(self.back_background)
        # return  self.list_image_background and self.index_background

        #Load card button
        self.list_image_card = []
        self.load_card_button = self.findChild(QPushButton, 'card_button')
        self.number_card = self.findChild(QLabel, 'number_card')
        self.load_card_button.clicked.connect(self.load_file_card)
        self.number_show_card = self.findChild(QLabel, 'number_show_card')

        #Back Next card button
        self.back_card_button = self.findChild(QPushButton, 'pushButton_2')
        self.back_card_button.clicked.connect(self.back_card)
        self.next_card_button = self.findChild(QPushButton, 'pushButton_3')
        self.next_card_button.clicked.connect(self.next_card)
        self.index_card = 0
        # return  self.list_image_card and self.index_card

        #Position mouse
        self.mouse_position = self.findChild(QLabel, 'mouse_position')
        self.mouse_position.setAlignment(Qt.AlignCenter)

        #Paste card to background
        self.list_point = []
        self.list_polygon = []
        #self.paste_button = self.findChild(QPushButton, 'paste_button')
        #self.paste_button.clicked.connect(self.paste_card_to_background)
        self.c = -1 #bien check ve nhieu card tren 1 back ground

        #Ve lai
        self.undo_button = self.findChild(QPushButton, 'pushButton_4')
        self.undo_button.clicked.connect(self.undo_paste)

        #Select class
        self.class_index = 0
        self.select_class_button = self.findChild(QComboBox, 'class_combobox')
        self.select_class_button.currentIndexChanged.connect(self.select_class)

        #select draw
        self.draw_point = 0
        self.select_draw_point = self.findChild(QComboBox, 'comboBox')
        self.select_draw_point.currentIndexChanged.connect(self.select_draw)

        #Load Folder save data
        self.folder_save_data = ''
        self.save_folder_button = self.findChild(QPushButton, 'save_folder_button')
        self.save_folder_button.clicked.connect(self.load_folder_save)

        #Save button
        self.save_button = self.findChild(QPushButton, 'save_data_button')
        self.save_button.clicked.connect(self.save_data_to_folder)
        self.data_yolo = []
        self.action_image = ''

        #increase_brightness
        self.brightness = 0
        self.increase_brightness_button = self.findChild(QPushButton, 'increase_brightness')
        self.increase_brightness_button.clicked.connect(self.tang_do_sang)

        self.decrease_brightness_button = self.findChild(QPushButton, 'decrease_brightness')
        self.decrease_brightness_button.clicked.connect(self.giam_do_sang)

        #noise adder
        self.noise_button = self.findChild(QPushButton, 'noise_button')
        self.noise_button.clicked.connect(self.add_noise)

        self.noise_button_2 = self.findChild(QPushButton, 'noise_button_2')
        self.noise_button_2.clicked.connect(self.add_noise_2)

        self.smoke_button = self.findChild(QPushButton, 'smoke_button')
        self.smoke_button.clicked.connect(self.add_smoke)

        #them nut tat
        self.task_button = self.findChild(QPushButton, 'task_al')
        self.task_button.clicked.connect(self.all_task)

    def all_task(self):
        self.save_data_to_folder()
        self.tang_do_sang()
        self.add_noise()
        self.add_noise_2()
        self.add_smoke()


    def paste_card_to_background(self):
        #return self.data_yolo list, self.bg_mask
        if len(self.list_image_card) != 0:
            if len(self.list_polygon)==1:
                bg = cv2.imread(self.list_image_background[self.index_background])
            else:
                bg = self.image_pasted

            card = cv2.imread(self.list_image_card[self.index_card])
            #print(self.list_polygon[len(self.list_polygon)-1])
            self.image_pasted = card_to_background(bg, card, self.list_polygon[len(self.list_polygon)-1])
            temp = get_data_yolo(self.w_image, self.h_image, self.list_polygon[len(self.list_polygon)-1], self.class_index )
            self.mouse_position.setText(temp)
            self.data_yolo.append(temp)
            #bbox = get_box(temp, self.image_pasted)
            #self.image_pasted_bbox = draw_poly(self.image_pasted, bbox, size=0.005, color_bgr=[0, 0, 255])
            self.show_image_pasted(self.image_pasted)
        else:
            QMessageBox.warning(self, 'Canh bao!', 'Chưa chọn file!')
    def load_folder_save(self):
        self.folder_save_data  = QFileDialog.getExistingDirectory(None, 'Tạo mới folder để lưu:', '/home/',
                                                QFileDialog.ShowDirsOnly)
                                                
    def save_data(self):
        if self.folder_save_data != '':
            self.mouse_position.setText('Saving ...')
            temp = self.list_image_background[self.index_background]
            temp = temp.split('/')
            temp = temp.pop()

            temp = temp.split('.')
            temp.pop()
            path = self.folder_save_data +'/'+ ''.join(temp) + self.action_image

            action = self.action_image.split('_')
            action = action.pop()
                

                #ve mask cho background
            bg_mask = self.image_pasted
            h, w, channel = bg_mask.shape
            for i in self.list_polygon:
                newpolygon = find_new_polygon(i, 1)
                bg = fill_poly(bg_mask, newpolygon, (0, 0, 0))
                #cv2.imshow('ff',bg)
                #cv2.waitKey()
                #self.show_image_pasted(bg)
            rand = random.randint(0, len(self.list_image_card)-1)
            if True:
                bg = bg_mask

                card = cv2.imread(self.list_image_card[rand])
                card = cv2.resize(card, (w,h))
                temp = self.list_image_card[rand]
                temp = temp.split('/')
                temp = temp.pop()

                temp = temp.split('.')
                temp.pop()
                card_name = ''.join(temp)
    
                for j in self.list_polygon:
                    temp = four_point_transform(card, j)
                    bg = cv2.add(bg, temp)
                        
                    #cv2.imshow('gg', bg)
                    #cv2.waitKey()

                if action == 'new':
                    img_path = path + card_name + '_%d'%(rand) + '.jpg'
                    cv2.imwrite(img_path, bg)
                    
                    txt_path = path + card_name + '_%d'%(rand) + '.txt'
                    data_save = '\n'.join(self.data_yolo)
                    file = open(txt_path, 'w')
                    file.write(data_save)
                    file.close()
                elif action == 'sun':
                    noise_image = cv2.imread('img/nang_noise.jpeg')

                    bg = blend(bg, noise_image, opaque=0.3)
                    img_path = path + card_name + '_%d'%(rand) + '.jpg'
                    cv2.imwrite(img_path, bg)
                    txt_path = path + card_name + '_%d'%(rand) + '.txt'
                    data_save = '\n'.join(self.data_yolo)
                    file = open(txt_path, 'w')
                    file.write(data_save)
                    file.close()
                elif action == 'rain':
                    noise_image = cv2.imread('img/mua.jpg')
                    bg = blend(bg, noise_image, opaque=0.1)
                    img_path = path + card_name+'_%d'%(rand) + '.jpg'
                    cv2.imwrite(img_path, bg)
                    txt_path = path + card_name + '_%d'%(rand) + '.txt'
                    data_save = '\n'.join(self.data_yolo)
                    file = open(txt_path, 'w')
                    file.write(data_save)
                    file.close()
                elif action == 'ts':
                    bg = change_brightness(bg)
                    img_path = path + card_name+ '_%d'%(rand) + '.jpg'
                    cv2.imwrite(img_path, bg)
                    txt_path = path + card_name + '_%d'%(rand) + '.txt'
                    data_save = '\n'.join(self.data_yolo)
                    file = open(txt_path, 'w')
                    file.write(data_save)
                    file.close()
                elif action == 'gs':
                    bg = change_brightness(bg, -30)
                    img_path = path + card_name+ '_%d'%(rand) + '.jpg'
                    cv2.imwrite(img_path, bg)
                    txt_path = path + card_name + '_%d'%(rand) + '.txt'
                    data_save = '\n'.join(self.data_yolo)
                    file = open(txt_path, 'w')
                    file.write(data_save)
                    file.close()
                elif action == 'smk':
                    noise_image = cv2.imread('img/khoi.jpg')
                    bg = blend(bg, noise_image, opaque = 0.2)
                    img_path = path + card_name+ '_%d'%(rand) + '.jpg'
                    cv2.imwrite(img_path, bg)
                    txt_path = path + card_name + '_%d'%(rand) + '.txt'
                    data_save = '\n'.join(self.data_yolo)
                    file = open(txt_path, 'w')
                    file.write(data_save)
                    file.close()
                    

            self.mouse_position.setText('Đã lưu '+self.action_image+'!')
        else:
            QMessageBox.warning(self, 'Canh bao!', 'Chưa chọn file save!')
            self.load_folder_save()
    def add_smoke(self):
        self.action_image = self.action_image + '_smk'
        self.save_data()
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])


    def tang_do_sang(self):
        self.action_image = self.action_image + '_ts'
        self.save_data()
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])

    def giam_do_sang(self):  
        self.action_image = self.action_image + '_gs'
        self.save_data()
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])
    def save_data_to_folder(self):
        self.action_image = self.action_image + '_new'
        self.save_data()
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])
        #self.list_polygon = []


    def add_noise(self):

        self.action_image = self.action_image + '_sun'
        self.save_data()
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])
        #self.list_polygon = []
        

    def add_noise_2(self):
        self.action_image = self.action_image + '_rain'
        self.save_data()
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])
        #self.list_polygon = []


    def load_file_card(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select', '/home/',
                                                QFileDialog.ShowDirsOnly)                                               
        self.list_image_card = glob(dir_ + "/*")
        self.show_image_card(self.list_image_card[0])
        self.number_card.setText('{} anh'.format(len(self.list_image_card)))
        self.number_show_card.setAlignment(Qt.AlignCenter)
        self.number_show_card.setText('{}/{}'.format(self.index_card+1, len(self.list_image_card)))
    def back_card(self):
        self.index_card -= 1
        #self.list_point = []
        if self.index_card >=0:
            #print(self.index_background)
            self.show_image_card(self.list_image_card[self.index_card])
        else:
            self.index_card += 1
            #QMessageBox.warning(self, 'Canh bao!', 'het')
        self.number_show_card.setText('{}/{}'.format(self.index_card+1, len(self.list_image_card)))
    def next_card(self):
        self.index_card += 1
        #self.list_point = []
        
        if self.index_card < len(self.list_image_card):
            #print(self.index_background)
            self.show_image_card(self.list_image_card[self.index_card])
        else:
            self.index_card -= 1
            #QMessageBox.warning(self, 'Canh bao!', 'het')
        self.number_show_card.setText('{}/{}'.format(self.index_card+1, len(self.list_image_card)))

        
    def select_class(self, i):
        self.class_index = i
    def select_draw(self, i):
        self.draw_point = i
    def load_file_background(self):
        self.data_yolo = []
        self.number_card_in_image = 0
        self.list_polygon = []
        dir_ = QFileDialog.getExistingDirectory(None, 'Select', '/home/',
                                                QFileDialog.ShowDirsOnly)                                               
        self.list_image_background = glob(dir_ + "/*")
        self.list_image_background.sort()
        self.show_image_background(self.list_image_background[0])
        self.image_pasted = cv2.imread(self.list_image_background[0])
        self.number_background.setText('{} anh'.format(len(self.list_image_background)))
        self.number_show_image.setAlignment(Qt.AlignCenter)
        self.number_show_image.setText('{}/{}'.format(self.index_background+1, len(self.list_image_background)))
    def next_background(self):
        self.index_background += 1
        self.list_point = []
        self.list_polygon = []
        self.data_yolo = []
        self.action_image = ''
        
        if self.index_background < len(self.list_image_background):
            #print(self.index_background)
            self.show_image_background(self.list_image_background[self.index_background])
            self.image_pasted = cv2.imread(self.list_image_background[self.index_background])
        else:
            self.index_background -= 1
            QMessageBox.warning(self, 'Canh bao!', 'het')
        self.number_show_image.setText('{}/{}'.format(self.index_background+1, len(self.list_image_background)))
        self.mouse_position.setText('')
        self.number_card_in_image = 0
        

    def back_background(self):
        self.data_yolo = []
        self.index_background -= 1
        self.list_point = []
        self.list_polygon = []
        self.action_image = ''
        if self.index_background >=0:
            #print(self.index_background)
            self.show_image_background(self.list_image_background[self.index_background])
            self.image_pasted = cv2.imread(self.list_image_background[self.index_background])
        else:
            self.index_background += 1
            QMessageBox.warning(self, 'Canh bao!', 'het')
        self.number_show_image.setText('{}/{}'.format(self.index_background+1, len(self.list_image_background)))
        self.mouse_position.setText('')
        self.number_card_in_image = 0
    def undo_paste(self):
        self.data_yolo = []
        self.list_point = []
        self.list_polygon = []
        self.action_image = ''
        self.number_show_image.setText('{}/{}'.format(self.index_background+1, len(self.list_image_background)))
        self.mouse_position.setText('')
        self.number_card_in_image = 0
        self.show_image_background(self.list_image_background[self.index_background])
        self.image_pasted = cv2.imread(self.list_image_background[self.index_background])


    def show_image_background(self, path_image):
        arr_image = cv2.imread(path_image)
        self.h_image, self.w_image, c = arr_image.shape

        ratio_w = self.w_display/self.w_image
        ratio_h = self.h_display/self.h_image
        if (ratio_w<ratio_h):
            self.w = int(self.w_image * ratio_w)
            self.h = int(self.h_image * ratio_w)
        else:
            self.w = int(self.w_image * ratio_h)
            self.h = int(self.h_image * ratio_h)

        arr_image = cv2.resize(arr_image, (self.w, self.h), interpolation=cv2.INTER_AREA)

        height, width, channel = arr_image.shape
        self.label_show_image.setFixedWidth(width) # sua size label = size anh
        self.label_show_image.setFixedHeight(height)
        #convert tu BGR (opencv) -> hien thi chuan RGB
        img = QImage(cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB), width, height, width * 3, QImage.Format_RGB888)
        pix_map = QPixmap(img).scaled(width, height, Qt.KeepAspectRatio)
        self.label_show_image.setPixmap(pix_map)
        self.label_show_image.setScaledContents(True)
        self.label_show_image.show()
    def show_image_pasted(self, arr_image):
        self.h_image, self.w_image, c = arr_image.shape

        ratio_w = self.w_display/self.w_image
        ratio_h = self.h_display/self.h_image
        if (ratio_w<ratio_h):
            self.w = int(self.w_image * ratio_w)
            self.h = int(self.h_image * ratio_w)
        else:
            self.w = int(self.w_image * ratio_h)
            self.h = int(self.h_image * ratio_h)
        arr_image = cv2.resize(arr_image, (self.w, self.h), interpolation=cv2.INTER_AREA)

        #arr_image = cv2.resize(arr_image, (self.w_display, self.h_display), interpolation=cv2.INTER_AREA)
        height, width, channel = arr_image.shape
        self.label_show_image.setFixedWidth(width) # sua size label = size anh
        self.label_show_image.setFixedHeight(height)
        #convert tu BGR (opencv) -> hien thi chuan RGB
        img = QImage(cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB), width, height, width * 3, QImage.Format_RGB888)
        pix_map = QPixmap(img).scaled(width, height, Qt.KeepAspectRatio)
        self.label_show_image.setPixmap(pix_map)
        self.label_show_image.setScaledContents(True)
        self.label_show_image.show()

    def show_image_card(self, path_image):
        arr_image = cv2.imread(path_image)
        arr_image = cv2.resize(arr_image, (300, 200), interpolation=cv2.INTER_AREA)
        height, width, channel = arr_image.shape
        self.label_show_card.setFixedWidth(width) # sua size label = size anh
        self.label_show_card.setFixedHeight(height)
        #convert tu BGR (opencv) -> hien thi chuan RGB
        img = QImage(cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB), width, height, width * 3, QImage.Format_RGB888)
        pix_map = QPixmap(img).scaled(width, height, Qt.KeepAspectRatio)
        self.label_show_card.setPixmap(pix_map)
        self.label_show_card.setScaledContents(True)
        self.label_show_card.show()

    def mousePressEvent(self, event):
        self.pos = event.pos()
        self.pos =  self.label_show_image.mapFromParent(event.pos()) #dat goc toa do la goc label
        #self.position_in_image()
        #self.mouse_position.setText(' %d : %d ' % (self.pos.x(), self.pos.y()))
        self.get_list_point()
        #print(self.list_point)
        #self.update()
    def get_list_point(self):
        if len(self.list_image_background) !=0:
            img = cv2.imread(self.list_image_background[self.index_background])
            h, w, channel = img.shape
            if self.draw_point == 1:
                if len(self.list_point)<3:
                    if self.pos.x()>=0 and self.pos.x()<= self.w and self.pos.y() >=0 and self.pos.y()<= self.h:
                        self.list_point.append((self.pos.x(), self.pos.y()))
                        self.mouse_position.setText('Điểm %d: (%d : %d) ' % (len(self.list_point), self.pos.x(), self.pos.y()))
                        #print(self.list_point)
                    if len(self.list_point) == 3:
                        self.list_point = find_4th_point(self.list_point)
                        self.list_point = get_new_list_point(self.list_point, self.w, self.h, self.w_image, self.h_image)
                        self.mouse_position.setText('Điểm 4')
                        self.list_polygon.append(self.list_point)
                        self.paste_card_to_background()

                else:
                    self.list_point = []
                    self.list_point.append((self.pos.x(), self.pos.y()))
            if self.draw_point == 0:
                if len(self.list_point)<4:
                    if self.pos.x()>=0 and self.pos.x()<= self.w and self.pos.y() >=0 and self.pos.y()<= self.h:
                        self.list_point.append((self.pos.x(), self.pos.y()))
                        self.mouse_position.setText('Điểm %d: (%d : %d) ' % (len(self.list_point), self.pos.x(), self.pos.y()))
                        #print(self.list_point)
                    if len(self.list_point) == 4:

                        self.list_point = get_new_list_point(self.list_point, self.w, self.h, self.w_image, self.h_image)
                        self.mouse_position.setText('Điểm 4')
                        self.list_polygon.append(self.list_point)
                        self.paste_card_to_background()

                else:
                    self.list_point = []
                    self.list_point.append((self.pos.x(), self.pos.y()))
        else:
            QMessageBox.warning(self, 'Canh bao!', 'Chưa chọn file!')


def main():
   app = QApplication(sys.argv)
   ex = window()
   ex.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()



