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
        self.root = None
        self.pick_size = 8
        self.pickers = []  # Lista de pickers, cada um com posição e cor própria
        self.dragging_picker = None
        self.offset = 0

    def load_image(self):
        try:
            image = cv2.imread(self.image_path)
            if image is None:
                raise IOError("Não foi possível carregar a imagem.")
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def create_picker(self):
        x = int(self.image.shape[1]/2 + self.offset)
        y = int(self.image.shape[0]/2 + self.offset)
        color = self.image[x, y]
        self.offset += 10
        picker = {
            'color': color, 
            'position': (x, y),
            'color_image': None,
            'rgb_label': None,
            'color_label': None,
            'frame': None
        }
        picker['frame'] = Frame(self.root, bd=5)#Frame(picker['rgb_label'])
        picker['frame'].pack(fill=X, pady=1)
        picker['rgb_label'] = Label(picker['frame'], text='')
        picker['rgb_label'].pack(side=RIGHT)
        picker['color_label'] = Label(picker['frame'], image=None)
        picker['color_label'].pack(side=LEFT)
        self.pickers.append(picker)

    def draw_pickers(self):
        for picker in self.pickers:
            color = self.image[picker['position'][1], picker['position'][0]]
            color_bgr = tuple(int(c) for c in color)
            cv2.circle(self.image, picker['position'], self.pick_size, color_bgr, -1)
            cv2.circle(self.image, picker['position'], self.pick_size+1, (255,255,255), 2)
            cv2.circle(self.image, picker['position'], self.pick_size-1, (0,0,0), 2)
            # cv2.circle(self.image, picker['position'], self.pick_size, picker['color'], 2)
            

    def get_color(self, picker):
        x, y = picker['position']
        if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
            color = self.image[y, x]
            color_text = "RGB: ({:03d}, {:03d}, {:03d})".format(color[0], color[1], color[2])
            
            picker['color_image'] = Image.new('RGB', (15, 15), color=tuple(color))
            picker['rgb_label'].config(text=color_text )
            self.update_color_label(picker)
            

    def update_color_label(self, picker):
        color_image_tk = ImageTk.PhotoImage(image=picker['color_image'])
        picker['color_label'].configure(image=color_image_tk)
        picker['color_label'].image = color_image_tk

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
        self.clear_image()
        if self.dragging_picker:
            self.dragging_picker['position'] = (event.x, event.y)
        for picker in self.pickers:
            self.get_color(picker)
        self.update_image()
        
    def clear_image(self, value = None):
        self.load_image()
        self.update_image()
        
    def update_image(self):
        self.draw_pickers()
        self.display_image()

    def display_image(self):
        img = Image.fromarray(self.image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.configure(image=imgtk)
        self.label.image = imgtk
    
    def resize_image(self, value):
        self.clear_image()
        new_width = int(self.image.shape[1] * value)
        new_height = int(self.image.shape[0] * value)
        dim = (new_width, new_height)
        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA) 
        self.update_image()
        
    def change_color_callback(self, value):
        self.clear_image()
        size = len(self.pickers)
        if  size%2 == 0 and size > 0 :
            first_interval = ()
            second_interval = ()
            # im_r,im_g,im_b = cv2.split(self.image)
            im_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            
            for i in range(len(self.pickers)):
                x,y = self.pickers[i]['position']
                color = im_hsv[y, x]
                print(color)
                if( i %2 ==0):
                    first_interval = (*first_interval, np.array(color))
                else:
                    second_interval = (*second_interval, np.array(color))
            if(len(first_interval)>2):
                first_mask = cv2.inRange(self.image, first_interval[0], first_interval[1])
                second_mask = cv2.inRange(self.image, second_interval[0], second_interval[1])
            else:
                first_mask = cv2.inRange(self.image, first_interval[0], first_interval[0])
                second_mask = cv2.inRange(self.image, second_interval[0], second_interval[0])
            im_hsv[first_mask > 0] =first_interval[0]
            im_hsv[second_mask > 0] = second_interval[0]
            self.image = im_hsv
            self.update_image()
            
    def create_picker_callback(self, value):
        try:
            self.create_picker()
            self.update_image()
        except IndexError:
            print('limits')
    def start(self):
        self.load_image()
        if self.image is not None:
            self.root = Tk(screenName='ColorPicker')
            self.frame = Frame(self.root, bd=5)
            self.frame.pack(side=LEFT)

            self.label = Label(self.frame, image=None)
            self.label.pack(side=LEFT)

            # self.color_label = Label(frame, image=None)
            # self.color_label.pack(side=LEFT)

            # self.rgb_label = Label(frame, text='')
            # self.rgb_label.pack(side=LEFT)

            # for color in self.picker_colors:
            #     self.create_picker()

            # self.create_picker_labels()
            self.update_image()
            # self.resize_image(0.5)

            self.label.bind("<ButtonPress-1>", self.on_click)
            self.label.bind("<ButtonRelease-1>", self.on_release)
            self.label.bind("<B1-Motion>", self.on_motion)
            self.root.bind("<space>", self.create_picker_callback)
            self.root.bind("<c>", self.change_color_callback)
            self.root.bind("<r>", self.clear_image)

            self.root.mainloop()
