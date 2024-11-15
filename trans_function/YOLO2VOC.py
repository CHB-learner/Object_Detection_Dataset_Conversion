import argparse
import os
import sys
import shutil

import cv2
from lxml import etree, objectify

# 将标签信息写入xml
from tqdm import tqdm


global images_nums,category_nums,bbox_nums
images_nums = 0
category_nums = 0
bbox_nums = 0


def YOLO2VOC(input_folder, output_folder):
    print(f"正在将 YOLO 格式转换为 VOC 格式...")
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder}")


    def save_anno_to_xml(filename, size, objs, save_path):
        E = objectify.ElementMaker(annotate=False)
        dir_NAME = save_path.split('/')[-2]
        anno_tree = E.annotation(
            E.folder(f"{dir_NAME}"),
            E.filename(filename),
            E.source(
                E.database("The VOC Database"),
                E.annotation("PASCAL VOC"),
                E.image("flickr")
            ),
            E.size(
                E.width(size[1]),
                E.height(size[0]),
                E.depth(size[2])
            ),
            E.segmented(0)
        )
        for obj in objs:
            E2 = objectify.ElementMaker(annotate=False)
            anno_tree2 = E2.object(
                E.name(obj[0]),
                E.pose("Unspecified"),
                E.truncated(0),
                E.difficult(0),
                E.bndbox(
                    E.xmin(obj[1][0]),
                    E.ymin(obj[1][1]),
                    E.xmax(obj[1][2]),
                    E.ymax(obj[1][3])
                )
            )
            anno_tree.append(anno_tree2)
        anno_path = os.path.join(save_path, filename[:-3] + "xml")
        etree.ElementTree(anno_tree).write(anno_path, pretty_print=True)


    def xywhn2xyxy(bbox, size):
        bbox = list(map(float, bbox))
        size = list(map(float, size))
        xmin = (bbox[0] - bbox[2] / 2.) * size[1]
        ymin = (bbox[1] - bbox[3] / 2.) * size[0]
        xmax = (bbox[0] + bbox[2] / 2.) * size[1]
        ymax = (bbox[1] + bbox[3] / 2.) * size[0]
        box = [xmin, ymin, xmax, ymax]
        return list(map(int, box))


    def parseXmlFilse(image_path, anno_path, save_path):
        global images_nums, category_nums, bbox_nums
        assert os.path.exists(image_path), "ERROR {} dose not exists".format(image_path)
        assert os.path.exists(anno_path), "ERROR {} dose not exists".format(anno_path)
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)

        category_set = []
        with open(input_folder + '/classes.txt', 'r') as f:
            for i in f.readlines():
                category_set.append(i.strip())
        category_nums = len(category_set)
        category_id = dict((k, v) for k, v in enumerate(category_set))

        images = [os.path.join(image_path, i) for i in os.listdir(image_path)]
        files = [os.path.join(anno_path, i) for i in os.listdir(anno_path)]
        images_index = dict((v.split(os.sep)[-1][:-4], k) for k, v in enumerate(images))
        images_nums = len(images)

        for file in tqdm(files):
            if os.path.splitext(file)[-1] != '.txt' or 'classes' in file.split(os.sep)[-1]:
                continue
            if file.split(os.sep)[-1][:-4] in images_index:
                index = images_index[file.split(os.sep)[-1][:-4]]
                img = cv2.imread(images[index])
                shape = img.shape
                filename = images[index].split(os.sep)[-1]
            else:
                continue
            objects = []
            with open(file, 'r') as fid:
                for i in fid.readlines():
                    i = i.strip().split()
                    category = int(i[0])
                    category_name = category_id[category]
                    bbox = xywhn2xyxy((i[1], i[2], i[3], i[4]), shape)
                    obj = [category_name, bbox]
                    objects.append(obj)
            bbox_nums += len(objects)
            save_anno_to_xml(filename, shape, objects, save_path)
    
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

    #  input_folder,output_folder

    anno_path = os.path.join(input_folder,'labels')
    image_path = os.path.join(input_folder,'images')
    save_anno_path = os.path.join(output_folder,'Annotations')
    output_image_path = os.path.join(output_folder,'JPEGImages')

    parseXmlFilse(image_path, anno_path, save_anno_path)
    copy_images(image_path, output_image_path)

    return



if __name__ == '__main__':

    """
    脚本说明：
        本脚本用于将yolo格式的标注文件.txt转换为voc格式的标注文件.xml
    参数说明：
        anno_path:标注文件txt存储路径
        save_path:json文件输出的文件夹
        image_path:图片路径
    """
    input_folder = './test_data/input/yolo/'
    output_folder = './test_data/output/yolo2voc/'
    YOLO2VOC(input_folder, output_folder)
