from random import choice
import os

def rename(file):
	name, _ = file.split('.')
	_, num = name.split('_')
	if num < 2:
		name = choice(train)
		train.remove(name)
	else:
		name = choice(test)
		test.remove(name)

	os.rename(file, f'{name}.png')
	log.write(f'{name}.png~{file}\n')
		


l = os.listdir()
l.remove('Rename.py')
l.remove('Prep_OCR.py')
log = open('yLog.txt', 'w')
y = int(len(l)*0.8)
train = [x for x in range(y)]
test = [x for x in range(y, len(l))]

for i in l:
	rename(i)