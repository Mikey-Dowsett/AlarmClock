import random
import tkinter as tk
from tkinter import ttk
import time
import requests
from PIL import Image, ImageTk
import os
import sys
import RenderFont
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

font_family = "Nunito"
BLACK = "#17111a"
WHITE = "#f5efe8"
RED = "#83443e"
BLUE = "#90b5c6"
YELLOW = "#c98d3f"
GREEN = "#9a945c"

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg=BLACK)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.attributes('-fullscreen', True)

        self.screen_height = self.winfo_screenheight()
        self.tiny_text = int(self.screen_height * 0.035)
        self.small_text = int(self.screen_height * 0.045)
        self.medium_text = int(self.screen_height * 0.065)
        self.large_text = int(self.screen_height * 0.09)
        self.tiny_image = int(self.screen_height * 0.08)
        self.small_image = int(self.screen_height * 0.15)
        self.large_image = int(self.screen_height * 0.22)

        # Clock frame on "left" (column 0)
        self.clock_frame = tk.Frame(self, bg=BLACK)
        self.date_label = tk.Label(self.clock_frame, text="05/25/2024", font=(font_family, self.small_text), fg=WHITE,
                                   bg=BLACK)
        self.date_label.pack(anchor='w')  # "left" align inside frame
        self.clock_label = tk.Label(self.clock_frame, text="00:00:00", font=(font_family, self.small_text),
                                    fg=WHITE, bg=BLACK)
        self.clock_label.pack(anchor='w')
        self.cozy_image_label = tk.Label(self.clock_frame, bg=BLACK)
        self.cozy_image_label.pack(pady=(10, 0))
        self.clock_frame.grid(row=0, rowspan=3, column=0, pady=40, padx=40, sticky='nw')

        # Weather frame on right (column 1)
        self.weather_frame = tk.Frame(self, bg=BLACK)

        # Weather ICON
        self.weather_image_label = tk.Label(self.weather_frame, bg=BLACK)
        self.weather_image_label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        # Current TEMP
        self.current_temp_label = tk.Label(self.weather_frame, text="25\u00B0",
                                           font=(font_family, self.small_text, "bold"), fg=WHITE, bg=BLACK)
        self.current_temp_label.grid(row=0, column=1, sticky='e', padx=(0, 10))

        # Weather DESCRIPTION
        self.current_weather_label = tk.Label(self.weather_frame, text="Thunderstorm",
                                              font=(font_family, self.small_text, "bold"), fg=WHITE, bg=BLACK)
        self.current_weather_label.grid(row=0, column=2, sticky='e', padx=(0, 10))

        # High/Low temps below weather_frame, still in column 1 on right
        self.high_low_frame = tk.Frame(self.weather_frame, bg=BLACK)
        self.temp_low_image = ImageTk.PhotoImage(
            Image.open("Images/lowtemp.png").resize((self.tiny_image, self.tiny_image)))
        self.temp_low_image_label = tk.Label(self.high_low_frame, image=self.temp_low_image, bg=BLACK)
        self.temp_low_label = tk.Label(self.high_low_frame, text="20\u00B0", font=(font_family, self.tiny_text),
                                       fg=WHITE, bg=BLACK)
        self.temp_high_image = ImageTk.PhotoImage(
            Image.open("Images/hightemp.png").resize((self.tiny_image, self.tiny_image)))
        self.temp_high_image_label = tk.Label(self.high_low_frame, image=self.temp_high_image, bg=BLACK)
        self.temp_high_label = tk.Label(self.high_low_frame, text="25\u00B0", font=(font_family, self.tiny_text),
                                        fg=WHITE, bg=BLACK)

        self.temp_low_image_label.grid(row=0, column=0)
        self.temp_low_label.grid(row=0, column=1, padx=(5, 20))
        self.temp_high_image_label.grid(row=0, column=2)
        self.temp_high_label.grid(row=0, column=3, padx=(5, 0))

        self.high_low_frame.grid(row=1, column=1, columnspan=2, sticky='e', padx=40, pady=(0, 20))

        # Feels like temp below current temp
        self.feels_like_temp_label = tk.Label(self.weather_frame, text="Feels Like 25\u00B0",
                                              font=(font_family, int(self.small_text * 0.9)), fg="gray70", bg=BLACK)
        self.feels_like_temp_label.grid(row=2, column=1, columnspan=2, sticky='e', pady=(5, 0))

        self.weather_frame.grid(row=0, column=1, sticky='ne', padx=40, pady=30)

        # Humidity and UV info side-by-side below high/low temps on right
        self.weather_data_frame = tk.Frame(self, bg=BLACK)

        # # Humidity
        # self.humidity_frame = tk.Frame(self.weather_data_frame, bg=BLACK)
        # self.humidity_image = ImageTk.PhotoImage(
        #     Image.open("Images/humidity.png").resize((self.small_image, self.small_image)))
        # self.humidity_image_label = tk.Label(self.humidity_frame, image=self.humidity_image, bg=BLACK)
        # self.humidity_label = tk.Label(self.humidity_frame, text="15%", font=(font_family, self.small_text), fg=WHITE,
        #                                bg=BLACK)
        # self.humidity_image_label.pack(side="left")
        # self.humidity_label.pack(side="left", padx=(10, 0))
        # self.humidity_frame.pack(side="left", padx=(0, 30))
        #
        # # UV
        # self.uv_frame = tk.Frame(self.weather_data_frame, bg=BLACK)
        # self.uv_image = ImageTk.PhotoImage(Image.open("Images/uv.png").resize((self.small_image, self.small_image)))
        # self.uv_image_label = tk.Label(self.uv_frame, image=self.uv_image, bg=BLACK)
        # self.uv_label = tk.Label(self.uv_frame, text="15", font=(font_family, self.small_text), fg=WHITE, bg=BLACK)
        # self.uv_image_label.pack(side="left")
        # self.uv_label.pack(side="left", padx=(10, 0))
        # self.uv_frame.pack(side="left")

        self.weather_data_frame.grid(row=2, column=1, sticky='ne', padx=40)



        # Get and Display current weather
        self.api_key_weather = "ecd0981e6c7ecb45051875dd7e89ba19"
        self.base_url_weather = "http://api.openweathermap.org/data/3.0/onecall?"
        self.complete_url_weather = self.base_url_weather + "lat=38&lon=-94&appid=" + self.api_key_weather + "&units=metric"

        self.update_clock()
        self.pick_cozy_image()
        self.update_weather()

    #Update the time
    def update_clock(self):
        #Update clock with custom font
        current_time = time.strftime("%H:%M:%S")
        img = RenderFont.render_clock_text(current_time, BLACK, WHITE, self.medium_text)
        self.clock_label.config(image=img)
        self.clock_label.image = img

        #Update date
        self.date_label.config(text=f'{time.strftime("%d %B")}')
        self.after(1000, lambda:self.update_clock())

        minutes = time.strftime('%M')
        seconds = time.strftime('%S')
        if int(minutes) % 10 == 0 and int(seconds) == 0:
            self.update_weather()
            self.pick_cozy_image()

    def update_weather(self):
        print("Weather Updated")
        response_weather = requests.get(self.complete_url_weather) #Gets the response object
        weather_data = response_weather.json() #Convert json format in python format
        print(weather_data)

        if "cod" not in weather_data:
            weather_data_main = weather_data["current"]
            weather_data_weather = weather_data_main["weather"][0]

            self.current_temp_label.config(text=f"{int(weather_data_main['temp'])}\u00B0")
            self.feels_like_temp_label.config(text=f"Feels Like {int(weather_data_main['feels_like'])}\u00B0")
            # self.humidity_label.config(text=weather_data_main["humidity"])
            # self.uv_label.config(text=int(round(weather_data_main["uvi"],0)))

            weather_data_daily = weather_data["daily"][0]
            self.temp_low_label.config(text=f"{int(weather_data_daily['temp']['min'])}\u00B0")
            self.temp_high_label.config(text=f"{int(weather_data_daily['temp']['max'])}\u00B0")

            self.weather_image = Image.open("Images/" + weather_data_weather["icon"] + ".png")
            self.weather_image = ImageTk.PhotoImage(self.weather_image.resize((self.tiny_image, self.tiny_image)))
            self.weather_image_label.config(image=self.weather_image)

            self.current_weather_label.config(text=weather_data_weather["main"])

    def pick_cozy_image(self):
        self.cozy_image = Image.open(f"Cozy/{random.randrange(0, 9, 1)}.png")
        self.cozy_image = ImageTk.PhotoImage(self.cozy_image.resize((self.large_image, self.large_image)))
        self.cozy_image_label.config(image=self.cozy_image)

if __name__ == "__main__":
    window = Clock()
    window.config(cursor="none")
    window.mainloop()