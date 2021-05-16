from .feature_handler import FeatureHandler, ColorLayout, Histogram, Texture


class CBIR:
    def __init__(self):
        self.database_handler = DatabaseHandler()
        

    def search(self, algo_type: str, image):
        matched_images = []

        self.feature_handler = self.__get_extractor(algo_type)
        image_features = self.feature_handler.extract(image)
        images = self.database_handler.get_images()

        for db_image in images:
            db_image_features = self.feature_handler.extract(db_image)
            if self.feature_handler.match(image_features, db_image_features):
                matched_images.append(db_image)
            else:
                continue

        return matched_images
        

    def insert(self):
        pass

    def __get_extractor(self, algo_type):
        if algo_type == "histogram":
            return Histogram()
        
        elif algo_type == "color_layout":
            return ColorLayout()

        elif algo_type == "texture":
            return Texture()
        
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
        pass