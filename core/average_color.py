import numpy as np
from feature_handler import FeatureHandler
import cv2


class AverageColor(FeatureHandler):
    def __init__(self):
        super().__init__()

    def extract(self, image):
        return image.mean(axis=0).mean(axis=0)

    def match(self, features_1, features_2):
        # Mean Absolute Error
        MAE = np.mean(np.abs(features_1 - features_2))        
        print(f"Match from AverageColor {MAE}")
        return MAE


