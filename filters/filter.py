import cv2
import numpy as np

def equalizeHistRGB(src):
    RGB = cv2.split(src)
    Blue  = RGB[0]
    Green = RGB[1]
    Red   = RGB[2]

    for i in range(3):
        cv2.equalizeHist(RGB[i])
    img_hist = cv2.merge([RGB[0],RGB[1], RGB[2]])
    return img_hist

# ガウシアンノイズ
def addGaussianNoise(src):
    row,col,ch= src.shape
    mean = 0
    var = 0.1
    sigma = 15
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = src + gauss
    return noisy

# salt&pepperノイズ
def addPepperNoise(src):
    row,col,ch = src.shape
    s_vs_p = 0.5
    amount = 0.01
    out = src.copy()

    # Salt mode
    num_salt = np.ceil(amount * src.size * s_vs_p)
    coords = [np.random.randint(0, i-1 , int(num_salt))for i in src.shape]
    out[coords[:-1]] = (255,255,255)
    return out

def addSoltNoise(src):
    row,col,ch = src.shape
    s_vs_p = 0.5
    amount = 0.01
    out = src.copy()

    # Pepper mode
    num_pepper = np.ceil(amount* src.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i-1 , int(num_pepper))for i in src.shape]
    out[coords[:-1]] = (0,0,0)
    return out

def create_gamma_img(gamma, img):
    gamma_cvt = np.zeros((256,1), dtype=np.uint8)
    for i in range(256):
        gamma_cvt[i][0] = 255*(float(i)/255)**(1.0/gamma)
    return cv2.LUT(img, gamma_cvt)