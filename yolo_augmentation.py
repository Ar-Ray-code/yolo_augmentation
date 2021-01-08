import filters.filter as fil

import os
import re
import sys
import cv2

from tqdm import tqdm
import argparse

# get list-----------------------------------------------------
def get_folder_list(_path,_format):
    files = []
    img_files = []

    for filename in os.listdir(_path):
        if os.path.isfile(os.path.join(_path, filename)):
            files.append(filename)

    regex = re.compile(r'('+_format+')$')
    for name in files:
        if regex.search(name):
            img_files.append(name)

    return img_files

# flip(x2)-----------------------------------------------------
def flip_img(_path,_img_files,_format,bar):
    for img_name in _img_files:
        name_only = img_name[:-4]
        img = cv2.imread(os.path.join(_path,img_name))
        
        cv2.imwrite(os.path.join(_path,name_only)+"_flip."+_format , cv2.flip(img,1))

        read_txt_file  = open(os.path.join(_path,name_only+".txt"),'r')
        write_txt_file = open(os.path.join(_path,name_only+"_flip.txt"),'w')
        
        lines = read_txt_file.readlines()
        for line in lines:
            txt_str = line.split()
            x_center = 1-float(txt_str[1])
            txt_str[1] = str(x_center)
            write_txt_file.write(' '.join(txt_str)+"\n")
            txt_str.clear()
        
        read_txt_file.close()
        write_txt_file.close()
        bar.update(1)

# add solt & paper---------------------------------------------
def soltpaper_img(_path,_img_files,_format,bar):
    for img_name in _img_files:
        name_only = img_name[:-4]
        img = cv2.imread(os.path.join(_path,img_name))

        cv2.imwrite(os.path.join(_path,name_only)+"_solt."+_format , fil.addSoltNoise(img))
        cv2.imwrite(os.path.join(_path,name_only)+"_papper."+_format, fil.addPepperNoise(img))

        read_txt_file  = open(os.path.join(_path,name_only+".txt"),'r')
        solt_write_txt_file  = open(os.path.join(_path,name_only+"_solt.txt"),'w')
        paper_write_txt_file = open(os.path.join(_path,name_only+"_papper.txt"),'w')
        
        lines = read_txt_file.readlines()
        for line in lines:
            txt_str = line.split()
            solt_write_txt_file.write(' '.join(txt_str)+"\n")
            paper_write_txt_file.write(' '.join(txt_str)+"\n")
            txt_str.clear()

        read_txt_file.close()
        solt_write_txt_file.close()
        paper_write_txt_file.close()
        bar.update(2)
        
# add solt & paper---------------------------------------------
def brightness_img(_path,_img_files,_format,bar):
    global progress_num
    for img_name in _img_files:
        name_only = img_name[:-4]
        img = cv2.imread(os.path.join(_path,img_name))

        cv2.imwrite(os.path.join(_path,name_only)+"_hist."+_format , fil.equalizeHistRGB(img))
        cv2.imwrite(os.path.join(_path,name_only)+"_bright."+_format, fil.create_gamma_img(1.4,img))
        cv2.imwrite(os.path.join(_path,name_only)+"_dark."+_format , fil.create_gamma_img(0.6,img))
        
        read_txt_file  = open(os.path.join(_path,name_only+".txt"),'r')
        hist_write_txt_file = open(os.path.join(_path,name_only+"_hist.txt"),'w')
        bright_write_txt_file = open(os.path.join(_path,name_only+"_bright.txt"),'w')
        dark_write_txt_file = open(os.path.join(_path,name_only+"_dark.txt"),'w')
        
        lines = read_txt_file.readlines()
        for line in lines:
            txt_str = line.split()
            hist_write_txt_file.write(' '.join(txt_str)+"\n")
            bright_write_txt_file.write(' '.join(txt_str)+"\n")
            dark_write_txt_file.write(' '.join(txt_str)+"\n")
            txt_str.clear()

        read_txt_file.close()
        hist_write_txt_file.close()
        bright_write_txt_file.close()
        dark_write_txt_file.close()
        bar.update(3)

if __name__=='__main__':
    description_txt = "This program is augment .txt when augment images for YOLO."

    parser = argparse.ArgumentParser(description=description_txt)
    parser.add_argument("-p","--path",default=None,help="Images folder's path.")
    parser.add_argument("-f","--format",default="jpg",help="Select target image format.(jpg, png, ..)")

    args = parser.parse_args()
    path = args.path
    img_format = args.format

    bar = tqdm(total = len(get_folder_list(path,img_format))*23)
    
    flip_img(path, get_folder_list(path,img_format),img_format,bar)
    soltpaper_img(path, get_folder_list(path,img_format),img_format,bar)
    brightness_img(path, get_folder_list(path,img_format),img_format,bar)
