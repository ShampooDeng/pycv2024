import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os
from utils import load_img

window_title = "Line&Circle fitting"
data_dir = "./assets/"


def line_detection(img: np.ndarray, threshold):
    # extract outlines with Canny algorithm
    dst = cv.Canny(img, 50, 200, None, 3)

    # Convert gray image to BGR for output
    output = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    # Detect lines
    lines = cv.HoughLines(
        dst,
        1,  # resolution of rho, use 1 pixel here
        np.pi / 180,  # resolution of theta, use 1 degree here(in radian)
        threshold,  # the threshold of intersection point to detect a line
    )
    if lines is None :
        print("No line detected")
        return img

    # Draw detected lines
    for line in lines:
        rho = line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv.line(output, pt1, pt2, (0, 255, 0), 1, cv.LINE_AA)
    return output


def circle_detection(img: np.ndarray, threshold):
    output = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    img = cv.medianBlur(img, 5)
    circles = cv.HoughCircles(
        img,
        cv.HOUGH_GRADIENT,
        1,  # The inverse ratio of resolution
        img.shape[0] / 8,  # Minimum distance between detected centers
        param1=100,  # Upper threshold for internel canny edge detector
        param2=threshold,  # threshhold for circle center detection
        maxRadius=30,  # Maxiumn radius
        minRadius=1,  # Miniumn radius
    )
    if circles is None:
        return output

    for circle in circles[0, :]:
        center_x = circle[0].astype(int)
        center_y = circle[1].astype(int)
        radius = circle[2].astype(int)

        # NOTE: center and radius MUST be int
        cv.circle(output, (center_x, center_y), radius, (0, 255, 0), 2)
        cv.circle(output, (center_x, center_y), 1, (0, 0, 255), 3)

    return output


class App:
    def __init__(self, window_name) -> None:
        self.detected_features = [
            "lines",
            "circles",
        ]
        self.config_gui(window_name)

    def config_gui(self, window_name, width=500, height=300):
        self.app = tk.Tk(window_name)
        self.app.title(window_title)
        self.app.minsize(width, height)

        ## config layout
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=1)
        self.app.columnconfigure(2, weight=1)
        self.app.rowconfigure(0, minsize=30)
        self.app.rowconfigure(1, minsize=20)
        self.app.rowconfigure(2, minsize=20)
        self.app.rowconfigure(3, minsize=20)
        self.app.rowconfigure(4, weight=1)

        ## Selective image
        image_src_label = ttk.Label(self.app, text="Image: ")
        image_src_label.grid(row=0, column=0, padx=10, sticky="e")
        self.image_src = tk.StringVar(self.app)
        self.image_src.set("./assets/1.png")
        image_src_dropdown = ttk.Combobox(
            self.app, width=27, textvariable=self.image_src
        )
        image_src_dropdown["value"] = [
            "./assets/" + filename for filename in os.listdir(data_dir)
        ]
        image_src_dropdown.grid(row=0, column=1, columnspan=3, padx=10, sticky="we")
        self.image_src.trace_add("write", self.update_gui)

        ## Select detected feature
        feature_to_detect_label = ttk.Label(self.app, text="Feature to detect:")
        feature_to_detect_label.grid(row=1, column=0, padx=10, sticky="e")
        self.feature_to_detect = tk.StringVar(self.app)
        self.feature_to_detect.set(self.detected_features[0])
        feature_to_detect_dropdown = ttk.Combobox(
            self.app,
            width=27,
            textvariable=self.feature_to_detect,
        )
        feature_to_detect_dropdown["value"] = self.detected_features
        feature_to_detect_dropdown.grid(row=1, column=1, columnspan=3, padx=10, sticky="we")
        self.feature_to_detect.trace_add("write", self.update_gui)

        ## Slidebar to adjust line detection threshold
        self.line_threshold = tk.IntVar(self.app)
        self.line_threshold.set(150)
        scalebar = ttk.Scale(
            self.app,
            from_=80,
            to=180,
            variable=self.line_threshold,
            orient="horizontal",
            command=self.update_gui,
        )
        scalebar.grid(row=2, column=1, columnspan=2, padx=20, sticky="we")
        self.line_threshold_label = ttk.Label(
            self.app, text="Line Detection threshold: " + str(self.line_threshold.get())
        )
        self.line_threshold_label.grid(row=2, column=0, padx=20, sticky="e")

        ## Slidebar to adjust circle detection threshold
        self.circle_threshold = tk.IntVar(self.app)
        self.circle_threshold.set(30)
        scalebar = ttk.Scale(
            self.app,
            from_=10,
            to=50,
            variable=self.circle_threshold,
            orient="horizontal",
            command=self.update_gui,
        )
        scalebar.grid(row=3, column=1, columnspan=2, padx=20, sticky="we")
        self.circle_threshold_label = ttk.Label(
            self.app, text="Line Detection threshold: " + str(self.circle_threshold.get())
        )
        self.circle_threshold_label.grid(row=3, column=0, padx=20, sticky="e")

        ## Display image
        mat = load_img(self.image_src.get())
        mat = self.process_img(mat)
        img_tk = ImageTk.PhotoImage(Image.fromarray(mat))
        self.image_label = ttk.Label(self.app, image=img_tk)
        self.image_label.image = (
            img_tk  # NOTE: Preventing image_tk from being garbage collected
        )
        self.image_label.grid(row=4, column=0, columnspan=3, pady=20)

    def loop(self):
        self.app.mainloop()

    def process_img(self, mat):
        feature_to_detect = self.feature_to_detect.get()
        if feature_to_detect == self.detected_features[0]:
            mat = line_detection(mat, self.line_threshold.get())
        elif feature_to_detect == self.detected_features[1]:
            mat = circle_detection(mat, self.circle_threshold.get())
        else:
            raise NotImplementedError(f"{feature_to_detect} detections method is not implemented")
        return mat

    def update_gui(self, *args):
        ## read from image src
        mat = load_img(self.image_src.get())

        ## update threshold label
        self.line_threshold_label.config(text="Line detection threshold: " + str(self.line_threshold.get()))
        self.circle_threshold_label.config(text="Circle detection threshold: " + str(self.circle_threshold.get()))

        ## update processing result
        result = self.process_img(mat)
        self.img_tk = ImageTk.PhotoImage(Image.fromarray(result))
        self.image_label.config(image=self.img_tk)
        self.image_label.image = (
            self.img_tk  # NOTE: Preventing image_tk from being garbage collected
        )


if __name__ == "__main__":
    app = App(window_title)
    app.loop()