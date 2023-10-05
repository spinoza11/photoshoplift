#source C:/Users/blanche.jay/Anaconda3/Scripts/activate ai4t
import os
#from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor

import cv2
import numpy
from PIL import Image, ImageTk

import filters
#import random
#from screeninfo import get_monitors
from app_settings import app_settings
from new_image_window import new_image_window
from save import save, save_as

property
#ToDo:
"""
 - save settings to file / open settings from file [LATER]
 - paint bucket
 - a brush that changes only the opacity of existing pixels
 - add transparency / RGBA gestion
 - ctrl Z / Y on full brushstroke
 - bezier curve for brush stroke
 - Size menu when creating image
"""

#Issues
"""
#Issue: performance of draw_numpy
#Fix: rewrite the draw_numpy funcitons to work with cv2
"""

class app:
    def __init__(self) -> None:
        self.settings = app_settings()
        #colors : backgrounds
        self.body_bg='#777777'
        self.header_bg="#333333"
        self.footer_bg="#333333"
        #colors : buttons
        self.button_pbg='#888888'
        self.button_abg='#000000'

        #font
        self.fg='#ffffff'
        self.body_fg='#000000'
        self.font_name="Helvetica"
        self.font_file = None
        self.font_size = 12
        self.font = f'{self.font_name} {self.font_size}'
        #self.window size
        self.width = 300
        self.height = 500
        #location on screen
        self.location_x = 400
        self.location_y = 300

        #title
        self.app_name = "Pop_out"
        #create self.window
        if __name__=='__main__':
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel()
        #self.window.geometry(f"{self.width}x{self.height}+{self.location_x}+{self.location_y}") #Whatever size
        self.window.title(self.app_name)
        self.window.configure(background=self.body_bg)
        self.current_tool = "opacity_brush"
        self.last_click = "left"
        self.current_image = None
        self.current_image_photo = None
        self.motion_list = []
        self.undo_history = []
        self.current_file_path = None
        self.tk_image = None

        #menu
        self.menubar = tk.Menu(self.window,fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg)
        self.window.config(menu= self.menubar)
        file_menu = tk.Menu( self.menubar,tearoff=0,fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg)
        file_menu.add_command(label='New',command = lambda: new_image_window(self))
        file_menu.add_command(label='Open',command = lambda: open(self))
        file_menu.add_command(label='save',command = lambda: save(self))
        file_menu.add_command(label='save as',command = lambda: save_as(self))
        file_menu.add_command(label='Close',command = lambda: close(self))

        self.menubar.add_cascade(label="File",menu=file_menu)
        
        filter_menu = tk.Menu( self.menubar,tearoff=0,fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg)
        filter_menu.add_command(label='Gaussian blur',command = lambda: filters.gaussian_blur(self))
        filter_menu.add_command(label='Rotate 90°',command = lambda: filters.rotate_90(self))
        filter_menu.add_command(label='Invert',command = lambda: filters.invert(self))

        self.menubar.add_cascade(label="Filters",menu=filter_menu)
        #New image
        self.new_button = tk.Button(self.window, text = "New image",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: new_image_window(self), padx=20,pady=10)
        #self.new_button.pack( padx=10, pady=10)
        self.new_button.grid(row = 0, column = 0, sticky = "W",padx = 10, pady = 10)
        #save current image
        save_button = tk.Button(self.window, text = "Save",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: save(self), padx=20,pady=10)
        #save_button.pack( padx=10, pady=10)
        save_button.grid(row = 1, column = 0, sticky = "W",padx = 10, pady = 10)

        #save current image as
        save_button = tk.Button(self.window, text = "Save as",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: save_as(self), padx=20,pady=10)
        #save_button.pack( padx=10, pady=10)
        save_button.grid(row = 2, column = 0, sticky = "W",padx = 10, pady = 10)

        #open image
        open_button = tk.Button(self.window, text = "Open",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: open(self), padx=20,pady=10)
        #open_button.pack( padx=10, pady=10)
        open_button.grid(row = 3, column = 0, sticky = "W",padx = 10, pady = 10)

        #close app button
        close_button = tk.Button(self.window, text = "Close \n without saving",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: close(self), padx=20,pady=10)
        #close_button.pack( padx=10,pady=10)
        close_button.grid(row = 4, column = 0, sticky = "W",padx = 10, pady = 10)
       
        #colored border for left color chooser button
        self.border_l = tk.Frame( self.window,background= '#%02x%02x%02x' %(self.settings.paint_color))
        #left color chooser button
        color_button_l = tk.Button(self.border_l, text = "Color L",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: self.change_color_l())
        color_button_l.pack(padx=10)
        self.border_l.grid(row = 0, column = 2, columnspan=2, sticky = "W",padx = 10, pady = 10)

        self.border_r = tk.Frame( self.window,background= '#%02x%02x%02x' %(self.settings.paint_color_2))
        #right color chooser button
        color_button_r = tk.Button(self.border_r, text = "Color R",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: self.change_color_r())
        color_button_r.pack(padx=10)
        self.border_r.grid(row = 1, column = 2, columnspan=2 ,sticky = "W",padx = 10, pady = 10)

        radius_label = tk.Label(self.window,text = "Radius: " , fg=self.body_fg,font=self.font,bg = self.body_bg)
        radius_label.grid(row = 2, column = 2,sticky = "W", pady = 10)

        r = self.settings.radius
        self.radius_circle = Image.new(self.settings.mode, size=(2*r, 2*r),color=self.body_bg)
        self.radius_circle_tk = self.brush_round()

        self.radius_image = tk.Label(self.window,image=self.radius_circle_tk, fg=self.fg,font=self.font,bg = self.body_bg)
        self.radius_image.grid(row = 2, column = 3,sticky = "W")

        self.radius_image.bind("<B1-Motion>", self.increase_radius)
        self.radius_image.bind("<B3-Motion>", self.decrease_radius)

        self.opacity_label = tk.Label(self.window,text = f"Opacity:{self.settings.opacity}",bg=self.body_bg,fg=self.body_fg)
        self.opacity_label.grid(row = 3, column = 2,sticky = "W")

        self.opacity_label.bind("<B1-Motion>", self.increase_opacity)
        self.opacity_label.bind("<B3-Motion>", self.decrease_opacity)



        self.opacity_brush_button = tk.Button(self.window, text = "Opacity brush",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: self.set_current_tool("opacity_brush"))
        self.opacity_brush_button.grid(row = 4, column = 2 ,sticky = "W",padx = 10, pady = 10)
        
        self.pencil_button = tk.Button(self.window, text = "Pencil",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: self.set_current_tool("pencil"))
        self.pencil_button.grid(row = 4, column = 3 ,sticky = "W",padx = 10, pady = 10)

        self.pencil_button = tk.Button(self.window, text = "Soft brush",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: self.set_current_tool("soft_brush"))
        self.pencil_button.grid(row = 4, column = 4 ,sticky = "W",padx = 10, pady = 10)
        self.window.mainloop()

    def set_current_tool(self,tool):
        self.current_tool = tool

    def change_color_l(self):
        new_color = askcolor(title="Choose left-click color", initialcolor=self.settings.paint_color)[0]
        if new_color:
            print(new_color)
            self.settings.paint_color = new_color
            self.border_l.configure(background='#%02x%02x%02x' %(self.settings.paint_color))
            self.radius_circle = Image.new(self.settings.mode, size=(2*self.settings.radius, 2*self.settings.radius),color=self.body_bg)
            self.radius_circle_tk = self.brush_round(self.settings.radius)
            self.radius_image.configure(image=self.radius_circle_tk)        

    def change_color_r(self):
        new_color = askcolor(title="Choose right-click color", initialcolor=self.settings.paint_color_2)[0]
        if new_color:
            self.settings.paint_color_2 = new_color
            self.border_r.configure(background='#%02x%02x%02x' %(self.settings.paint_color_2))

    def increase_radius(self,event):
        self.settings.radius = self.settings.radius+self.get_horizontal_movement(event)
        self.radius_circle = Image.new(self.settings.mode, size=(2*self.settings.radius, 2*self.settings.radius),color=self.body_bg)
        self.radius_circle_tk = self.brush_round(self.settings.radius)
        self.radius_image.configure(image=self.radius_circle_tk)

    def decrease_radius(self,event):
        r = self.settings.radius-self.get_horizontal_movement(event)
        if r>0:
            self.settings.radius = r
            self.radius_circle = Image.new(self.settings.mode, size=(2*self.settings.radius, 2*self.settings.radius),color=self.body_bg)
            self.radius_circle_tk = self.brush_round(self.settings.radius)
            self.radius_image.configure(image=self.radius_circle_tk)

    #ToDo: opacity modifier
    def increase_opacity(self,event):
        new_opacity = self.settings.opacity+0.011*self.get_horizontal_movement(event)
        if(new_opacity<=1.01):       
            self.settings.opacity = new_opacity
        self.opacity_label.configure(text = f"Opacity:{self.settings.opacity:.2f}")

    def decrease_opacity(self,event):
        new_opacity = self.settings.opacity-0.011*self.get_horizontal_movement(event)
        if(new_opacity>=0):
            self.settings.opacity = new_opacity
        self.opacity_label.configure(text = f"Opacity:{self.settings.opacity:.2f}")

    def get_horizontal_movement(self,event):
        return 1

    def brush_round(self,radius = None):
        if radius==None:
            r = self.settings.radius
        else:
            r = radius
        img = numpy.array(self.radius_circle)
        cv2.circle(img, (r, r ), r, color = self.settings.paint_color,thickness=-1)
        return ImageTk.PhotoImage(Image.fromarray(img))

    def left_click_action(self,event):
        self.last_click = "left" 
        self.undo_history = []
        img = numpy.array(self.current_image)
        self.motion_list.append(img)
        if self.current_tool =="pencil":
            self.draw(event,img,self.settings.paint_color)
        elif self.current_tool =="soft_brush":
            draw_soft(self,event,img,self.settings.paint_color)
        elif self.current_tool=="opacity_brush":
            draw_numpy(self,event,img,self.settings.paint_color)

    def right_click_action(self,event):
        self.last_click = "right"
        self.undo_history = []
        img = numpy.array(self.current_image)
        self.motion_list.append(img)
        if self.current_tool =="pencil":
            self.draw(event,img,self.settings.paint_color_2)
        if self.current_tool =="soft_brush":
            draw_soft(self,event,img,self.settings.paint_color_2)
        elif self.current_tool=="opacity_brush":
            draw_numpy(self,event,img,self.settings.paint_color_2)

    
    def middle_click_action(self,event):
        #print(event.x,event.y)
        if self.last_click=="left":
            img = numpy.array(self.current_image)
            new_color = (int(img[event.y][event.x][0]),int(img[event.y][event.x][1]),int(img[event.y][event.x][2]))
            self.settings.paint_color = new_color
            self.border_l.configure(background='#%02x%02x%02x' %(self.settings.paint_color))
            self.radius_circle = Image.new(self.settings.mode, size=(2*self.settings.radius, 2*self.settings.radius),color=self.body_bg)
            self.radius_circle_tk = self.brush_round(self.settings.radius)
            self.radius_image.configure(image=self.radius_circle_tk)   
        elif self.last_click=="right":
            img = numpy.array(self.current_image)
            new_color = (int(img[event.y][event.x][0]),int(img[event.y][event.x][1]),int(img[event.y][event.x][2]))
            self.settings.paint_color_2 = new_color
            self.border_r.configure(background='#%02x%02x%02x' %(self.settings.paint_color_2))

    def create_image(self):
        self.current_image = Image.new(self.settings.mode, size=(self.settings.im_width, self.settings.im_height),color=self.settings.background_color)
        self.motion_list = [numpy.array(self.current_image)]
        show_current_image_in_app(self)
    
    
    def create_canvas_test(self):
        self.current_image = Image.new(self.settings.mode, size=(self.settings.im_width, self.settings.im_height),color=self.settings.background_color)
        img =  numpy.array(self.current_image)
        h=len(img)
        w=len(img[0])
        for i in range(h):
            for j in range(w):
                i_dec = int(i/10)
                j_dec=int(j/10)
                if((j_dec/2==int(j_dec/2.0)) and (i_dec/2==int(i_dec/2.0))):
                    img[i][j] = (200,200,200)
                else:
                    img[i][j] = (255,255,255)
        self.current_image = Image.fromarray(img)
        self.motion_list = [numpy.array(self.current_image)]

        show_current_image_in_app(self)
            
    def draw(self,event,image,color):
        img = cv2.circle(image, (event.x, event.y), self.settings.radius, color = color,thickness=-1)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.current_image = Image.fromarray(img)
        show_current_image_in_app(self)

    def get_pixels_square(self,event,img_shape):
        x_max,y_max = img_shape
        list = [(event.x+i,event.y+j) for i,j in range(-self.settings.radius,self.settings.radius) if(event.x+i>0 and event.y+j>0 and event.y+j+i<x_max and event.x+i<y_max)]
        return list

    def get_pixels_round(self,event,img_shape):
        list = []
        x_max,y_max = img_shape
        r = self.settings.radius
        for i in range(-r,r):
            for j in range(-r,r):
                if(i**2+j**2<=r**2):
                    px=event.x+i
                    py=event.y+j
                    if(px>0 and py>0 and py<x_max and px<y_max):
                        list.append((px,py))
        return list
    

    def get_pixels_circle(self,event,img_shape,r):
        list = []
        x_max,y_max = img_shape
        for i in range(-r,r):
            for j in range(-r,r):
                if(i**2+j**2<=r**2):# and(i**2+j**2>=(r-1)**2)):
                    px=event.x+i
                    py=event.y+j
                    if(px>0 and py>0 and py<x_max and px<y_max):
                        list.append((px,py))
        return list
    
    def undo(self,event):
        if(len(self.motion_list)):
            self.undo_history.insert(0, numpy.array(self.current_image ))
            self.current_image =  Image.fromarray(self.motion_list.pop())
            show_current_image_in_app(self)
    
    def redo(self,event):
        if(len(self.undo_history)):
            self.motion_list.append(numpy.array(self.current_image))
            self.current_image = Image.fromarray(self.undo_history.pop(0))
            show_current_image_in_app(self)
            
    def invert_filter(self,event=None):
        filters.invert(self)
    
    def rotate_filter(self, event=None):
        filters.rotate_90(self)

    def flip_filter(self,event=None):
        filters.flip_horizontally(self)

