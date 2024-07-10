import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os
from utils import load_img

data_dir = "./assets/"
window_title = "Morphology transformation"

def dilation(mat: np.ndarray, kernel: np.ndarray):
    mat = cv.dilate(mat, kernel, iterations=1)
    return mat


def erosion(mat: np.ndarray, kernel: np.ndarray):
    mat = cv.erode(mat, kernel, iterations=1)
    return mat


def opening(mat: np.ndarray, kernel: np.ndarray):
    mat = cv.morphologyEx(mat, cv.MORPH_OPEN, kernel)
    return mat


def closing(mat: np.ndarray, kernel: np.ndarray):
    mat = cv.morphologyEx(mat, cv.MORPH_CLOSE, kernel)
    return mat


class App:
    def __init__(self, window_name) -> None:
        self.operation_options = ["dilation", "erosion", "opening", "closing"]
        self.kernel_type_dict = {
            "rectangle": cv.MORPH_RECT,
            "cross": cv.MORPH_CROSS,
            "ellipse": cv.MORPH_ELLIPSE,
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
        self.app.rowconfigure(0, minsize=50)
        self.app.rowconfigure(1, minsize=20)
        self.app.rowconfigure(2, weight=1)

        ## Selective image
        self.image_src = tk.StringVar(self.app)
        self.image_src.set("./assets/1.png")
        image_src_dropdown = ttk.Combobox(self.app, width = 27, textvariable = self.image_src) 
        image_src_dropdown['value'] = ["./assets/"+ filename for filename in os.listdir(data_dir)]
        image_src_dropdown.grid(row=0, column=0, padx=10, sticky='we')
        self.image_src.trace_add('write', self.update_gui)

        ## Selective operation
        self.operation = tk.StringVar(self.app)
        self.operation.set("dilation")  # Default value
        image_src_dropdown = ttk.Combobox(self.app, width = 27, textvariable = self.operation) 
        image_src_dropdown['value'] = self.operation_options
        image_src_dropdown.grid(row=0, column=1, padx=10, sticky='we')
        self.operation.trace_add('write', self.update_gui)

        ## Selective kernel type
        self.kernel_type = tk.StringVar(self.app)
        self.kernel_type.set("rectangle")  # Default value
        image_src_dropdown = ttk.Combobox(self.app, width = 27, textvariable = self.kernel_type) 
        image_src_dropdown['value'] = list(self.kernel_type_dict.keys())
        image_src_dropdown.grid(row=0, column=2, padx=10, sticky='we')
        self.kernel_type.trace_add('write', self.update_gui)

        ## Scrollbar to adjust kernel size
        self.kernel_size = tk.IntVar(self.app)
        self.kernel_size.set(5)
        scalebar = ttk.Scale(self.app, from_=0, to=50, variable=self.kernel_size, orient="horizontal", command=self.update_gui)
        scalebar.grid(row=1, column=1,columnspan=2, padx=20,sticky='we')
        self.scalelabel = ttk.Label(self.app, text="Kernel size: "+str(self.kernel_size.get()))
        self.scalelabel.grid(row=1, column=0, padx=20,sticky='e')

        ## Display image
        mat = load_img(self.image_src.get())
        mat = self.process_img(mat)
        img_tk = ImageTk.PhotoImage(Image.fromarray(mat))
        self.image_label = ttk.Label(self.app, image=img_tk)
        self.image_label.image = (
            img_tk  # NOTE: Preventing image_tk from being garbage collected
        )
        self.image_label.grid(row=2, column=0, columnspan=3, pady=20)

    def loop(self):
        self.app.mainloop()

    def get_kernel_type(self):
        kernel_type = self.kernel_type.get()
        return self.kernel_type_dict[kernel_type]

    def process_img(self, mat):
        selected_operation = self.operation.get()
        kernel_type = self.get_kernel_type()
        kernel_szie = self.kernel_size.get()
        kernel = cv.getStructuringElement(kernel_type, (kernel_szie, kernel_szie))

        if selected_operation == "dilation":
            return dilation(mat, kernel)
        elif selected_operation == "erosion":
            return erosion(mat, kernel)
        elif selected_operation == "opening":
            return opening(mat, kernel)
        elif selected_operation == "closing":
            return closing(mat, kernel)

    def update_gui(self,*args):
        ## read from image src
        mat = load_img(self.image_src.get())
        ## udpate scalebar value
        self.scalelabel.config(text="Kernel size: "+str(self.kernel_size.get()))
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
