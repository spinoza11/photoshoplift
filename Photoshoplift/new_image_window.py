import tkinter as tk


class new_image_window:
    def __init__(self,app) -> None:
        self.app = app
        self.window = tk.Toplevel(background=self.app.body_bg)

        self.window.title( "New image")
        self.window.geometry("250x180")
        self.width = app.settings.im_width
        self.height = app.settings.im_height
        self.title1 = tk.Label(self.window, text="width", background=self.app.body_bg).grid(row = 0, column = 0, sticky = "W",padx = 10, pady = 10)
        self.a=tk.Entry(self.window, width=20)
        self.a.insert(0, f"{self.width}")
        self.a.grid(row = 0, column = 1, sticky = "E",padx = 10, pady = 10)
        self.title2 = tk.Label(self.window, text="height",background=self.app.body_bg).grid(row = 1, column = 0, sticky = "W",padx = 10, pady = 10)
        self.b=tk.Entry(self.window, width=20)
        self.b.insert(0, f"{self.height}")
        self.b.grid(row = 1, column = 1, sticky = "W",padx = 10, pady = 10)
        save_button = tk.Button(self.window, text = "Ok",command = self.ok, padx=20,pady=10)
        save_button.grid(row = 2, column = 1, columnspan = 2,sticky = "EW",padx = 10, pady = 10)
        self.window.bind_all("<Return>",self.ok)

    
    def ok(self,event=None):
        try:
            w = int(self.a.get())
            h = int(self.b.get())
            if(w<self.app.settings.max_width and h<self.app.settings.max_height):
                self.app.settings.im_width = w
                self.app.settings.im_height = h
                self.window.destroy()
                self.app.create_image()
                self.app.new_button = tk.Button(self.window, text = "New image",fg=self.fg,font=self.font, activeforeground=self.fg,bd=0,relief='flat' ,\
                activebackground=self.button_abg, bg = self.button_pbg,command = lambda: new_image_window(self.app), padx=20,pady=10)
                self.app.new_button.grid(row = 0, column = 0, sticky = "W",padx = 10, pady = 10)

        except:
            pass