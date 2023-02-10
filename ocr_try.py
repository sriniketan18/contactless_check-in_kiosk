import numpy as np
import pytesseract
import cv2
import ocr_try2
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

ocr_img=cv2.imread("sample.jpeg")
gray = cv2.cvtColor(ocr_img, cv2.COLOR_RGB2GRAY)

gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
"""
gray = cv2.bitwise_not(img_bin)

kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)

img = cv2.dilate(img, kernel, iterations=1)
cv2.imshow("a",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
te= ocr_try2.Text_Extractor(img_bin)
text=te.extract_text()
print(text)
#out_below = pytesseract.image_to_string(img)
#print("OUTPUT:", out_below)