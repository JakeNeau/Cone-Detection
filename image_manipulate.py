import cv2 as cv
import numpy as np

img = cv.imread('red.png')

# Find pixels in the color channels of the image that are above and below measured color for cones
b, g, r = cv.split(img)
ret, lowerBlue = cv.threshold(b, 5, 255, cv.THRESH_BINARY)
ret, upperBlue = cv.threshold(b, 55, 255, cv.THRESH_BINARY_INV)
ret, lowerGreen = cv.threshold(g, 5, 255, cv.THRESH_BINARY)
ret, upperGreen = cv.threshold(g, 50, 255, cv.THRESH_BINARY_INV)
ret, lowerRed = cv.threshold(r, 150, 255, cv.THRESH_BINARY)
ret, upperRed = cv.threshold(r, 235, 255, cv.THRESH_BINARY_INV)

# Bitwise_and found color thresholds together to find (mostly) only where cones are
relativeMap = cv.bitwise_and(lowerBlue, upperBlue)
relativeMap = cv.bitwise_and(lowerGreen, upperGreen, mask=relativeMap)
relativeMap = cv.bitwise_and(lowerRed, upperRed, mask=relativeMap)
resized = cv.resize(relativeMap, (relativeMap.shape[1]//4, relativeMap.shape[0]//4))

# Blur the image to reduce any noise
blur = cv.GaussianBlur(relativeMap, (5,5), 0)

# Threshold the blurred image to binarize
ret, coneMap = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)

# Finds all white pixels in the image and adds them to the correct points list
rightPointsX = []
rightPointsY = []
leftPointsX = []
leftPointsY = []
midLine = coneMap.shape[1]//2

for y in range(coneMap.shape[0]):
    for x in range(coneMap.shape[1]):
        if coneMap[y, x] == 255:
            if x < midLine:
                leftPointsX.append(x)
                leftPointsY.append(y)
            else:
                rightPointsX.append(x)
                rightPointsY.append(y)

# Find the best fit line parameters for the two sets of points
paramRight = np.polyfit(rightPointsX, rightPointsY, 1)
paramLeft = np.polyfit(leftPointsX, leftPointsY, 1)

# Draw the best fit line on the image
rightLinePoint1 = (int((-1) * paramRight[1] / paramRight[0]), 0)
rightLinePoint2 = (coneMap.shape[1], int(paramRight[0] * coneMap.shape[1] + paramRight[1]))
leftLinePoint1 = (int((-1) * paramLeft[1] / paramLeft[0]), 0)
leftLinePoint2 = (0, int(paramLeft[1]))

cv.line(img, rightLinePoint1, rightLinePoint2, (0, 0, 255), thickness=4)
cv.line(img, leftLinePoint1, leftLinePoint2, (0, 0, 255), thickness=4)

# Export final image
cv.imwrite('Answer.png', img)