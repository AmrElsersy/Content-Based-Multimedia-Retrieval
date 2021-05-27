import numpy as np
import cv2
from numpy.core.fromnumeric import std
from feature_handler import FeatureHandler
import matplotlib.pyplot as plt


class KeyframeExtraction(FeatureHandler):
    def __init__(self, k1 = 1, k2 = 1.5):
        super().__init__()
        self.threshold_value = None
        self.k1 = k1
        self.k2 = k2


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

        prev_hist = cv2.calcHist([preprocessed_frames[0]], [0], mask=None, histSize=[256], ranges=[0, 256])

        for i_frame in range(1, len(preprocessed_frames)):
            hist_i = cv2.calcHist([preprocessed_frames[i_frame]], [0], mask=None, histSize=[256], ranges=[0, 256])
            diff = np.abs(hist_i - prev_hist)

            sum_of_diff = np.sum(diff)
            hist_coeffs.append(sum_of_diff)

            print(f"Sum of diff: {sum_of_diff}")
            prev_hist = hist_i

        mu_ = np.mean(hist_coeffs)
        std_ = np.std(hist_coeffs)

        print(f"mean: {mu_}, std: {std_}")
        self.threshold_value = self.k1 * mu_ + self.k2 * std_
        print(self.threshold_value)

        for i_coeff in range(len(hist_coeffs)):
            if hist_coeffs[i_coeff] > self.threshold_value:
                keyframes.append(preprocessed_frames[i_coeff])

        print(f"keyframes len: {len(keyframes)}")
        # plt.plot(hist_0, 'r')
        # plt.plot(hist_1, 'b')
        # plt.plot(diff, 'g')
        # plt.legend()
        # plt.show()
        # for frame in keyframes:
        #     cv2.imshow("WD", frame)
        #     cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def match(self):
        pass




kf = KeyframeExtraction()
video_path = '/home/ayman/FOE-Linux/Graduation_Project/Stereo-3D-Detection/results/end-to-end_demo.mp4'
video = cv2.VideoCapture(video_path)

kf.extract(video)