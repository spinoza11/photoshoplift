import os
from pathlib import Path
from tkinter import filedialog
import random


def save(app):
    if app.current_image:
        app.base_image = app.current_image
        if not app.current_file_path:
            file_path = os.path.join(app.settings.save_dir,f'{app.settings.save_name}{app.settings.extension}')
            my_file = Path(file_path)
            if my_file.is_file():
                filename = f'{app.settings.save_name}_{random.randint(0,999)}{app.settings.extension}'
                file_path = os.path.join(app.settings.save_dir,filename)
            print(file_path)
            app.current_image.save(file_path) 
            app.current_file_path = file_path
        else:
            app.current_image.save(app.current_file_path)
       
    else:
        pass

def save_as(app):
    if app.current_image:
        file_path=filedialog.asksaveasfilename()
        file_name,file_ext=os.path.splitext(file_path)
        if not file_ext:
            file_path= f'{file_path}{app.settings.extension}'
            file_ext=app.settings.extension
        file_path = Path(file_path)
        if not file_path.is_file():
            app.current_image.save(file_path)
            app.base_image = app.current_image
        else:
            #file_path = f'{file_name}_{random.randint(0,999)}{file_ext}'
            app.current_image.save(file_path)
            app.base_image = app.current_image

    else:
        pass

