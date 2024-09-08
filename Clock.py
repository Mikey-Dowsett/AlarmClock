import tkinter
from tkinter import *
from tkinter.ttk import *
import time
import requests, json
from PIL import Image, ImageTk

font = "Nunito"

class Clock(Tk):
    def __init__(self):
        super().__init__()

        self.columnconfigure(0, weight=1)
        self.attributes('-fullscreen', True)
        self.screen_height = self.winfo_screenheight()
        self.smallest_text = int(self.screen_height * 0.05)
        self.medium_text = int(self.screen_height * 0.07)
        self.large_text = int(self.screen_height * 0.08)
        self.small_image = int(self.screen_height * 0.15)
        self.large_image = int(self.screen_height * 0.35)

        # Display the time
        self.clock_frame = Frame()
        self.date_label = Label(self.clock_frame, text="05/25/2024", font=(font, self.large_text))
        self.date_label.pack(anchor='e')
        self.clock_label = Label(self.clock_frame, text="00:00:00", font=(font, self.large_text))
        self.clock_label.pack(anchor='e')
        self.clock_frame.grid(row=0, column=1, pady=20, padx=20, sticky='nesw')
        self.update_clock()

        # Get and Display current weather
        self.api_key_weather = ""
        self.base_url_weather = "http://api.openweathermap.org/data/3.0/onecall?"
        self.complete_url_weather = self.base_url_weather + "lat=38&lon=-94&appid=" + self.api_key_weather + "&units=metric"

        #Create all the weather components
        self.weather_frame = Frame()
        self.current_temp_label = Label(self.weather_frame, text="25", font=(font, self.medium_text))
        self.feels_like_temp_label = Label(self.weather_frame, text="25", font=(font, int(self.smallest_text/2)))
        self.weather_image_label = Label(self.weather_frame)
        self.current_weather_label = Label(self.weather_frame, text="Thunderstorm", font=(font, self.large_text))

        #Place all the weather components
        self.weather_image_label.grid(row=0, rowspan=6, column=0, sticky='nw')
        self.current_weather_label.grid(row=1, column=1, padx=20, sticky="w")
        self.current_temp_label.grid(row=2, column=1, padx=20, sticky="w")
        self.feels_like_temp_label.grid(row=3, column=1, padx=20, sticky="w")
        self.weather_frame.grid(row=0, column=0, pady=10, padx=10, sticky='nw')

        #High Low Frame
        self.high_low_frame = Frame()
        self.temp_low_image = ImageTk.PhotoImage(Image.open("Images/lowtemp.png").resize((self.small_image, self.small_image)))
        self.temp_low_image_label = Label(self.high_low_frame, image=self.temp_low_image)
        self.temp_low_label = Label(self.high_low_frame, text="20", font=(font, self.smallest_text))
        self.temp_high_image = ImageTk.PhotoImage(Image.open("Images/hightemp.png").resize((self.small_image, self.small_image)))
        self.temp_high_image_label = Label(self.high_low_frame, image=self.temp_high_image)
        self.temp_high_label = Label(self.high_low_frame, text="25", font=(font, self.smallest_text))

        self.temp_low_image_label.grid(row=0, column=0)
        self.temp_low_label.grid(row=0, column=1)
        self.temp_high_image_label.grid(row=0, column=2, padx=(20,0))
        self.temp_high_label.grid(row=0, column=3)
        self.high_low_frame.grid(row=1, column=0, pady=10, padx=10, sticky='nw')

        #Other Weather Data
        self.weather_data_frame = Frame()
        #Humidity Frame
        self.humidity_frame = Frame(self.weather_data_frame)
        self.humidity_image = ImageTk.PhotoImage(Image.open("Images/humidity.png").resize((self.small_image, self.small_image)))
        self.humidity_image_label = Label(self.humidity_frame, image=self.humidity_image)
        self.humidity_label = Label(self.humidity_frame, text="15", font=(font, self.smallest_text))
        self.humidity_image_label.grid(row=0, column=0, sticky='n')
        self.humidity_label.grid(row=0, column=1)
        self.humidity_frame.grid(row=0, column=0, pady=10, padx=10, sticky='nw')

        #UV Frame
        self.uv_frame = Frame(self.weather_data_frame)
        self.uv_image = ImageTk.PhotoImage(Image.open("Images/uv.png").resize((self.small_image, self.small_image)))
        self.uv_image_label = Label(self.uv_frame, image=self.uv_image)
        self.uv_label = Label(self.uv_frame, text="15", font=(font, self.smallest_text))
        self.uv_image_label.grid(row=0, column=0, sticky='n')
        self.uv_label.grid(row=0, column=1)
        self.uv_frame.grid(row=0, column=1, pady=10, padx=10, sticky='nw')

        self.weather_data_frame.grid(row=2, column=0, pady=10, padx=10, sticky='nw')

        self.update_weather()

    #Update the time
    def update_clock(self):
        hours = time.strftime('%H')
        minutes = time.strftime('%M')
        seconds = time.strftime('%S')
        self.clock_label.config(text=f'{hours}:{minutes}:{seconds}')
        self.date_label.config(text=f'{time.strftime("%d %B")}')
        self.after(1000, lambda:self.update_clock())
        if int(minutes) % 30 == 0 and int(seconds) == 0:
            self.update_weather()

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
            self.humidity_label.config(text=weather_data_main["humidity"])
            self.uv_label.config(text=int(round(weather_data_main["uvi"],0)))

            weather_data_daily = weather_data["daily"][0]
            self.temp_low_label.config(text=f"{int(weather_data_daily['temp']['min'])}\u00B0")
            self.temp_high_label.config(text=f"{int(weather_data_daily['temp']['max'])}\u00B0")

            self.weather_image = Image.open("Images/" + weather_data_weather["icon"] + ".png")
            self.weather_image = ImageTk.PhotoImage(self.weather_image.resize((self.large_image, self.large_image)))
            self.weather_image_label.config(image=self.weather_image)

            self.current_weather_label.config(text=weather_data_weather["main"])

if __name__ == "__main__":
    window = Clock()
    window.mainloop()