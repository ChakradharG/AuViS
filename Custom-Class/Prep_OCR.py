import cv2
import os
import numpy as np


def resize(image):
	s = 40
	#
	# h, w = image.shape

	# if h <= s and w <= s:
	# 	res = np.full((s, s), (0,), dtype = np.uint8)
	# 	x = (s - w)//2
	# 	y = (s - h)//2

	# 	res[y:y+h, x:x+w] = image
	# else:
	# 	res = cv2.resize(image, (s, s), interpolation = cv2.INTER_AREA)
	#
	res = cv2.resize(image, (s, s), interpolation = cv2.INTER_AREA)

	return res


def contours(name, j):
	baseIm = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
	_,image = cv2.threshold(baseIm, 127, 255, cv2.THRESH_BINARY)

	pixels = image.flatten()
	if np.count_nonzero(pixels == 0) < np.count_nonzero(pixels == 255):
		_,image = cv2.threshold(baseIm, 127, 255, cv2.THRESH_BINARY_INV)


	contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	l = []
	for c in contours:
		(x, y, w, h) = cv2.boundingRect(c)
		if w > 2 and h > 2:
			l.append((x, y, w, h))
	l.sort()
	
	k = 0
	for (x,y,w,h) in l:
		img = resize(image[y: y+h, x: x+w])
		cv2.imwrite(f'{j}_{k}.png', img)
		k += 1

	cv2.destroyAllWindows()


files = os.listdir()
files.remove('Prep_OCR.py')
j = 0
for i in files:
	contours(i, j)
	j += 1