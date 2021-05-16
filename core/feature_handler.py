
class FeatureHandler:
    def __init__(self):
        pass 

    def extract(self):
        raise NotImplementedError

    def match(self):
        raise NotImplementedError


class Histogram(FeatureHandler):
    def __init__(self):
        pass

    def extract(self):
        print("Extract from Histogram")

    def match(self):
        print("Match from Histogram")



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
