import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os
from enum import Enum, auto
from utils import load_img

data_dir = "./assets/"
window_title = "Edge detection"


class EdgeDetectionMethods(Enum):
    Canny = auto()
    Threshold = auto()


def detect_edge_canny(mat: np.ndarray, lower_threshold, upper_threshold):
    # Apply gaussian blur to denoise image
    blurred = cv.GaussianBlur(mat, (3, 3), 0)
    edges = cv.Canny(blurred, lower_threshold, upper_threshold)
    return edges


def detect_edge_threshold(mat: np.ndarray, lower_threshold, upper_threshold):
    # Gaussian filter the original image
    blurred = cv.GaussianBlur(mat, (5, 5), 0)
    # Threshold the filtered result
    retval, thresholded = cv.threshold(
        blurred, lower_threshold, upper_threshold, cv.THRESH_BINARY
    )
    return thresholded


class App:
    def __init__(self, window_name) -> None:
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
        self.app.rowconfigure(3, weight=1)

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

        ## Selective edge detection methods
        edge_detection_method_label = ttk.Label(
            self.app, text="Edge detection methods: "
        )
        edge_detection_method_label.grid(row=1, column=0, padx=10, sticky="e")
        self.edge_detection_method = tk.StringVar(self.app)
        self.edge_detection_method.set(EdgeDetectionMethods.Canny.name)
        edge_detection_method_dropdown = ttk.Combobox(
            self.app, width=27, textvariable=self.edge_detection_method
        )
        edge_detection_method_dropdown["value"] = [
            item[0] for item in EdgeDetectionMethods.__members__.items()
        ]
        edge_detection_method_dropdown.grid(
            row=1, column=1, columnspan=3, padx=10, sticky="we"
        )
        self.edge_detection_method.trace_add("write", self.update_gui)

        ## Slidebar to adjust lower threshold
        self.lower_threshold = tk.IntVar(self.app)
        self.lower_threshold.set(40)
        scalebar = ttk.Scale(
            self.app,
            from_=0,
            to=255,
            variable=self.lower_threshold,
            orient="horizontal",
            command=self.update_gui,
        )
        scalebar.grid(row=2, column=1, columnspan=2, padx=20, sticky="we")
        self.lower_label = ttk.Label(
            self.app, text="lower threshold: " + str(self.lower_threshold.get())
        )
        self.lower_label.grid(row=2, column=0, padx=20, sticky="e")

        ## Slidebar to adjust upper threshold
        self.upper_threshold = tk.IntVar(self.app)
        self.upper_threshold.set(220)
        scalebar = ttk.Scale(
            self.app,
            from_=0,
            to=255,
            variable=self.upper_threshold,
            orient="horizontal",
            command=self.update_gui,
        )
        scalebar.grid(row=3, column=1, columnspan=2, padx=20, sticky="we")
        self.upper_label = ttk.Label(
            self.app, text="upper threshold: " + str(self.upper_threshold.get())
        )
        self.upper_label.grid(row=3, column=0, padx=20, sticky="e")

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
        lower = self.lower_threshold.get()
        upper = self.upper_threshold.get()
        print(self.edge_detection_method.get())
        if self.edge_detection_method.get() == EdgeDetectionMethods.Canny.name:
            mat = detect_edge_canny(mat, lower, upper)
        elif self.edge_detection_method.get() == EdgeDetectionMethods.Threshold.name:
            mat = detect_edge_threshold(mat, lower, upper)
        return mat

    def update_gui(self, *args):
        ## read from image src
        mat = load_img(self.image_src.get())

        ## udpate scalebar value
        self.upper_label.config(
            text="upper threshold: " + str(self.upper_threshold.get())
        )
        self.lower_label.config(
            text="lower threshold: " + str(self.lower_threshold.get())
        )

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
