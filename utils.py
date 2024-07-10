import cv2 as cv
import numpy as np

def load_img(img_src, grayscale: bool = True) -> np.ndarray:
    if grayscale:
        mat = cv.imread(img_src, cv.IMREAD_GRAYSCALE)
    else:
        mat = cv.imread(img_src, cv.IMREAD_COLOR)

    # resize image if it's too big
    threshold = 400
    w,h = mat.shape
    if w >= threshold or h >= threshold:
        mat = cv.resize(mat, (int(threshold), int(threshold*h/w)))
    return mat
