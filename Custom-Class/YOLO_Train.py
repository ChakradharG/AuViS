# -*- coding: utf-8 -*-
#Run this in colab or in a jupyter notebook

"""Prerequisites"""

!pip3 install tensorflow-gpu==1.13.1
!pip3 install imageai --upgrade
!wget https://github.com/OlafenwaMoses/ImageAI/releases/download/essential-v4/pretrained-yolov3.h5

"""Change data_directory and object_names_array appropriately"""

from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="/content/drive/My Drive/Football/")
trainer.setTrainConfig(object_names_array=["Bundesliga", "EPL", "LaLiga"], batch_size=4, num_experiments=7, train_from_pretrained_model="pretrained-yolov3.h5")
trainer.trainModel()

"""Pick the model with maximum mAP"""

from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="/content/drive/My Drive/Football")
trainer.evaluateModel(model_path="/content/drive/My Drive/Football/models", json_path="/content/drive/My Drive/Football/json/detection_config.json", iou_threshold=0.5, object_threshold=0.3, nms_threshold=0.5)