# import sys
# sys.path.append('./detectron2_webapp')


import sys
from pathlib import Path
FILE = Path(__file__).resolve()
ROOT = str(FILE.parents[0])
sys.path.insert(0, ROOT)

import cv2 as cv
import json
import os
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
from com_ineuron_utils.utils import encodeImageIntoBase64


class DetectorDetectron:

	def __init__(self,filename,model_n):
		
		self.filename = filename
		self.cfg = get_cfg()
		self.cfg.MODEL.DEVICE = "cpu"
		self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.50
		if model_n == "faster_rcnn_R_50_FPN_1x":
			print("\nThe model selected is faster_rcnn_R_50_FPN_1x\n")
			self.model = 'faster_rcnn_R_50_FPN_1x.yaml' 
			self.cfg.merge_from_file("utils/detectron_utils/yaml/faster_rcnn_R_50_FPN_1x.yaml")
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml")
			# self.cfg.MODEL.WEIGHTS = "tdy_models/detectron2/model_1/model_final_b275ba.pkl"
		
		elif model_n=="faster_rcnn_R_50_FPN_3x":
			print("\nThe model selected is faster_rcnn_R_50_FPN_3x\n")
			self.model = 'faster_rcnn_R_50_FPN_3x.yaml' 
			self.cfg.merge_from_file("utils/detectron_utils/yaml/faster_rcnn_R_50_FPN_3x.yaml")
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
			# self.cfg.MODEL.WEIGHTS = "tdy_models/detectron2/model_2/model_final_280758.pkl"

		elif model_n=="faster_rcnn_R_101_FPN_3x":
			print("\nThe model selected is faster_rcnn_R_101_FPN_3x\n")
			self.model = 'faster_rcnn_R_101_FPN_3x.yaml' 
			self.cfg.merge_from_file("utils/detectron_utils/yaml/faster_rcnn_R_101_FPN_3x.yaml")
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
			# self.cfg.MODEL.WEIGHTS = "tdy_models/detectron2/model_3/model_final_f6e8b1.pkl"
		

		elif model_n=="retinanet_R_50_FPN_1x":
			print("\nThe model selected is retinanet_R_50_FPN_1x\n")
			self.model = 'retinanet_R_50_FPN_1x.yaml' 
			self.cfg.merge_from_file("utils/detectron_utils/yaml/retinanet_R_50_FPN_1x.yaml")
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_50_FPN_1x.yaml")
			# self.cfg.MODEL.WEIGHTS = "tdy_models/detectron2/model_4/model_final_bfca0b.pkl"

		elif model_n=="faster_rcnn_R_50_C4_1x":
			print("\nThe model selected is faster_rcnn_R_50_C4_1x\n")
			self.model = 'faster_rcnn_R_50_C4_1x.yaml' 
			self.cfg.merge_from_file("utils/detectron_utils/yaml/faster_rcnn_R_50_C4_1x.yaml")
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")
			# self.cfg.MODEL.WEIGHTS = "tdy_models/detectron2/model_5/model_final_721ade.pkl"
		
		else:
			print("PLEASE SELECT THE DETECTRON2 MODEL")

		



		# build model from weights
		# self.cfg.MODEL.WEIGHTS = self.convert_model_for_inference()
		# self.cfg.MODEL.WEIGHTS="./weights/model_2/faster_rcnn_R_50_FPN_3x.pth"
	# build model and convert for inference
	# def convert_model_for_inference(self):

	# 	# build model
	# 	model = build_model(self.cfg)

	# 	# save as checkpoint
	# 	torch.save(model.state_dict(), './weights/model_2/faster_rcnn_R_50_FPN_3x.pth')

	# 	# return path to inference model
	# 	return './weights/model_2/faster_rcnn_R_50_FPN_3x.pth'


	def inference(self, file):
		predictor = DefaultPredictor(self.cfg)
		im = cv.imread(file)
		outputs = predictor(im)
		print("Number of prediction =", len(outputs["instances"].pred_classes.tolist()))
		print(outputs["instances"].pred_boxes)
		metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])

		# visualise
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.2)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
		predicted_image = v.get_image()
		im_rgb = cv.cvtColor(predicted_image, cv.COLOR_RGB2BGR)
		cv.imwrite('predicted_output_image.jpg', im_rgb)
		# imagekeeper = []
		opencodedbase64 = encodeImageIntoBase64("predicted_output_image.jpg")
		# imagekeeper.append({"image": opencodedbase64.decode('utf-8')})
		result = {"image" : opencodedbase64.decode('utf-8') }
		return result