def show_current_image_in_app(app:app):
    #app.window.geometry("")
    app.current_image_photo=ImageTk.PhotoImage(app.current_image)
    if not app.tk_image:
        app.tk_image = tk.Label(app.window, image = app.current_image_photo)
        #app.tk_image.pack(padx=20,pady=20)
        app.tk_image.grid(row = 0, column = 1, rowspan=5)

        
    else:
        app.tk_image.configure(image=app.current_image_photo)
    app.tk_image.bind("<B1-Motion>", app.left_click_action )
    app.tk_image.bind("<Button-1>", app.left_click_action )
    app.tk_image.bind("<B3-Motion>", app.right_click_action )
    app.tk_image.bind("<Button-3>", app.right_click_action )
    app.window.bind_all("<Button-2>", app.middle_click_action )
    app.window.bind_all('<Control-Key-z>', app.undo)
    app.window.bind_all('<Control-Key-y>', app.redo)
    app.window.bind_all('<Control-Key-i>', app.invert_filter)
    app.window.bind_all('<Control-Key-r>', app.rotate_filter)
    app.window.bind_all('<Control-Key-f>', app.flip_filter)

def draw_numpy(app:app,event,img,color):
    list_pixels = app.get_pixels_round(event,img.shape[0:2])
    o1=app.settings.opacity
    o2=1-o1
    for pixels_to_draw in list_pixels:
        for j in range(3):
            img[pixels_to_draw[1]][pixels_to_draw[0]][j] = o1*color[j]+o2*img[pixels_to_draw[1]][pixels_to_draw[0]][j]
    app.current_image = Image.fromarray(img)
    show_current_image_in_app(app)

