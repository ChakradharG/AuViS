import cv2
import os
import shutil
from random import choice
from PIL import Image

path = os.getcwd()


def ss(vidName, imgCnt):
	video = cv2.VideoCapture(f'{vidName}.mp4')
	frCnt = int(int(input('Enter length of video in seconds: ')) * video.get(cv2.CAP_PROP_FPS)/imgCnt)

	try:
		shutil.rmtree(path)
	except:
		pass
	finally:
		os.mkdir(path); os.chdir(path)

	i = 0
	while(video.isOpened()):
		ret, frame = video.read()
		if ret == False:
			break
		if i % frCnt == 0:
			cv2.imwrite(f'{vidName}{i}.jpg', frame)
		i += 1

	video.release()
	cv2.destroyAllWindows()
	c = input(f'{(i+1)//frCnt} Screenshots saved, please delete images without scoreboard and press enter to continue')


def crop():
	files = os.listdir()
	os.mkdir('ScoreBoards')

	area = tuple(map(int, input('Enter xmin ymin xmax ymax of the scoreboard: ').split()))
	for file in files:
		im = Image.open(file)
		op = im.crop(area)
		op.save(f'{path}\\ScoreBoards\\_{file}')

	c = input('Scoreboards saved, please check and press enter to continue')


def rename(vidName):
	files = os.listdir()
	files.remove('ScoreBoards')
	names = [x for x in range(len(files))]

	for file in files:
		name = choice(names)
		names.remove(name)
		os.rename(file, f'{vidName}_{name}.jpg')

	c = input('Press enter to continue')


def label(lines):
	files = os.listdir()
	files.remove('ScoreBoards')

	for file in files:
		name = file[:-4]
		f = open(f'{name}.xml', 'w')

		for i in range(2):
			f.write(lines[i])

		f.write('	<filename>' + file + '</filename>\n')
		f.write('	<path>' + path + '\\images\\' + file + '</path>\n')

		for i in range(4,26):
			f.write(lines[i])

		f.close()

	c = input('Press enter to finish')


def main():
	global path

	f = open('X.xml')
	lines = f.readlines()
	f.close()

	vidName = input('Enter name of the video file: ')
	imgCnt = int(input('How many images do you want? '))
	path = f'{path}\\{vidName}'

	ss(vidName, imgCnt)

	crop()

	rename(vidName)

	label(lines)


main()
