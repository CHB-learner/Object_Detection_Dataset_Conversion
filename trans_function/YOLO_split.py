import os  # 用于处理文件路径、创建目录等操作
import random  # 用于生成随机数种子、打乱列表等操作
import shutil  # 用于复制文件
import datetime

def YOLO_SPLIT(input_dir, output_dir, train, val, test):
    # 定义文件夹路径
    image_dir = os.path.join(input_dir, 'images')  # 原始图像所在的子目录
    label_dir = os.path.join(input_dir, 'labels')  # 原始标签所在的子目录

    # 输出路径
    now = datetime.datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    out_put_name = f'YOLO_{train}_{val}_{test}__{folder_name}'
    output_root = os.path.join(output_dir, out_put_name)
    os.makedirs(output_root, exist_ok=True)
    output_dir = output_root

    shutil.copy(os.path.join(input_dir,'classes.txt'), output_dir)

    # 定义训练集、验证集和测试集比例
    train_ratio = train
    valid_ratio = val
    test_ratio = test
    
    # 获取所有图像文件的文件名和扩展名
    image_filenames = [
        os.path.splitext(f) for f in os.listdir(image_dir) 
        if os.path.isfile(os.path.join(image_dir, f))
    ]  # 返回 [(name, ext), ...] 的列表
    
    # 随机打乱文件名列表
    random.shuffle(image_filenames)
    
    # 计算训练集、验证集和测试集的数量
    total_count = len(image_filenames)
    train_count = int(total_count * train_ratio)
    valid_count = int(total_count * valid_ratio)
    test_count = total_count - train_count - valid_count
    
    # 定义输出文件夹路径
    train_image_dir = os.path.join(output_dir, 'train', 'images')
    train_label_dir = os.path.join(output_dir, 'train', 'labels')
    valid_image_dir = os.path.join(output_dir, 'val', 'images')
    valid_label_dir = os.path.join(output_dir, 'val', 'labels')
    test_image_dir = os.path.join(output_dir, 'test', 'images')
    test_label_dir = os.path.join(output_dir, 'test', 'labels')
    
    # 创建输出文件夹
    os.makedirs(train_image_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(valid_image_dir, exist_ok=True)
    os.makedirs(valid_label_dir, exist_ok=True)
    os.makedirs(test_image_dir, exist_ok=True)
    os.makedirs(test_label_dir, exist_ok=True)
    
    # 将图像和标签文件划分到不同的数据集中
    for i, (filename, ext) in enumerate(image_filenames):
        if i < train_count:
            output_image_dir = train_image_dir
            output_label_dir = train_label_dir
        elif i < train_count + valid_count or test == 0 or test == 0.0:
            output_image_dir = valid_image_dir
            output_label_dir = valid_label_dir
        else:
            output_image_dir = test_image_dir
            output_label_dir = test_label_dir
    
        # 复制图像文件
        src_image_path = os.path.join(image_dir, filename + ext)
        dst_image_path = os.path.join(output_image_dir, filename + ext)
        shutil.copy(src_image_path, dst_image_path)
    
        # 复制标签文件（标签文件默认是 .txt 格式）
        src_label_path = os.path.join(label_dir, filename + '.txt')
        dst_label_path = os.path.join(output_label_dir, filename + '.txt')
        if os.path.exists(src_label_path):  # 确保标签存在
            shutil.copy(src_label_path, dst_label_path)

    print(f"数据集已成功划分并保存到: {output_dir}")

if __name__ == '__main__':
    input_folder = './test_data/input/yolo/'
    output_folder = './test_data/output/'
    
    # YOLO_SPLIT(input_folder, output_folder, 0.5, 0.5, 0)
    YOLO_SPLIT(input_folder, output_folder, 0.8, 0.2, 0)

