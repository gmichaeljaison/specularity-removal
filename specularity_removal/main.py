import cv2 as cv
import numpy as np
import logging
import os

from specularity_removal.homography import homography

RESULTS_DIR = 'results/'

DIFF_THRESHOLD = 20


def remove_specularity(img_files):
    """
    Removes highlights/specularity in Images from multiple view points

    :param img_files: File names of input images in horizontal order (important)
    """
    # read images from file names
    imgs = read_images(img_files)

    # solve each pair of image.
    # assumption: Input images are in order
    for i in range(len(imgs) - 1):
        logging.debug('processing images {} and {}'.format(i+1, i+2))
        imgs[i], imgs[i+1] = _solve(imgs[i], imgs[i + 1])

    for i, path in enumerate(img_files):
        fname = os.path.basename(path)
        res_file = os.path.join(RESULTS_DIR, fname)

        logging.info('saving the results in {}'.format(res_file))
        cv.imwrite(res_file, imgs[i])


def read_images(img_files):
    """
    Reads images from the given file locations.
    Also does basic validations like:
        - All images should be of same size

    :param img_files: Image file names
    :return: Read image objects
    """
    imgs = list()
    for fname in img_files:
        img = cv.imread(fname)
        imgs.append(img)

    # validations
    if len(imgs) > 0:
        h, w = imgs[0].shape[:2]
        logging.debug('Images are of resolution: {}x{}'.format(w, h))
        if h > 1000 or w > 1200:
            logging.warning('Image resolution is too high. It might take longer time to process. '
                            'Try reducing the resolution')
        for i in range(1, len(imgs)):
            if imgs[i].shape[0] != h or imgs[i].shape[1] != w:
                logging.error('Images are not of same size')
                raise(Exception('Sorry! This method works for same sized images only'))

    return imgs


def _solve(img1, img2):
    h, w, d = img1.shape

    # step 1: Find homography of 2 images
    homo = homography(img2, img1)

    # step 2: warp image2 to image1 frame
    img2_w = cv.warpPerspective(img2, homo, (w, h))

    # step 3: resolve highlights by picking the best pixels out of two images
    im1 = _resolve_spec(img1, img2_w)

    # step 4: repeat the same process for Image2 using warped Image1
    im_w = cv.warpPerspective(im1, np.linalg.inv(homo), (w, h))
    im2 = _resolve_spec(img2, im_w)

    return im1, im2


def _resolve_spec(im1, im2):
    im = im1.copy()

    img1 = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    img2 = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)

    # Best pixel selection criteria
    #   1. Pixel difference should be more than 20. (just an experimentally value. Free to change!)
    #   2. Best pixel should have less intensity
    #   3. pixel should not be pure black. (just an additional constraint
    #       to remove black background created by warping)
    mask = np.logical_and((img1 - img2) > DIFF_THRESHOLD, img1 > img2)
    mask = np.logical_and(mask, img2 != 0)

    im[mask] = im2[mask]
    return im
