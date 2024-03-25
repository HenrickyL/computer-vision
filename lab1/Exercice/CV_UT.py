import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

class ColorPicker:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.color_image = None
        self.rgb_label = None
        self.pick_size = 8
        self.pickers = []  # Lista de pickers, cada um com posição e cor própria
        self.dragging_picker = None
        self.picker_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Cores dos pickers
        self.offset = 0

    def load_image(self):
        try:
            image = cv2.imread(self.image_path)
            if image is None:
                raise IOError("Não foi possível carregar a imagem.")
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def create_picker(self, color):
        x = int(self.image.shape[1]/2)
        y = int(self.image.shape[0]/2)
        self.offset += 10
        
        picker = {'color': color, 'position': (x+ self.offset, y+self.offset)}
        self.pickers.append(picker)

    def draw_pickers(self):
        for picker in self.pickers:
            color = self.image[picker['position'][1], picker['position'][0]]
            color_bgr = tuple(int(c) for c in color)
            print(type(color[0]),type(color_bgr[0]), '-', type(picker['color'][0]))
            cv2.circle(self.image, picker['position'], self.pick_size, color_bgr, -1)
            cv2.circle(self.image, picker['position'], self.pick_size+1, (255,255,255), 2)
            cv2.circle(self.image, picker['position'], self.pick_size-1, (0,0,0), 2)
            # cv2.circle(self.image, picker['position'], self.pick_size, picker['color'], 2)
            

    def get_color(self, picker):
        x, y = picker['position']
        if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
            color = self.image[y, x]
            color_image = Image.new('RGB', (30, 30), color=tuple(color))
            self.rgb_label.config(text=f'RGB: {color}')
            self.update_color_label(color_image)

    def update_color_label(self, color_image):
        color_image_tk = ImageTk.PhotoImage(image=color_image)
        self.color_label.configure(image=color_image_tk)
        self.color_label.image = color_image_tk

    def on_click(self, event):
        x, y = event.x, event.y
        for picker in self.pickers:
            px, py = picker['position']
            if abs(px - x) <= self.pick_size and abs(py - y) <= self.pick_size:
                self.dragging_picker = picker
                break

    def on_release(self, event):
        self.dragging_picker = None

    def on_motion(self, event):
        if self.dragging_picker:
            self.dragging_picker['position'] = (event.x, event.y)
            self.get_color(self.dragging_picker)
            self.update_image()

    def update_image(self):
        self.load_image()
        self.draw_pickers()
        self.display_image()

    def display_image(self):
        img = Image.fromarray(self.image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.configure(image=imgtk)
        self.label.image = imgtk

    def start(self):
        self.load_image()
        if self.image is not None:
            root = Tk()
            frame = Frame(root, bd=5)
            frame.pack(side=LEFT)

            self.label = Label(frame, image=None)
            self.label.pack(side=LEFT)

            self.color_label = Label(frame, image=None)
            self.color_label.pack(side=LEFT)

            self.rgb_label = Label(frame, text='')
            self.rgb_label.pack(side=LEFT)

            for color in self.picker_colors:
                self.create_picker(color)

            self.update_image()

            self.label.bind("<ButtonPress-1>", self.on_click)
            self.label.bind("<ButtonRelease-1>", self.on_release)
            self.label.bind("<B1-Motion>", self.on_motion)

            root.mainloop()
