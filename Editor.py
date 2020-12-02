from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


def combine(vidName, extension, timeStamps):
	'''Clipping small segments from the video and stitching them into a single video'''

	delta = 15	#Seconds before and after the event
	print('\nGenerating Highlights')
	os.chdir('..')
	video = VideoFileClip(f'{os.getcwd()}/{vidName}.{extension}')
	videoClips = list(map(lambda x: video.subclip(x-delta, x+delta), timeStamps))
	finalClip = concatenate_videoclips(videoClips)
	finalClip.write_videofile(f'{os.getcwd()}/{vidName}/Highlights.{extension}')