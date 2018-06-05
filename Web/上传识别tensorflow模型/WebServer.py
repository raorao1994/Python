#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import json;
import os
import numpy as np
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# 这是需要的，因为笔记本是存储在Object_Protection文件夹中的。
#sys.path.append("..")
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
  raise ImportError('请将您的TensorFlow安装升级到1.4.*或更高版本！')

#Object detection imports
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# 模型名称。
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
# 冰冻检测图的路径。这是用于对象检测的实际模型。
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# 用于为每个框添加正确标签的字符串列表。
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
# 分类数
NUM_CLASSES = 90

#将(冻结的)TensorFlow模型加载到内存中。
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
print("加载模型完成");

#Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

#图像处理函数
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

#Detection物体识别函数
def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # 获取输入和输出张量的句柄
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # 以下处理仅针对单个图像
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # 重新帧需要将掩码从框坐标转换为图像坐标，并与图像大小相匹配。
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # 按照惯例添加批处理维度
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # 运行推理
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # 所有输出都是浮动的32个numpy数组，因此可以根据需要转换类型。
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict

#通过图片路径识别图像
def RecogintionImg(path):
    image = Image.open(path)
    print("开始识别图片。。。");
    # 基于数组的图像表示将在稍后使用
    # 以便准备，结果图像与框和标签在上面。
    image_np = load_image_into_numpy_array(image)
    # 扩展维数，因为模型期望图像具有形状。: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # 开始识别
    output_dict = run_inference_for_single_image(image_np, detection_graph)
    # 打印结果
    print("识别完成。。")
    return output_dict;

def ArrayToStr(data):
    return "";

IMG_LIST = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', img_list=IMG_LIST)

    def post(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        print(self.get_argument('user'))
        print(self.get_arguments('favor'))
        file_metas = self.request.files["filedata"]
        # print(file_metas)
        imgpath="";
        for meta in file_metas:
            # 要上传的文件名
            file_name = meta['filename']
            imgpath=os.path.join('test_images', file_name);
            with open(imgpath, 'wb') as up:
                up.write(meta['body'])
            IMG_LIST.append(file_name)
        #识别图像
        output_dict=RecogintionImg(imgpath);
        boxes=output_dict['detection_boxes']
        classes=output_dict['detection_classes']
        scores=output_dict['detection_scores']
        #筛选出分数较高的物体
        index=0;
        result=[];
        for score in scores:
            if score>0.5:
                id=classes[index];
                obj={"score":score,"box":boxes[index],"class":classes[index],"name":category_index[id]};
                result.append(obj);
            index=index+1;
        print("识别结果")
        print(result);
        strResult=str(result)
        self.write(strResult)

settings = {
    'static_path': 'test_images',
    'static_url_prefix': '/test_images/',
}

application = tornado.web.Application([
    (r"/index", IndexHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8889)
    print("开启服务：服务端口为8888");
    tornado.ioloop.IOLoop.instance().start()