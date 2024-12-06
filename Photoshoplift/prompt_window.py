import tkinter as tk
from app_settings import app_settings

number_inputs = []


class prompt_window:
    def __init__(
        self,
        settings: app_settings,
        caller_name: str,
        number_inputs_names: list,
        buttons: list,
    ) -> None:
        self.window = tk.Toplevel(background=settings.background_color)
        self.window.title(f"{caller_name}")
        inputs = [(name, 0) for name in number_inputs_names]
        self.field_names = []
        self.fields = []
        for i in range(len(inputs)):

            self.field_names.append(
                tk.Label(
                    self.window, text=f"{inputs[i][0]}", background=self.app.body_bg
                ).grid(row=i, column=0, sticky="W", padx=10, pady=10)
            )
            self.field_names.append(
                tk.Entry(self.window, width=20).grid(
                    row=i, column=1, sticky="E", padx=10, pady=10
                )
            )
        self.a = tk.Entry(self.window, width=20)
        self.a.insert(0, f"{self.width}")
        self.a.grid(row=i, column=1, sticky="E", padx=10, pady=10)
        self.title2 = tk.Label(
            self.window, text="height", background=settings.background_color
        ).grid(row=1, column=0, sticky="W", padx=10, pady=10)
        self.b = tk.Entry(self.window, width=20)
        self.b.insert(0, f"{self.height}")
        self.b.grid(row=1, column=1, sticky="W", padx=10, pady=10)
        save_button = tk.Button(
            self.window, text="Ok", command=self.ok, padx=20, pady=10
        )
        save_button.grid(row=2, column=1, columnspan=2, sticky="EW", padx=10, pady=10)
        self.window.bind_all("<Return>", self.ok)

    def ok(self, event=None):
        try:
            w = int(self.a.get())
            h = int(self.b.get())
            if w < self.app.settings.max_width and h < self.app.settings.max_height:
                self.app.settings.im_width = w
                self.app.settings.im_height = h
                self.window.destroy()
                self.app.create_image()
                self.app.new_button = tk.Button(
                    self.window,
                    text="New image",
                    fg=self.fg,
                    font=self.font,
                    activeforeground=self.fg,
                    bd=0,
                    relief="flat",
                    activebackground=self.button_abg,
                    bg=self.button_pbg,
                    command=lambda: new_image_window(self.app),
                    padx=20,
                    pady=10,
                )
                self.app.new_button.grid(row=0, column=0, sticky="W", padx=10, pady=10)

        except Exception as e:
            print(e)
