#Importing Modules
import os
import shutil
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'	#To suppress warnings thrown by tensorflow
import Detector as D
import Ocr as O


#@@
def kabaddi(score, preScore, sec, log, events):
	'''Function for generation of highlights for a game of Kabaddi'''

	diff1, diff2 = score[0] - preScore[0], score[1] - preScore[1]
	posDiff = list(range(3,11))

	if diff1 in posDiff or diff2 in posDiff:
		print(f'{sec//60}:{sec%60} ~ Super Raid')
		log.write(f'{sec//60}:{sec%60} ~ Super Raid\n')
		events['Super Raids'] += 1


def football(score, preScore, sec, log, events):
	'''Function for generation of highlights for a game of Football'''

	if score[0] == preScore[0] + 1:
		print(f'{sec//60}:{sec%60} ~ Home team scored')
		log.write(f'{sec//60}:{sec%60} ~ Home team scored\n')
		events['Goals Scored by the Home Team'] += 1
	elif score[1] == preScore[1] + 1:
		print(f'{sec//60}:{sec%60} ~ Away team scored')
		log.write(f'{sec//60}:{sec%60} ~ Away team scored\n')
		events['Goals Scored by the Away Team'] += 1


def cricket(score, preScore, sec, log, events):
	'''Function for generation of highlights for a game of Cricket'''

	if score[1] == preScore[1] + 1:
		print(f'{sec//60}:{sec%60} ~ Wicket')
		log.write(f'{sec//60}:{sec%60} ~ Wicket\n')
		events['Wickets'] += 1

	runDiff = score[0] - preScore[0]

	if runDiff == 6:
		print(f'{sec//60}:{sec%60} ~ Six')
		log.write(f'{sec//60}:{sec%60} ~ Six\n')
		events['Sixes'] += 1
	elif runDiff == 4:
		print(f'{sec//60}:{sec%60} ~ Four')
		log.write(f'{sec//60}:{sec%60} ~ Four\n')
		events['Fours'] += 1
	elif runDiff == 3 or runDiff == 5:
		print(f'{sec//60}:{sec%60} ~ 3 or 5 runs')
		log.write(f'{sec//60}:{sec%60} ~ 3 or 5 runs\n')
		events['3s or 5s'] += 1


def main(vid, video, game):
	'''Function to locate scoreboard, crop the image accordingly and call the function corresponding to the game every second'''

	log = open('events.txt', 'w')
	frRt = int(video.get(cv2.CAP_PROP_FPS))	#Framerate of the video
	
	i, k, box = 0, 0, []
	while(vid.isOpened()):	#Looping to locate the scoreboard
		ret, frame = vid.read()
		if not ret:
			break
		if i % (30*frRt) == 0:	#Checking for scoreboard every 30s
			cv2.imwrite('Image.png',frame)
			b = D.detect()
			if b != None:
				box.extend(b)	#Accumulating the locations of detected scoreboards to take the average over them
				k += 1
				if k == 10:	#Maximum number of scoreboards to take average over
					break
		i += 1
	if box == []:
		input('Couldn\'t find scoreboard in the video'); exit()
	else:
		for i in range(1, k):	#Averaging over scoreboard locations
			for j in range(4):
				box[j] += box[4*i + j]
		box = list(map(lambda x: x//k, box[:4]))
	vid.release()
	
	gameFunc = {'1': kabaddi, '2': football, '3': cricket}[game]	#@@
	events = {
			'1': {'Super Raids': 0},
			'2': {'Goals Scored by the Home Team': 0, 'Goals Scored by the Away Team': 0},
			'3': {'Wickets': 0, 'Sixes': 0, 'Fours': 0, '3s or 5s': 0}
			}[game]	#@@
	frNo = 0	#Frame number
	preScore = (0, 0)	#@@To keep track of score in the previous frame

	while(video.isOpened()):	#Looping over frames of the video
		ret, frame = video.read()
		if not ret:
			break
		if frNo % frRt == 0:	#Updating score every second
			cv2.imwrite('Image.png',frame)
			if D.detect() != None:
				cv2.imwrite('Scoreboard.png', frame[box[1]:box[3], box[0]:box[2]])	#Saving the cropped scoreboard image
				score = O.ocr(preScore)
				gameFunc(score, preScore, frNo//frRt, log, events)
				preScore = score
		frNo += 1
	video.release()
	cv2.destroyAllWindows()

	print(events)
	for i,j in events.items():
		log.write(f'\n{i}: {j}')
	log.close()


def getGame():
	'''Getting user inputs, creating a subfolder for the desired video'''

	game = input('Enter Choice of Game\n1.Kabaddi\n2.Football\n3.Cricket\n')	#@@
	if game not in '123':	#@@
		input('Wrong Choice'); exit()
	vidName = input('Enter Name of Video File: ')

	path = f'{os.getcwd()}/{vidName}'	#Path of the working directory
	try:	#Creating a folder for the given video
		shutil.rmtree(path)
	except:
		pass
	finally:
		os.mkdir(path); os.chdir(path)

	try:	#Opening video file
		vid = cv2.VideoCapture(f'{path}.mp4')	#Video used for detecting the location of the scoreboard
		video = cv2.VideoCapture(f'{path}.mp4')	#Video used for actual extraction
	except:
		input('No such file'); exit()

	D.load(game)
	main(vid, video, game)


getGame()
