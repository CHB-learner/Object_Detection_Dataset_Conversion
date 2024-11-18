# 导入的模块
import os
import glob
import random
import xml.etree.ElementTree as ET
import datetime
import shutil

def VOC_SPLIT(input_dir,output_dir,train,val,test):    

    # 配置项
    config = {
        # Annotations path(Annotations 的文件夹路径)
        "Annotation":os.path.join(input_dir,'Annotations'),
        # JPEGImages path(JPEGImages 的文件夹路径)
        "JPEGImages":os.path.join(input_dir,'JPEGImages'),
    }


    # 划分数据集


    # 数据划分比例
    # (训练集+验证集)与测试集的比例，默认情况下 (训练集+验证集):测试集 = 9:1

    # 按照比例划分数据集
    train_per = train
    valid_per = val
    test_per = test

    data_xml_list = glob.glob(os.path.join(config['Annotation'], '*.xml'))
    random.seed(666)
    random.shuffle(data_xml_list)
    data_length = len(data_xml_list)

    train_point = int(data_length * train_per)
    train_valid_point = int(data_length * (train_per + valid_per))

    # 生成训练集，验证集, 测试集(8 : 1 : 1)
    train_list = data_xml_list[:train_point]
    valid_list = data_xml_list[train_point:train_valid_point]
    test_list = data_xml_list[train_valid_point:]

    # 生成label标签:
    label = set()
    for xml_path in data_xml_list:
            label = label | set([i.find('name').text for i in ET.parse(xml_path).findall('object')])


    # 输出路径
    now = datetime.datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    out_put_name = f'YOLO_{train}_{val}_{test}__{folder_name}'
    output_dir = os.path.join(output_dir, out_put_name)
    os.makedirs(output_dir, exist_ok=True)

    shutil.copytree(config['Annotation'], os.path.join(output_dir,'Annotations'))
    shutil.copytree(config['JPEGImages'], os.path.join(output_dir,'JPEGImages'))

    # 写入文件中
    ftrain = open(os.path.join(output_dir,'train.txt'), 'w')
    fvalid = open(os.path.join(output_dir,'valid.txt'), 'w')
    ftest = open(os.path.join(output_dir,'test.txt'), 'w')
    flabel = open(os.path.join(output_dir,'label.txt'), 'w')


    for i in train_list:
            i = './Annotations' + i.split('Annotations')[-1]
            ftrain.write(i + "\n")
    for j in valid_list:
            j = './Annotations' + j.split('Annotations')[-1]
            fvalid.write(j + "\n")
    for k in test_list:
            k = './Annotations' + k.split('Annotations')[-1]
            ftest.write(k + "\n")
    for l in label:
            # l = './Annotations' + l.split('Annotations')[-1]
            flabel.write(l + "\n")
    ftrain.close()
    fvalid.close()
    ftest.close()
    flabel.close()
    print("总数据量:{}, 训练集:{}, 验证集:{}, 测试集:{}, 标签:{}".format(len(data_xml_list), len(train_list), len(valid_list), len(test_list), len(label)))
    print("done!")


    return

if __name__ == '__main__':
    input_folder = './test_data/input/voc/'
    output_folder = './test_data/output/'
    
    VOC_SPLIT(input_folder, output_folder, 0.5, 0.5, 0)
