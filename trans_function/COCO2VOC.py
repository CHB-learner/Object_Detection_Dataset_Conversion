from pycocotools.coco import COCO
import os
from lxml import etree, objectify
import shutil
from tqdm import tqdm
import sys
import argparse



def COCO2VOC(input_folder, output_folder):
    # 将类别名字和id建立索引
    def catid2name(coco):
        classes = dict()
        for cat in coco.dataset['categories']:
            classes[cat['id']] = cat['name']
        return classes


    # 将标签信息写入xml
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
                E.width(size['width']),
                E.height(size['height']),
                E.depth(size['depth'])
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
                    E.xmin(obj[1]),
                    E.ymin(obj[2]),
                    E.xmax(obj[3]),
                    E.ymax(obj[4])
                )
            )
            anno_tree.append(anno_tree2)
        anno_path = os.path.join(save_path, filename[:-3] + "xml")
        etree.ElementTree(anno_tree).write(anno_path, pretty_print=True)


    # 利用cocoAPI从json中加载信息
    def load_coco(anno_file, xml_save_path):
        if os.path.exists(xml_save_path):
            shutil.rmtree(xml_save_path)
        os.makedirs(xml_save_path)

        coco = COCO(anno_file)
        classes = catid2name(coco)
        imgIds = coco.getImgIds()
        classesIds = coco.getCatIds()
        for imgId in tqdm(imgIds):
            size = {}
            img = coco.loadImgs(imgId)[0]
            filename = img['file_name']
            width = img['width']
            height = img['height']
            size['width'] = width
            size['height'] = height
            size['depth'] = 3
            annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
            anns = coco.loadAnns(annIds)
            objs = []
            for ann in anns:
                object_name = classes[ann['category_id']]
                # bbox:[x,y,w,h]
                bbox = list(map(int, ann['bbox']))
                xmin = bbox[0]
                ymin = bbox[1]
                xmax = bbox[0] + bbox[2]
                ymax = bbox[1] + bbox[3]
                obj = [object_name, xmin, ymin, xmax, ymax]
                objs.append(obj)
            save_anno_to_xml(filename, size, objs, xml_save_path)


    def parseJsonFile(data_dir, xmls_save_path):
        assert os.path.exists(data_dir), "data dir:{} does not exits".format(data_dir)

        if os.path.isdir(data_dir):
            data_types = ['train2017', 'val2017']
            for data_type in data_types:
                ann_file = 'instances_{}.json'.format(data_type)
                xmls_save_path = os.path.join(xmls_save_path, data_type)
                load_coco(ann_file, xmls_save_path)
        elif os.path.isfile(data_dir):
            anno_file = data_dir
            load_coco(anno_file, xmls_save_path)


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

    json_path =  os.path.join(input_folder,'annotation','annotation.json')
    xml_save_path = os.path.join(output_folder,'Annotations')


    image_path = os.path.join(input_folder,'images')
    output_image_path = os.path.join(output_folder,'JPEGImages')
    parseJsonFile(json_path, xmls_save_path=xml_save_path)
    copy_images(image_path, output_image_path)
    

    return

if __name__ == '__main__':
    input_folder = './test_data/input/coco/'
    output_folder = './test_data/output/coco2voc/'
    COCO2VOC(input_folder, output_folder)