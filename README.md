# Cone-Detection
A program which takes an image of two lines of cones as input and finds the continuous connecting line for each. Makes use of the cv2 and numpy libraries.

## Step 1: Load Image and Single Out Correct Colored Pixels
Image loading and manipulation is handled with OpenCV. In order to single out the red pixels of the cones, the blue, green, and red color channels are thresholded on upper and lower bounds for each color. This gives six images of pixels that satisfy each cooresponding threshold. These are bitwise anded together to obtain a binary image for pixels of the cones.

![relativeColorMap](https://user-images.githubusercontent.com/103858787/195229200-2403d93b-80c8-4edc-9a61-e9449dfa773b.png)

Initially a pass through a same size array of all white color values was used. Each pixel was penalized lower depending on how far away from the correct RGB value it lied. This was scrapped because array indexing for four arrays (all white and each color channel) proved to be far too slow.


## Step 2: Blur
The previous step results in artifacts. Some cones may have shaded portions which are too far away from the cone's color to be included.

![LowResCone](https://user-images.githubusercontent.com/103858787/195230192-e0c7b485-df5f-4826-ad71-6ded5b4e6242.PNG)

Noise may also be introduced due to similar-colored object in the image.

![Noise](https://user-images.githubusercontent.com/103858787/195230198-0df65263-d43d-4d99-bc8c-442a786ad4c9.PNG)

As such, a gaussian blur is applied to smooth over the cones and reduce noise in the image.

![blurred](https://user-images.githubusercontent.com/103858787/195230499-5f435e5a-6acf-4941-86bc-e3cec977d5a4.png)


## Step 3: Binarize
Applying the gaussian blur adds colors of gray to image when the algorithm depends on each pixel either being white or black. Another threshold is applied to the image to set all pixels accordingly. The exact cutoff value to get the most number of cone pixels in with no noise proved to be tedious to find.

![ConeMap](https://user-images.githubusercontent.com/103858787/195230989-95ba6de1-7a0d-455d-a16d-da6b127259fe.png)


## Step 4: Find Coordinate Variables
The image is then analyzed to find the coordinate points of each cone. Ideally, each cone would coorespond to one point on the image, but this was difficult to implement. Instead, the algorithm uses each white pixel as one coordinate point. This is sufficient, but is sub-optimal. A short delay is introduced when array indexing over the entire image and farther away cones are weighted proportionally less.


## Step 5: Sort Coordinate Variables
The coordinates must then be sorted according to if they are part of the left line or part of the right line. Initially, the algorithm would sort each point based on its expected contribution to the slope for each line. This would allow for extremely off-center lines to still be read in correctly. Instead, the algoritm sorts each coordinate depending on if it is on the right or left of the image. This is slightly faster for this implementation where each pixel cooresponds to one coordinate point, but it loses the functionality for reading off-center lines and sorting can be combines with the previous step.


## Step 6: Get Line Parameters and Draw Lines
Numpy is used to find the best fit line parameters for all coordinate variables in each list. These parameters are then used to draw a line over the source image and the answer is outputted to Answer.png in the same directory.

![Answer](https://user-images.githubusercontent.com/103858787/195233625-422b0ae0-427a-4577-ad0d-489626d00c5a.png)



