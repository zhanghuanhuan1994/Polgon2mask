# -*- coding:utf-8 -*-
# !/usr/bin/env python

import argparse
import json
import matplotlib.pyplot as plt
import skimage.io as io
import cv2
import numpy as np
import glob
import PIL.Image
import PIL.ImageDraw
import os,sys
import scipy.misc

imgs_path='.\output_json_200'
save_path='.\maskjpg'
if __name__=='__main__':
    for name in os.listdir(imgs_path):
        print(name)
        name0 = os.path.splitext(name)[0]
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser()
        parser.add_argument('-jf', '--json_file', help="json file", type=str, default=name)
        args = parser.parse_args()

        data = json.load(open(args.json_file))
 
        height = data['size']['height']
        width = data['size']['width']
        # print (height)
        # print (width)
        segmentation = data['outputs']['object']  # 对象的边界点
       
        seg = segmentation

        # print (seg[1]['polygon'])
        
        polygons = []
        for i in range(0, len(seg), 2):
            polygons.append([list(seg[i]['polygon'].values()), list(seg[i + 1]['polygon'].values())])
        
        #[[[54, 40, 41, 53, 1241, 1035, 1257, 1021], [6, 86, 0, 102, 1211, 1092, 1226, 1081]]]
        # print(polygons[0][0])
        array= np.zeros((2,4,2),dtype = np.int32)
        # print (array)
      
        array[0][0][0] = polygons[0][0][0]
        array[0][0][1] = polygons[0][0][1]
        array[0][1][0] = polygons[0][0][2]
        array[0][1][1] = polygons[0][0][3]
        array[0][2][0] = polygons[0][0][4]
        array[0][2][1] = polygons[0][0][5]
        array[0][3][0] = polygons[0][0][6]
        array[0][3][1] = polygons[0][0][7]

        array[1][0][0] = polygons[0][1][0]
        array[1][0][1] = polygons[0][1][1]
        array[1][1][0] = polygons[0][1][2]
        array[1][1][1] = polygons[0][1][3]
        array[1][2][0] = polygons[0][1][4]
        array[1][2][1] = polygons[0][1][5]
        array[1][3][0] = polygons[0][1][6]
        array[1][3][1] = polygons[0][1][7]
        #print (array)
        mask0=polygons_to_mask2([height,width],array)
        #mask = np.zeros([height,width], dtype=np.uint8)
        mask = np.zeros([height,width], dtype=np.int32)
        # print('polygons[0]:',polygons[0])
        # print('polygons[1]:',polygons[1])
        #第一个polygon
        polygons0 = np.asarray(array[0], np.int32) # 这里必须是int32，其他类型使用fillPoly会报错
        # cv2.fillPoly(mask, polygons, 1) # 非int32 会报错
        cv2.fillConvexPoly(mask, polygons0, 1)  # 非int32 会报错
        
        #第二个polygon
        polygons1 = np.asarray(array[1], np.int32)
        #  cv2.fillPoly(mask, polygons, 1) 
        cv2.fillConvexPoly(mask, polygons1, 1) 
        #mask 转成0、1二值图片
        # mask0 = mask0.astype(np.uint8)
        # plt.subplot(131)
        # plt.imshow(mask, 'gray')
        # plt.show()
        scipy.misc.imsave("{0}/{1}.jpg".format(save_path, name0), mask)


   
