import cv2 as cv
import json
import os
import sys
sys.path.insert(0,os.getcwd() + "\detectron")
sys.path.insert(0,os.getcwd() + "\Helpers")
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.modeling import build_model
import torch
import numpy as np
from PIL import Image
from Helpers.utils import encodeImageIntoBase64


class Dectron_Detector:

	def __init__(self,filename,model):
		self.filename = filename  
		self.cfg = get_cfg() 
		self.cfg.MODEL.DEVICE = "cpu"
		self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.50 
		if model == "faster_rcnn_R_50_FPN_1x":
			print("\n The model selected for detection is:",model)
			self.model = 'faster_rcnn_R_50_FPN_1x.yaml'
			self.cfg.merge_from_file(os.path.join(os.getcwd()+ '\\detectron\\detectron_yaml\yaml\\'+'faster_rcnn_R_50_FPN_1x.yaml'))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml")

		elif model == "faster_rcnn_R_50_C4_1x":
			print("\n The model selected for detection is:",model)
			self.model = 'faster_rcnn_R_50_C4_1x.yaml'
			self.cfg.merge_from_file(os.path.join(os.getcwd()+ '\\detectron\\detectron_yaml\yaml\\'+'faster_rcnn_R_50_C4_1x.yaml'))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")
			
		elif model =="faster_rcnn_R_101_C4_3x":
			print("\n The model selected for detection is:",model)
			self.model = 'faster_rcnn_R_101_C4_3x.yaml'
			self.cfg.merge_from_file(os.path.join(os.getcwd()+ '\\detectron\\detectron_yaml\yaml\\'+'faster_rcnn_R_101_C4_3x.yaml'))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_C4_3x.yaml")

		elif model =="faster_rcnn_R_101_FPN_3x":
			print("\n The model selected for detection is:",model)
			self.model = 'faster_rcnn_R_101_FPN_3x.yaml'
			self.cfg.merge_from_file(os.path.join(os.getcwd()+ '\\detectron\\detectron_yaml\yaml\\'+'faster_rcnn_R_101_FPN_3x.yaml'))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

		elif model =="retinanet_R_50_FPN_1x":
			print("\n The model selected for detection is:",model)
			self.model = 'retinanet_R_50_FPN_1x.yaml'
			self.cfg.merge_from_file(os.path.join(os.getcwd()+ '\\detectron\\detectron_yaml\yaml\\'+'retinanet_R_50_FPN_1x.yaml'))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_50_FPN_1x.yaml")


	
		# elif model =="X101-FPN":
		# 	model_config_download_url = 'https://github.com/facebookresearch/detectron2/blob/main/configs/COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml'
		# 	model_download_url = 'https://dl.fbaipublicfiles.com/detectron2/COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x/139173657/model_final_68b088.pkl'
		# 	model_config_filename = 'faster_rcnn_X_101_32x8d_FPN_3x.yaml'
		# 	model_name = 'model_final_68b088.pkl'
		# 	detection_model_dir,detection_model_config = detectron_download_model(model,model_config_download_url,model_download_url,model_config_filename,model_name)
		# 	number_of_classes_of_model = 80
		else:
			print("Please choose correct model")
		

	# build model and convert for inference
	def convert_model_for_inference(self):

		# build model
		model = build_model(self.cfg)

		# save as checkpoint
		torch.save(model.state_dict(), 'checkpoint.pth')

		# return path to inference model
		return 'checkpoint.pth'


	def inference(self, file):

		predictor = DefaultPredictor(self.cfg)
		im = cv.imread(file)
		outputs = predictor(im)
		#print(outputs["instances"].pred_classes)
		#print(outputs["instances"].pred_boxes)
		metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).set(thing_classes=['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'])
		
		# visualise
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.2)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
		predicted_image = v.get_image()
		im_rgb = cv.cvtColor(predicted_image, cv.COLOR_RGB2BGR)
		cv.imwrite('color_img.jpg', im_rgb)
		# imagekeeper = []
		opencodedbase64 = encodeImageIntoBase64("color_img.jpg")
		# imagekeeper.append({"image": opencodedbase64.decode('utf-8')})
		result = {"image" : opencodedbase64.decode('utf-8') }
		return result




