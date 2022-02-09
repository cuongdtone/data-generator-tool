import os
from glob import glob
import random
import shutil
from split_folder_to_train import split_folder_to_train

train_path = ''
valid_path = ''
new_dataset = ''

new_train_path = ''
new_valid_path = ''

train_ratio = 0.8

list_train = glob(train_path + "*.jpg")
list_valid = glob(valid_path + "*.jpg")
list_new_dataset = glob(new_dataset + "*.jpg")

list_new = list_new_dataset + list_valid + list_train
random.shuffle(list_new)

new_list_train = list_new[0:int(train_ratio*len(list_new))]
new_list_valid = list_new[int(train_ratio*len(list_new)):]

for i in new_list_train:
    temp = i.split('/')
    shutil.copyfile(i, )