def draw_soft(app:app,event,img,color):
    o1 = app.settings.opacity*(1/app.settings.radius)
    o2 = 1-o1
    for r in range(1,app.settings.radius):
        
        list_pixels = app.get_pixels_circle(event,img.shape[0:2],r)
        for pixels_to_draw in list_pixels:
            for j in range(3):
                img[pixels_to_draw[1]][pixels_to_draw[0]][j] = o1*color[j]+o2*img[pixels_to_draw[1]][pixels_to_draw[0]][j]
    app.current_image = Image.fromarray(img)
    show_current_image_in_app(app)

def close(app:app):
    if app.tk_image:
        app.undo_history = []
        app.motion_list = []
        app.tk_image.configure(image='',text="No image to show", fg=app.body_fg,font = app.font,bg=app.body_bg)
        #app.window.geometry(f"{app.width}x{app.height}+{app.window.winfo_x()}+{app.window.winfo_y()}")
        app.current_file_path = None
        app.current_image = None
        app.current_image_photo = None

def open(app:app):
    file_path=filedialog.askopenfilename(filetypes=[("JPEG files","*.jpg"),("PNG files", "*.png")])
    file_name,file_ext=os.path.splitext(file_path)

    if file_ext in app.settings.supported_exensions:
        if file_path:
            app.current_image=Image.open(file_path)
            app.motion_list = [numpy.array(app.current_image)]
            show_current_image_in_app(app)
            app.current_file_path = file_path


if __name__ =="__main__":
    app()



