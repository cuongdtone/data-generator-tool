import cv2
import numpy as np
from image_process import draw_poly
def get_new_list_point(polygon, w_dis, h_dis, w_img, h_img):
    ratio_w = w_img/w_dis
    ratio_h = h_img/h_dis
    x = (np.array([polygon[0][0], polygon[1][0], polygon[2][0], polygon[3][0]])*ratio_h).astype(int)
    y = (np.array([polygon[0][1], polygon[1][1], polygon[2][1], polygon[3][1]])*ratio_w).astype(int)
    return [(x[0], y[0]), (x[1], y[1]), (x[2], y[2]), (x[3], y[3])]
    

def get_data_yolo(w, h, polygon, c):
    x = [polygon[0][0], polygon[1][0], polygon[2][0], polygon[3][0]]
    y = [polygon[0][1], polygon[1][1], polygon[2][1], polygon[3][1]]

    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)

    width = (x_max-x_min)
    height = (y_max-y_min)
    x_center = (x_min + width/2)/w
    y_center = (y_min + height/2)/h
    width = width/w
    height = height/h

    x_topleft = x[0]/w
    y_topleft = y[0]/h

    x_topright = x[1]/w
    y_topright = y[1]/h

    x_bottomright = x[2]/w
    y_bottomright = y[2]/h

    x_bottomleft = x[3]/w
    y_bottomleft = y[3]/h

    card =          '%d %f %f %f %f' %(c, x_center, y_center, width, height)

    w_angle = max(width, height)/4
    h_angle = w_angle * w / h
    top_left =      '1 %f %f %f %f'  %(x_topleft, y_topleft, w_angle, h_angle)
    top_right =     '2 %f %f %f %f'  %(x_topright, y_topright, w_angle, h_angle)
    bottom_right =  '3 %f %f %f %f'  %(x_bottomright, y_bottomright, w_angle, h_angle)
    bottom_left =   '4 %f %f %f %f'  %(x_bottomleft, y_bottomleft, w_angle, h_angle)
    str = card + '\n' + top_left + '\n' + top_right + '\n' + bottom_right + '\n' + bottom_left
    return str

def get_box(str, img):
    point = str.split(' ')
    for i in range(len(point)):
        point[i] = float(point[i])
    h, w, c = img.shape
    #print(point)

    x_center = point[1]
    y_center = point[2]
    width = point[3]
    height = point[4]

    x_point_1 = int((x_center - width/2)*w)
    y_point_1 = int((y_center - height/2)*h)
    point1 = (x_point_1, y_point_1)

    x_point_2 = int((x_center + width/2)*w)
    point2 = (x_point_2, y_point_1)

    y_point_3 = int((y_center + height/2)*h)
    point4 = (x_point_1, y_point_3)

    point3 = (x_point_2, y_point_3)

    r = [point1, point2, point3, point4]
    #print(r)
    #img_bbox = draw_poly(img, r, size=0.005, color_bgr=[0, 0, 255])
    return r
'''
img = cv2.imread('/home/cuong/Desktop/tool_ghep_card/img/Nguoideothe_12.jpeg')
str = '0 0.25 0.25 0.25 0.25'
img = get_box(str, img)
cv2.imshow('gg', img)
cv2.waitKey()
'''

