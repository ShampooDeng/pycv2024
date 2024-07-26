import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os
from utils import load_img

data_dir = "./assets/"
window_title = "Image Filtering"


def guassian_filering(mat: np.ndarray, kernel_size, sigma):
    if kernel_size % 2 == 0:
        kernel_size += 1
    filtered_image = cv.GaussianBlur(mat, (kernel_size, kernel_size), sigma, sigma)
    return filtered_image


def medium_filtering(mat: np.ndarray, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv.medianBlur(mat, kernel_size)


def bilateral_filtering(mat: np.ndarray, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv.bilateralFilter(mat, kernel_size, kernel_size*2, kernel_size/2)


class App:
    def __init__(self, window_name) -> None:
        self.filter_methods = [
            "gaussian blur",
            "medium filtering",
            "bilateral filtering",
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

        ## Select filtering method
        filter_method_label = ttk.Label(self.app, text="Filtering method: ")
        filter_method_label.grid(row=1, column=0, padx=10, sticky="e")
        self.filter_type = tk.StringVar(self.app)
        self.filter_type.set(self.filter_methods[0])
        filter_method_dropdown = ttk.Combobox(
            self.app,
            width=27,
            textvariable=self.filter_type,
        )
        filter_method_dropdown["value"] = self.filter_methods
        filter_method_dropdown.grid(row=1, column=1, columnspan=3, padx=10, sticky="we")
        self.filter_type.trace_add("write", self.update_gui)

        ## Slidebar to adjust kernel size
        self.kernel_size = tk.IntVar(self.app)
        self.kernel_size.set(0)
        scalebar = ttk.Scale(
            self.app,
            from_=0,
            to=50,
            variable=self.kernel_size,
            orient="horizontal",
            command=self.update_gui,
        )
        scalebar.grid(row=2, column=1, columnspan=2, padx=20, sticky="we")
        self.kernel_size_label = ttk.Label(
            self.app, text="Kernel size: " + str(self.kernel_size.get())
        )
        self.kernel_size_label.grid(row=2, column=0, padx=20, sticky="e")

        ## Slidebar to adjust upper threshold
        self.sigma = tk.IntVar(self.app)
        self.sigma.set(0)
        scalebar = ttk.Scale(
            self.app,
            from_=0,
            to=25,
            variable=self.sigma,
            orient="horizontal",
            command=self.update_gui,
        )
        scalebar.grid(row=3, column=1, columnspan=2, padx=20, sticky="we")
        self.simga_label = ttk.Label(self.app, text="Sigma: " + str(self.sigma.get()))
        self.simga_label.grid(row=3, column=0, padx=20, sticky="e")

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
        kernel_size = self.kernel_size.get()
        sigma = self.sigma.get()

        filter_type = self.filter_type.get()
        if filter_type == self.filter_methods[0]:
            mat = guassian_filering(mat, kernel_size, sigma)
        elif filter_type == self.filter_methods[1]:
            mat = medium_filtering(mat, kernel_size)
        elif filter_type == self.filter_methods[2]:
            mat = bilateral_filtering(mat, kernel_size)
        else:
            raise ValueError(f"Unknown filtering method {self.filter_type}")
        return mat

    def update_gui(self, *args):
        ## read from image src
        mat = load_img(self.image_src.get())

        ## udpate scalebar value
        self.simga_label.config(text="Sigma: " + str(self.sigma.get()))
        self.kernel_size_label.config(
            text="Kernel size: " + str(self.kernel_size.get())
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
