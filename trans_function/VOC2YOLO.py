import os
import json

import shutil
from lxml import etree
global category_set,image_set,bbox_nums

category_set = set()
image_set = set()
bbox_nums = 0


def VOC2YOLO(input_folder, output_folder):
    def parse_xml_to_dict(xml):
        """
        将xml文件解析成字典形式，参考tensorflow的recursive_parse_xml_to_dict
        Args:
            xml: xml tree obtained by parsing XML file contents using lxml.etree

        Returns:
            Python dictionary holding XML contents.
        """
        if len(xml) == 0:  # 遍历到底层，直接返回tag对应的信息
            return {xml.tag: xml.text}

        result = {}
        for child in xml:
            child_result = parse_xml_to_dict(child)  # 递归遍历标签信息
            if child.tag != 'object':
                result[child.tag] = child_result[child.tag]
            else:
                if child.tag not in result:  # 因为object可能有多个，所以需要放入列表里
                    result[child.tag] = []
                result[child.tag].append(child_result[child.tag])
        return {xml.tag: result}


    def write_classIndices(category_set):
        class_indices = dict((k, v) for v, k in enumerate(category_set))
        json_str = json.dumps(dict((val, key) for key, val in class_indices.items()), indent=4)
        with open('class_indices.json', 'w') as json_file:
            json_file.write(json_str)


    def xyxy2xywhn(bbox, size):
        bbox = list(map(float, bbox))
        size = list(map(float, size))
        xc = (bbox[0] + (bbox[2] - bbox[0]) / 2.) / size[0]
        yc = (bbox[1] + (bbox[3] - bbox[1]) / 2.) / size[1]
        wn = (bbox[2] - bbox[0]) / size[0]
        hn = (bbox[3] - bbox[1]) / size[1]
        return (xc, yc, wn, hn)


    def parser_info(info: dict, only_cat=True, class_indices=None):
        filename = info['annotation']['filename']
        image_set.add(filename)
        objects = []
        width = int(info['annotation']['size']['width'])
        height = int(info['annotation']['size']['height'])
        for obj in info['annotation']['object']:
            obj_name = obj['name']
            category_set.add(obj_name)
            if only_cat:
                continue
            xmin = int(obj['bndbox']['xmin'])
            ymin = int(obj['bndbox']['ymin'])
            xmax = int(obj['bndbox']['xmax'])
            ymax = int(obj['bndbox']['ymax'])
            bbox = xyxy2xywhn((xmin, ymin, xmax, ymax), (width, height))
            if class_indices is not None:
                obj_category = class_indices[obj_name]
                object = [obj_category, bbox]
                objects.append(object)

        return filename, objects

    ''' # 不支持带有xml声明的
        def parseXmlFilse(voc_dir, save_dir):
            assert os.path.exists(voc_dir), "ERROR {} does not exists".format(voc_dir)
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
            os.makedirs(save_dir)

            xml_files = [os.path.join(voc_dir, i) for i in os.listdir(voc_dir) if os.path.splitext(i)[-1] == '.xml']
            for xml_file in xml_files:
                with open(xml_file) as fid:
                    xml_str = fid.read()
                xml = etree.fromstring(xml_str)
                info_dict = parse_xml_to_dict(xml)
                parser_info(info_dict, only_cat=True)

            with open(output_folder + "/classes.txt", 'w') as classes_file:
                for cat in sorted(category_set):
                    classes_file.write("{}\n".format(cat))

            class_indices = dict((v, k) for k, v in enumerate(sorted(category_set)))

            xml_files = (xml_files)
            for xml_file in xml_files:
                with open(xml_file) as fid:
                    xml_str = fid.read()
                xml = etree.fromstring(xml_str)
                info_dict = parse_xml_to_dict(xml)
                filename, objects = parser_info(info_dict, only_cat=False, class_indices=class_indices)
                if len(objects) != 0:
                    global bbox_nums
                    bbox_nums += len(objects)
                    with open(save_dir + "/" + filename.split(".")[0] + ".txt", 'w') as f:
                        for obj in objects:
                            f.write(
                                "{} {:.5f} {:.5f} {:.5f} {:.5f}\n".format(obj[0], obj[1][0], obj[1][1], obj[1][2], obj[1][3]))
    '''
    def parseXmlFilse(voc_dir, save_dir):
        assert os.path.exists(voc_dir), "ERROR {} does not exists".format(voc_dir)
        if not os.path.exists(save_dir):
            # shutil.rmtree(save_dir)
            os.makedirs(save_dir)

        # 获取所有 XML 文件路径
        xml_files = [os.path.join(voc_dir, i) for i in os.listdir(voc_dir) if os.path.splitext(i)[-1] == '.xml']

        # 第一次遍历，统计类别信息
        for xml_file in xml_files:
            with open(xml_file, "rb") as fid:  # 使用二进制模式打开文件
                xml_str = fid.read()
            xml = etree.fromstring(xml_str)  # 解析字节流为 XML 对象
            info_dict = parse_xml_to_dict(xml)  # 转换为字典
            parser_info(info_dict, only_cat=True)  # 提取类别信息

        # 写入类别文件
        with open(output_folder + "/classes.txt", 'w') as classes_file:
            for cat in sorted(category_set):
                classes_file.write("{}\n".format(cat))

        # 生成类别索引映射
        class_indices = dict((v, k) for k, v in enumerate(sorted(category_set)))

        # 第二次遍历，生成 YOLO 格式的标注文件
        # xml_files = xml_files  # 加入进度条显示
        for xml_file in xml_files:
            with open(xml_file, "rb") as fid:  # 使用二进制模式打开文件
                xml_str = fid.read()
            xml = etree.fromstring(xml_str)  # 解析字节流为 XML 对象
            info_dict = parse_xml_to_dict(xml)  # 转换为字典
            filename, objects = parser_info(info_dict, only_cat=False, class_indices=class_indices)  # 提取信息

            if len(objects) != 0:
                global bbox_nums
                bbox_nums += len(objects)  # 累计标注框数量
                # 写入 YOLO 格式标注文件
                with open(save_dir + "/" + filename.split(".")[0] + ".txt", 'w') as f:
                    for obj in objects:
                        f.write(
                            "{} {:.5f} {:.5f} {:.5f} {:.5f}\n".format(obj[0], obj[1][0], obj[1][1], obj[1][2], obj[1][3]))




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
        
    voc_dir = os.path.join(input_folder,'Annotations')
    save_dir = os.path.join(output_folder,'labels')
    parseXmlFilse(voc_dir, save_dir)

    image_path = os.path.join(input_folder,'JPEGImages')
    output_image_path = os.path.join(output_folder,'images')

    copy_images(image_path, output_image_path)

    return


if __name__ == '__main__':
    input_folder = './test_data/input/SHIP_VOC/'
    output_folder = './test_data/output/VOC2YOLO/'
    VOC2YOLO(input_folder, output_folder)