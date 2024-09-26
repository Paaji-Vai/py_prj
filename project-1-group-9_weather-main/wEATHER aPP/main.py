import json
import win32com.client as wincom
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class WeatherApp:
    """Weather App class for fetching and displaying weather information."""

    def __init__(self, api_key):
        """
        Initialize the Weather App with the provided API key.

        Parameters:
            api_key (str): The API key for accessing weather data.
        """
        self.api_key = api_key
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.configure(bg="lightblue")

        self.location_label = tk.Label(self.root, text="Location:")
        self.location_label.grid(row=0, column=0, padx=5, pady=5)

        self.location_entry = tk.Entry(self.root)
        self.location_entry.grid(row=0, column=1, padx=5, pady=5)
        self.location_entry.bind("<Return>", lambda event: self.get_weather_and_speak())

        self.get_weather_button = tk.Button(self.root, text="Get Weather", command=self.get_weather_and_speak)
        self.get_weather_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = tk.Text(self.root, wrap="word", height=10, width=50)
        self.result_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.weather_image_label = tk.Label(self.root)
        self.weather_image_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def get_weather(self, location):
        """
        Fetch weather data for the given location from the OpenWeatherMap API.

        Parameters:
            location (str): The location for which weather data is requested.

        Returns:
            tuple: A tuple containing weather information.
        """
        result = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={self.api_key}')
        if result.json()['cod'] == '404':
            messagebox.showerror("Error", "Invalid location!")
            return None, None, None, None, None, None, None, None, None

        weather_data = result.json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temperature = round(weather_data['main']['temp'])
        feels_like = round(weather_data['main']['feels_like'])
        high = round(weather_data['main']['temp_max'])
        low = round(weather_data['main']['temp_min'])
        wind_speed = weather_data['wind']['speed']
        coordinates = weather_data['coord']

        return location, description, icon, temperature, feels_like, high, low, wind_speed, coordinates

    def speak_weather(self, location, description, temperature, feels_like, high, low, wind_speed, coordinates):
        """
        Speak weather information using text-to-speech synthesis.

        Parameters:
            location (str): The location for which weather information is spoken.
            description (str): The weather description.
            temperature (float): The temperature in degrees Celsius.
            feels_like (float): The 'feels like' temperature in degrees Celsius.
            high (float): The highest temperature forecasted for the day in degrees Celsius.
            low (float): The lowest temperature forecasted for the day in degrees Celsius.
            wind_speed (float): The wind speed in meters per second.
            coordinates (dict): Dictionary containing latitude and longitude coordinates.

        Returns:
            str: The spoken weather information.
        """
        speak = wincom.Dispatch("SAPI.SpVoice")
        text = (
            f"The current weather in {location} is {temperature} degrees celsius with {description}. \n"
            f"It feels like {feels_like} degrees celsius. \n"
            f"Today's high is {high} degrees celsius and today's low is {low} degrees celsius. \n"
            f"Wind speed is {wind_speed} meters per second. \n"
            f"The coordinates are latitude {coordinates['lat']} and longitude {coordinates['lon']}."
        )
        print(text)
        speak.Speak(text)
        return text

    def get_weather_and_speak(self):
        """Get weather information for the entered location and speak it."""
        location = self.location_entry.get()
        if location:
            self.result_text.delete(1.0, tk.END)
            location, description, icon, temperature, feels_like, high, low, wind_speed, coordinates = self.get_weather(
                location)
            if location:
                image_url = f"http://openweathermap.org/img/wn/{icon}.png"
                image_data = requests.get(image_url).content
                with open("weather_icon.png", "wb") as f:
                    f.write(image_data)
                weather_image = Image.open("weather_icon.png")
                weather_image = weather_image.resize((50, 50))
                weather_photo = ImageTk.PhotoImage(weather_image)
                self.weather_image_label.configure(image=weather_photo)
                self.weather_image_label.image = weather_photo

                text = self.speak_weather(location, description, temperature, feels_like, high, low, wind_speed,
                                          coordinates)
                self.result_text.insert(tk.END, text)

    def run(self):
        """Run the Weather App."""
        self.root.mainloop()


if __name__ == "__main__":
    api_key = "c28935aecacc23829b96fcd40ccb38d3"
    app = WeatherApp(api_key)
    app.run()
