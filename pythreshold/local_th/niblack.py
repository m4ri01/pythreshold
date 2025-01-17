# -*- coding:utf-8 -*-

import numpy as np

__copyright__ = 'Copyright 2017'
__author__ = u'BSc. Manuel Aguado Martínez'


def niblack_threshold(img, w_size=15, k=-0.2):
    """ Runs the niblack's thresholding algorithm.
    
    Reference:
    Niblack, W.: ‘An introduction to digital image
    processing’ (Prentice- Hall, Englewood Cliffs, NJ, 1986), pp. 115–116

    Modifications: Using integral images to compute the local mean and
    standard deviation

    @param img: The input image
    @type img: ndarray
    @param w_size: The size of the local window to compute
        each pixel threshold. Should be and odd value
    @type w_size: int 
    @param k: Controls the value of the local threshold. Should lie in the
        interval [-0.2, -0.1]
    @type k: float
    
    @return: The estimated local threshold for each pixel
    @rtype: ndarray
    """
    # Obtaining rows and cols
    rows, cols = img.shape
    i_rows, i_cols = rows + 1, cols + 1

    # Computing integral images
    # Leaving first row and column in zero for convenience
    integ = np.zeros((i_rows, i_cols), np.float32)
    sqr_integral = np.zeros((i_rows, i_cols), np.float32)

    integ[1:, 1:] = np.cumsum(np.cumsum(img.astype(np.float32), axis=0), axis=1)
    sqr_img = np.square(img.astype(np.float32))
    sqr_integral[1:, 1:] = np.cumsum(np.cumsum(sqr_img, axis=0), axis=1)

    # Defining grid
    x, y = np.meshgrid(np.arange(1, i_cols), np.arange(1, i_rows))

    # Obtaining local coordinates
    hw_size = w_size // 2
    x1 = (x - hw_size).clip(1, cols)
    x2 = (x + hw_size).clip(1, cols)
    y1 = (y - hw_size).clip(1, rows)
    y2 = (y + hw_size).clip(1, rows)

    # Obtaining local areas size
    l_size = (y2 - y1 + 1) * (x2 - x1 + 1)

    # Computing sums
    sums = (integ[y2, x2] - integ[y2, x1 - 1] -
            integ[y1 - 1, x2] + integ[y1 - 1, x1 - 1])
    sqr_sums = (sqr_integral[y2, x2] - sqr_integral[y2, x1 - 1] -
                sqr_integral[y1 - 1, x2] + sqr_integral[y1 - 1, x1 - 1])

    # Computing local means
    means = sums / l_size

    # Computing local standard deviation
    stds = np.sqrt(sqr_sums / l_size - np.square(means))

    # Computing thresholds
    thresholds = means + k * stds

    return thresholds
