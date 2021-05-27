import cv2
import os
import time
 
from feature_handler import FeatureHandler
from histogram import Histogram
from mean_color import MeanColor
from dominant_color import DominantColor
from matching_fns import *


class CBIR:
    def __init__(self, matching_thresh=100):
        self.database_handler = DatabaseHandler()
        self.matching_threshold = matching_thresh

    def search(self, algo_type: str, image, matching_fn: str):
        matched_images = {}

        self.feature_handler = self.__get_extractor(algo_type)

        image_features = self.feature_handler.extract(image)
        # print(f"Features: {image_features}, Shape: {image_features.shape}")
        images = self.database_handler.get_images()

        for db_image in images:
            db_image_features = self.feature_handler.extract(db_image)
            loss = self.__get_matching_loss(matching_fn, image_features, db_image_features)

            if loss < self.matching_threshold:
            # if self.feature_handler.match(image_features, db_image_features):
                matched_images[str(db_image)] = loss
            else:
                continue

        return matched_images
        

    def insert(self):
        pass

    def __get_extractor(self, algo_type):
        if algo_type == "histogram":
            return Histogram()
        
        elif algo_type == "mean_color":
            return MeanColor()

        elif algo_type == "dominant_color":
            return DominantColor()

        else:
            raise NameError("The specified algorithm isn't implemented")


    def __get_matching_loss(self, matching_fn, feature1, feature2):
        if matching_fn == "mean_square_match":
            return mean_square_match(feature1, feature2)
        
        elif matching_fn == "mean_abs_match":
            return mean_abs_match(feature1, feature2)

        elif matching_fn == "absolute_diff_match":
            return absolute_diff_match(feature1, feature2)

        elif matching_fn == "spatial_cosine_match":
            return spatial_cosine_match(feature1, feature2)
        
        elif matching_fn == "chi_squared_match":
            return chi_squared_match(feature1, feature2)

        elif matching_fn == "d2_norm_match":
            return d2_norm_match(feature1, feature2)

        else:
            raise NameError("The specified matching_fn isn't implemented")



class DatabaseHandler:
    def __init__(self):
        pass

    def insert(self, image, features, algo_type):
        pass

    def get_image(self, path):
        pass

    def get_images(self):
        path = "/home/ayman/Downloads/www.google.com/cars - Google Search - 26-05-2021 00-17-42"
        images = []
        for image in os.listdir(path):
            image = cv2.imread(os.path.join(path, image))
            images.append(image)

        return images


cbir = CBIR()
test_img = cv2.imread("/home/ayman/Downloads/www.google.com/cars - Google Search - 26-05-2021 00-17-42/image (3).jpeg") 
matched_imgs = cbir.search(algo_type="mean_color", image=test_img, matching_fn="mean_square_match")

for img in matched_imgs.keys():
    print(f"{img} - loss{matched_imgs[img]}")
    #     cv2.imshow("WD", img)
    #     cv2.waitKey(0)

cv2.destroyAllWindows()

