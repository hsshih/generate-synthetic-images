# Generate Synthetic Data 

This tool is adapted from [SynDataGeneration](https://github.com/debidatta/syndata-generation) by the authors of the [Cut, Paste and Learn: Surprisingly Easy Synthesis for Instance Detection](https://arxiv.org/pdf/1708.01642.pdf). The license for the original code is included in this repository. 

Modified to allow using two separate masks per object, one mask to select the object pixels, another mask used to create the bounding box. Useful if you want to include certain objects pixels for context, but do not necessarily want to the bounding box to include the context pixels. 

## Pre-requisites 
1. OpenCV (pip install opencv-python)
2. PIL (pip install Pillow)
3. Poisson Blending (Follow instructions [here](https://github.com/yskmt/pb)
4. PyBlur (pip install pyblur, some modifications may be necessary, see PyBlur_notes.txt)
5. PyAMG (pip install pyamg)

To be able to generate scenes this code assumes you have the object masks for all images. There is no pre-requisite on what algorithm is used to generate these masks as for different applications different algorithms might end up doing a good job. 

The demo data included here uses manually annotated images using [CVAT](https://github.com/openvinotoolkit/cvat). See the [original repository](https://github.com/debidatta/syndata-generation) for other reccomendats from the [Cut, Paste and Learn](https://arxiv.org/pdf/1708.01642.pdf) paper authors. 

## Setting up Defaults
The first section in the defaults.py file contains paths to various files and libraries. Set them up accordingly.

The other defaults refer to different image generating parameters that might be varied to produce scenes with different levels of clutter, occlusion, data augmentation etc. 

## Running the Script
```
python dataset_generator2.py [-h] [--selected] [--scale] [--rotation]
                            [--num NUM] [--dontocclude] [--add_distractors]
                            root exp

Create dataset with different augmentations

positional arguments:
  root               The root directory which contains the images and annotations. Masks are assumed to have be named [ImageName].pbm
  exp                The directory where images and annotation lists will be created.

optional arguments:
  -h, --help            Show this help message and exit
  --selected            Keep only selected instances in the test dataset. Default is to keep all instances in the root directory.
  --scale               Do not scale augmentation. Default is to add scale augmentation.
  --rotation            Do not rotation augmentation. Default is to add rotation augmentation.
  --num NUM             Number of times each image will be in dataset
  --n_image NUM         Number of synthetic images to generate
  --dontocclude         Add objects without occlusion. Default is to produce occlusions
  --add_distractors     Add distractors objects. Default is to not use distractors
  --separate_annot_mask Use separate annotation masks to produce bounding boxes. 
                        Assumes name of masks to be [ImageName]_annot.pbm
```

## Training an object detector
The code produces all the files required to train an object detector. The output is in Pascal VOC format and is directly useful for Faster R-CNN but might be adapted for different object detectors too. The different files produced are:
1. __labels.txt__ - Contains the labels of the objects being trained
2. __annotations/*.xml__ - Contains annotation files in XML format which contain bounding box annotations for various scenes
3. __images/*.jpg__ - Contain image files of the synthetic scenes in JPEG format 
4. __train.txt__ - Contains list of synthetic image files and corresponding annotation files

## Helpful tools in the src directory
- preprocess_image.py - Resize input images to squares with or without padding
- mask_and_scale_image.py - Convert png outputs from CVAT to masks, resize masks and images, 
                            replace object background to prevent unnatural edges in synthesized images
- rotate_object_img_and_mask - Rotate object images and their corresponding masks
- convert_xml_to_yolo.py - convert the XML annotation files to YOLO format. 

## Demo Data

Demo data set places images of two types of controllers on random electrical cabinet backgrounds. The demo output is generated using the following command. Note that the output does not override any existing folders and images. Check to make sure that the output directory does not exist before proceeding. 

python dataset_generator2.py --n_image 10 --separate_annot_mask --dontocclude 'demo_data_dir/objects_dir' 'demo_output_dir'
