import cv2
import numpy as np
import random

def blend(bg, fg, x=0, y=0, opaque=0.2, gamma=0):
    """
        bg: background (color image)
        fg: foreground (color image)
        x, y: top-left point of foreground image (percentage)
    """
    h, w = bg.shape[:2]
    fg = cv2.resize(fg, (w, h))
    x_abs, y_abs = int(x*w), int(y*h)
    
    fg_h, fg_w = fg.shape[:2]
    patch = bg[y_abs:y_abs+fg_h, x_abs:x_abs+fg_w, :]
    
    blended = cv2.addWeighted(src1=patch, alpha=1-opaque, src2=fg, beta=opaque, gamma=gamma)
    result = bg.copy()
    result[y_abs:y_abs+fg_h, x_abs:x_abs+fg_w, :] = blended
    return result
def change_brightness(img, value=30):
   '''Truyen vao img, value <0: giam do sang, value >0 : tang do sang '''
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   h, s, v = cv2.split(hsv)
   v = cv2.add(v,value)
   v[v > 255] = 255
   v[v < 0] = 0
   final_hsv = cv2.merge((h, s, v))
   img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
   return img
   

def fill_poly(img, polygon, color = (255,255,255)):
    contours = np.array( polygon)
    image = cv2.fillPoly(img, pts =[contours], color=color)
    return image
def draw_poly(image,
              pts,
              is_closed=True,
              color_bgr=[255, 0, 0], 
              size=0.01, # 1%
              line_type=cv2.LINE_AA,
              is_copy=True):
    assert size > 0
    
    image = image.copy() if is_copy else image # copy/clone a new image
    
    # calculate thickness
    
    h, w = image.shape[:2]
    if size > 0:        
        short_edge = min(h, w)
        thickness = int(short_edge * size)
        thickness = 1 if thickness <= 0 else thickness
    else:
        thickness = -1
    
    # docs: https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html#gaa3c25f9fb764b6bef791bf034f6e26f5
    cv2.polylines(img=image,
                  pts=[np.int32(pts)],
                  isClosed=is_closed,
                  color=color_bgr,
                  thickness=1,
                  lineType=line_type,
                  shift=0)
    return image

def four_point_transform(img, polygon):
    h, w, chanel = img.shape
    pts = np.array([(0, 0), (w, 0), (w, h), (0, h)], dtype="float32")
    dst = np.array(polygon, dtype="float32")
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img, M, (w, h))
    warped = change_brightness(warped, random.randint(-60, -20))
    warped = cv2.blur(warped, ksize=(3, 3))
    return warped
    
def find_new_polygon(polygon, change):
    x_sort = [polygon[0][0], polygon[1][0], polygon[2][0], polygon[3][0]]
    y_sort = [polygon[0][1], polygon[1][1], polygon[2][1], polygon[3][1]]
    #print(x_sort)
    #print(y_sort)
    
    temp = x_sort.copy()
    temp.sort()
    x = temp[1]

    temp = y_sort.copy()
    temp.sort()
    y = temp[1]

    for i in range(len(x_sort)):
        if x_sort[i]<=x:
            x_sort[i] += change
        else:
            x_sort[i] -= change
    for i in range(len(y_sort)):
        if y_sort[i]<=y:
            y_sort[i] += change
        else:
            y_sort[i] -= change
    #print(y_sort)
    result = []
    for i in range(4):
        temp = (x_sort[i], y_sort[i])
        result.append(temp)
    #print(result)
    return result
def find_4th_point(polygon):
    xa = polygon[0][0]
    ya = polygon[0][1]
    xb = polygon[1][0]
    yb = polygon[1][1]
    xc = polygon[2][0]
    yc = polygon[2][1]

    xd = -(xb-xa-xc)
    yd = -(yb-ya-yc)
    d = (xd, yd)
    polygon.append(d)
    return polygon
def card_to_background(bg, card, polygon, vien = 3):
    newpolygon = find_new_polygon(polygon, vien)
    bg = fill_poly(bg, newpolygon, (0, 0, 0))
    h, w, channel = bg.shape
    card = cv2.resize(card, (w, h))
    card = four_point_transform(card, polygon)
    card = change_brightness(card, -60)
    
    return cv2.blur(cv2.add(bg, card), ksize=(3, 3))



