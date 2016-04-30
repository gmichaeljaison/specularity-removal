import cv2 as cv
import numpy as np
import logging

# FLANN - Fast Library for Approximate Nearest Neighbors
FLANN_INDEX_KDTREE = 0
SCH_PARAM_CHECKS = 50
INDEX_PARAM_TREES = 5

GOOD_MATCH_THRESHOLD = 0.6
MIN_MATCH_COUNT = 20


def homography(img1, img2, visualize=False):
    """
    Finds Homography matrix from Image1 to Image2.
        Two images should be a plane and can change in viewpoint

    :param img1: Source image
    :param img2: Target image
    :param visualize: Flag to visualize the matched pixels and Homography warping
    :return: Homography matrix. (or) Homography matrix, Visualization image - if visualize is True
    """
    sift = cv.xfeatures2d.SIFT_create()
    kp1, desc1 = sift.detectAndCompute(img1, None)
    kp2, desc2 = sift.detectAndCompute(img2, None)

    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=INDEX_PARAM_TREES)
    # number of times the trees in the index should be recursively traversed
    # Higher values gives better precision, but also takes more time
    sch_params = dict(checks=SCH_PARAM_CHECKS)
    flann = cv.FlannBasedMatcher(index_params, sch_params)

    matches = flann.knnMatch(desc1, desc2, k=2)
    logging.debug('{} matches found'.format(len(matches)))

    # select good matches
    matches_arr = []
    good_matches = []
    for m, n in matches:
        if m.distance < GOOD_MATCH_THRESHOLD * n.distance:
            good_matches.append(m)
        matches_arr.append(m)

    if len(good_matches) < MIN_MATCH_COUNT:
        raise (Exception('Not enough matches found'))
    else:
        logging.debug('{} of {} are good matches'.format(len(good_matches), len(matches)))

    src_pts = [kp1[m.queryIdx].pt for m in good_matches]
    src_pts = np.array(src_pts, dtype=np.float32).reshape((-1, 1, 2))
    dst_pts = [kp2[m.trainIdx].pt for m in good_matches]
    dst_pts = np.array(dst_pts, dtype=np.float32).reshape((-1, 1, 2))

    homo, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5)

    if visualize:
        res = visualize_homo(img1, img2, kp1, kp2, matches, homo, mask)
        return homo, res

    return homo


def visualize_homo(img1, img2, kp1, kp2, matches, homo, mask):
    h, w, d = img1.shape
    pts = [[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]
    pts = np.array(pts, dtype=np.float32).reshape((-1, 1, 2))
    dst = cv.perspectiveTransform(pts, homo)

    img2 = cv.polylines(img2, [np.int32(dst)], True, [255, 0, 0], 3, 8)

    matches_mask = mask.ravel().tolist()
    draw_params = dict(matchesMask=matches_mask,
                       singlePointColor=None,
                       matchColor=(0, 255, 0),
                       flags=2)
    res = cv.drawMatches(img1, kp1, img2, kp2, matches, None, **draw_params)
    return res
