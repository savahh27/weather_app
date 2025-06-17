import requests
from tkinter import *
from tkinter import messagebox
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


root = Tk()
root.configure(bg="#deecbe")
root.title("Weather")
root.iconbitmap('icons\sun_and_cloud.ico')

e = Entry(root, bd = 4, width=30, font=('Helvetica', 14), bg="#9ce1cf")
e.grid(row=0, column=0, pady=(10, 5))
def touch():
    if not e.get().strip():
        messagebox.showerror("Error", "Enter city name!")
        return
    newWindow = Toplevel()
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": e.get().capitalize(),
            "appid": API_KEY, 
            "units": "metric"
        }
        response = requests.get(url, params=params)
        data = response.json()

        newWindow.title("Weather in " + str(e.get()).capitalize())
        newWindow.configure(bg="#deecbe")

        if data.get("cod") != 200:
            newWindow.destroy()
            messagebox.showerror("Error", data.get("message", "Unknown error"))
            return
        if data["weather"][0]["main"] == "Rain" or data["weather"][0]["main"] == "Drizzle" or data["weather"][0]["main"] == "Thunderstorm":
            newWindow.iconbitmap("icons\rain.ico")
        elif data["weather"][0]["main"] == "Clouds":
            newWindow.iconbitmap("icons\clouds.ico")
        elif data["weather"][0]["main"] == "Clear":
            newWindow.iconbitmap("icons\sunny.ico")
        elif data["weather"][0]["main"] == "Snow":
            newWindow.iconbitmap("icons\snow.ico")
        elif data["weather"][0]["main"] == "Wind":
            newWindow.iconbitmap("icons\wind.ico")
        else:
            newWindow.iconbitmap("icons\sun_and_cloud.ico")

        myLabel = Label(newWindow, text="City: " + data["name"] + "\n" + "Temperature: " + 
                        str(data["main"]["temp"]) + "°C (Feels like: " + str(data["main"]["feels_like"]) + ")\n" + 
                         "Pressure: " + str(data["main"]["pressure"]) + "\nHumidity: " + str(data["main"]["humidity"]) + 
                        "\nBrief description: " + str(data["weather"][0]["main"]) + ", " + 
                        str(data["weather"][0]["description"]),
                        font=("Helvetica", 14), justify=LEFT, bg="#deecbe", fg="#464a3e")
        myLabel.grid(row=0, column=0)
    except KeyError:
        newWindow.destroy()
        messagebox.showerror("Error", "Enter correct city name!")
        

bttn = Button(root, text="Tell Weather", command=touch, font=("Helvetica", 12), 
              activebackground="#c3f7ea", activeforeground="#b9c69c", bd=3, cursor="hand2", bg="#9ce1cf", fg="#6a705d")
bttn.grid(row=1, column=0, pady=(0, 10))

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()