from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("detection_model-ex-004--loss-0001.566.h5")
detector.setJsonPath("detection_config.json")
detector.loadModel()

while True:
	name = input("Name: ")
	# name += ".jpg"
	detections = detector.detectObjectsFromImage(input_image=name, output_image_path=name[:-4] +"-detected.png")
	for detection in detections:
		print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
	c = input()
	if c == 'n':
		break

c = input()
