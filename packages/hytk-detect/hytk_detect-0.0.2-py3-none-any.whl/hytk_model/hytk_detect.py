import numpy as np
from PIL import Image
import requests
from io import BytesIO

class HytkDetect(object):
    def __init__(self,w,h,thred):
        self.w = w
        self.h = h
        self.gray_thred = thred

    def checkGray(self,r, g, b):
        # chip_gray = cv2.cvtColor(chip,cv2.COLOR_BGR2GRAY)
        # r, g, b = cv.split(chip)
        r = np.array(r.getdata()).astype(np.float32)
        g = np.array(g.getdata()).astype(np.float32)
        b = np.array(b.getdata()).astype(np.float32)
        # s_w, s_h = r.shape[:2]
        x = (r + b + g) / 3

        # area_s = s_w * s_h
        area_s = len(r)
        # x = chip_gray
        r_gray = abs(r - x)
        g_gray = abs(g - x)
        b_gray = abs(b - x)
        r_sum = np.sum(r_gray) / area_s
        g_sum = np.sum(g_gray) / area_s
        b_sum = np.sum(b_gray) / area_s
        gray_degree = (r_sum + g_sum + b_sum) / 3
        if gray_degree < self.gray_thred:
            return True, gray_degree
        else:
            return False, gray_degree

    def detect(self,img, type):
        if type == 'local':
            img = Image.open(img)
            img = img.resize((self.w, self.h))
        if type == 'url':
            if img.find("png")>0:
                resp = requests.get(img, timeout=10)
                img = Image.open(BytesIO(resp.content))
                img = img.resize((self.w, self.h))
            else:
                score=0
                gray = 1000
                return score, gray
        try:
            r, g, b, a = img.split()
            if_gray, gray = self.checkGray(r, g, b)
            # print(gray)
            if if_gray:
                img_array = a.getdata()
                # img_array = [round(i / 255, 2) for i in np.array(img_array)]
                img_array = np.array(img_array)
                score = round(img_array.mean(), 2)
            else:
                score = -1
        except:
            score = 0
            gray = 1000
        return score, gray





















