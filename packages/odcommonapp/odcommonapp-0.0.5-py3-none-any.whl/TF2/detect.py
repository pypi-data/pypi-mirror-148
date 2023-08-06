
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
from operator import itemgetter
import sys
sys.path.insert(0,os.getcwd() + "\Helpers")
sys.path.insert(0,os.getcwd() + "\TF2")
from Helpers.download_models import TF2_download_model
from TF2.object_detection.utils import ops as utils_ops
from TF2.object_detection.utils import label_map_util
from TF2.object_detection.utils import visualization_utils as vis_util
from Helpers.utils import encodeImageIntoBase64

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

class TF2Predictor:
    def __init__(self,model):
        if model == "EfficientDet D1 640x640":
            print ("The Required "+" " + model + " " + "started downloading")
            self.download_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/efficientdet_d1_coco17_tpu-32.tar.gz'
            model_folder_name = 'efficientdet_d1_coco17_tpu-32'
            model_tar_file_name = 'efficientdet_d1_coco17_tpu-32.tar.gz'
            model_dir = TF2_download_model(self.download_url,model_folder_name,model_tar_file_name)
            print("\n")
            print('------------------------------------------------------------')
            print("The Prediction started with"+" " + model + " " + "Model")
            print('------------------------------------------------------------')
            self.model = tf.saved_model.load(model_dir)
            self.category_index = label_map_util.create_category_index_from_labelmap("TF2\labelmap.pbtxt",use_display_name=True)

        elif model == "SSD MobileNet v2 320x320":
            print ("The Required "+" " + model + " " + "started downloading")
            self.download_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz'
            model_folder_name = 'ssd_mobilenet_v2_320x320_coco17_tpu-8'
            model_tar_file_name = 'ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz'
            model_dir = TF2_download_model(self.download_url,model_folder_name,model_tar_file_name)
            print("\n")
            print('------------------------------------------------------------')
            print("The Prediction started with"+" " + model + " " + "Model")
            print('------------------------------------------------------------')
            self.model = tf.saved_model.load(model_dir)
            self.category_index = label_map_util.create_category_index_from_labelmap("TF2\labelmap.pbtxt",use_display_name=True)
  
        elif model == "SSD MobileNet V2 FPNLite 320x320":
            print ("The Required "+" " + model + " " + "started downloading")
            self.download_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
            model_folder_name = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
            model_tar_file_name = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
            model_dir = TF2_download_model(self.download_url,model_folder_name,model_tar_file_name)
            print("\n")
            print('------------------------------------------------------------')
            print("The Prediction started with"+" " + model + " " + "Model")
            print('------------------------------------------------------------')
            self.model = tf.saved_model.load(model_dir)
            self.category_index = label_map_util.create_category_index_from_labelmap("TF2\labelmap.pbtxt",
                                                                                use_display_name=True)
        elif model == "Faster R-CNN ResNet50 V1 640x640":
            print ("The Required "+" " + model + " " + "started downloading")
            self.download_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz'
            model_folder_name = 'faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.'
            model_tar_file_name = 'faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz'
            model_dir = TF2_download_model(self.download_url,model_folder_name,model_tar_file_name)
            print("\n")
            print('------------------------------------------------------------')
            print("The Prediction started with"+" " + model + " " + "Model")
            print('------------------------------------------------------------')
            self.model = tf.saved_model.load(model_dir)
            self.category_index = label_map_util.create_category_index_from_labelmap("TF2\labelmap.pbtxt",
                                                                                use_display_name=True)
        elif model == "Faster R-CNN ResNet101 V1 640x640":
            print ("The Required "+" " + model + " " + "started downloading")
            self.download_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet101_v1_640x640_coco17_tpu-8.tar.gz'
            model_folder_name = 'faster_rcnn_resnet101_v1_640x640_coco17_tpu-8.'
            model_tar_file_name = 'faster_rcnn_resnet101_v1_640x640_coco17_tpu-8.tar.gz'
            model_dir = TF2_download_model(self.download_url,model_folder_name,model_tar_file_name)
            print("\n")
            print('------------------------------------------------------------')
            print("The Prediction started with"+" " + model + " " + "Model")
            print('------------------------------------------------------------')
            self.model = tf.saved_model.load(model_dir)
            self.category_index = label_map_util.create_category_index_from_labelmap("TF2\labelmap.pbtxt",
                                                                                    use_display_name=True)
        else:
            print("Please select suitable model")

    
    
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
            min_score_thresh=.5,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8)
        output_filename = 'output.jpg'
        cv2.imwrite(output_filename, image_np)
        opencodedbase64 = encodeImageIntoBase64("output.jpg")
        #listOfOutput = []       
        classes = output_dict['detection_classes']
        scores= output_dict['detection_scores']
        min_score_thresh = 0.5
        # Getting the class name
        index_value = np.where(scores > min_score_thresh)[0]
        print(index_value)
        print("No_of_objects_detected_by_mode:",len(scores[scores>min_score_thresh]))
        result = {"image": opencodedbase64.decode('utf-8')}
        return result

#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Detect objects inside webcam videostream')
#     parser.add_argument('-m', '--model', type=str, required=True, help='Model Path')
#     parser.add_argument('-l', '--labelmap', type=str, required=True, help='Path to Labelmap')
#     parser.add_argument('-i', '--image_path', type=str, required=True, help='Path to image (or folder)')
#     args = parser.parse_args()

# detection_model = load_model(args.model)
# category_index = label_map_util.create_category_index_from_labelmap(args.labelmap, use_display_name=True)
#
# run_inference(detection_model, category_index, args.image_path)


