import numpy as np
import cv2

class FeatureHandler:
    def __init__(self):
        self.matching_threshold = 0.5

    def extract(self, *args, **kwargs):
        raise NotImplementedError

    def match(self, *args, **kwargs):
        raise NotImplementedError


class Histogram(FeatureHandler):
    def __init__(self):
        super().__init__()

    def extract(self, image):
        mu = np.mean(image.ravel())
        return mu

    def match(self, features_1, features_2):
        diff = features_1 - features_2
        if diff < self.matching_threshold:
            return True
        else:
            return False


class Texture(FeatureHandler):
    def __init__(self):
        pass

    def extract(self):
        print("Extract from Texture")

    def match(self):
        print("Match from Texture")

class ColorLayout(FeatureHandler):
    def __init__(self):
        pass

    def extract(self):
        print("Extract from ColorLayout")

    def match(self):
        print("Match from ColorLayout")
