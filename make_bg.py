
import skimage.io
import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_ubyte
import cv2


def make_bg(img_path,bg_path):
    img = skimage.io.imread(img_path)
    cv_img = img_as_ubyte(img.copy())
    mask = img[:,:,3]

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    cv_img = cv2.bitwise_and(cv_img[:,:,:3], cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB))

    bg = skimage.io.imread(bg_path)

    bg_new = cv2.rotate(bg, 2)

    bg_new = cv2.resize(bg_new,(5472,int(np.round(1920*(5472/1080)))))


    image = cv2.copyMakeBorder(cv_img, (9728-cv_img.shape[0])//2, (9728-cv_img.shape[0])//2, 0, 0, cv2.BORDER_CONSTANT)
    mask_overlay =  cv2.copyMakeBorder(mask_rgb, (9728-cv_img.shape[0])//2, (9728-cv_img.shape[0])//2, 0, 0, cv2.BORDER_CONSTANT)


    background = bg_new
    overlay = image[:,:,:3]

    background = cv2.bitwise_and(background, (255-mask_overlay))
    added_image = cv2.addWeighted(background,1,overlay,1,3)


    added_image.shape


    final = added_image[(added_image.shape[0]-3648)//2:(added_image.shape[0]-3648)//2+3648,:,:]
    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGBA)
    return final


