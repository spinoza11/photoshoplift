class app_settings:
    def __init__(self) -> None:
        self.DEFAULT_SAVE_DIR = "saved"
        self.DEFAULT_OPEN_DIR = "C:/Users/blanche.jay/Desktop/pop_out/saved"
        self.DEFAULT_EXTENSION = ".png"
        self.DEFAULT_SAVE_NAME = "untitled"
        self.save_dir = self.DEFAULT_SAVE_DIR
        self.open_dir = self.DEFAULT_OPEN_DIR
        self.save_name = self.DEFAULT_SAVE_NAME
        self.extension=self.DEFAULT_EXTENSION
        self.im_width=500
        self.im_height=300
        self.max_width = 1920
        self.max_height = 1080
        self.mode='RGB'
        self.background_color="#808080"
        self.supported_exensions = [".png",".jpg"]
        
        self.paint_color = (0,0,0)
        self.paint_color_2 = (255,255,255)
        self.radius = 15
        self.opacity = 0.2
        self.rotation_angle = -90
        self.fill_tolerance = 64
        self.blur_range = 10
    
    def set_height_and_width(self,value,value2):
        self.im_width=value
        self.im_height=value2