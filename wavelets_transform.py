import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pywt
from pywt._doc_utils import draw_2d_wp_basis, wavedec2_keys

src = "./assets/1.png"
window_title = "test"


def wavelet_transform_2d(mat: np.ndarray, decomposition_level: int):
    # compute the 2D DWT
    c = pywt.wavedec2(mat, "db2", mode="periodization", level=decomposition_level)
    # normalize each coefficient array independently for better visibility
    c[0] /= np.abs(c[0]).max()
    for detail_level in range(decomposition_level):
        c[detail_level + 1] = [d / np.abs(d).max() for d in c[detail_level + 1]]

    # DEBUG ONLY 
    # print(f'---level{decomposition_level}---')
    # print(f'c type:{type(c)}')
    # print(f'c length: {len(c)}')
    # print(f'c[0] ndim:{c[0].ndim}')
    # print('-----into c------')
    # for i in c:
    #     print(type(i),end='')
    #     if type(i) != list:
    #         print(i.shape)
    #         continue
    #     else:
    #         print(len(i))
    #     print('\t-----into i------')
    #     for j in i:
    #         print('\t',end='')
    #         print(type(j),end='')
    #         print(j.shape)

    arr, slices = pywt.coeffs_to_array(c)
    return arr


def multilevel_wavelet_transform_demo(
    img_src: str,
):
    mat = cv.imread(img_src)
    x = cv.cvtColor(mat, cv.COLOR_BGRA2GRAY)
    shape = x.shape

    max_lev = 2  # how many levels of decomposition to draw
    label_levels = 2  # how many levels to explicitly label on the plots

    fig, axes = plt.subplots(2, max_lev + 1, figsize=[14, 8])
    for level in range(max_lev + 1):
        if level == 0:
            # show the original image before decomposition
            axes[0, 0].set_axis_off()
            axes[1, 0].imshow(x, cmap=plt.cm.gray)
            axes[1, 0].set_title("Image")
            axes[1, 0].set_axis_off()
            continue

        # plot subband boundaries of a standard DWT basis
        draw_2d_wp_basis(
            shape, wavedec2_keys(level), ax=axes[0, level], label_levels=label_levels
        )
        axes[0, level].set_title(f"{level} level\ndecomposition")

        arr = wavelet_transform_2d(x, level)
        # show the normalized coefficients
        axes[1, level].imshow(arr, cmap=plt.cm.gray)
        axes[1, level].set_title(f"Coefficients\n({level} level)")
        axes[1, level].set_axis_off()

    plt.tight_layout()
    plt.show()
    plt.savefig()


if __name__ == "__main__":
    multilevel_wavelet_transform_demo(src)
