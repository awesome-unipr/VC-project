import aiohttp
import asyncio
import datetime
import time
import json
import tkinter as tk
from tkinter import font
from tkinter import *
from PIL import ImageTk, Image
from random import randint


#TEST VARIABLES
class TkinterGui:
    def __init__(self):
        #WINDOW
        self.window = tk.Tk()
        self.window.title('Brum Brum GUI')
        self.window.geometry('1200x700')

        self.window.resizable(width = 'false', height = 'false') # fix window size

        """
        for i in font.families():
            self.el = Label(self.window, text = i, font = (i, 15))
            self.el.pack()
        """

        #MAIN FRAME
        self.main_frame = Frame(self.window)
        self.main_frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)

        #LEFT FRAME
        self.left_frame = Frame(self.main_frame)
        self.left_frame.place(relwidth = 0.3, relheight = 1, anchor = tk.NW)

        #BLANK FRAME
        self.blank_frame = Frame(self.left_frame)
        self.blank_frame.place(relx = 1, relwidth = 0.5, relheight = 1, anchor = tk.NE)

        #CONTROL FRAME
        self.control_frame = Frame(self.left_frame, background = '#16161d', highlightbackground = '#36454F', highlightthickness = 6, padx=10)
        self.control_frame.place(relwidth = 0.5, relheight = 1, anchor = tk.NW)
            #KEY
        self.key_icon = Image.open("Icons/key.png")
        self.keycv = tk.Canvas(self.control_frame, background = '#16161d', highlightthickness = 0)
        self.keycv.place(rely = 0.025, relwidth = 1, relheight = 0.2, anchor = tk.NW)
            #LOCK
        self.lock_icon = Image.open("Icons/lock.png")
        self.lockcv = tk.Canvas(self.control_frame, background = '#16161d', highlightthickness = 0)
        self.lockcv.place(rely = 0.275, relwidth = 1, relheight = 0.2, anchor = tk.NW)
            #SEC
        self.sec_icon = Image.open("Icons/sec.png")
        self.seccv = tk.Canvas(self.control_frame, background = '#16161d', highlightthickness = 0)
        self.seccv.place(rely = 0.525, relwidth = 1, relheight = 0.2, anchor = tk.NW)
            #ABS
        self.abs_icon = Image.open("Icons/abs.png")
        self.abscv = tk.Canvas(self.control_frame, background = '#16161d', highlightthickness = 0)
        self.abscv.place(rely = 0.775, relwidth = 1, relheight = 0.2, anchor = tk.NW)

        #PLACE IMAGES ON CANVAS
        self.window.update()

        self.driver_text = self.keycv.create_text(self.keycv.winfo_width() / 2, self.keycv.winfo_height() / 4, text = '', fill = '#08c044', font = ('Small Fonts', 14))
        self.key_icon = self.key_icon.resize((self.keycv.winfo_width(), self.keycv.winfo_height()))
        self.tk_key = ImageTk.PhotoImage(self.key_icon)
        self.keycv.create_image(0, 0, image = self.tk_key, anchor = tk.NW)

        self.lock_icon = self.lock_icon.resize((self.lockcv.winfo_width(), self.lockcv.winfo_height()))
        self.tk_lock = ImageTk.PhotoImage(self.lock_icon)
        self.lockcv.create_image(0, 0, image = self.tk_lock, anchor = tk.NW)

        self.sec_icon = self.sec_icon.resize((self.seccv.winfo_width(), self.seccv.winfo_height()))
        self.tk_sec = ImageTk.PhotoImage(self.sec_icon)
        self.seccv.create_image(0, 0, image = self.tk_sec, anchor = tk.NW)

        self.abs_icon = self.abs_icon.resize((self.abscv.winfo_width(), self.abscv.winfo_height()))
        self.tk_abs = ImageTk.PhotoImage(self.abs_icon)
        self.abscv.create_image(0, 0, image = self.tk_abs, anchor = tk.NW)

        #self.abscv.bind('<Configure>', lambda e : self.stretch_image(e)) #sus solution

        #RIGHT FRAME
        self.right_frame = Frame(self.main_frame)
        self.right_frame.place(relx = 1, relwidth = 0.7, relheight = 1, anchor = tk.NE)

        #RADIO FRAME
        self.radio_frame = Frame(self.right_frame, highlightbackground = '#36454F', highlightthickness = 6)
        self.radio_frame.place(relwidth = 1, relheight = 0.1, anchor = tk.NW)

        self.station = Label(self.radio_frame, text = '-----------', bg = '#16161d', fg = 'white', font = ('Small Fonts', 20))
        self.prev_st = Button(self.radio_frame, text = '<', bg = '#36454F', fg = 'white', font = ('System', 20))
        self.next_st = Button(self.radio_frame, text = '>', bg = '#36454F', fg = 'white', font = ('System', 20))
  
        self.station.place(relx = 0.2, relwidth = 0.6, relheight = 1, anchor = tk.NW)
        self.prev_st.place(relwidth = 0.2, relheight = 1, anchor = tk.NW)
        self.next_st.place(relx = 0.8, relwidth = 0.2, relheight = 1, anchor = tk.NW)
        
        #BLANK FRAME
        self.blank_frame_1 = Frame(self.right_frame)
        self.blank_frame_1.place(rely = 0.1, relwidth = 1, relheight = 0.1, anchor = tk.NW)

        #DMS FRAME
        self.dms_bg = '#16161d'

        self.dms_frame = Frame(self.right_frame, bg = self.dms_bg, highlightbackground = "#36454F", highlightthickness = 6)
        self.dms_frame.place(rely = 0.2, relwidth = 0.45, relheight = 0.8, anchor = tk.NW)

        self.state_frame = [0 for i in range(10)]

        self.state = [0 for i in range(10)]

        for i in range(10):
            self.state_frame[i] = Frame(self.dms_frame, bg = self.dms_bg, highlightbackground = "#36454F", highlightthickness = 2)
            self.state_frame[i].place(relx = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1, anchor = tk.NW)

            self.state[i] = Label(self.state_frame[i], text = '', bg = self.dms_bg, fg = '#2b2b30', font = ('Small Fonts', 14))

            self.state[i].place(relx = 0.3, rely = 0, relwidth = 0.5, relheight = 1, anchor = tk.NW)

        #WEATHER FRAME
        self.weather_bg = '#4848ff'
        self.weather_frame = Frame(self.right_frame, background = self.weather_bg, highlightbackground = "#36454F", highlightthickness = 6)
        self.weather_frame.place(relx = 0.55, rely = 0.2, relwidth = 0.45, relheight = 0.8, anchor = tk.NW)

        self.current_weather_frame = Frame(self.weather_frame, bg = self.weather_bg, highlightbackground = "#36454F", highlightthickness = 3, padx = 5, pady = 5)
        self.current_weather_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.3, anchor = tk.NW)

        self.current_city = Label(self.current_weather_frame, text = 'Placeholder', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 20))
        self.current_time = Label(self.current_weather_frame, text = '00:00', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 20))
        self.cw_cv = tk.Canvas(self.current_weather_frame, background = self.weather_bg, highlightthickness = 0)
        self.current_weather = Label(self.current_weather_frame, text = '--------', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 20))
        self.current_temperature = Label(self.current_weather_frame, text = '----', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 20))

        self.current_city.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.5, anchor = tk.NW)
        self.current_time.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 0.5, anchor = tk.NW)
        self.cw_cv.place(relx = 0.05, rely = 0.5, relwidth = 0.25, relheight = 0.5, anchor = tk.NW)
        self.current_weather.place(relx = 0.3, rely = 0.5, relwidth = 0.5, relheight = 0.5, anchor = tk.NW)
        self.current_temperature.place(relx = 0.8, rely = 0.5, relwidth = 0.2, relheight = 0.5, anchor = tk.NW)

        #TEST CURRENT WEATHER ICONS
        self.window.update()

        self.cloud_icon = Image.open("Icons/cloud.png")
        self.sun_icon = Image.open("Icons/sun.png")
        self.pcloud_icon = Image.open("Icons/cloud_and_sun.png")
        self.rain_icon = Image.open("Icons/rain.png")
        self.snow_icon = Image.open("Icons/snow.png")
        self.mist_icon = Image.open("Icons/mist.png")
        self.storm_icon = Image.open("Icons/storm.png")
        self.defweather_icon = Image.open("Icons/default_weather.png")

        self.cloud_icon = self.cloud_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_cloud = ImageTk.PhotoImage(self.cloud_icon)
        self.sun_icon = self.sun_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_sun = ImageTk.PhotoImage(self.sun_icon)
        self.pcloud_icon = self.pcloud_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_pcloud = ImageTk.PhotoImage(self.pcloud_icon)
        self.rain_icon = self.rain_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_rain = ImageTk.PhotoImage(self.rain_icon)
        self.snow_icon = self.snow_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_snow = ImageTk.PhotoImage(self.snow_icon)
        self.mist_icon = self.mist_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_mist = ImageTk.PhotoImage(self.mist_icon)
        self.storm_icon = self.storm_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_storm = ImageTk.PhotoImage(self.storm_icon)
        self.defweather_icon = self.defweather_icon.resize((self.cw_cv.winfo_width(), self.cw_cv.winfo_height()))
        self.tk_defweather = ImageTk.PhotoImage(self.defweather_icon)

        self.forecast_frame = [0 for i in range(7)]

        self.time = [0 for i in range(7)]
        self.fw_cv = [0 for i in range(7)]
        self.weather = [0 for i in range(7)]
        self.temperature = [0 for i in range(7)]

        for i in range(7):
            self.forecast_frame[i] = Frame(self.weather_frame, bg = self.weather_bg, highlightbackground = "#36454F", highlightthickness = 2)
            self.forecast_frame[i].place(relx = 0, rely = 0.3 + 0.1 * i, relwidth = 1, relheight = 0.1, anchor = tk.NW)

            self.time[i] = Label(self.forecast_frame[i], text = '00:00', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 14))
            self.fw_cv[i] = tk.Canvas(self.forecast_frame[i], background = self.weather_bg, highlightthickness = 0)
            self.weather[i] = Label(self.forecast_frame[i], text = '--------', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 14))
            self.temperature[i] = Label(self.forecast_frame[i], text = '----', bg = self.weather_bg, fg = 'white', font = ('Small Fonts', 14))

            self.time[i].place(relx = 0, rely = 0, relwidth = 0.2, relheight = 1, anchor = tk.NW)
            self.fw_cv[i].place(relx = 0.25, rely = 0, relwidth = 0.15, relheight = 1, anchor = tk.NW)
            self.weather[i].place(relx = 0.4, rely = 0, relwidth = 0.4, relheight = 1, anchor = tk.NW)
            self.temperature[i].place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 1, anchor = tk.NW)

        #SETTINGS
        self.settings_button = Button(self.window, text = '=', highlightbackground = "black", highlightthickness = 2, bg = '#36454F', fg = 'white')
        self.settings_button.place(relx = 0.98, rely = 0.02, width = 50, height = 50, anchor = tk.NE)
        self.settings_button.config(command = self.open_settings)

        self.settings_frame = Frame(self.window, highlightbackground = "black", highlightthickness = 2)
        self.settings_frame.place(relx = 1, rely = 0, relwidth = 0.3, relheight = 1)

        self.settings_button = Button(self.settings_frame, text = '=', highlightbackground = "black", highlightthickness = 2, bg = '#36454F', fg = 'white')
        self.settings_button.place(relx = 0.04, rely = 0.02, width = 50, height = 50, anchor = tk.NW)
        self.settings_button.config(command = self.close_settings)

        self.settings_title = Label(self.settings_frame, text = 'Control Settings', fg = 'black', font = ('Arial', 20))
        self.settings_title.place(relx = 0.90, rely = 0.03, anchor = tk.NE)

        self.login_driver = Button(self.settings_frame, text = 'Access Vehicle', highlightbackground = "black", highlightthickness = 2, bg = '#36454F', fg = 'white')
        self.login_driver.place(relx = 0.04, rely = 0.2, relwidth = 0.92, height = 50, anchor = tk.NW)

        self.logout_driver = Button(self.settings_frame, text = 'Leave Vehicle', highlightbackground = "black", highlightthickness = 2, bg = '#36454F', fg = 'white')
        self.logout_driver.place(relx = 0.04, rely = 0.3, relwidth = 0.92, height = 50, anchor = tk.NW)

        self.unrecognized_driver = Button(self.settings_frame, text = 'Urecognized Access', highlightbackground = "black", highlightthickness = 2, bg = '#36454F', fg = 'white')
        self.unrecognized_driver.place(relx = 0.04, rely = 0.4, relwidth = 0.92, height = 50, anchor = tk.NW)

        self.random_weather = Button(self.settings_frame, text = 'Set Random Weather', highlightbackground = "black", highlightthickness = 2, bg = '#36454F', fg = 'white')
        self.random_weather.place(relx = 0.04, rely = 0.5, relwidth = 0.92, height = 50, anchor = tk.NW)

    def open_settings(self):
        self.settings_frame.place(relx = 0.7, rely = 0, relwidth = 0.3, relheight = 1)
    
    def close_settings(self):
        self.settings_frame.place(relx = 1, rely = 0, relwidth = 0.3, relheight = 1)

    """
    def stretch_image(self, event):
        #WINDOW SIZE 
        width = event.width
        height = event.height
        
        #RESIZED IMAGES
        global tk_key
        global tk_lock
        global tk_sec
        global tk_abs

        #RESIZE
        resized_image = self.key_icon.resize((width, height))
        tk_key = ImageTk.PhotoImage(resized_image)

        resized_image = self.lock_icon.resize((width, height))
        tk_lock = ImageTk.PhotoImage(resized_image)

        resized_image = self.sec_icon.resize((width, height))
        tk_sec = ImageTk.PhotoImage(resized_image)

        resized_image = self.abs_icon.resize((width, height))
        tk_abs = ImageTk.PhotoImage(resized_image)

        #PLACE ON CANVAS
        self.keycv.create_image(0, 0, image = tk_key, anchor = tk.NW)
        self.lockcv.create_image(0, 0, image = tk_lock, anchor = tk.NW)
        self.seccv.create_image(0, 0, image = tk_sec, anchor = tk.NW)
        self.abscv.create_image(0, 0, image = tk_abs, anchor = tk.NW)
    """

    def start_main_loop(self):
        self.window.mainloop()

