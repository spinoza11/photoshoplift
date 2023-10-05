import cv2
import numpy
from PIL import Image
from main import show_current_image_in_app
from scipy.ndimage import rotate
import tkinter as tk




def gaussian_blur(app):
    if app.current_image:
        app.undo_history = []
        img = numpy.array(app.current_image)
        r=app.settings.blur_range
        if int(r/2)==r/2.0:
            r+=1
        img = cv2.GaussianBlur(img,(r,r),sigmaX=0,sigmaY=0)
        app.current_image = Image.fromarray(img)
        show_current_image_in_app(app)
    else:
        pass

def invert(app):
    if app.current_image:
        app.undo_history = []
        img = numpy.array(app.current_image)
        app.current_image = Image.fromarray(cv2.bitwise_not(img))
        show_current_image_in_app(app)
    else:
        pass

def rotate_90(app):
    if app.current_image:
        app.undo_history = []
        img2 = rotate(app.current_image,-90)
        app.current_image = Image.fromarray(img2,mode="RGB")
        show_current_image_in_app(app)
    else:
        pass

def flip_horizontally(app):
    if app.current_image:
        app.undo_history = []
        img2 =  app.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        app.current_image = img2# Image.fromarray(img2,mode="RGB")
        show_current_image_in_app(app)
    else:
        pass
