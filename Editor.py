from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


def combine(vidName, extension, timeStamps, path):
	'''Clipping small segments from the video and stitching them into a single video'''

	delta = 15	#%%Seconds before and after the event
	print('\nGenerating Highlights')
	video = VideoFileClip(f'{path}.{extension}')
	videoClips = list(map(lambda x: video.subclip(x-delta, x+delta), timeStamps))
	finalClip = concatenate_videoclips(videoClips)
	finalClip.write_videofile(f'{path}/Highlights.mp4', codec='libx264')	#%%Small size, inferior quality
	# finalClip.write_videofile(f'{path}/Highlights.avi', codec='rawvideo')	#%%Large size, superior quality
