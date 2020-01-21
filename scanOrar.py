from pdf2image import convert_from_path
import imutils
import cv2
import numpy as np
import os


def getCoordinatedFromCropped(original, cropped, pointsx, pointsy):
    
    # print('orig dims (x, y): ', (original.shape[:2][0], original.shape[:2][1]))
    # print('cropped dims (x, y): ', (cropped.shape[:2][0], cropped.shape[:2][1]))
    
    kx = original.shape[:2][0] / cropped.shape[:2][0]
    ky = original.shape[:2][1] / cropped.shape[:2][1]
    
    # print('kx ', kx)
    # print('ky ', ky)

    new_pointsx = [round(kx * p) for p in pointsx]
    new_pointsy = [round(ky * p) for p in pointsy]
    
    # return (new_x - 20, new_y), (new_x+w, new+y+h + 5)
    return (min(new_pointsx)-20, min(new_pointsy)), (max(new_pointsx), max(new_pointsy)+5) 


def findBottomLeftPointOrar(cnts, img):
    tmpX = img.shape[:2][1] # width of the img
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
    tmpX = img.shape[:2][1] # width of the img
    tmpY = img.shape[:2][0] # height of the img

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
    tmpX = 0 # width of the img
    tmpY = img.shape[:2][0] # height of the img

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

boundary = [204, 204, 204]

img = cv2.imread(destSave)
resized = img.copy()
final_orar = img.copy()
resized = imutils.resize(img, width=1500)

boundary = np.array(boundary, dtype= "uint8")

mask = cv2.inRange(resized, boundary, boundary)
gray_grid = cv2.bitwise_and(resized, resized, mask=mask)

# show the images
cv2.imshow("gray_grid", gray_grid)

gray = cv2.cvtColor(gray_grid, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

cv2.imshow('edges', edges)


blank_image = np.zeros((resized.shape[:2][0], resized.shape[:2][1], 3), np.uint8)
blank_image2 = np.zeros((resized.shape[:2][0], resized.shape[:2][1], 3), np.uint8)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if not cv2.contourArea(cnt) > 20:
        continue
    
    x, y, *_ = cv2.boundingRect(cnt)
    cv2.circle(blank_image, (x, y), 1, (0, 255, 0), 1) 
    
    # momentan nu mai am nevoie de textul scris in coloanele/randurile delimitatoare gri, deci nu conteaza daca iau punctele de sus/jos - in cazul asta am luat mijlocul (sau coltul stanga jos?) conturului.

cv2.imshow('before morph', blank_image)

structElem = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
blank_image2 = cv2.morphologyEx(blank_image, cv2.MORPH_CLOSE, structElem)

cv2.imshow('after morph', blank_image2)

# cv2.circle(blank_image2, findBottomLeftPointOrar(contours, blank_image2), 1, (255, 0, 0), 10)
# cv2.circle(blank_image2, findTopLeftPointOrar(contours, blank_image2), 1, (255, 0, 0), 10)

# trage liniile finale
cv2.line(blank_image2, findTopLeftPointOrar(contours, blank_image2), findBottomLeftPointOrar(contours, blank_image2), (0, 255, 0), 1)
cv2.line(blank_image2, findTopLeftPointOrar(contours, blank_image2), findTopRightPointOrar(contours, blank_image2), (0, 255, 0), 1)

cv2.imshow('after morph + lines', blank_image2)

gray = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)


contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

cv2.waitKey()
cv2.destroyAllWindows()

# showing each cel:

for ind, cnt in enumerate(contours):
    
    if cv2.contourArea(cnt) < 20000 or cv2.contourArea(cnt) > 50000:
        print('not included: ', cv2.contourArea(cnt))
        continue

    name = 'cel' + str(ind+1) + '.jpg'
    folder = 'zileExtraseOrar'

    # print(cv2.contourArea(cnt))
    x, y, w, h = cv2.boundingRect(cnt)
    
    print('cropped coords: ', y, y+h, x, x+w)
    ROI_cropped = resized[y:y+h, x:x+w]
    cv2.imshow('ROI_cropped', ROI_cropped)
    
    newCoords = getCoordinatedFromCropped(final_orar, resized, [x, x+w], [y, y+h])
    print('orig coords: ', newCoords[0][1], newCoords[1][1], newCoords[0][0], newCoords[1][0])
    ROI_original = final_orar[newCoords[0][1]:newCoords[1][1], newCoords[0][0]:newCoords[1][0]]
    
    cv2.imshow('ROI_original', ROI_original)

    if not os.path.exists(folder):
        os.makedirs(folder)

    cv2.imwrite(os.path.join(folder, name), ROI_original)

    if cv2.waitKey() == ord('q'):
        break
