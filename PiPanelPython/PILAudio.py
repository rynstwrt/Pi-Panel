import tkinter
from PIL import Image, ImageTk, ImageDraw
from PILVideoCaptures import PILVideoCapture
import pyaudio
import numpy as np
np.set_printoptions(suppress=True)


AUDIO_CHUNK_SIZE = 4096
AUDIO_RATE = 32000


class PILAudio:
    def __init__(self, window, num_cols):
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=AUDIO_RATE,
            input=True,
            frames_per_buffer=AUDIO_CHUNK_SIZE
        )

        self.window = window
        self.num_cols = num_cols

        self.w, self.h = window.winfo_screenwidth(), window.winfo_screenheight()
        self.window.overrideredirect(1)
        self.window.geometry("%dx%d+0+0" % (self.w, self.h))
        self.window.focus_set()    
        self.window.bind("<Button>", lambda e: self.window.destroy())

        self.canvas = tkinter.Canvas(self.window, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='black', cursor="none")

        self.pil_img = Image.new("RGB", (self.w, self.h))
        self.draw = ImageDraw.Draw(self.pil_img)

        self.bar_padding = 25
        self.delay = 15
        self.update()

        self.window.mainloop()

    

    def update(self):
        data = np.frombuffer(self.stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False), dtype=np.int16)
        data = data - np.average(data)

        n = len(data)
        k = np.arange(n)

        tarr = n / float(AUDIO_RATE)
        
        frqarr = k / float(tarr)
        frqarr = frqarr[range(n // 2)]

        data = np.fft.fft(data) / n
        data = abs(data[range(n // 2)])

        y_values = []

        chunked_data = np.split(data, len(data) / (len(data) // self.num_cols))

        for i in range(len(chunked_data)):
            y_value = np.average(chunked_data[i]).astype(np.int64)
            y_values.append(y_value)
        
        y_values = np.array(y_values, dtype=np.int16)
        y_values = list(np.interp(y_values, (y_values.min(), y_values.max()), (10, self.h)))
        print(y_values)

        self.draw.rectangle((0, 0, self.w, self.h), fill=(0, 0, 0, 0))

        bar_width = self.w / self.num_cols - (self.bar_padding / 2)
        for x in range(len(y_values)):
            new_x = x * (bar_width + (self.bar_padding / 2)) 
            y_value = y_values[x] * 20
            y_value = y_values[x]
            self.draw.rectangle([(new_x, self.h - self.bar_padding), (new_x + bar_width, self.h - self.bar_padding - y_value)], fill=(255, 0, 255))


        imgWidth, imgHeight = self.pil_img.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w / imgWidth, self.h / imgHeight)
            imgWidth = int(imgWidth * ratio)
            imgHeight = int(imgHeight * ratio)
            self.pil_img = self.pil_img.resize((imgWidth, imgHeight), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(self.pil_img)
        self.canvas.create_image(self.w / 2, self.h / 2, image=self.photo)
        self.window.after(self.delay, self.update)