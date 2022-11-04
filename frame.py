import cv2
import numpy as np

white = np.zeros((480, 640, 3))
white += 255
cv2.imwrite('white.png',white)

I1 = cv2.imread('s1.png', cv2.IMREAD_GRAYSCALE)
I2 = cv2.imread('s3.png', cv2.IMREAD_GRAYSCALE)
I3 = cv2.imread('s5.png', cv2.IMREAD_GRAYSCALE)
W = cv2.imread('white.png', cv2.IMREAD_GRAYSCALE)

img_diff1 = cv2.absdiff(I2,I1)
img_diff2 = cv2.absdiff(I3,I2)

Im = cv2.bitwise_and(img_diff1, img_diff2)

img_th = cv2.threshold(Im, 60, 255,cv2.THRESH_BINARY)[1]

operator = np.ones((3,3), np.uint8)
img_dilate = cv2.dilate(img_th, operator, iterations=4)
img_mask = cv2.erode(img_dilate,operator,iterations=4)

img_dst = cv2.bitwise_and(W, img_mask)

kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(img_dst, cv2.MORPH_OPEN, kernel)

ret,thresh1 = cv2.threshold(opening,127,255,cv2.THRESH_BINARY)

contours=cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[0]

area_thresh = 50
contours = list(filter(lambda x: cv2.contourArea(x) > area_thresh, contours))

for cnt in contours:
    _x,_y,width,height=cv2.boundingRect(cnt)
    cv2.rectangle((opening),(_x,_y),(_x+width,_y+height),color=(255,255,255),thickness=2)


cv2.imshow("Show BACKGROUND SUBSTRACTION image",opening)
cv2.waitKey(0)
cv2.destroyAllWindows()