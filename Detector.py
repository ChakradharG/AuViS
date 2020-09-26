from imageai.Detection.Custom import CustomObjectDetection
import os


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
modelPath = os.getcwd()


def load(game):
	'''Loading the appropriate model files'''

	#@@
	if game == '1':	#Kabaddi
		detector.setModelPath(f'{modelPath}/Kabaddi.h5') 
		detector.setJsonPath(f'{modelPath}/Kabaddi.json')
	elif game == '2':	#Football
		detector.setModelPath(f'{modelPath}/Football.h5') 
		detector.setJsonPath(f'{modelPath}/Football.json')
	elif game == '3':	#Cricket
		detector.setModelPath(f'{modelPath}/Cricket.h5') 
		detector.setJsonPath(f'{modelPath}/Cricket.json')

	detector.loadModel()


def detect():
	'''Detecting the scoreboard in the image and returning its location'''

	detections = detector.detectObjectsFromImage(input_image='Image.png', output_image_path='DetectedImage.png')
	for detection in detections:

		return detection['box_points']
