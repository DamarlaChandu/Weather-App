import requests
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from PIL import Image, ImageTk

# API Configuration
API_KEY = "8af49577337bf619015c644ac3e664f6"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Weather Image Mapping (fixed with raw strings for Windows paths)
WEATHER_IMAGES = {
    "clear": r"C:\Users\damar\OneDrive\Desktop\weather app\clear.png",
    "clouds": r"C:\Users\damar\OneDrive\Desktop\weather app\clouds.png",
    "rain": r"C:\Users\damar\OneDrive\Desktop\weather app\rain.png",
    "snow": r"C:\Users\damar\OneDrive\Desktop\weather app\snow.png",
    "thunderstorm": r"C:\Users\damar\OneDrive\Desktop\weather app\thunderstorm.png",
    "drizzle": r"C:\Users\damar\OneDrive\Desktop\weather app\drizzle.png",
    "mist": r"C:\Users\damar\OneDrive\Desktop\weather app\mist.png",
    "fog": r"C:\Users\damar\OneDrive\Desktop\weather app\fog.png"
}

# Fetch Weather Data
def get_weather(city_name):
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            main = data['main']
            weather = data['weather'][0]
            wind = data['wind']
            sys = data['sys']

            sunrise = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M')

            return {
                'temp': main['temp'],
                'feels_like': main['feels_like'],
                'humidity': main['humidity'],
                'pressure': main['pressure'],
                'wind_speed': wind['speed'],
                'description': weather['description'],
                'main': weather['main'].lower(),
                'city': data['name'],
                'country': sys['country'],
                'sunrise': sunrise,
                'sunset': sunset
            }
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Weather App Class
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WeatherWise Animated")
        self.root.geometry("1000x600")
        self.root.configure(bg="#A7C7E7")
        self.setup_ui()

    def setup_ui(self):
        # Left Frame
        self.left_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # Right Frame
        self.right_frame = tk.Frame(self.root, bg="#B3E5FC")
        self.right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # Left Frame Widgets
        self.city_entry = ttk.Entry(self.left_frame, font=("Poppins", 18))
        self.city_entry.pack(pady=30, padx=20)

        self.search_btn = ttk.Button(self.left_frame, text="Search Weather", command=self.fetch_weather)
        self.search_btn.pack(pady=15)

        self.temp_label = tk.Label(self.left_frame, text="--°C", font=("Poppins", 48, "bold"), bg="#E0F7FA", fg="#00796B")
        self.temp_label.pack(pady=10)

        self.desc_label = tk.Label(self.left_frame, text="Description", font=("Poppins", 24), bg="#E0F7FA", fg="#004D40")
        self.desc_label.pack(pady=5)

        self.extra_info = tk.Label(self.left_frame, text="Humidity: --%\nPressure: --hPa\nWind: --km/h", 
                                   font=("Poppins", 16), bg="#E0F7FA", fg="#00695C", justify="left")
        self.extra_info.pack(pady=20)

        self.sun_times = tk.Label(self.left_frame, text="Sunrise: --\nSunset: --", 
                                  font=("Poppins", 16), bg="#E0F7FA", fg="#00695C")
        self.sun_times.pack(pady=10)

        # Right Frame Image Area
        self.image_label = tk.Label(self.right_frame, bg="#B3E5FC")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

    def fetch_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Warning", "Enter a city name")
            return

        weather = get_weather(city)
        if weather:
            self.update_display(weather)
        else:
            messagebox.showerror("Error", "City not found or API error.")

    def update_display(self, weather):
        self.temp_label.config(text=f"{weather['temp']:.1f}°C")
        self.desc_label.config(text=weather['description'].capitalize())
        self.extra_info.config(
            text=f"Humidity: {weather['humidity']}%\nPressure: {weather['pressure']} hPa\nWind: {weather['wind_speed']} km/h")
        self.sun_times.config(text=f"Sunrise: {weather['sunrise']}\nSunset: {weather['sunset']}")

        self.current_weather_main = weather['main']
        self.show_image()

    def show_image(self):
        image_path = WEATHER_IMAGES.get(self.current_weather_main, WEATHER_IMAGES["clear"])
        try:
            img = Image.open(image_path)
            img = img.resize((350, 350), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img_tk)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label.config(image=None)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()