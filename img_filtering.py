import cv2
import numpy as np

# 初始化高斯滤波参数，调节可拖动的最小值和最大值在45行，47行   图片地址在第9行
kernel_size = 5
sigma = 1
border_type = cv2.BORDER_DEFAULT

# 读取图片（请修改图片地址），可以改为绝对坐标 如果图片在程序文件的相同目录下，只需要改为名字就可以
image_path = './assets/3.png'
original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

if original_image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")


# 定义滑动条回调函数
def update_image(x):
    global kernel_size, sigma, border_type
    try:
        kernel_size = cv2.getTrackbarPos('Kernel Size', 'Gaussian Filter') * 2 + 1
        sigma = cv2.getTrackbarPos('Sigma', 'Gaussian Filter')
        border_type_index = cv2.getTrackbarPos('Border Type', 'Gaussian Filter')

        border_types = [
            cv2.BORDER_CONSTANT, cv2.BORDER_REPLICATE, cv2.BORDER_REFLECT,
            cv2.BORDER_WRAP, cv2.BORDER_REFLECT_101, cv2.BORDER_DEFAULT,
            cv2.BORDER_TRANSPARENT
        ]
        border_type = border_types[border_type_index]

        if kernel_size % 2 == 0:
            kernel_size += 1

        filtered_image = cv2.GaussianBlur(original_image, (kernel_size, kernel_size), sigma, borderType=border_type)
        cv2.imshow('Gaussian Filter', filtered_image)
    except cv2.error as e:
        print("Error accessing trackbar value:", e)


# 创建窗口
cv2.namedWindow('Gaussian Filter')
# FIXME: setup window size for created windows

# 创建滑动条 这里可以改变滑动条的可以拖动的最小值和最大值
cv2.createTrackbar('Kernel Size', 'Gaussian Filter', 2, 101, update_image)
# Kernel Size 是卷积核大小因此，通过调整 Kernel Size 的大小，可以控制图像在进行高斯滤波时的模糊程度和效果。，
cv2.createTrackbar('Sigma', 'Gaussian Filter', 1, 50, update_image)
# Sigma 是高斯函数的标准差参数，也称为高斯核的方差。它决定了高斯分布的形状，从而影响了滤波器如何在图像上进行模糊操作。较大的 Sigma 值会导致更多的周围像素对中心像素的影响，从而产生更强的模糊效果。而较小的 Sigma 值则会产生较为锐利的图像，因为只有较近的像素对中心像素产生显著的影响。
cv2.createTrackbar('Border Type', 'Gaussian Filter', 0, 6, update_image)
# 在高斯滤波中，"Border Type"（边界类型）指定了在对图像进行卷积时处理图像边界的方式。

# 初始化滑动条的初始值
cv2.setTrackbarPos('Kernel Size', 'Gaussian Filter', 2)
cv2.setTrackbarPos('Sigma', 'Gaussian Filter', 1)
cv2.setTrackbarPos('Border Type', 'Gaussian Filter', 0)

# 调用一次更新函数以初始化显示
update_image(0)

# 显示初始图像
cv2.imshow('Gaussian Filter', original_image)

while True:
    # BUG: program doesn't exit after close window
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # 按 's' 保存图像
        cv2.imwrite('filtered_image.jpg',
                    cv2.GaussianBlur(original_image, (kernel_size, kernel_size), sigma, borderType=border_type))
    elif key == 27:  # 按 'ESC' 退出程序
        break

cv2.destroyAllWindows()