class VehicleStatus:
    def __init__(self, gui, cobu_port, skr_port):
        #GUI CONFIGURATION
        self._gui = gui

        #HTTP SETTINGS
        self.cobu_port = cobu_port
        self.rks_port = skr_port
        
        #OBUs STATUS
        self.radio = ''
        self.current_weather = ''
        self.forecast_weather = ''
        self.driver_state = ''
        self.brake_state = ''
        self.key_access = ''
        self.invalid_key_access = ''
        self.driver = 'XXXXX'

        #UPDATE CYCLE
        self.upd_interval = 1000
        self._gui.window.after(self.upd_interval, lambda : asyncio.run(self.update_cycle()))

    async def change_driver(self):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url = 'http://localhost:'+ str(self.rks_port) +'/driver') as response:
                        data = await response.json()
                        
                        self.driver = data['message']

                        self.invalid_key_access = data['warning']

            except Exception as e:
                print("Error in the http request to /driver: " + str(e))

    def display_w_icon(self, weather, canvas):

        canvas.delete('all')

        if weather == 'Sunny':
            canvas.create_image(0, 0, image = self._gui.tk_sun, anchor = tk.NW)
        elif weather == 'Cloudy':
            canvas.create_image(0, 0, image = self._gui.tk_cloud, anchor = tk.NW)
        elif weather == 'Partly Cloudy':
            canvas.create_image(0, 0, image = self._gui.tk_pcloud, anchor = tk.NW)
        elif weather == 'Rainy':
            canvas.create_image(0, 0, image = self._gui.tk_rain, anchor = tk.NW)
        elif weather == 'Snowy':
            canvas.create_image(0, 0, image = self._gui.tk_snow, anchor = tk.NW)
        elif weather == 'Misty':
            canvas.create_image(0, 0, image = self._gui.tk_mist, anchor = tk.NW)
        elif weather == 'Stormy':
            canvas.create_image(0, 0, image = self._gui.tk_storm, anchor = tk.NW)
        else:
            canvas.create_image(0, 0, image = self._gui.tk_defweather, anchor = tk.NW)

    async def update_status(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url = 'http://localhost:'+ str(self.cobu_port) +'/vehicle-status') as response:

                    status = await response.json()
                    #print(status)
                    for o in status['Obu']:
                        if o['name'] == 'radio':
                            self.radio = o['status']
                        if o['name'] == 'weather-current':
                            try:
                                self.current_weather = json.loads(o['status'])
                            except:
                                pass
                        if o['name'] == 'weather-forecast':
                            try:
                                self.forecast_weather = json.loads(o['status'])
                            except:
                                pass
                        if o['name'] == 'dms':
                            self.driver_state = o['status']
                        if o['name'] == 'brake':
                            self.brake_state = o['status']
                        if o['name'] == 'key-is-ok':
                            self.key_access = o['status']
                        if o['name'] == 'key-not-recognized':
                            self.unrecognize_key = o['status']

                    #molto brutto perchè manda tante richieste inutili se il veicolo è unlock (updated: non più così brutto) (updated again: è tornato brutto (sad emoji) )
                    if self.key_access == 'VALID KEY':
                        await self.change_driver()

                    self.update_gui()
        except Exception as e:
            print("Error in the http request to /vehicle-status: " + str(e))

    def update_gui(self):
        #RADIO UPDATE
        self._gui.station.config(text = self.radio)

        #WEATHER UPDATE
        try:
            now = datetime.datetime.now()
    
            self._gui.current_city.config(text = self.current_weather['city'])
            self._gui.current_time.config(text = str(now.time().hour) + ':' + str(now.time().minute))
            self._gui.current_weather.config(text = self.current_weather['weather'])
            self._gui.current_temperature.config(text = str(self.current_weather['temperature']) + ' °F')

            self.display_w_icon(self.current_weather['weather'], self._gui.cw_cv)

            for i, w in enumerate(self.forecast_weather):
                self._gui.time[i].config(text = str(self.forecast_weather[w]['time']) + ':00')
                self._gui.weather[i].config(text = self.forecast_weather[w]['weather'])
                self._gui.temperature[i].config(text = str(self.forecast_weather[w]['temperature']) + ' °F')
                self.display_w_icon(self.forecast_weather[w]['weather'], self._gui.fw_cv[i])
        except:
            print("weather gui update error")


        #DMS UPDATE
        for i in self._gui.state:
            if i.cget('text') == self.driver_state:
                i.config(fg = 'yellow')
            else:
                i.config(fg = '#2b2b30')
        
        #BRAKING UPDATE
        if self.brake_state == 'Alert' and self.unrecognize_key == 'KEY VALID':
            self._gui.abscv.itemconfig(1, state = 'normal')
        else:
            self._gui.abscv.itemconfig(1, state = 'hidden')
        
        #KEY UPDATE
        self._gui.keycv.itemconfig(self._gui.driver_text, text = self.driver)

        if self.key_access == 'VALID KEY':
            self._gui.keycv.itemconfig(1, state = 'normal')
            self._gui.keycv.itemconfig(2, state = 'normal')
            self._gui.lockcv.itemconfig(1, state = 'hidden')
        elif self.key_access == 'NO KEY':
            self._gui.keycv.itemconfig(1, state = 'hidden')
            self._gui.keycv.itemconfig(2, state = 'hidden')
            self._gui.lockcv.itemconfig(1, state = 'normal')
        else:
            self._gui.keycv.itemconfig(1, state = 'hidden')
            self._gui.keycv.itemconfig(2, state = 'hidden')
            self._gui.lockcv.itemconfig(1, state = 'hidden')

        if self.invalid_key_access != '':
            self._gui.seccv.itemconfig(1, state = 'normal')
        else:
            self._gui.seccv.itemconfig(1, state = 'hidden')

    async def update_cycle(self):
        await self.update_status()
        self._gui.window.after(self.upd_interval, lambda : asyncio.run(self.update_cycle()))

