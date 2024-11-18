"""
此脚本的主要内容:
将dota的数据集格式转换成yolo格式，取包裹住多边形最小的矩形框
x1 y1 x2 y2 x3 y3 x4 y4 classname diffcult ========> cls_id cx cy w h

使用方法，需要输入四个参数：
--dataset-dir: 数据集的根路径。同时要确保classes.txt在该目录下，输出数据集label的索引值见按照该文件中的内容来确定。
--image-dirname: 图片的文件夹名称，默认值为images（图片文件夹需要放在数据集的根文件夹中）
--label-dirname: dota标签的文件夹名称，默认值为labelTxt（标签文件夹需要放在数据集的根文件夹中）
--difficult-thres: dota标签中每个标签都还有一个difficult值，用于表示识别的难易度，值越大，越难识别。
该参数的默认值为2，difficult的值若小于该值，则将标签保留下来，反之亦然

输入的路径：文件夹名称固定值为labels (放在数据集的根文件夹中）
"""

import argparse
import glob
import logging
import os
import os.path as osp
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

global IMG_FORMATS

Image.MAX_IMAGE_PIXELS = None
IMG_FORMATS = 'bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm'  # include image suffixes


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-dir', type=str, required=True, help='input dataset dir')
    parser.add_argument('--image-dirname', type=str, default='images',
                        help='the image directory name under the dataset directory')
    parser.add_argument('--label-dirname', type=str, default='labelTxt',
                        help='the dota label directory name under the dataset directory')
    parser.add_argument('--difficult-thres', type=int, default=1,
                        help='skip the lable by difficult less than or equal to difficult-thres')
    opt = parser.parse_args()
    return opt


def get_path_basename(path):
    """获取文件路径的文件名称，不包含拓展名"""
    p = Path(path)
    return p.name.split(p.suffix)[0]


def poly2hbb(polys):
    """Convert polygons to horizontal bboxes.

    Args:
        polys (np.array): Polygons with shape (N, 8)

    Returns:
        np.array: Horizontal bboxes. xyxy
    """
    shape = polys.shape
    polys = polys.reshape(*shape[:-1], shape[-1] // 2, 2)
    lt_point = np.min(polys, axis=-2)
    rb_point = np.max(polys, axis=-2)
    return np.concatenate([lt_point, rb_point], axis=-1)


def xyxy2xywh(x):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[..., 0] = (x[..., 0] + x[..., 2]) / 2  # x center
    y[..., 1] = (x[..., 1] + x[..., 3]) / 2  # y center
    y[..., 2] = x[..., 2] - x[..., 0]  # width
    y[..., 3] = x[..., 3] - x[..., 1]  # height
    return y


def dota2yolo(in_file, out_file, classes, img_wh, difficult_thres):
    with open(in_file, mode='r', encoding='utf-8') as f:
        labels = [str(x).strip().split(' ') for x in f.readlines()]
    polys, cls_ids = [], []
    for i, label in enumerate(labels):
        class_name = label[-2]
        difficult = int(label[-1])
        if class_name not in classes:
            print(f"ignore {in_file} line {i}, because label name not in classes.txt")
            continue
        elif difficult > difficult_thres:
            print(f"ignore {in_file} line {i}, because difficult is greater than {difficult_thres}")
            continue
        polys.append(label[:-2])
        cls_ids.append(classes.index(class_name))

    content_lines = []
    if len(polys):
        # 取包裹住object的水平框
        """
        rects = []
        for poly in polys:
            poly = np.float32(poly).reshape((4, 2))
            # 这里生成的是左上角的坐标，不是中心点的坐标
            rect = cv2.boundingRect(poly)  # (x, y, w, h)
            x = rect[0] + 0.5 * rect[2]  # x + 0.5w
            y = rect[1] + 0.5 * rect[3]  # y + 0.5h
            rects.append([x, y, rect[2], rect[3]])
        rects = np.array(rects, dtype=np.float32)
        """
        content_lines = []
        polys = np.array(polys, dtype=np.float32).reshape(-1, 8)
        rects = poly2hbb(polys)
        rects = xyxy2xywh(rects)
        # 归一化
        rects[:, [0, 2]] /= img_wh[0]
        rects[:, [1, 3]] /= img_wh[1]

        for cls_id, rect in zip(cls_ids, rects):
            line_one = str(cls_id) + ' ' + ' '.join([str(a) for a in rect]) + '\n'
            content_lines.append(line_one)

    if len(content_lines) == 0:
        logging.warning(f'no lines to save, the file: {out_file} is empty')

    # 将内容写入文件
    with open(out_file, mode='w', encoding='utf-8') as f:
        f.writelines(content_lines)

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

def DOTA2YOLO(dataset_dir,output_folder):
    difficult_thres = 1
    image_dirname='images'
    label_dirname='labelTxt'

    assert difficult_thres >= 0, "the param difficult_thres must be greate than or equal to 0"
    class_filepath = osp.join(dataset_dir, 'classes.txt')
    assert os.path.exists(class_filepath), f'please make sure the classes.txt is in path: {dataset_dir}'
    with open(class_filepath, 'r', encoding='utf-8') as f:
        classes = [str(x).strip() for x in f.readlines()]
    label_dir = osp.join(dataset_dir, label_dirname)
    image_dir = osp.join(dataset_dir, image_dirname)
    label_files = [osp.join(label_dir, x) for x in os.listdir(label_dir)]

    save_dir = osp.join(output_folder, 'labels')
    save_image_dir = osp.join(output_folder, 'images')
    if os.path.exists(save_dir):
        logging.info(f"remove outdate directory {save_dir}...")
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)

    shutil.copy(class_filepath, output_folder)

    for label_file in tqdm(label_files, total=len(label_files)):
        out_file = osp.join(save_dir, Path(label_file).name)
        # 在图片文件夹中寻找相同文件名称的图片文件
        file_basename = get_path_basename(label_file)
        try:
            image_file = glob.glob(osp.join(image_dir, file_basename + '.*'))[0]
        except Exception as e:
            assert 0, f"please make sure the folder: {image_dir} have correct image named like {file_basename}"
        assert image_file.rsplit('.')[-1] in IMG_FORMATS, f'find file: {image_file}, but is not an image format'
        img_wh = Image.open(image_file).size
        dota2yolo(label_file, out_file, classes, img_wh, difficult_thres)
    # print msg
    print(f"convert dataset: {Path(dataset_dir).name} dota label to yolo Success!!!")
    print(f"convert label is in folder labels")
    copy_images(image_dir,save_image_dir)
    
    return





# def DOTA2YOLO(input_folder, output_folder):

#     return



if __name__ == '__main__':
    # opt = parse_opt()
    # DOTA2YOLO(dataset_dir=opt.dataset_dir,
    #     image_dirname=opt.image_dirname,
    #     label_dirname=opt.label_dirname,
    #     difficult_thres=opt.difficult_thres)
    
    input_folder = "test_data/input/DOTA/train"
    output_folder = "test_data/output/DOTA2YOLO"
    DOTA2YOLO(input_folder, output_folder)
    
