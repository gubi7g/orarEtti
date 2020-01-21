from pdf2image import convert_from_path
import imutils
import cv2
import numpy as np
import os


def getCoordinatedFromCropped(original, cropped, pointsx, pointsy):
    kx = round(original.shape[:2][1] / cropped.shape[:2][1])
    ky = round(original.shape[:2][0] / cropped.shape[:2][0])

    new_pointsx = [kx * p for p in pointsx]
    new_pointsy = [ky * p for p in pointsy]

    return (min(new_pointsx), min(new_pointsy)), (max(new_pointsx), max(new_pointsy)) # (x, y), (x+w, y+h)


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


destSave = 'res/orarJpg.jpg'

if not os.path.isfile(destSave):
    pages = convert_from_path('res/orarPdf.pdf', 500)
    for page in pages:
        page.save(destSave, 'JPEG')


# we start the image detection

boundaries = [([204, 204, 204], [204, 204, 204])]

img = cv2.imread(destSave)
resized = img.copy()
final_orar = img.copy()
resized = imutils.resize(img, width=1500)

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

    # not necessary:

    x, y, *_ = cv2.boundingRect(cnt)
    cv2.circle(blank_image, (x, y), 1, (0, 255, 0), 1) # mai bun decat draw contours
    # momentan nu mai am nevoie de textul scris in coloanele/randurile delimitatoare gri, deci nu conteaza daca iau punctele de sus/jos - in cazul asta am luat mijlocul (sau coltul stanga jos?) conturului.


structElem = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
blank_image2 = cv2.morphologyEx(blank_image, cv2.MORPH_CLOSE, structElem)

# cv2.circle(blank_image2, findBottomLeftPointOrar(contours, blank_image2), 1, (255, 0, 0), 10)
# cv2.circle(blank_image2, findTopLeftPointOrar(contours, blank_image2), 1, (255, 0, 0), 10)

# trage liniile finale
cv2.line(blank_image2, findTopLeftPointOrar(contours, blank_image2), findBottomLeftPointOrar(contours, blank_image2), (0, 255, 0), 1)
cv2.line(blank_image2, findTopLeftPointOrar(contours, blank_image2), findTopRightPointOrar(contours, blank_image2), (0, 255, 0), 1)

cv2.imshow('after morph', blank_image2)

gray = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)


contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

for ind, cnt in enumerate(contours):
    
    if cv2.contourArea(cnt) < 20000 or cv2.contourArea(cnt) > 50000:
        print('not included: ', cv2.contourArea(cnt))
        continue

    name = 'cel' + str(ind+1) + '.jpg'
    folder = 'zileExtraseOrar'
    print(name)

    print(cv2.contourArea(cnt))
    x, y, w, h = cv2.boundingRect(cnt)
    tmp = getCoordinatedFromCropped(final_orar, resized, [x, x+w], [y, y+h])
    cv2.rectangle(final_orar, tmp[0], tmp[1], (255, 0, 0))
    print(tmp[0][1], tmp[1][1], tmp[0][0], tmp[0][1])
    ROI = final_orar[tmp[0][1]:tmp[1][1], tmp[0][0]:tmp[1][0]]
    # cv2.imshow('ROI', ROI)

    if not os.path.exists(folder):
        os.makedirs(folder)

    cv2.imwrite(os.path.join(folder, name), ROI)

    # if cv2.waitKey() == ord(q):
    #     break

# TODO: In cazul in care OCR nu poate citi numele seriilor (top row cells), va trebui sa fac o functie care
# gaseste upper top row points si sa le scada valoarea (aka sa le ridice un pic mai sus). functia findTopLeftPointOrar
# o sa fie utila pt asta

cv2.imshow('final_orar', final_orar)
cv2.waitKey()