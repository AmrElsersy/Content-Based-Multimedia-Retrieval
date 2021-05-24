import numpy as np
from feature_handler import FeatureHandler
import cv2


class DominantColor(FeatureHandler):
    def __init__(self, n_color_clusters = 6, n_max_iter = 50, eps = 0.1, init_attempts = 10):
        super().__init__()
        self.n_color_clusters = n_color_clusters
        self.n_max_iter = n_max_iter
        self.eps = eps
        self.init_attempts = init_attempts

    def extract(self, image):
        pixels = np.float32(image.reshape(-1,3))

        termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, self.n_max_iter, self.eps)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, self.n_color_clusters, None, \
            termination_criteria, self.init_attempts, flags)

        _, counts = np.unique(labels, return_counts=True)

        return palette[np.argmax(counts)]

    def match(self, features_1, features_2):
        # Mean Absolute Error
        MAE = np.mean(np.abs(features_1 - features_2))        
        print(f"Match from  dominant_color {MAE}")
        return MAE


