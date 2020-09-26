from keras.models import load_model
import tensorflow as tf
from keras.utils.generic_utils import CustomObjectScope
import numpy as np
import cv2
import re


with CustomObjectScope({'softmax_v2': tf.nn.softmax}):
	model = load_model('OCR.h5')

s = 40	#Input image size for the NN
chars = {10: '-', 11: '-', 12: 'P'}	#@@
ob = re.compile(r'(\D)*(\d+)(\D)*(-)(\D)*(\d+)(\D)*')	#@@(If the format of the score is different)


def formatScore(text, preScore):	#@@(If the format of the score is different)
	'''Filtering out false positives and formatting the score into a tuple'''

	a = ob.search(text)
	if a != None:
		text = a.group(2) + a.group(4) + a.group(6)
		score = tuple(map(int, text.split('-')))
	else:
		score = preScore

	return score


def readText(image, regions):
	'''Reading the characters in the image regions'''

	text = ''
	for (xx, yy, wd, ht) in regions:	#Iterating over all the regions
		img = image[yy: yy+ht, xx: xx+wd]

		#Resizing the image
		reg = cv2.resize(img, (s, s), interpolation = cv2.INTER_AREA)

		#Prediciting the character in the image
		pred = model.predict(reg.reshape(1, s, s, 1))
		text += str(chars.get(pred.argmax(), pred.argmax()))
	
	return text


def process():
	'''Preprocessing the image and finding regions of characters in it'''

	baseIm = cv2.imread('Scoreboard.png', cv2.IMREAD_GRAYSCALE)
	_, image = cv2.threshold(baseIm, 127, 255, cv2.THRESH_BINARY)

	pixels = image.flatten()
	if np.count_nonzero(pixels == 0) < np.count_nonzero(pixels == 255):
		_, image = cv2.threshold(baseIm, 127, 255, cv2.THRESH_BINARY_INV)

	contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)	#Finding contours in the scoreboard

	#Defining regions around the contours
	regions = []
	for contour in contours:
		(xx, yy, wd, ht) = cv2.boundingRect(contour)
		if wd > 2 and ht > 2:	#Size threshold on contours
			regions.append((xx, yy, wd, ht))

	return image, sorted(regions)
		

def ocr(preScore):
	image, regions = process()
	text = readText(image, regions)
	score = formatScore(text, preScore)

	return score
