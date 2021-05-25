

class FeatureHandler:
    def __init__(self):
        self.matching_threshold = 100

    def extract(self, *args, **kwargs):
        raise NotImplementedError

    def match(self, *args, **kwargs):
        raise NotImplementedError

