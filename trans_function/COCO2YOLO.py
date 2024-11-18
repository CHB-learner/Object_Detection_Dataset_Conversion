from pycocotools.coco import COCO
import os
import shutil

global images_nums,category_nums,bbox_nums

images_nums = 0
category_nums = 0
bbox_nums = 0


def COCO2YOLO(input_folder, output_folder):
    # 将类别名字和id建立索引
    def catid2name(coco):
        classes = dict()
        for cat in coco.dataset['categories']:
            classes[cat['id']] = cat['name']
        return classes


    # 将[xmin,ymin,xmax,ymax]转换为yolo格式[x_center, y_center, w, h](做归一化)
    def xyxy2xywhn(object, width, height):
        cat_id = object[0]
        xn = object[1] / width
        yn = object[2] / height
        wn = object[3] / width
        hn = object[4] / height
        out = "{} {:.5f} {:.5f} {:.5f} {:.5f}".format(cat_id, xn, yn, wn, hn)
        return out


    def save_anno_to_txt(images_info, save_path):
        filename = images_info['filename']
        txt_name = filename[:-3] + "txt"
        with open(os.path.join(save_path, txt_name), "w") as f:
            for obj in images_info['objects']:
                line = xyxy2xywhn(obj, images_info['width'], images_info['height'])
                f.write("{}\n".format(line))


    # 利用cocoAPI从json中加载信息
    def load_coco(anno_file, xml_save_path):
        if not os.path.exists(xml_save_path):
            # shutil.rmtree(xml_save_path)
            os.makedirs(xml_save_path)

        coco = COCO(anno_file)
        classes = catid2name(coco)
        imgIds = coco.getImgIds()
        classesIds = coco.getCatIds()

        with open(os.path.join(output_folder, "classes.txt"), 'w') as f:
            for id in classesIds:
                f.write("{}\n".format(classes[id]))

        for imgId in imgIds:
            info = {}
            img = coco.loadImgs(imgId)[0]
            filename = img['file_name']
            width = img['width']
            height = img['height']
            info['filename'] = filename
            info['width'] = width
            info['height'] = height
            annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
            anns = coco.loadAnns(annIds)
            objs = []
            for ann in anns:
                object_name = classes[ann['category_id']]
                # bbox:[x,y,w,h]
                bbox = list(map(float, ann['bbox']))
                xc = bbox[0] + bbox[2] / 2.
                yc = bbox[1] + bbox[3] / 2.
                w = bbox[2]
                h = bbox[3]
                obj = [ann['category_id'], xc, yc, w, h]
                objs.append(obj)
            info['objects'] = objs
            save_anno_to_txt(info, xml_save_path)


    def parseJsonFile(json_path, txt_save_path):
        assert os.path.exists(json_path), "json path:{} does not exists".format(json_path)
        if not os.path.exists(txt_save_path):
            # shutil.rmtree(txt_save_path)
            os.makedirs(txt_save_path)

        assert json_path.endswith('json'), "json file:{} It is not json file!".format(json_path)

        load_coco(json_path, txt_save_path)

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
    txt_save_path =  os.path.join(output_folder,'labels')
    parseJsonFile(json_path, txt_save_path)

    image_path = os.path.join(input_folder,'images')
    output_image_path = os.path.join(output_folder,'images')
    copy_images(image_path, output_image_path)

    return


if __name__ == '__main__':
    input_folder = './test_data/input/coco/'
    output_folder = './test_data/output/coco2yolo/'
    COCO2YOLO(input_folder, output_folder)


