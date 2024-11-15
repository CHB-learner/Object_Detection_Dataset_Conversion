import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # 导入 messagebox 用于弹窗提示
from trans_function.YOLO2COCO import YOLO2COCO
from trans_function.YOLO2VOC import YOLO2VOC
from trans_function.COCO2YOLO import COCO2YOLO
from trans_function.COCO2VOC import COCO2VOC
from trans_function.VOC2YOLO import VOC2YOLO
from trans_function.VOC2COCO import VOC2COCO


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


def on_select_input(value):
    # 根据选择的输入格式更新文本框内容
    input_text_var.delete(1.0, tk.END)
    if value == "YOLO":
        input_text_var.insert(tk.END, YOLO_format)
    elif value == "COCO":
        input_text_var.insert(tk.END, COCO_format)
    elif value == "VOC":
        input_text_var.insert(tk.END, VOC_format)
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
        
    # # 弹窗提示转换完成
    # messagebox.showinfo("转换完成", "文件转换已完成！")

    # 开始转换
    print('开始转换',input_format, output_format)

# 创建主窗口
top = tk.Tk()

# 设置窗口标题
top.title("目标检测数据集格式转换")

# 创建输入格式下拉框
input_label = tk.Label(top, text="输入格式")
input_label.grid(row=0, column=0, padx=10, pady=10)

input_options = ['YOLO', 'COCO', 'VOC']
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

input_folder_path_label = tk.Label(top, textvariable=input_folder_var)
input_folder_path_label.grid(row=2, column=2, padx=10, pady=10)

# 创建选择输出文件夹按钮
output_folder_label = tk.Label(top, text="选择输出文件夹")
output_folder_label.grid(row=3, column=0, padx=10, pady=10)

output_folder_var = tk.StringVar(value="")  # 用来保存选择的文件夹路径
output_folder_button = tk.Button(top, text="选择输出文件夹", command=select_output_folder)
output_folder_button.grid(row=3, column=1, padx=10, pady=10)

output_folder_path_label = tk.Label(top, textvariable=output_folder_var)
output_folder_path_label.grid(row=3, column=2, padx=10, pady=10)

# 创建转换按钮
convert_button = tk.Button(top, text="转换", command=lambda: convert(input_var.get(), output_var.get(), input_folder_var.get(), output_folder_var.get()))
convert_button.grid(row=4, column=1, columnspan=2, padx=10, pady=20)

# 进入消息循环
top.mainloop()