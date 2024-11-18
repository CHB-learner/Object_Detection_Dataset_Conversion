import os
import json
import os
import shutil   
from datetime import datetime

import cv2

global coco, category_set, image_set, image_id, annotation_id

coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []

category_set = dict()
image_set = set()
image_id = 000000
annotation_id = 0


def YOLO2COCO(input_folder, output_folder):
    print(f"正在将 YOLO 格式转换为 COCO 格式...")
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder}")
    def addCatItem(category_dict):
        for k, v in category_dict.items():
            category_item = dict()
            category_item['supercategory'] = 'none'
            category_item['id'] = int(k)
            category_item['name'] = v
            coco['categories'].append(category_item)


    def addImgItem(file_name, size):
        global image_id
        image_id += 1
        image_item = dict()
        image_item['id'] = image_id
        image_item['file_name'] = file_name
        image_item['width'] = size[1]
        image_item['height'] = size[0]
        image_item['license'] = None
        image_item['flickr_url'] = None
        image_item['coco_url'] = None
        image_item['date_captured'] = str(datetime.today())
        coco['images'].append(image_item)
        image_set.add(file_name)
        return image_id


    def addAnnoItem(object_name, image_id, category_id, bbox):
        global annotation_id
        annotation_item = dict()
        annotation_item['segmentation'] = []
        seg = []
        # bbox[] is x,y,w,h
        # left_top
        seg.append(bbox[0])
        seg.append(bbox[1])
        # left_bottom
        seg.append(bbox[0])
        seg.append(bbox[1] + bbox[3])
        # right_bottom
        seg.append(bbox[0] + bbox[2])
        seg.append(bbox[1] + bbox[3])
        # right_top
        seg.append(bbox[0] + bbox[2])
        seg.append(bbox[1])

        annotation_item['segmentation'].append(seg)

        annotation_item['area'] = bbox[2] * bbox[3]
        annotation_item['iscrowd'] = 0
        annotation_item['ignore'] = 0
        annotation_item['image_id'] = image_id
        annotation_item['bbox'] = bbox
        annotation_item['category_id'] = category_id
        annotation_id += 1
        annotation_item['id'] = annotation_id
        coco['annotations'].append(annotation_item)


    def xywhn2xywh(bbox, size):
        bbox = list(map(float, bbox))
        size = list(map(float, size))
        xmin = (bbox[0] - bbox[2] / 2.) * size[1]
        ymin = (bbox[1] - bbox[3] / 2.) * size[0]
        w = bbox[2] * size[1]
        h = bbox[3] * size[0]
        box = (xmin, ymin, w, h)
        return list(map(int, box))


    def parseXmlFilse(image_path, anno_path, save_path, json_name='annotation.json'):
        assert os.path.exists(image_path), "ERROR {} dose not exists".format(image_path)
        assert os.path.exists(anno_path), "ERROR {} dose not exists".format(anno_path)
        
        # if os.path.exists(save_path):
        #     shutil.rmtree(save_path)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        json_path = os.path.join(save_path, 'annotation',json_name)

        category_set = []
        with open(input_folder + '/classes.txt', 'r') as f:
            for i in f.readlines():
                category_set.append(i.strip())
        category_id = dict((k, v) for k, v in enumerate(category_set))
        addCatItem(category_id)

        images = [os.path.join(image_path, i) for i in os.listdir(image_path)]
        files = [os.path.join(anno_path, i) for i in os.listdir(anno_path)]
        images_index = dict((v.split(os.sep)[-1][:-4], k) for k, v in enumerate(images))
        for file in files:
            if os.path.splitext(file)[-1] != '.txt' or 'classes' in file.split(os.sep)[-1]:
                continue
            if file.split(os.sep)[-1][:-4] in images_index:
                index = images_index[file.split(os.sep)[-1][:-4]]
                img = cv2.imread(images[index])
                shape = img.shape
                filename = images[index].split(os.sep)[-1]
                current_image_id = addImgItem(filename, shape)
            else:
                continue
            with open(file, 'r') as fid:
                for i in fid.readlines():
                    i = i.strip().split()
                    category = int(i[0])
                    category_name = category_id[category]
                    bbox = xywhn2xywh((i[1], i[2], i[3], i[4]), shape)
                    addAnnoItem(category_name, current_image_id, category, bbox)
        # 确保目标路径存在，如果不存在就创建
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        json.dump(coco, open(json_path, 'w'))
        print("class nums:{}".format(len(coco['categories'])))
        print("image nums:{}".format(len(coco['images'])))
        print("bbox nums:{}".format(len(coco['annotations'])))



    def copy_images(image_path, output_image_path):
        # 检查输入目录是否存在
        if not os.path.exists(image_path):
            print(f"错误：输入目录 {image_path} 不存在！")
            return

        # 检查输出目录是否存在，如果不存在则创建
        # os.makedirs(output_image_path)
        if not os.path.exists(output_image_path):
            os.makedirs(output_image_path)
        
        # 获取所有图片文件
        for filename in os.listdir(image_path):
            # 检查文件扩展名是否是常见的图片格式
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                source_path = os.path.join(image_path, filename)
                destination_path = os.path.join(output_image_path, filename)
                try:
                    # 复制文件
                    shutil.copy(source_path, destination_path)
                    print(f"已复制：{filename} TO",destination_path)
                except Exception as e:
                    print(f"无法复制文件 {filename}: {e}")
        
        print("图片复制完成！")



    # """
    # 脚本说明：
    #     本脚本用于将yolo格式的标注文件.txt转换为coco格式的标注文件.json
    # 参数说明：
    #     anno_path:标注文件txt存储路径
    #     save_path:json文件输出的文件夹
    #     image_path:图片路径
    #     json_name:json文件名字
    # """

    anno_path = os.path.join(input_folder,'labels')
    image_path = os.path.join(input_folder,'images')

    save_path = output_folder
    json_name = 'train.json'
    output_image_path = os.path.join(output_folder,'images')
    parseXmlFilse(image_path, anno_path, save_path, json_name)
    copy_images(image_path, output_image_path)

    return




if __name__ == '__main__':
    input_folder = './test_data/input/yolo/'
    output_folder = './test_data/output/yolo2coco/'
    YOLO2COCO(input_folder, output_folder)