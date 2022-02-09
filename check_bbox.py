from glob import glob
import cv2

def show_bbox_of_image(img, bbox):
    """
    :param img:
    :param bbox: [x1, y1, x2, y2]
    :return:
    """
    cv2.rectangle(img, (bbox[0], bbox[1]),
                  (bbox[2], bbox[3]), (255, 0, 0), 5)
    cv2.imshow('ff', img)
    cv2.waitKey()
def show_label_select():
    list_files_image = glob("/home/cuong-pc/Desktop/img_check/*.jpg")
    list_files_label = glob("/home/cuong-pc/Desktop/img_check/*.txt")
    list_files_image.sort()
    list_files_label.sort()
    for i in range(len(list_files_image)):
        image_file = list_files_image[i]
        label_file = list_files_label[i]
        img = cv2.imread(image_file)
        (H, W) = img.shape[:2]
        print('label_file', label_file)
        with open(label_file) as fr:
            lines = fr.readlines()
            print(lines)
            print(len(lines))
            for line in lines:
                class_id = int(float(line.split(' ')[0]))
                x = int(float(line.split(' ')[1]) * W)
                y = int(float(line.split(' ')[2]) * H)
                w = int(float(line.split(' ')[3]) * W)
                h = int(float(line.split(' ')[4]) * H)
                # x = int(float(line.split(' ')[1]))
                # y = int(float(line.split(' ')[2]))
                # w = int(float(line.split(' ')[3]))
                # h = int(float(line.split(' ')[4]))
                show_bbox_of_image(img, [x - int(w / 2), y - int(h / 2), x + int(w / 2), y + int(h / 2)])

                # crop_img = img[y - int(h / 2):y + int(h / 2), x - int(w / 2):x + int(w / 2)]
                # plt.imshow(img)
                # plt.imshow(crop_img)
                # plt.show()


if __name__ == '__main__':
    show_label_select()