from pdf2image import convert_from_path
import imutils
import cv2

def detect(self, c):

    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

pages = convert_from_path('res/orarPdf.pdf', 500)
destSave = 'res/orarJpg.jpg'

for page in pages:
    page.save(destSave, 'JPEG')

img = cv2.imread(destSave)
resized = imutils.resize(img, width=1920)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

cv2.imshow('gray', gray)
cv2.waitKey()