class InfotainmentSystem:
    def __init__(self, gui, port):
        #GUI CONFIGURATION
        self._gui = gui
        self._gui.next_st.config(command = lambda : asyncio.run(self.next_station()))
        self._gui.prev_st.config(command = lambda : asyncio.run(self.previous_station()))

        #HTTP SETTINGS
        self._port = port

        #STATION SETTINGS
        self._stations = ['RTL 102.5', 'Radio Deejay', 'Radio 105', 'R101', 'RDS', 'Radio 1', 'Radio 2', 'Radio Maria']
        self._sindex = 0

        asyncio.run(self.change_station())
    
    async def change_station(self):
        try:
            async with aiohttp.ClientSession() as session:

                payload = {'station': self._stations[self._sindex]}

                async with session.post(url = 'http://localhost:'+ str(self._port) +'/radio-change/', data = payload) as response:

                    #print("Status:", response.status)
                    await response.text()

                    await vehicle.update_status()
        except:
            print("Error in the http request to /radio-change")

    async def next_station(self):
        if(self._sindex == len(self._stations) - 1):
            self._sindex = 0
        else:
            self._sindex += 1

        await self.change_station()

    async def previous_station(self):
        if(self._sindex == 0):
            self._sindex = len(self._stations) - 1
        else:
            self._sindex -= 1

        await self.change_station()

