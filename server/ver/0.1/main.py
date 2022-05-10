import threading
import math
import select
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import json
import socket

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kmplot.backend_kivyagg import FigureCanvas

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

matplotlib.use('module://kmplot.backend_kivy')

from kv import KV

fan_enabled=False
window_opened=False
door_opened = False
led_enabled = False

connected = False

current="Moisture"

Moisture = []
Moisture_Time = []
CO2 = []
CO2_Time = []
Motion = []
Motion_Time = []
Illumination = []
Illumination_Time = []

fig_moisture, ax_moisture = plt.subplots()
fig_CO2, ax_CO2 = plt.subplots()
fig_Motion, ax_Motion = plt.subplots()
fig_Illumination, ax_Illumination = plt.subplots()

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ContentError(FloatLayout):
    pass

class App(MDApp):
    def build(self):
        global builder
        builder = Builder.load_string(KV)
        return builder

    def disconnect(self):
        sock.close()

    def server_connect(self):
            global sock_server, event, connected
            if connected == False:
                sock_server = socket.socket()
                sock_server.settimeout(1)
                try:
                    sock_server.connect(("0meka0.hopto.org", 443))
                    sock_server.send(bytes("This is android client", "utf-8"))
                    connected = True
                except:
                    App.show_popup(self)
                    connected = False
            else:
                pass

    def show_popup(self):
        global popupWindow
        show = ContentError()
        popupWindow = Popup(title="Ошибка", content = show, size_hint=(None, None), size=("400dp", "400dp"), on_dismiss = App.reset_to_main)
        popupWindow.open()

    def close_popup(self):
        global popupWindow
        popupWindow.dismiss()

    def reset_to_main(self):
        builder.ids.screen_manager.current = "Main"

    def start_receiving(self):
        global event
        event = Clock.schedule_interval(App.receive_data, 0.3)

    def server_disconnect(self):
        global sock_server, connected
        if connected == True:
            sock_server.close()
            connected = False

    def stop_receiving(self):
        global event
        try:
            Clock.unschedule(event)
        except:
            pass

    def receive_data(self):
        global sock_server, data
        ready = select.select([sock_server], [], [], .1)
        if ready[0]:
            try:
                data = sock_server.recv(4096)
                data = data.decode()
                App.Update_Moisture(self, data)
                App.Update_CO2(self, data)
                App.Update_Motion(self, data)
                App.Update_Illumination(self, data)
            except ConnectionResetError:
                App.show_popup(self)
                App.stop_receiving(self)
                connected = False

    def change_graph_left(self):
        global current
        if current == "Moisture":
            pass
        if current == "CO2":
            current = "Moisture"
            App.clear_graphs(self)
        if current == "Motion":
            current = "CO2"
            App.clear_graphs(self)
        if current == "Illumination":
            current = "Motion"
            App.clear_graphs(self)

    def change_graph_right(self):
        global current
        if current == "Moisture":
            current = "CO2"
            App.clear_graphs(self)
            return
        if current == "CO2":
            current = "Motion"
            App.clear_graphs(self)
            return
        if current == "Motion":
            current = "Illumination"
            App.clear_graphs(self)
            return
        if current == "Illumination":
            pass

    def clear_graphs(self):
        ax_moisture.cla()
        ax_CO2.cla()
        ax_Motion.cla()
        ax_Illumination.cla()
        Moisture.clear()
        Moisture_Time.clear()
        CO2.clear()
        CO2_Time.clear()
        Motion.clear()
        Motion_Time.clear()
        Illumination.clear()
        Illumination_Time.clear()

    def on_press_vent(self):
        global fan_enabled, x, y, connected
        if fan_enabled == False and connected == True:
            try:
                sock_server.send(b'e')
                builder.ids.fan.icon = "fan"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            fan_enabled = True
        else:
            try:
                sock_server.send(b'd')
                builder.ids.fan.icon = "fan-off"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            fan_enabled = False

    def on_press_window(self):
        global window_opened, connected
        if window_opened == False and connected == True:
            try:
                sock_server.send(b'w')
                builder.ids.window.icon = "window-open-variant"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            window_opened = True
        else:
            try:
                sock_server.send(b'n')
                builder.ids.window.icon = "window-closed-variant"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            window_opened = False

    def on_press_door(self):
        global door_opened, connected
        if door_opened == False and connected == True:
            try:
                sock_server.send(b'o')
                builder.ids.door.icon = "door-open"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            door_opened = True
        else:
            try:
                sock_server.send(b'b')
                builder.ids.door.icon = "door-closed"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            door_opened = False

    def led_enable(self):
        global led_enabled, connected
        if led_enabled == False and connected == True:
            try:
                sock_server.send(b'm')
                builder.ids.led.icon = "led-on"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            led_enabled = True
        else:
            try:
                sock_server.send(b'p')
                builder.ids.led.icon = "led-off"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            led_enabled = False

    def change_vent_speed(self):
        global fan_enabled
        try:
            if math.ceil(builder.ids.vent_speed.value) == 0:
                fan_enabled = False
                builder.ids.fan.icon = "fan-off"
            else :
                fan_enabled = True
                builder.ids.fan.icon = "fan"
            sock_server.send(bytes("a"+str(math.ceil(builder.ids.vent_speed.value))+"#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def change_window_rotation(self):
        global window_opened
        try:
            if math.ceil(builder.ids.window_rotation.value) == 0:
                window_opened = False
                builder.ids.window.icon = "window-closed-variant"
            else:
                window_opened = True
                builder.ids.window.icon = "window-open-variant"
            sock_server.send(bytes("r"+str(math.ceil(builder.ids.window_rotation.value))+"#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def change_door_rotation(self):
        global door_opened
        try:
            if math.ceil(builder.ids.door_rotation.value) == 0:
                door_opened = False
                builder.ids.door.icon = "door-closed"
            else:
                door_opened = True
                builder.ids.door.icon = "door-open"
            sock_server.send(bytes("v"+str(math.ceil(builder.ids.door_rotation.value))+"#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def change_led(self):
        global led_enabled
        try:
            if math.ceil(builder.ids.led_change.value) == 0:
                led_enabled = False
                builder.ids.led.icon = "led-off"
            else:
                led_enabled = True
                builder.ids.led.icon = "led-on"
            sock_server.send(bytes("l"+str(math.ceil(builder.ids.led_change.value))+"#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def Update_Moisture(self, data):
        global Moisture, Moisture_Time, current

        if current == "Moisture":
            dict = json.loads(data[0:data.find('/')])
            ax_moisture.cla()

            builder.ids.graph.clear_widgets()

            if len(Moisture) == 25:
                Moisture.clear()
                Moisture_Time.clear()
            Moisture.append(dict["Moisture"])
            Moisture_Time.append(datetime.fromisoformat(str(datetime.now())))
            ax_moisture.set_ylabel('Moisture')
            ax_moisture.set_xlabel('Time')
            ax_moisture.plot(Moisture_Time, Moisture, color='orange')
            builder.ids.graph.add_widget(FigureCanvas(fig_moisture))
        else:
            pass

    def Update_CO2(self, data):
        global CO2, CO2_Time, current
        if current == "CO2":
            dict = json.loads(data[0:data.find('/')])

            ax_CO2.cla()

            builder.ids.graph.clear_widgets()

            if len(CO2) == 25:
                ax_CO2.cla()
                CO2.clear()
                CO2_Time.clear()
            CO2.append(dict["CO2"])
            CO2_Time.append(datetime.fromisoformat(str(datetime.now())))
            ax_CO2.set_ylabel("CO2")
            ax_CO2.set_xlabel("Time")
            ax_CO2.plot(CO2_Time, CO2, color='orange')
            builder.ids.graph.add_widget(FigureCanvas(fig_CO2))
        else:
            pass

    def Update_Motion(self, data):
        global Motion, Motion_Time, current
        if current == "Motion":
            dict = json.loads(data[0:data.find('/')])

            ax_Motion.cla()

            builder.ids.graph.clear_widgets()

            if len(Motion) == 25:
                ax_Motion.cla()
                Motion.clear()
                Motion_Time.clear()
            Motion.append(dict["Motion"])
            Motion_Time.append(datetime.fromisoformat(str(datetime.now())))
            ax_Motion.set_ylabel("Motion")
            ax_Motion.set_xlabel("Time")
            ax_Motion.plot(Motion_Time, Motion, color='orange')
            builder.ids.graph.add_widget(FigureCanvas(fig_Motion))
        else:
            pass

    def Update_Illumination(self, data):
        global Illumination, Illumination_Time, current
        if current == "Illumination":
            dict = json.loads(data[0:data.find('/')])

            ax_Illumination.cla()

            builder.ids.graph.clear_widgets()

            if len(Illumination) == 25:
                ax_Illumination.cla()
                Illumination.clear()
                Illumination_Time.clear()
            Illumination.append(dict["Illumination"])
            Illumination_Time.append(datetime.fromisoformat(str(datetime.now())))
            ax_Illumination.set_ylabel("Illumination")
            ax_Illumination.set_xlabel("Time")
            ax_Illumination.plot(Illumination_Time, Illumination, color='orange')
            builder.ids.graph.add_widget(FigureCanvas(fig_Illumination))
        else:
            pass

app = App()
app.run()