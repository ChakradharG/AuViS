import cv2
import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'	#To suppress warnings thrown by tensorflow
from keras.models import load_model
import tensorflow as tf
from keras.utils.generic_utils import CustomObjectScope

with CustomObjectScope({'softmax_v2': tf.nn.softmax}):
	model = load_model('OCR pad.h5')
log = open('pad.txt', 'w')
s = 40
d = {10:'-', 11:'|', 12: 'P'}

def resize(image):
	#
	h, w = image.shape

	if h <= s and w <= s:
		res = np.full((s, s), (0,), dtype = np.uint8)
		x = (s - w)//2
		y = (s - h)//2

		res[y:y+h, x:x+w] = image
	else:
		res = cv2.resize(image, (s, s), interpolation = cv2.INTER_AREA)
	#
	# res = cv2.resize(image, (s, s), interpolation = cv2.INTER_AREA)

	return res


def contours(name):
	text = ''
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
	
	
	for (x,y,w,h) in l:
		img = resize(image[y: y+h, x: x+w])
		# cv2.imshow('e', img)
		# cv2.waitKey(0)
		pred = model.predict(img.reshape(1, s, s, 1))
		ch = d.get(pred.argmax(), str(pred.argmax()))
		text += ch

	log.write(f'{name} ~ {text}\n')
		

	cv2.destroyAllWindows()


files = os.listdir()
for i in files:
	_, ty = i.split('.')
	if ty == 'py' or ty == 'h5' or ty == 'txt':
		continue
	# print(i)
	contours(i)
log.close()