# Content-Based-Multimedia-Retrieval

The project is a GUI application in which two of content-based multimedia retrieval systems are designed and implemented: 

1. Content-based image retrieval (CBIR) system 
2. Content-based video retrieval (CBVR) system


## CBIR

### Feature Extraction Algorithms:

- Mean Color
    - Getting the mean color of each channel and store it as a feature vector.

- Dominant Color
    - Applying K mean clustering with 50 iterations to get the dominant color in each channel and store them as a feature vector.

- Histogram
    - Getting the histogram of each channel and flatten those histograms into a feature vector.

### Matching Algorithms:

- Absolute Difference Mean Matching.
- Squared Difference Mean matching.
- Chi Squared Matching.

## CBVR

Threshold based keyframe extraction method is implemented.

Pipeline: 

1. Read the test video and convert the frames to grayscale.
2. Read 𝐹𝑟𝑎𝑚𝑒𝑖 and 𝐹𝑟𝑎𝑚𝑒𝑖+1
3. Find intensity histogram 𝐻𝑖𝑠𝑖 and 𝐻𝑖𝑠𝑖+1 for frames read in step 2.
4. Compute the absolute difference between 𝐻𝑖𝑠𝑖 and 𝐻𝑖𝑠𝑖+1
5. Calculate the sum of differences obtained over all the bins of histogram and store them as Histogram coefficients.
6. Find the mean 𝑥̅ and standard deviation 𝜎 of histograms coefficients obtained for all the frames.
7. Compute threshold value from mean and standard deviation values obtained in step 6 using Eq. (4): 𝑇ℎ = 𝑘1 ∗ 𝑥̅ + 𝑘2 ∗ 𝜎 (4) Where k1 and k2 are constants which are found empirically.
8. Compare the Histogram coefficient values of all the frames with the threshold value to identify most dissimilar frames as keyframes.

To this point, we extracted the key frames from the video. Next steps are to match these keyframes with database video features (matching)

9. Calculate each keyframe histogram as the feature vectors of the video 
10. Comparing the calculated features with the features of database videos (matching)
11. Thresholding the big error matching
12. Visualizing the results on the GUI


## Dependencies & Environment  

Create conda environment 

```bash
conda create -n my_env python
```

Install the dependencies

```bash
pip install -r requirements.txt
```

## Test the App

```bash
cd ui_files && python main.py 
```





