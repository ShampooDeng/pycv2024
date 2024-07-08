import cv2

# 读取图片（请修改图片地址），可以改为绝对坐标 如果图片在程序文件的相同目录下，只需要改为名字就可以
image_path = './assets/3.png'
# 这里调节边缘检测拖动按钮的最大值和最小值，
#low_threshold 和max_low_threshold  是边缘检测第一阈值可以拖动的最小值和最大值
#high_threshold和 max_low_threshold 是边缘检测第二阈值可以拖动的最小值和最大值
low_threshold = 0
high_threshold = 0

max_high_threshold = 500
max_low_threshold = 100

# 更新边缘检测结果的函数
def update_edge_detection(image, low_thresh, high_thresh):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, low_thresh, high_thresh)
    return edges

# 处理滑动条变化的回调函数
def on_trackbar_change(val):
    global low_threshold, high_threshold, image_path

    image = cv2.imread(image_path)

    low_threshold = cv2.getTrackbarPos('Low Threshold', 'Edge Detection')
    high_threshold = cv2.getTrackbarPos('High Threshold', 'Edge Detection')

    edges = update_edge_detection(image, low_threshold, high_threshold)

    cv2.imshow('Edge Detection', edges)

# 初始化GUI
def main():
    global image_path

    cv2.namedWindow('Edge Detection')

    cv2.createTrackbar('Low Threshold', 'Edge Detection', low_threshold, max_low_threshold, on_trackbar_change)
    cv2.createTrackbar('High Threshold', 'Edge Detection', high_threshold, max_high_threshold, on_trackbar_change)
    # FIXME: setup window size for created windows

    image = cv2.imread(image_path)
    edges = update_edge_detection(image, low_threshold, high_threshold)
    cv2.imshow('Edge Detection', edges)

    while True:
        # BUG: program doesn't exit after close window
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # 按 'esc' 退出
            break
        elif key == ord('s'):  # 按 's' 保存当前显示的图像
            cv2.imwrite('edges_detected.jpg',  update_edge_detection(image, low_threshold, high_threshold))
            print('保存边缘检测结果为 edges_detected.jpg')

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
