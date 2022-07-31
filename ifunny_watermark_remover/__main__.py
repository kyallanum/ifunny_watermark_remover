import cv2 as cv
import os
import argparse
import logging
import pkg_resources
from ifunny_watermark_remover._version import __description__, __tool_name__, __version__

WATERMARK_PATH = pkg_resources.resource_filename(__tool_name__, "resources/watermark.jpg")
watermark = None
args = None

logger = logging.getLogger(__tool_name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"{__description__} Version: {__version__}")
    parser.add_argument('-d', '--directory', help="Directory of images", dest="img_dir", required=True)
    parser.add_argument('-o', '--output', help="Output Directory", dest="output_dir")

    return parser.parse_args()


def is_wartermarked(img: cv.Mat) -> bool:
    global watermark

    watermark_img = watermark[0:watermark.shape[0], watermark.shape[1]-142:watermark.shape[1]]
    testing_img = img[0:img.shape[0], img.shape[1]-142:img.shape[1]]

    watermark_img = cv.GaussianBlur(watermark_img, (3,3), 0)
    testing_img = cv.GaussianBlur(testing_img, (3,3), 0)

    height = watermark_img.shape[0]
    width = watermark_img.shape[1]

    delta = cv.norm(watermark_img, testing_img, cv.NORM_L2)

    similarity = 1 - delta / (height * width)

    logger.info(f"Similarity: {similarity}")

    if similarity >= .90:
        return True

    return False

def apply_grayscale(img: cv.Mat) -> cv.Mat:
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def get_watermarked_area(img: cv.Mat) -> cv.Mat:
    '''
    This is x1: x2, y1: y2. Some banners are 21 pixels. Some are 20 pixels. 
    One pixel difference isn't worth a lot of extra computation. 
    We just use this for determining whether there is a watermark or not.
    '''
    height = img.shape[0]
    width = img.shape[1]

    img = img[height-20: height, 0:width] 
    img = apply_grayscale(img)
    cv.waitKey(0)

    return img

def crop_image(img: cv.Mat) -> cv.Mat:
    return img[0:img.shape[0]-24, 0:img.shape[1]]

def main():
    global watermark, args
    args = parse_args()

    if not args.output_dir:
        args.output_dir = args.img_dir
    elif not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    out_dir = os.path.join(os.getcwd(), args.output_dir)

    logger.info(f"{__description__} version: {__version__}")
    os.chdir(args.img_dir)

    logger.info(f"Getting Watermark and applying grayscale")
    watermark = cv.imread(WATERMARK_PATH)
    watermark = apply_grayscale(watermark)

    num_cropped = 0

    logger.info("Getting images:")
    for image_file in os.listdir("."):
        logger.info(f"Processing image: {image_file}")
        img = cv.imread(image_file)
        img_watermark = get_watermarked_area(img)
        if is_wartermarked(img_watermark):
            img = crop_image(img)
            cv.imwrite(os.path.join(out_dir, image_file), img)
            logger.info("Image Cropped.")
            logger.info("----------------")
            num_cropped += 1
    
    print()
    logger.info(f"Cropping Completed: {num_cropped} files cropped.")


if __name__ == "__main__":
    main()