class WeatherInformation:
    def __init__(self, gui, port):
        #GUI CONFIGURATION
        self._gui = gui

        #HTTP SETTINGS
        self._port = port

        self._gui.random_weather.config(command = lambda : asyncio.run(self.set_weather()))
        

    async def set_weather(self):
        cities = ['Parma', 'Bologna', 'Milano', 'Torino', 'Firenze', 'Piacenza', 'Rimini', 'Roma', 'Napoli']
        current_city = cities[randint(0, len(cities) - 1)]

        current_time = datetime.datetime.now()
        forecast_times = []
        for i in range(0, 7):
            time = int(current_time.time().strftime("%H")) + (i + 1) * 3
            if time >= 24:
                forecast_times.append(time - 24)
            else:
                forecast_times.append(time)

        current_temperature = randint(0, 99)
        forecast_temperatures = []
        for i in range(0, 7):
            forecast_temperatures.append(randint(0, 99))

        weathers = ['Sunny', 'Cloudy', 'Partly Cloudy', 'Rainy', 'Snowy', 'Misty', 'Stormy']
        current_weather = weathers[randint(0, len(weathers) - 1)]
        forecast_weathers = []
        for i in range(0, 7):
            forecast_weathers.append(weathers[randint(0, len(weathers) - 1)])

        payload_current = {'current_city': current_city, 'current_temperature': current_temperature, 'current_kind': current_weather}

        forecast = json.loads('{}')
        for i in range(0, 7):
            item = {i: {'time': str(forecast_times[i]), 'temperature': str(forecast_temperatures[i]), 'kind': forecast_weathers[i]}}
            forecast.update(item)

        payload_forecast = json.dumps(forecast)

        print(str(payload_forecast))

        async with aiohttp.ClientSession() as session:

            async with session.post(url = 'http://localhost:' + str(self._port) + '/weathercurrent', data = payload_current) as response:
                print(response)
                
            async with session.post('http://localhost:' + str(self._port) + '/weatherforecast', json = payload_forecast) as response:
                print(response)

