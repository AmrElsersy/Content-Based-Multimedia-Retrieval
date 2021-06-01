from typing import Dict
import numpy as np
import cv2
from numpy.core.fromnumeric import std
from feature_handler import FeatureHandler
import matplotlib.pyplot as plt
from matching_fns import *


class KeyframeExtraction(FeatureHandler):
    def __init__(self, k1 = 1, k2 = 1.5, matching_threshold=500):
        super().__init__()
        self.threshold_value = None
        self.k1 = k1
        self.k2 = k2
        self.matching_thresh = matching_threshold
        self.max_keyframes = 20


    def __preprocess_video(self, video):
        frames = []

        success, image = video.read()
        count = 0
        while success:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            frames.append(image)
            success,image = video.read()
            count += 1

        return frames

    def extract(self, video):
        preprocessed_frames =  self.__preprocess_video(video)
        hist_coeffs = []
        keyframes = []
        video_features = []
        keyframes_vs_diff = {} 

        prev_hist = cv2.calcHist([preprocessed_frames[0]], [0], mask=None, histSize=[256], ranges=[0, 256])

        for i_frame in range(1, len(preprocessed_frames)):
            hist_i = cv2.calcHist([preprocessed_frames[i_frame]], [0], mask=None, histSize=[256], ranges=[0, 256])
            diff = np.abs(hist_i - prev_hist)

            sum_of_diff = np.sum(diff)
            hist_coeffs.append(sum_of_diff)

            # print(f"Sum of diff: {sum_of_diff}")
            prev_hist = hist_i

        mu_ = np.mean(hist_coeffs)
        std_ = np.std(hist_coeffs)

        # print(f"mean: {mu_}, std: {std_}")
        self.threshold_value = self.k1 * mu_ + self.k2 * std_

        for i_coeff in range(len(hist_coeffs)):
            if hist_coeffs[i_coeff] > self.threshold_value:
                keyframes.append(preprocessed_frames[i_coeff])
                keyframes_vs_diff[i_coeff] = hist_coeffs[i_coeff]

        # print(f"keyframes len: {len(keyframes)}")
        # plt.plot(hist_0, 'r')
        # plt.plot(hist_1, 'b')
        # plt.plot(diff, 'g')
        # plt.legend()
        # plt.show()
        # for frame in keyframes:
        #     cv2.imshow("WD", frame)
        #     cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if len(keyframes) > self.max_keyframes:
            keyframes_truncated = []
            keyframes_vs_diff = dict(sorted(keyframes_vs_diff.items(), key=lambda item: item[1], reverse=True))

            i = 0
            for key in keyframes_vs_diff.keys():
                if i == self.max_keyframes:
                    break
                keyframes_truncated.append(preprocessed_frames[key])
                # print(keyframes_vs_diff[key], key)
                i += 1

            keyframes = keyframes_truncated

        for frame in keyframes:
            hist = cv2.calcHist([frame], [0], mask=None, histSize=[256], ranges=[0, 256])
            hist = hist.flatten()
            video_features.append(hist)

        return np.array(video_features)
    
    def match(self, features1, features2):
    
        features1 = np.array(features1)
        features2 = np.array(features2)
        print(f"No. of KeyFrames in Feature1: {features1.shape[0]}")
        print(f"No. of KeyFrames in Feature2: {features2.shape[0]}")

        num_of_matches = 0
        is_matched = False
        for feat_1 in range((features1.shape[0])):
            for feat_2 in range((features2.shape[0])):
                hist_diff = np.mean(np.abs(features1[feat_1] - features2[feat_2]))
                print(hist_diff)
                if hist_diff < self.matching_thresh:
                    # num_of_matches += 1
                    is_matched = True

            if is_matched:
                num_of_matches += 1
                is_matched = False

        print(f"num_of_matches: {num_of_matches}")
        # matching_percent = num_of_matches / (features1.shape[0] * features2.shape[0])
        matching_percent = num_of_matches / (features1.shape[0])
        print(f"Matching Percentage: {matching_percent*100}%")
        return matching_percent


# kf = KeyframeExtraction()
# video_path = '/home/ayman/FOE-Linux/Graduation_Project/Stereo-3D-Detection/results/end-to-end_demo.mp4'
# video = cv2.VideoCapture(video_path)

# feat_1 = kf.extract(video)
# feat_2 = kf.extract(cv2.VideoCapture('/home/ayman/FOE-Linux/Graduation_Project/Stereo-3D-Detection/demo_video_test.mp4'))
# kf.match(feat_1, feat_2)

