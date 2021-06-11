import cv2
import os
import time
import sys

from numpy.lib.histograms import histogram

sys.path.insert(1, 'C:/Users/Dina/Desktop/Content-Based-Multimedia-Retrieval')

from feature_handler import FeatureHandler
from histogram import Histogram
from mean_color import MeanColor
from dominant_color import DominantColor
from matching_fns import *
from database.database import DataBase


class CBIR:
    def __init__(self, matching_thresh=400):
        self.database_handler = DataBase()
        self.matching_threshold = matching_thresh
        self.algo_index = {
            "histogram": 1,
            "dominant_color": 2,
            "mean_color": 3
            }

    def search(self, algo_type: str, image, matching_fn: str):
        matched_images = {}

        self.feature_handler = self.__get_extractor(algo_type)

        image_features = self.feature_handler.extract(image)
        # print(f"Features: {image_features}, Shape: {image_features.shape}")
        db_query_images = self.database_handler.get_images()
        # print(db_query_images)

        for element in db_query_images:
            # hist, domin, aver
            db_img_feature = element[ self.algo_index[algo_type] ] 
            loss = self.__get_matching_loss(matching_fn, image_features, db_img_feature) 
            print(f"Loss: {loss}")
            if loss < self.matching_threshold:
                # if self.feature_handler.match(image_features, db_image_features):
                matched_images[str(element[0])] = loss
            
        
        return dict(sorted(matched_images.items(), key=lambda item: item[1]))
        

    def insert(self, img_path):
        img = cv2.imread(img_path)

        hist = Histogram()
        mean_clr = MeanColor()
        domin_clr = DominantColor()

        self.database_handler.insert_into_table(img_path, hist.extract(img), "histogram")
        self.database_handler.insert_into_table(img_path, mean_clr.extract(img), "average_color")
        self.database_handler.insert_into_table(img_path, domin_clr.extract(img), "dominant_color")



    def __get_extractor(self, algo_type):
        if algo_type == "histogram":
            self.matching_threshold = 50
            return Histogram()

        
        elif algo_type == "mean_color":
            self.matching_threshold = 40
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


cbir = CBIR()

test_img = cv2.imread("/home/ayman/Downloads/www.google.com/flowers - Google Search - 25-05-2021 23-16-00/image (26).jpeg") 
matched_imgs = cbir.search(algo_type="mean_color", image=test_img, matching_fn="mean_abs_match")
# print(matched_imgs)

for img in matched_imgs.keys():
    print(f"{img} - loss: {matched_imgs[img]}")
    img = cv2.imread(img)
    cv2.imshow("WD", img)
    cv2.waitKey(0)
cv2.destroyAllWindows()

imgs_path1 = '/home/ayman/Downloads/www.google.com/cars - Google Search - 26-05-2021 00-17-42'
imgs_path2 = '/home/ayman/Downloads/www.google.com/flowers - Google Search - 25-05-2021 23-16-00'


# for img_path in os.listdir(imgs_path1):
#     print(f"1: {img_path}")
#     cbir.insert(os.path.join(imgs_path1, img_path))

# for img_path in os.listdir(imgs_path2):
#     print(f"2: {img_path}")
#     cbir.insert(os.path.join(imgs_path2, img_path))

