import cv2
import os
import time
 
from feature_handler import FeatureHandler
from histogram import Histogram
from average_color import AverageColor
from dominant_color import DominantColor
from matching import *


class CBIR:
    def __init__(self):
        self.database_handler = DatabaseHandler()
        
    def search(self, algo_type: str, image):
        matched_images = []

        self.feature_handler = self.__get_extractor(algo_type)
        t1 = time.time()
        image_features = self.feature_handler.extract(image)
        t2 = time.time()
        print(f"Time taken: {t2-t1}s")
        images = self.database_handler.get_images()

        for db_image in images:
            db_image_features = self.feature_handler.extract(db_image)

            loss = chi_squared_match(image_features, db_image_features)
            print(f"loss: {loss}")
            if loss < 2e4:
            # if self.feature_handler.match(image_features, db_image_features):
                matched_images.append(db_image)
            else:
                continue

        return matched_images
        

    def insert(self):
        pass

    def __get_extractor(self, algo_type):
        if algo_type == "histogram":
            return Histogram()
        
        elif algo_type == "average_color":
            return AverageColor()

        elif algo_type == "dominant_color":
            return DominantColor()
        
        else:
            raise NameError("The specified algorithm isn't implemented")



class DatabaseHandler:
    def __init__(self):
        pass

    def insert(self, image, features, algo_type):
        pass

    def get_image(self, path):
        pass

    def get_images(self):
        path = "/home/ayman/Downloads/www.google.com/flowers - Google Search - 25-05-2021 23-16-00"
        images = []
        for image in os.listdir(path):
            image = cv2.imread(os.path.join(path, image))
            images.append(image)

        return images


cbir = CBIR()
test_img = cv2.imread("/home/ayman/Downloads/www.google.com/flowers - Google Search - 25-05-2021 23-16-00/image (10).jpeg") 
matched_imgs = cbir.search("average_color" ,test_img)
time.sleep(15)
for img in matched_imgs:
    cv2.imshow("WD", img)
    cv2.waitKey(0)

cv2.destroyAllWindows()

