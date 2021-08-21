#!/usr/bin/env python
# coding: utf-8

import glob
import os
import shutil
import random
import numpy as np
from PIL import Image, ImageOps


def pad_to_square(image_dir, resize=None, in_image_type = 'jpg', out_image_type = 'jpg'):
     # Pad images to make square, resize image if the resize keyword is defined
    os.chdir(image_dir)
    images = glob.glob('*.'+in_image_type)

    for image in images:
        old_im = Image.open(image)
        old_im = ImageOps.exif_transpose(old_im)
        old_size = old_im.size

        new_size = (max(old_im.size), max(old_im.size))
        new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
        new_im.paste(old_im, ((new_size[0]-old_size[0])//2,
                              (new_size[1]-old_size[1])//2))
        
        if resize:
            new_im = new_im.resize((resize,resize))

        #new_im.show()
        im_root_name = image.split('.')
        new_im.save('sq_' + im_root_name[0] + '.'+out_image_type)


def resize_to_square(image_dir, resize=640, in_image_type = 'jpg', out_image_type = 'jpg', output_dir=''):
    # Resize images to square (without padding)
    os.chdir(image_dir)
    images = glob.glob('*.'+in_image_type)

    for image in images:
        im = Image.open(image)
        im = ImageOps.exif_transpose(im)
        im = im.resize((resize,resize))

        im_root_name = image.split('.')
        im.save(output_dir+'re_' + im_root_name[0] + '.'+out_image_type)



def split_train_test(data_dir,train_frac=0.8):
    # Take the images and labels in one directory and split them into train and test sets
    os.chdir(data_dir)
    image_names = glob.glob('*.jpg')
    
    root_names = [name.split('.')[0] for name in image_names]

    n_images = len(root_names)
        
    all_idx = set(range(0, n_images))
    train_idx = set(random.sample(range(0, n_images), round(n_images*0.8)))
    test_idx = all_idx.difference(train_idx)

    train_names = [root_names[i] for i in train_idx]
    test_names = [root_names[i] for i in test_idx]
    
    os.mkdir('train')
    os.mkdir('test')
    
    os.mkdir('train/images')
    os.mkdir('train/labels')
    os.mkdir('test/images')
    os.mkdir('test/labels')
    
    for name in train_names:
        shutil.move(name + '.jpg', 'train/images/' + name + '.jpg')
        shutil.move(name + '.txt', 'train/labels/' + name + '.txt')
        
    for name in test_names:
        shutil.move(name + '.jpg', 'test/images/' + name + '.jpg')
        shutil.move(name + '.txt', 'test/labels/' + name + '.txt')



def rename_images(data_dir,image_root_name='image',start_image_num=0, in_image_type = 'jpg', out_image_type = 'jpg'):
    # Rename images in the given directory using a given image_root_name + image_num
    
    os.chdir(data_dir)
    image_names = glob.glob('*.'+in_image_type)
    n_images = len(image_names)
    
    i = 0
    
    for name in image_names:
        os.rename(name,image_root_name+'_'+str(i+start_image_num)+'.'+out_image_type)
        i+=1
