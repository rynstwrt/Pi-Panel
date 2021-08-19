import tkinter
from PIL import Image, ImageTk
from PILVideoCaptures import PILVideoCapture


class PILVideo:
    def __init__(self, window, device_index, video_capture_func=PILVideoCapture):
        self.window = window
        self.device_index = device_index

        self.cap = video_capture_func(device_index)

        self.w, self.h = window.winfo_screenwidth(), window.winfo_screenheight()
        self.window.overrideredirect(1)
        self.window.geometry("%dx%d+0+0" % (self.w, self.h))
        self.window.focus_set()    
        self.window.bind("<Button>", lambda e: self.window.destroy())

        self.canvas = tkinter.Canvas(self.window, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='black', cursor="none")

        self.delay = 17
        self.update()

        self.window.mainloop()

    def update(self):

        frame = self.cap.get_frame()
        pil_image = Image.fromarray(frame).resize((self.w, self.h))

        imgWidth, imgHeight = pil_image.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w / imgWidth, self.h / imgHeight)
            imgWidth = int(imgWidth * ratio)
            imgHeight = int(imgHeight * ratio)
            pil_image = pil_image.resize((imgWidth, imgHeight), Image.ANTIALIAS)
            
        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(self.w / 2, self.h / 2, image=self.photo)
        self.window.after(self.delay, self.update)