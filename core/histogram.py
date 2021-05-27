import numpy as np
import cv2
from feature_handler import FeatureHandler


class Histogram(FeatureHandler):
    def __init__(self, hist_size = [8, 8, 8]):
        super().__init__()
        self.hist_size = hist_size

    def extract(self, image):
        hist = cv2.calcHist([image], [0, 1, 2], mask=None, histSize=self.hist_size, ranges=[0, 256, 0, 256, 0, 256])
        hist = hist.flatten()
        return hist

    # def match(self, features_1, features_2):
    #     # Mean Absolute Error
    #     MAE = np.mean(np.abs(features_1 - features_2))        
    #     print(f"Match from Histogram {MAE}")
    #     return MAE
