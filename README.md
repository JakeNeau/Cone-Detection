# Cone-Detection
A program which takes an image of two lines of cones as input and finds the continuous connecting line for each

## Step 1: Load Image and Single Out Correct Colored Pixels
Image loading and manipulation is handled with OpenCV. In order to single out the red pixels of the cones, the blue, green, and red color channels are thresholded on upper and lower bounds for each color. This gives six images of pixels that satisfy each threshold and these are bitwise anded together to obtain a binary image for pixels of the cones.
