from PIL import Image
import numpy as np
import cv2

img_path = r"D:\stark\bash_scripts\test.jpg"
image = Image.open(img_path)
imgref = image
imgref.load()
image = np.array(image, dtype = np.uint8)
imgref2 = image
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
kernel = np.ones((1, 1), np.uint8)
image = cv2.dilate(image, kernel, iterations=1)
image = cv2.erode(image, kernel, iterations=1)
image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
#image.load()
#data = np.asarray(image, dtype = "int32")
#img = Image.fromarray( np.asarray( np.clip(image,0,255), dtype="uint8"), "L" )
#img.load()
#img.show()
#print(image[0][0])
'''row = image.shape[0]
cols = image.shape[1]
print(row, end = ' ')
print(cols)
for r in range(0, row) :
	for c in range(0, cols) :
		#coordinates = r, c
		#print(coordinates)
		#x = img.getpixel(coordinates)[0]
		if image[r][c] == 0 :
			print(r, end = ' ')
			print(c)
			imgref.putpixel((c, r), (255, 0, 0))
imgref.show()'''
pts = cv2.findNonZero(image)
ret = cv2.minAreaRect(pts)

(cx,cy), (w,h), ang = ret
if w>h:
    w,h = h,w
    ang += 90

## (4) Find rotated matrix, do rotation
M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
rotated = cv2.warpAffine(image, M, (imgref2.shape[1], imgref2.shape[0]))

## (5) find and draw the upper and lower boundary of each lines
hist = cv2.reduce(rotated,1, cv2.REDUCE_AVG).reshape(-1)

th = 2
H,W = imgref2.shape[:2]
uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
for y in uppers:
    cv2.line(rotated, (0,y), (W, y), (255,0,0), 1)

for y in lowers:
    cv2.line(rotated, (0,y), (W, y), (0,255,0), 1)

cv2.imwrite("result3.png", rotated)
#cv2.imshow(rotated)