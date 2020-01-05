import numpy as np
import cv2
import pytesseract
from PIL import Image
import threading
from queue import Queue

cap = cv2.VideoCapture(0)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
q = Queue()
print_lock = threading.Lock()

def doWork(work) :
	result = pytesseract.image_to_string(Image.fromarray(work))
	with print_lock :
		print(result)

def threader() :
	while(True) :
		work = q.get()
		doWork(work)
		q.task_done()

for i in range(10) :
	t = threading.Thread(target = threader)
	t.daemon = True
	t.start()

while(True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=1)
    frame = cv2.erode(frame, kernel, iterations=1)
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    q.put(frame)
    #result = pytesseract.image_to_string(Image.fromarray(frame))
    #print(result)
 
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break
cap.release()
cv2.destroyAllWindows()
q.join()