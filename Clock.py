from tkinter import *
from tkinter.ttk import *
import time
import requests, json
from PIL import Image, ImageTk

font = "System"

class Clock(Tk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.attributes('-fullscreen', True)

        # Display the time
        self.clock_label = Label(self, text="00:00:00", font=(font, 50))
        self.clock_label.grid(row=0, column=0, pady=20, padx=20)
        self.update_clock()

        # Get and Display current weather
        self.api_key_weather = "ecd0981e6c7ecb45051875dd7e89ba19"
        self.base_url_weather = "http://api.openweathermap.org/data/2.5/weather?"
        self.complete_url_weather = self.base_url_weather + "lat=38&lon=-94&appid=" + self.api_key_weather
        self.weather_image_label = Label()
        self.update_weather()

    #Update the time
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.after(1000, lambda:self.update_clock())

    def update_weather(self):
        response_weather = requests.get(self.complete_url_weather) #Gets the response object
        weather_data = response_weather.json() #Convert json format in python format

        if weather_data["cod"] != "404":
            weather_data_main = weather_data["main"]
            weather_data_weather = weather_data["weather"][0]

            current_temp = round(weather_data_main["temp"] - 273.15, 1)
            current_temp_label = Label(self, text=f"Temp: {current_temp}", font=(font, 30))
            current_temp_label.grid(row=1, column=0)

            feels_like = round(weather_data_main["feels_like"] - 273.15, 1)
            feels_like_temp_label = Label(self, text=f"Feels Like: {feels_like}", font=(font, 20))
            feels_like_temp_label.grid(row=1, column=1)

            humidity = weather_data_main["humidity"]
            humidity_label = Label(self, text=f"Humidity: {humidity}", font=(font, 20))
            humidity_label.grid(row=2, column=0)


            self.weather_image = Image.open("Images/" + weather_data_weather["icon"] + ".png")
            self.weather_image = ImageTk.PhotoImage(self.weather_image.resize((300, 300)))
            self.weather_image_label = Label(self, image=self.weather_image)
            self.weather_image_label.grid(row=0, rowspan=2, column=4)

            current_weather_label = Label(self, text=weather_data_weather["main"], font=(font, 40))
            current_weather_label.grid(row=0, column=3)


if __name__ == "__main__":
    window = Clock()
    window.mainloop()