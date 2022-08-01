# iFunny Watermark Remover
This simple python application removes watermarks from images downloaded from iFunny. 

### How it works
This simple application uses opencv to read images, and then compare them to a sample watermark image. If they are similar enough, then it will crop out the watermark to remove it.

### Supports
- **(Windows 10)**

I have not yet tested support on any other operating systems.

### Installation
To install this app, you can download this repository and then install it with pip by running the following command while in the project directory:
```shell
python -m pip install .
```

### Usage
Here is the full usage for the program:
```shell
usage: ifunny_watermark_remover [-h] [-d IMG_DIR] [-o OUTPUT_DIR]

iFunny Watermark Remover Version: 1.0.0

options:
  -h, --help            show this help message and exit
  -d IMG_DIR, --directory IMG_DIR
                        Directory of images
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        Output Directory
```
NOTE:  
- If no image directory is provided then it will use the current directory.  
- If no output directory is provided then it will overwrite each image.
