# Automated-Video-Summarization
Automated Video Summarization for sports videos was developed for the final year project of my Engineering curriculum.

<br>

## How to Use
Works on latest editions of Bundesliga, English Premier League, Indian Pro Kabaddi, Indian Premier League, ICC Worldcup 2019 (as of 2020)

1. Install Python
2. Install Microsoft Visual C++ (any of 2015, 2017, 2019)
3. Install the required modules
4. Copy the desired input video into this folder
5. Run Highlights.py

_requirements_: tensorflow, imageai, keras, opencv-python

<br>

## To create a model for a different game
1. Copy video of desired game into the Custom Class folder
2. Training requires 200 to 300 images with scoreboards(as diverse in scores as possible) so accordingly copy number of videos
3. Create annotation file for the scoreboard using LabelImg python program and name it X.xml
4. Run Prep_YOLO.py
5. Run Yolo.py in colab or jupyter notebook
6. You can check the performance of the model using ModelTrial.py
7. Copy Prep_OCR.py into the Scoreboards folder and run it
8. Rename the character images generated according to the character in the images (These will be the labels for training the Neural Netword for OCR)
9. Run Rename.py
10. Run OCR_Train.py in colab or jupyter notebook
11. In main code (Highlights.py, Detector.py, Ocr.py) change the places marked as '#@@' appropriately to accomodate for the addition of the new class(es)
12. Copy model files into the main folder
