from pdf2image import convert_from_path
import imutils
import cv2
import numpy as np

def detect(self, c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

pages = convert_from_path('res/orarPdf.pdf', 500)
destSave = 'res/orarJpg.jpg'

for page in pages:
    page.save(destSave, 'JPEG')


# we start the image detection

boundaries = [([190, 190, 190], [210, 210, 210])]

img = cv2.imread(destSave)
resized = imutils.resize(img, width=1000)

(lower, upper) = boundaries[0]
lower = np.array(lower, dtype= "uint8")
upper = np.array(upper, dtype= "uint8")

mask = cv2.inRange(resized, lower, upper)
output = cv2.bitwise_and(resized, resized, mask= mask)

# show the images
cv2.imshow("output", output)

gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)

sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]

kernel = np.ones((7, 7), np.uint8)  # note this is a horizontal kernel
d_im = cv2.dilate(thresh, kernel, iterations=1)
e_im = cv2.erode(d_im, kernel, iterations=1)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    if not cv2.contourArea(cnt) > 500:
        continue
    
    cv2.drawContours(output, [cnt], 0, (0,255,0), 3)

    cv2.imshow('out + contours', output)
    if cv2.waitKey() == 'q':
        break




# thresh = cv2.threshold(sharpen,160,255, cv2.THRESH_BINARY_INV)[1]
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# min_area = 100
# max_area = 1500
# image_number = 0
# for c in cnts:
#     area = cv2.contourArea(c)
#     if area > min_area and area < max_area:
#         x,y,w,h = cv2.boundingRect(c)
#         ROI = resized[y:y+h, x:x+h]
#         cv2.rectangle(resized, (x, y), (x + w, y + h), (36,255,12), 2)
#         image_number += 1

# cv2.imshow('sharpen', sharpen)
# cv2.imshow('close', close)
# cv2.imshow('thresh', thresh)
# cv2.imshow('image', resized)
# cv2.waitKey()