import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # 导入 messagebox 用于弹窗提示
from trans_function.YOLO2COCO import YOLO2COCO
from trans_function.YOLO2VOC import YOLO2VOC
from trans_function.COCO2YOLO import COCO2YOLO
from trans_function.COCO2VOC import COCO2VOC
from trans_function.VOC2YOLO import VOC2YOLO
from trans_function.VOC2COCO import VOC2COCO
from trans_function.YOLO_split import YOLO_SPLIT
from trans_function.COCO_split import COCO_SPLIT
from trans_function.VOC_split import VOC_SPLIT
from trans_function.DOTA2YOLO import DOTA2YOLO
import os

YOLO_format = """ 
示例：
（作为输入时，带*的目录请保证名称一样）
yolo
├── classes.txt*
├── images*
│   ├── train_29635.jpg
│   ├── train_29641.jpg
│   ├── train_30090.jpg
│   ...
└── labels*
    ├── train_29635.txt
    ├── train_29641.txt
    ├── train_30090.txt
    ├── train_30092.txt
    ...
"""


COCO_format = """ 
示例：
（作为输入时，带*的目录请保证名称一样）
coco
├── annotation*
│   └── annotation.json*
└── images*
    ├── train_29635.jpg
    ├── train_29641.jpg
    ├── train_30090.jpg
    ├── train_30092.jpg
    ...
"""


VOC_format = """ 
示例：
（作为输入时，带*的目录请保证名称一样）
voc
├── Annotations*
│   ├── train_29635.xml
│   ├── train_29641.xml
│   ├── train_30090.xml
│   ...
└── JPEGImages*
    ├── train_29635.jpg
    ├── train_29641.jpg
    ├── train_30090.jpg
    ...
"""
DOTA_format = """
示例：
（作为输入时，带*的目录请保证名称一样）
DOTA
├── classes.txt*
├── images*
│   ├── g1000.jpg
│   ├── g1001.jpg
│   └── ...
└── labelTxt*
    ├── g1000.txt
    ├── g1001.txt
    ...
"""

def on_select_input(value):
    # 根据选择的输入格式更新文本框内容
    input_text_var.delete(1.0, tk.END)
    if value == "YOLO":
        input_text_var.insert(tk.END, YOLO_format)
    elif value == "COCO":
        input_text_var.insert(tk.END, COCO_format)
    elif value == "VOC":
        input_text_var.insert(tk.END, VOC_format)
    elif value == "DOTA":
        input_text_var.insert(tk.END, DOTA_format)
    else:
        input_text_var.insert(tk.END, "已选择输入格式: ")



def on_select_output(value):
    output_text_var.delete(1.0, tk.END)
    # 根据选择的输出格式更新文本框内容
    if value == "YOLO":
        output_text_var.insert(tk.END, YOLO_format)
    elif value == "COCO":
        output_text_var.insert(tk.END, COCO_format)
    elif value == "VOC":
        output_text_var.insert(tk.END, VOC_format)
    else:
        output_text_var.insert(tk.END, "已选择输出格式: ")



def select_input_folder():
    folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
    input_folder_var.set(folder_selected)  # 设置输入文件夹路径变量

def select_output_folder():
    folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
    output_folder_var.set(folder_selected)  # 设置输出文件夹路径变量

def datas_split_select_input_folder():
    folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
    data_split_input_folder_var.set(folder_selected)  # 设置输入文件夹路径变量

def datas_split_select_output_folder():
    folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
    data_split_output_folder_var.set(folder_selected)  # 设置输出文件夹路径变量



