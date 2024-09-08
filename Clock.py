import tkinter
from tkinter import *
from tkinter.ttk import *
import time
import requests, json
from PIL import Image, ImageTk

font = "Goudy Stout"

class Clock(Tk):
    def __init__(self):
        super().__init__()

        self.columnconfigure(0, weight=1)
        self.attributes('-fullscreen', True)
        self.screen_height = self.winfo_screenheight()
        print(self.screen_height)

        # Display the time
        self.clock_frame = Frame()
        self.clock_label = Label(self.clock_frame, text="00:00:00", font=(font, int(self.screen_height * 0.05)))
        self.clock_label.pack()
        self.clock_frame.grid(row=0, column=1, pady=20, padx=20, sticky='ne')
        self.update_clock()

        # Get and Display current weather
        self.api_key_weather = ""
        self.base_url_weather = "http://api.openweathermap.org/data/2.5/weather?"
        self.complete_url_weather = self.base_url_weather + "lat=38&lon=-94&appid=" + self.api_key_weather

        #Create all the weather components
        self.weather_frame = Frame()
        self.current_temp_label = Label(self.weather_frame, text="Temp1", font=(font, int(self.screen_height * 0.04)))
        self.feels_like_temp_label = Label(self.weather_frame, text="Temp2", font=(font, int(self.screen_height * 0.03)))
        self.weather_image_label = Label(self.weather_frame)
        self.current_weather_label = Label(self.weather_frame, text="Weather", font=(font, int(self.screen_height * 0.05)))

        #Place all the weather components
        self.weather_image_label.grid(row=0, rowspan=6, column=0, sticky='nw')
        self.current_weather_label.grid(row=1, column=1, padx=20, sticky="w")
        self.current_temp_label.grid(row=2, column=1, padx=20, sticky="w")
        self.feels_like_temp_label.grid(row=3, column=1, padx=20, sticky="w")
        self.weather_frame.grid(row=0, column=0, pady=10, padx=10, sticky='nw')

        #High Low Frame
        self.high_low_frame = Frame()
        self.temp_low_image = ImageTk.PhotoImage(Image.open("Images/lowtemp.png").resize((int(self.screen_height * 0.1), int(self.screen_height * 0.1))))
        self.temp_low_image_label = Label(self.high_low_frame, image=self.temp_low_image)
        self.temp_low_label = Label(self.high_low_frame, text="20", font=(font, int(self.screen_height * 0.03)))
        self.temp_high_image = ImageTk.PhotoImage(Image.open("Images/hightemp.png").resize((int(self.screen_height * 0.1), int(self.screen_height * 0.1))))
        self.temp_high_image_label = Label(self.high_low_frame, image=self.temp_high_image)
        self.temp_high_label = Label(self.high_low_frame, text="25", font=(font, int(self.screen_height * 0.03)))
        self.temp_low_image_label.grid(row=0, column=0)
        self.temp_low_label.grid(row=0, column=1)
        self.temp_high_image_label.grid(row=0, column=2, padx=(20,0))
        self.temp_high_label.grid(row=0, column=3)
        self.high_low_frame.grid(row=1, column=0, pady=10, padx=10, sticky='nw')

        #Humidity Frame
        self.humidity_frame = Frame()
        self.humidity_image = ImageTk.PhotoImage(Image.open("Images/humidity.png").resize((int(self.screen_height * 0.1), int(self.screen_height * 0.1))))
        self.humidity_image_label = Label(self.humidity_frame, image=self.humidity_image)
        self.humidity_label = Label(self.humidity_frame, text="Humidity", font=(font, int(self.screen_height * 0.03)))
        self.humidity_image_label.grid(row=0, column=0, sticky='n')
        self.humidity_label.grid(row=0, column=1)
        self.humidity_frame.grid(row=2, column=0, pady=10, padx=10, sticky='nw')

        self.update_weather()

    #Update the time
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.after(1000, lambda:self.update_clock())
        if int(time.strftime('%M'))%10 == 0 and int(time.strftime('%S')) == 0:
            self.update_weather()

    def update_weather(self):
        response_weather = requests.get(self.complete_url_weather) #Gets the response object
        weather_data = response_weather.json() #Convert json format in python format

        if weather_data["cod"] != "404":
            print(weather_data)
            weather_data_main = weather_data["main"]
            weather_data_weather = weather_data["weather"][0]

            current_temp = round(weather_data_main["temp"] - 273.15, 1)
            self.current_temp_label.config(text=f"{current_temp}\u00B0")

            feels_like = round(weather_data_main["feels_like"] - 273.15, 1)
            self.feels_like_temp_label.config(text=f"{feels_like}\u00B0")

            self.humidity_label.config(text=weather_data_main["humidity"])
            self.temp_low_label.config(text=round(weather_data_main["temp_min"] - 273.15, 1))
            self.temp_high_label.config(text=round(weather_data_main["temp_max"] - 273.15, 1))

            self.weather_image = Image.open("Images/" + weather_data_weather["icon"] + ".png")
            self.weather_image = ImageTk.PhotoImage(self.weather_image.resize((int(self.screen_height * 0.25), int(self.screen_height * 0.25))))
            self.weather_image_label.config(image=self.weather_image)

            self.current_weather_label.config(text=weather_data_weather["main"])

if __name__ == "__main__":
    window = Clock()
    window.mainloop()