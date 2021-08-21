#!/usr/bin/env python
# coding: utf-8

import glob
import os
import random
from PIL import Image, ImageOps

def rotate_image_and_masks(image_file_name, rot_degree, inverted_mask=True):

    # Rotate an object image, and it's corresponding pixel mask and bounding box mask. Expands rotated image to include the entire object
    # Assumes that the masks are in the same directory, the pixel mask name is [image_name].pbm, and the annotation (bounding box) mask name is [image_name]_annot.pbm
    # Set inverted_mask=True if the masks are inverted (0 indicate the object and 1 indicate the background)
    
    pixel_mask_name = image_file_name.replace('.jpg', '.pbm')
    bndbox_mask_name = image_file_name.replace('.jpg', '_annot.pbm')
    
    # Open images
    im = Image.open(image_file_name)
    pixel_mask = Image.open(pixel_mask_name)
    bndbox_mask = Image.open(bndbox_mask_name)
    
    if inverted_mask:
        # Invert the masks so the rotation will work
        pixel_mask = ImageOps.invert(pixel_mask)
        bndbox_mask = ImageOps.invert(bndbox_mask)
    
    # Rotate images
    rot_im = im.rotate(rot_degree, resample=Image.BILINEAR, expand=1)
    rot_pixel_mask = pixel_mask.rotate(rot_degree, resample=Image.BILINEAR, expand=1)
    rot_bndbox_mask = bndbox_mask.rotate(rot_degree, resample=Image.BILINEAR, expand=1)
    
    if inverted_mask:
        # Invert the rotated mask
        rot_pixel_mask = ImageOps.invert(rot_pixel_mask)
        rot_bndbox_mask = ImageOps.invert(rot_bndbox_mask)
    
    # Get new image/mask names
    new_image_name = image_file_name.replace('.jpg', '_rot'+str(rot_degree)+'.jpg')
    new_pixel_mask_name = pixel_mask_name.replace('.pbm', '_rot'+str(rot_degree)+'.pbm')
    new_bndbox_mask_name = bndbox_mask_name.replace('_annot.pbm', '_rot'+str(rot_degree)+'_annot.pbm')
    
    # Save rotated image/mask
    rot_im.save(new_image_name)
    rot_pixel_mask.save(new_pixel_mask_name)
    rot_bndbox_mask.save(new_bndbox_mask_name)
