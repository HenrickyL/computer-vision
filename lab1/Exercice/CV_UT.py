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
        self.pickers = []
        self.pickersGroup1 = []
        self.pickersGroup2 = []
        self.onGroup1 = True
        self.dragging_picker = None
        self.offset = 0
        self.count = 0
        
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
        if(self.onGroup1):
            self.pickersGroup1.append(picker)
        else:
            self.pickersGroup2.append(picker)
        self.onGroup1 = not self.onGroup1

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
        
    def draw_img(self, img):
        cv2.imshow(f'img_{self.count}',img)
        self.count +=1
        
    def show_img(self):
        self.count=0
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def calculate_threshold_value(self, color):
        # Converter a cor do picker para o espaço de cores HSV
        color_hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        # Obter o componente de valor (V) da cor HSV
        v_value = color_hsv[2]
        # Definir um fator para ajustar o valor de thresholding
        threshold_factor = 0.8  # Ajuste conforme necessário
        # Calcular o valor de threshold com base no componente de valor (V)
        threshold_value = v_value * threshold_factor
        return threshold_value
    
    def colorVary(self, color, value):
        int8ToInt = lambda c: np.array((c[0], c[1], c[2]), dtype=np.int16)
        c = int8ToInt(color)
        top = c + 10
        bot = c - 10
        top[top>255] = 255
        top[top<0] = 0
        bot[bot>255] = 255
        bot[bot<0] = 0
        return top, bot
    
    def getGroup(self, img, pickerGroup):
        group = []
        im_r, im_g, im_b = cv2.split(img)
        for picker in pickerGroup:
            x,y = picker['position']
            color = img[y, x]
            
            # Calcula a média dos valores R, G e B
            avg_color = np.mean(color)
            
            # Determina qual componente tem o valor mais próximo da média
            diff = np.abs(color - avg_color)
            component_index = np.argmin(diff)
            
            # Escolhe o componente de cor correspondente
            if component_index == 0:
                component = im_r
                print('red')
            elif component_index == 1:
                component = im_g
                print('green')
            else:
                component = im_b
                print('blue')
            
            # Aplica o thresholding no componente escolhido
            ret, mask = cv2.threshold(component, self.calculate_threshold_value(color), 255, cv2.THRESH_BINARY)
            region = cv2.bitwise_and(component, mask)
            # value = self.calculate_threshold_value(color)
            # ret, mask = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
            # top,bot = self.colorVary(color, 10)
            # mask = cv2.inRange(img, top, bot)
            group.append({
                'color': color,
                'mask': mask,
                'region': region,
            })
        return group
    
    def change_color_callback(self, value):
        self.clear_image()
        size = len(self.pickers)
        if  size%2 == 0 and size > 0 :
            # im_r,im_g,im_b = cv2.split(self.image)
            im_hsv = self.image#cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            group1 = self.getGroup(im_hsv, self.pickersGroup1)
            group2 = self.getGroup(im_hsv, self.pickersGroup2)
            
            size = len(group1)
            for i in range(size):
                g1 = group1[i]
                g2 = group2[i]
                self.draw_img(g1['mask'])
                self.draw_img(g2['mask'])
                self.show_img()
                
                im_hsv[g1['mask'] > 0] = g2['color']
                im_hsv[g2['mask'] > 0] = g1['color']

            self.image = im_hsv#cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)
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