class DriverMonitoringSystem:
    def __init__(self, gui):
        #GUI CONFIGURATION
        self._gui = gui

        self.driver_states = ['Angry', 'Tired', 'Drunk', 'Distracted', 'Normal', 'Bored', 'Hungry', 'Sleepy', 'Dizzy', 'Unpresent']
        for i in self._gui.state:
            try:
                i.config(text = self.driver_states[self._gui.state.index(i)])
            except:
                pass

class RemoteKeylessSystem:
    def __init__(self, gui, port):
        #GUI CONFIGURATION
        self._gui = gui
        self._gui.login_driver.config(command = lambda : asyncio.run(self.login_driver()))
        self._gui.logout_driver.config(command = lambda : asyncio.run(self.logout_driver()))
        self._gui.unrecognized_driver.config(command = lambda : asyncio.run(self.unrecognized_driver()))

        #HTTP SETTINGS
        self.port = port
    
    async def login_driver(self):
        try:
            async with aiohttp.ClientSession() as session:

                with open('Config.json', 'r') as file:
                    config_file = json.load(file)
                
                payload = {'identity': config_file['Driver'][0]['identity'], 'sequence': config_file['Driver'][0]['sequence']}

                async with session.post(url = 'http://localhost:'+ str(self.port) +'/keyless', json = payload) as response:
                    
                    await response.text()

        except Exception as e:
                print("Error in the http request to /keyless: " + str(e))

    async def logout_driver(self):
        try:
            async with aiohttp.ClientSession() as session:
                
                with open('Config.json', 'r') as file:
                    config_file = json.load(file)
                
                payload = {'identity': config_file['Driver'][0]['identity'], 'sequence': config_file['Driver'][0]['sequence']}

                async with session.post(url = 'http://localhost:'+ str(self.port) +'/logout', json = payload) as response:
                    
                    await response.text()

        except Exception as e:
                print("Error in the http request to /logout: " + str(e))
    
    async def unrecognized_driver(self):
        try:
            async with aiohttp.ClientSession() as session:
                
                payload = {'identity': 'unauthorize', 'sequence': '00000000'}

                async with session.post(url = 'http://localhost:'+ str(self.port) +'/keyless', json = payload) as response:
                    
                    await response.text()

        except Exception as e:
                print("Error in the http request to /logout: " + str(e))


#MAIN
with open('Config.json', 'r') as file:
	config_file = json.load(file)

for o in config_file['Obu']:
    if o['name'] == 'Infotainment System':
        info_port = o['http_port']
    if o['name'] == 'Weather Information':
        weather_port = o['http_port']
    if o['name'] == 'Central Unit':
        central_port = o['http_port']
    if o['name'] == 'Remote Keyless System':
        keyless_port = o['http_port']

gui = TkinterGui()
vehicle = VehicleStatus(gui, central_port, keyless_port)
radio = InfotainmentSystem(gui, info_port)
meteo = WeatherInformation(gui, weather_port)
dms = DriverMonitoringSystem(gui)
rks = RemoteKeylessSystem(gui, keyless_port)

gui.start_main_loop()