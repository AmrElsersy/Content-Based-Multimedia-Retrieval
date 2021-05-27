import numpy as np
import numpy.linalg as linalg
import scipy.spatial as spatial


def mean_square_match(feature1, feature2):
    return np.mean(abs(feature2-feature1)**2)

def mean_abs_match(feature1, feature2):
    return np.mean(abs(feature2-feature1))

def absolute_diff_match(feature1, feature2):
    return np.sum(abs(feature2-feature1))

def spatial_cosine_match(feature1, feature2):
    # ref https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
    return np.dot(feature1, feature2)/ (linalg.norm(feature1) * linalg.norm(feature2))

def spatial_cosine_match2(feature1, feature2):
    return spatial.distance.cosine(feature1, feature2)

def chi_squared_match(feature1, feature2):
    # ref https://stats.stackexchange.com/questions/184101/comparing-two-histograms-using-chi-square-distance
    return 0.5 * np.sum(
        abs(feature2 - feature1) ** 2 / (feature1 + feature2 + 1e-8)
    )
    
def d2_norm_match(feature1, feature2):
    return 2 - 2 * np.dot(feature1, feature2)

