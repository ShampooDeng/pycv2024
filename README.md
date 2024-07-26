# pycv2024

本仓库包含了《图像处理与分析》课程中部分基础机器视觉算法的演示程序。主要内容包含：

* 边缘检测(edge detection)
* 灰度变换(gray value transform)
* 图像增强(image enhancement)
* 图像滤波(image filtering)
* 圆/直线检测(line/circle fitting)
* 形态学变换(morphology transform)

主要功能代码参考了[opencv官方教程](https://docs.opencv.org/3.4/d2/d96/tutorial_py_table_of_contents_imgproc.html)，演示程序界面采用[tkinter](https://docs.python.org/3/library/tkinter.html)框架实现，最终可执行程序采用pyinstaller进行打包发布。

## 环境配置

```shell
# conda
conda install -c conda-forge py-opencv matplotlib

# pip
pip install py-opencv matplotlib
```

## 使用

```shell
# 正确配置Python环境后，直接调用Python进行执行
python ./edge_detection.py
# 或   ./gray_value_transform.py
# 或   ./img_enhancement.py
# 或   ./img_filtering.py
# 或   ./line_circle_detection.py
# 或   ./morphology_transform.py
```

## 打包发布

如果需要打包发布，可以考虑使用[pyinstaller](https://pyinstaller.org/en/stable/)对程序进行打包。本项目使用了[multipackage-pyispec](https://github.com/ShampooDeng/multipackage-pyispec)脚本生成`pyinstaller`打包配置文件，将多个可执行文件打包至一个文件夹中，以节省空间。

```shell
# 打包仓库中python脚本为可执行文件
python ./multipackage-pyispec/generate_spec.py
pyinstaller ./pycv2024.spec
```
