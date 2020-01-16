from pdf2image import convert_from_path
import imutils
import cv2
import numpy as np

def findBottomLeftPointOrar(cnts, img):
    tmpX = img.shape[:2][1] # width
    tmpY = 0

    for cnt in cnts:
        for pnt in cnt:
            pX, pY = pnt[0]
            # print(pX, pY)
            if pX < tmpX:
                tmpX = pX
            if pY > tmpY:
                tmpY = pY
    return tmpX, tmpY

def findTopLeftPointOrar(cnts, img):
    tmpX = img.shape[:2][1] # width
    tmpY = img.shape[:2][0] # max height

    for cnt in cnts:
        for pnt in cnt:
            pX, pY = pnt[0]
            # print(pX, pY)
            if pX < tmpX:
                tmpX = pX
            if pY < tmpY:
                tmpY = pY
    return tmpX, tmpY

def findTopRightPointOrar(cnts, img):
    tmpX = 0 # width
    tmpY = img.shape[:2][0] # max height

    for cnt in cnts:
        for pnt in cnt:
            pX, pY = pnt[0]
            # print(pX, pY)
            if pX > tmpX:
                tmpX = pX
            if pY < tmpY:
                tmpY = pY
    return tmpX, tmpY

def detect(self, c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

# pages = convert_from_path('res/orarPdf.pdf', 500)
destSave = 'res/orarJpg.jpg'

# for page in pages:
#     page.save(destSave, 'JPEG')


# we start the image detection

boundaries = [([204, 204, 204], [204, 204, 204])]

img = cv2.imread(destSave)
resized = imutils.resize(img, width=1000)

(lower, upper) = boundaries[0]
lower = np.array(lower, dtype= "uint8")
upper = np.array(upper, dtype= "uint8")

mask = cv2.inRange(resized, lower, upper)
output = cv2.bitwise_and(resized, resized, mask=mask)

# show the images
cv2.imshow("output", output)

gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

cv2.imshow('edges', edges)

sharpen_kernel = np.array([[-1,-1,-1], [-1, 9, -1], [-1, -1, -1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]

kernel = np.ones((7, 7), np.uint8)  # note this is a horizontal kernel
d_im = cv2.dilate(thresh, kernel, iterations=1)
e_im = cv2.erode(d_im, kernel, iterations=1)

blank_image = np.zeros((resized.shape[:2][0], resized.shape[:2][1], 3), np.uint8)
blank_image2 = np.zeros((resized.shape[:2][0], resized.shape[:2][1], 3), np.uint8)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    if not cv2.contourArea(cnt) > 20:
        continue

    x, y, *_ = cv2.boundingRect(cnt)
    cv2.circle(blank_image, (x, y), 1, (0, 255, 0), 1) # mai bun decat draw contours
    # momentan nu mai am nevoie de textul scris in coloanele/randurile delimitatoare gri, deci nu conteaza daca iau punctele de sus/jos - in cazul asta am luat mijlocul (sau coltul stanga jos?) conturului.


structElem = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
blank_image2 = cv2.morphologyEx(blank_image, cv2.MORPH_CLOSE, structElem)

# cv2.circle(blank_image2, findBottomLeftPointOrar(contours, blank_image2), 1, (255, 0, 0), 10)
# cv2.circle(blank_image2, findTopLeftPointOrar(contours, blank_image2), 1, (255, 0, 0), 10)

# trage liniile finale
cv2.line(blank_image2, findTopLeftPointOrar(contours, blank_image2), findBottomLeftPointOrar(contours, blank_image2), (0, 255, 0), 2)
cv2.line(blank_image2, findTopLeftPointOrar(contours, blank_image2), findTopRightPointOrar(contours, blank_image2), (0, 255, 0), 2)

cv2.imshow('after morph', blank_image2)

gray = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

#--- find contours ---
contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

#--- copy of original image ---
img2 = resized.copy()

#--- select contours having a parent contour and append them to a list ---

#--- draw those contours ---
for cnt in contours:
    cv2.drawContours(img2, cnt, 0, (0,255,0), 5)

cv2.imshow('img2', img2)
cv2.waitKey()