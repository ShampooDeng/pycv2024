import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import os
from utils import load_img

data_dir = "./assets/"
window_title = "Gray value transform"


def thresholding(mat: np.ndarray, window_size: int, adptive_method, const=2):
    if window_size % 2 == 0:
        window_size = window_size + 1
    mat = cv.medianBlur(mat, 5)
    mat = cv.adaptiveThreshold(
        mat,
        255,
        adptive_method,
        cv.THRESH_BINARY,
        window_size,
        const,
    )
    return mat


def histgram_equlize(img: np.ndarray):
    output = np.copy(img)
    output = cv.equalizeHist(img)
    return output


def output_histgram(img: np.ndarray):
    ## compute cfd
    hist, bins = np.histogram(img.flatten(), bins=256, range=[0, 256])
    cfd = np.cumsum(hist)
    cfd_normalized = cfd / cfd.max() * hist.max().astype(float)

    ## plot figure
    fig = plt.figure(figsize=(10, 5))
    fig.add_subplot(121)
    plt.imshow(img, cmap="gray")
    fig.add_subplot(122)
    plt.hist(img.flatten(), bins=256, range=[0, 256], color="r", label="histgram")
    plt.plot(cfd_normalized, "b", label="cfd")
    plt.legend()

    ## draw plot turn it to np.ndarray
    canvas = fig.canvas
    canvas.draw()
    width, height = canvas.get_width_height()
    image_array = np.frombuffer(canvas.tostring_rgb(), dtype="uint8")
    image_array = image_array.reshape(height, width, 3)

    plt.close()
    return image_array


class App:
    def __init__(self, window_name) -> None:
        self.adptive_methods = {
            "gaussian": cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            "mean": cv.ADAPTIVE_THRESH_MEAN_C,
        }
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
        self.app.rowconfigure(1, minsize=30)
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

        ## Spinbox to adjust window size
        self.window_size = tk.IntVar(self.app)
        self.window_size.set(2)
        scalebar = ttk.Spinbox(
            self.app,
            from_=2,
            to=30,
            increment=1,
            textvariable=self.window_size,
            command=self.update_gui,
        )
        scalebar.grid(row=1, column=1, columnspan=1, padx=20, sticky="w")
        self.window_size_label = ttk.Label(
            self.app,
            text="window size: ",
        )
        self.window_size_label.grid(row=1, column=0, padx=20, sticky="e")

        # Checkbox to enable histgram equalization
        self.do_thresholding = tk.BooleanVar((self.app))
        self.do_thresholding.set(False)
        checkbox = ttk.Checkbutton(
            self.app, variable=self.do_thresholding, command=self.update_gui,text= "thresholding"
        )
        checkbox.grid(row=1, column=2, padx=20, sticky="we")
        self.do_equalization = tk.BooleanVar((self.app))
        self.do_equalization.set(False)
        checkbox = ttk.Checkbutton(
            self.app, variable=self.do_equalization, command=self.update_gui,text= "histgram equalization"
        )
        checkbox.grid(row=1, column=3, padx=20, sticky="we")

        ## Selective adaptive thresh method
        adptive_method_label = ttk.Label(self.app, text="adaptive thresholding methods:")
        adptive_method_label.grid(row=2, column=0, padx=10, sticky="e")
        self.adptive_method = tk.StringVar(self.app)
        self.adptive_method.set("gaussian")
        adptive_method_dropdown = ttk.Combobox(
            self.app, width=27, textvariable=self.adptive_method
        )
        adptive_method_dropdown["value"] = list(self.adptive_methods.keys())
        adptive_method_dropdown.grid(
            row=2, column=1, columnspan=3, padx=10, sticky="we"
        )
        self.adptive_method.trace_add("write", self.update_gui)

        ## Display image
        mat = load_img(self.image_src.get())
        mat = self.process_img(mat)
        img_tk = ImageTk.PhotoImage(Image.fromarray(mat))
        self.image_label = ttk.Label(self.app, image=img_tk)
        self.image_label.image = (
            img_tk  # NOTE: Preventing image_tk from being garbage collected
        )
        self.image_label.grid(row=3, column=0, columnspan=4, pady=20)

    def update_window_size(self, input):
        self.window_size = int(input)

    def loop(self):
        self.app.mainloop()

    def process_img(self, mat):
        if self.do_equalization.get():
            mat = histgram_equlize(mat)

        if self.do_thresholding.get():
            method = self.adptive_methods[self.adptive_method.get()]
            window_size = self.window_size.get()
            mat = thresholding(mat, window_size, adptive_method=method)
        output = output_histgram(mat)
        return output

    def update_gui(self, *args):
        ## read from image src
        mat = load_img(self.image_src.get())

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