def convert(input_format, output_format, input_folder, output_folder):
    if not input_format or not output_format or not input_folder or not output_folder:
        messagebox.showwarning("警告", "所有字段都必须填写！")  # 弹出警告框
        return

    if input_format == output_format:
        messagebox.showinfo("错误", "输入和输出格式一致")
        return
    
    if input_folder == output_folder:
        messagebox.showinfo("错误", "输入和输出路径一致")
        return
    
    if input_format == 'YOLO':
        if output_format == 'COCO':
            try:
                YOLO2COCO(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return
        if output_format == 'VOC':
            try:
                print('yolo2voc')
                YOLO2VOC(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return



    if input_format == 'COCO':
        if output_format == 'YOLO':
            try:
                COCO2YOLO(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return
        if output_format == 'VOC':
            try:
                COCO2VOC(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return
        




    if input_format == 'VOC':
        if output_format == 'YOLO':
            try:
                VOC2YOLO(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return
        if output_format == 'COCO':
            try:
                VOC2COCO(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return
        
    if input_format == 'DOTA':
        if output_format == 'YOLO':
            try:
                DOTA2YOLO(input_folder, output_folder)
                messagebox.showinfo("转换完成", "文件转换已完成！")
            except:
                messagebox.showinfo("错误", "输入数据格式不规范")
            return
        else:
            messagebox.showinfo("错误", "目前仅支持DOTA转YOLO")
        return

    # # 弹窗提示转换完成
    # messagebox.showinfo("转换完成", "文件转换已完成！")
    if output_format == 'DOTA':
        messagebox.showinfo("错误", "目前仅支持DOTA转YOLO")
        return 
    # 开始转换
    print('开始转换',input_format, output_format)


def data_split(input_dir,output_dir,train,val,test):
    print("input_dir:", input_dir)
    print("output_dir:", output_dir)
    print("train:", train)
    print("val:", val)
    print("test:", test)

    if not input_dir or not output_dir or not train or not val or not test:
        messagebox.showwarning("警告", "所有字段都必须填写！")  # 弹出警告框
        return

    if input_dir == output_dir:
        messagebox.showinfo("错误", "输入和输出目录一致")
        return
    
    train = float(train)
    val = float(val)
    test = float(test)

    if not (0 < train < 1 and 0 < val < 1 and 0 <= test < 1) or round(train + val + test, 10) != 1:
        messagebox.showinfo("错误", "train和val不可为0，且三部分之和为1")
        return

    # 如果一切无误：
    # 判断数据集格式
    if "annotation" in os.listdir(input_dir) and "images" in os.listdir(input_dir):
        print('COCO')
        try:
            COCO_SPLIT(input_dir,output_dir,train,val,test)
            messagebox.showinfo("完成", "COCO数据集划分完成")
        except:
            messagebox.showinfo("错误", "COCO输入数据格式不规范")
        return

    if "labels" in os.listdir(input_dir) and "images" in os.listdir(input_dir) and "classes.txt" in os.listdir(input_dir):
        print('YOLO')
        try:
            YOLO_SPLIT(input_dir,output_dir,train,val,test)
            messagebox.showinfo("完成", "YOLO数据集划分完成")
        except:
            messagebox.showinfo("错误", "YOLO输入数据格式不规范")
        return

    if "Annotations" in os.listdir(input_dir) and "JPEGImages" in os.listdir(input_dir):
        print('VOC')
        try:
            VOC_SPLIT(input_dir,output_dir,train,val,test)
            messagebox.showinfo("完成", "VOC数据集划分完成")
        except:
            messagebox.showinfo("错误", "VOC输入数据格式不规范")
        return



    messagebox.showinfo("错误", "未正确识别数据集格式")
    return


# 创建主窗口
top = tk.Tk()

# 设置窗口标题
top.title("目标检测数据集格式转换")

# 创建输入格式下拉框
input_label = tk.Label(top, text="输入格式")
input_label.grid(row=0, column=0, padx=10, pady=10)

input_options = ['YOLO', 'COCO', 'VOC' , 'DOTA']
input_var = tk.StringVar(value="None")  # 默认值为空字符串
input_menu = tk.OptionMenu(top, input_var, *input_options, command=on_select_input)
input_menu.grid(row=0, column=1, padx=10, pady=10)

# 创建输出格式下拉框
output_label = tk.Label(top, text="输出格式")
output_label.grid(row=0, column=2, padx=10, pady=10)

output_options = ['YOLO', 'COCO', 'VOC']
output_var = tk.StringVar(value="None")  # 默认值为空字符串
output_menu = tk.OptionMenu(top, output_var, *output_options, command=on_select_output)
output_menu.grid(row=0, column=3, padx=10, pady=10)

# -------------------------
# 创建输入格式显示的文本框 (使用 Text 组件)
text_height = 16
input_text_var = tk.Text(top, height=text_height, width=30, wrap=tk.WORD, padx=10, pady=10)
input_text_var.grid(row=1, column=1, padx=10, pady=10)
input_text_var.insert(tk.END, "示例输入格式")  # 默认显示文本
# input_text_var.config(state=tk.DISABLED)  # 设置为只读，防止用户修改

# 创建输出格式显示的文本框 (使用 Text 组件)
output_text_var = tk.Text(top, height=text_height, width=30, wrap=tk.WORD, padx=10, pady=10)
output_text_var.grid(row=1, column=3, padx=10, pady=10)
output_text_var.insert(tk.END, "示例输出格式:")  # 默认显示文本
# output_text_var.config(state=tk.DISABLED)  # 设置为只读，防止用户修改

# -------------------------

# 创建选择输入文件夹按钮
input_folder_label = tk.Label(top, text="选择输入文件夹")
input_folder_label.grid(row=2, column=0, padx=10, pady=10)

input_folder_var = tk.StringVar(value="")  # 用来保存选择的文件夹路径
input_folder_button = tk.Button(top, text="选择输入文件夹", command=select_input_folder)
input_folder_button.grid(row=2, column=1, padx=10, pady=10)

input_folder_path_label = tk.Label(top, textvariable=input_folder_var,wraplength=200)
input_folder_path_label.grid(row=2, column=2, padx=10, pady=10)

# 创建选择输出文件夹按钮
output_folder_label = tk.Label(top, text="选择输出文件夹")
output_folder_label.grid(row=3, column=0, padx=10, pady=10)

output_folder_var = tk.StringVar(value="")  # 用来保存选择的文件夹路径
output_folder_button = tk.Button(top, text="选择输出文件夹", command=select_output_folder)
output_folder_button.grid(row=3, column=1, padx=10, pady=10)

output_folder_path_label = tk.Label(top, textvariable=output_folder_var,wraplength=200)
output_folder_path_label.grid(row=3, column=2, padx=10, pady=10)

# 创建转换按钮
convert_button = tk.Button(top, text="数据集格式转换", command=lambda: convert(input_var.get(), output_var.get(), input_folder_var.get(), output_folder_var.get()))
convert_button.grid(row=4, column=1, columnspan=2, padx=10, pady=20)

# -----------------------------
# 数据集分割  row = 5
# -----------------------------
data_split_input_folder_label = tk.Label(top, text="待划分数据集(自动识别格式)")
data_split_input_folder_label.grid(row=5, column=0, padx=5, pady=10)

data_split_input_folder_var = tk.StringVar(value="")  # 用来保存选择的文件夹路径
data_split_input_folder_button = tk.Button(top, text="选择输入文件夹", command=datas_split_select_input_folder)
data_split_input_folder_button.grid(row=5, column=1, padx=5, pady=10)

data_split_input_folder_path_label = tk.Label(top, textvariable=data_split_input_folder_var,wraplength=200)
data_split_input_folder_path_label.grid(row=5, column=2, padx=5, pady=10)


# 创建选择输出文件夹按钮
data_split_output_folder_label = tk.Label(top, text="划分后数据集输出")
data_split_output_folder_label.grid(row=6, column=0, padx=5, pady=10)

data_split_output_folder_var = tk.StringVar(value="")  # 用来保存选择的文件夹路径
data_split_output_folder_button = tk.Button(top, text="选择输出文件夹", command=datas_split_select_output_folder)
data_split_output_folder_button.grid(row=6, column=1, padx=5, pady=10)

data_split_output_folder_path_label = tk.Label(top, textvariable=data_split_output_folder_var,wraplength=200)
data_split_output_folder_path_label.grid(row=6, column=2, padx=5, pady=10)

# Train Label 和输入框
train_data_split_input_folder_label = tk.Label(top, text="Train (0,1):")
train_data_split_input_folder_label.grid(row=5, column=3, padx=0, pady=0)

train_data_split_input_entry = tk.Entry(top, width=5)  # 修改宽度为 5
train_data_split_input_entry.grid(row=5, column=4, padx=0, pady=0)

# Val Label 和输入框
val_data_split_input_folder_label = tk.Label(top, text="Val (0,1):")
val_data_split_input_folder_label.grid(row=6, column=3, padx=0, pady=0)

val_data_split_input_entry = tk.Entry(top, width=5)  # 修改宽度为 5
val_data_split_input_entry.grid(row=6, column=4, padx=0, pady=0)

# Test Label 和输入框
test_data_split_input_folder_label = tk.Label(top, text="Test [0,1):")
test_data_split_input_folder_label.grid(row=7, column=3, padx=0, pady=0)

test_data_split_input_entry = tk.Entry(top, width=5)  # 修改宽度为 5
test_data_split_input_entry.grid(row=7, column=4, padx=0, pady=0)


# 数据集划分
datasplit_button = tk.Button(top, text="数据集划分", command=lambda: data_split(data_split_input_folder_var.get(), data_split_output_folder_var.get(), train_data_split_input_entry.get(), val_data_split_input_entry.get(), test_data_split_input_entry.get()))
datasplit_button.grid(row=7, column=1, columnspan=2, padx=10, pady=20)






# 数据增强
# 设置窗口大小为 800x600
top.geometry("850x700")

# 固定窗口大小，不可拖动
# top.resizable(False, False)

# 进入消息循环
top.mainloop()

