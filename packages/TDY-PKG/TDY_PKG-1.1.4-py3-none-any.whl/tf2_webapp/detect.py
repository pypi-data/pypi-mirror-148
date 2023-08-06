# import sys
# sys.path.append('./tf2_webapp')
import sys
from pathlib import Path
FILE = Path(__file__).resolve()
ROOT = str(FILE.parents[0])
sys.path.insert(0, ROOT)

import numpy as np
import argparse
import os
import tensorflow as tf
from PIL import Image
from io import BytesIO
import pathlib
import glob
import matplotlib.pyplot as plt
import cv2

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from com_in_ineuron_ai_utils.utils import encodeImageIntoBase64

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile


class PredictorTF2:
    def __init__(self,model_n):
        
        # self.model=tf.saved_model.load("tdy_models/tf2/ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8/saved_model")
       
        # self.model=tf.saved_model.load("tdy_models/tf2/ssd_resnet101_v1_fpn_1024x1024_coco17_tpu-8/saved_model")
        
        # self.model=tf.saved_model.load("tdy_models/tf2/efficientdet_d4_coco17_tpu-32/saved_model")
        
        # self.model=tf.saved_model.load("tdy_models/tf2/faster_rcnn_resnet101_v1_1024x1024_coco17_tpu-8/saved_model")
        
        # self.model=tf.saved_model.load("tdy_models/tf2/efficientdet_d7_coco17_tpu-32/saved_model")

        # self.model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
        if model_n=="ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8":
            print("\nThe model selected is ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8\n")
            self.model_name = 'ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8'

        elif model_n=="ssd_resnet101_v1_fpn_1024x1024_coco17_tpu-8":
            print("\nThe model selected is ssd_resnet101_v1_fpn_1024x1024_coco17_tpu-8\n")
            self.model_name = 'ssd_resnet101_v1_fpn_1024x1024_coco17_tpu-8'

        elif model_n=="efficientdet_d4_coco17_tpu-32":
            print("\nThe model selected is efficientdet_d4_coco17_tpu-32\n")
            self.model_name = 'efficientdet_d4_coco17_tpu-32'

        elif model_n=="faster_rcnn_resnet101_v1_1024x1024_coco17_tpu-8":
            print("\nThe model selected is faster_rcnn_resnet101_v1_1024x1024_coco17_tpu-8\n")
            self.model_name = 'faster_rcnn_resnet101_v1_1024x1024_coco17_tpu-8'

        elif model_n=="efficientdet_d7_coco17_tpu-32":
            print("\nThe model selected is efficientdet_d7_coco17_tpu-32\n")
            self.model_name = 'efficientdet_d7_coco17_tpu-32'

        else:
            print("PLEASE SELECT THE TF2 MODEL")

        # detection_model = self.load_model('ssd_mobilenet_v1_coco_2017_11_17')
        # self.model=detection_model.signatures['serving_default']

        self.base_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/'
        self.model_file = self.model_name + '.tar.gz'
        self.model_dir = tf.keras.utils.get_file(
        fname=self.model_name, 
        origin=self.base_url + self.model_file,
        untar=True)

        self.model_dir = pathlib.Path(self.model_dir)/"saved_model"
        print(self.model_dir)
        self.model = tf.saved_model.load(str(self.model_dir))
        # self.model=self.model.signatures['serving_default']

        self.category_index = label_map_util.create_category_index_from_labelmap("utils/tf2_utils/mscoco_label_map.pbtxt", use_display_name=True)
        
    def load_model(model_name):
        base_url = 'http://download.tensorflow.org/models/object_detection/'
        model_file = model_name + '.tar.gz'
        model_dir = tf.keras.utils.get_file(
        fname=model_name, 
        origin=base_url + model_file,
        untar=True)

        model_dir = pathlib.Path(model_dir)/"saved_model"

        model = tf.saved_model.load(str(model_dir))

        return model                                                                            

    def load_image_into_numpy_array(self, path):
        img_data = tf.io.gfile.GFile(path, 'rb').read()
        image = Image.open(BytesIO(img_data))
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def run_inference_for_single_image(self, model, image):
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run inference
        output_dict = model(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key: value[0, :num_detections].numpy()
                       for key, value in output_dict.items()}
        output_dict['num_detections'] = num_detections

        # detection_classes should be ints.
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

        # Handle models with masks:
        if 'detection_masks' in output_dict:
            # Reframe the the bbox mask to the image size.
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                output_dict['detection_masks'], output_dict['detection_boxes'],
                image.shape[0], image.shape[1])
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

        return output_dict

    def run_inference(self):
        image_path = "inputImage.jpg"
        image_np = self.load_image_into_numpy_array(image_path)
        # Actual detection.
        model = self.model
        output_dict = self.run_inference_for_single_image(model, image_np)

        category_index = self.category_index
        # Visualization of the results of a detection.

        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=3)

        print(output_dict['detection_boxes'])
        print(output_dict['detection_classes'])
        output_filename = 'predicted_output_image.jpg'
        cv2.imwrite(output_filename, cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
        opencodedbase64 = encodeImageIntoBase64("predicted_output_image.jpg")
        #listOfOutput = []
        result = {"image": opencodedbase64.decode('utf-8')}

        return result




