import threading
import math
import select
from datetime import datetime
import json
import socket
from math import sin

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy_garden.graph import Graph, LinePlot

from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

from kv import KV

fan_enabled = False
window_opened = False
door_opened = False
led_enabled = False

connected = False

current="Moisture"

x=[]
val = 0

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ContentError(FloatLayout):
    pass

class SetGraph(Widget):
    graph_test = ObjectProperty(None)
    def create_plot(self):
        global plot
        plot = LinePlot(color=[0.37, 0.98, 0.2, 1], line_width = 1.25)
        self.ids["graph"].add_plot(plot)

    def update_graph(self, data):
        global current, plot, val
        if len(x) == 25:
            x.clear()
        if current == "Moisture":
            self.ids.graph.ymax = 1000
            self.ids.graph.y_ticks_major = 100
            self.ids.graph.ymin = 0
        if current == "CO2":
            self.ids.graph.ymax = 30
            self.ids.graph.y_ticks_major = 5
            self.ids.graph.ymin = 0
        if current == "Motion":
            self.ids.graph.ymax = 1
            self.ids.graph.y_ticks_major = 1
            self.ids.graph.ymin = -1
        if current == "Illumination":
            self.ids.graph.ymax = 1000
            self.ids.graph.y_ticks_major = 100
            self.ids.graph.ymin = 0
        try:
            dict = json.loads(data[0:data.find('/')])
        except:
            return
        x.append(dict[current])
        val = dict[current]
        self.ids.graph.ylabel = current
        plot.points = [(i, x[i]) for i in range(0, len(x))]

class App(MDApp):
    def build(self):
        global builder, graph
        builder = Builder.load_string(KV)
        graph = SetGraph()
        graph.create_plot()
        builder.ids.analitics.add_widget(graph)
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
        event = Clock.schedule_interval(App.receive_data, 0.25)

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
        global sock_server, data, graph, builder, avl
        ready = select.select([sock_server], [], [], .1)
        if ready[0]:
            try:
                data = sock_server.recv(4096)
                data = data.decode()
                builder.ids.stats.text=current+": "+str(val)+"\n\n"+"Time: "+str(datetime.fromisoformat(str(datetime.now())))
                SetGraph.update_graph(graph, data)
            except ConnectionResetError:
                App.show_popup(self)
                App.stop_receiving(self)
                connected = False

    def change_graph_left(self):
        global current
        if current == "Moisture":
            current = "Illumination"
            x.clear()
            return
        if current == "CO2":
            current = "Moisture"
            x.clear()
            return
        if current == "Motion":
            current = "CO2"
            x.clear()
            return
        if current == "Illumination":
            current = "Motion"
            x.clear()
            return

    def change_graph_right(self):
        global current
        if current == "Moisture":
            current = "CO2"
            x.clear()
            return
        if current == "CO2":
            current = "Motion"
            x.clear()
            return
        if current == "Motion":
            current = "Illumination"
            x.clear()
            return
        if current == "Illumination":
            current = "Moisture"
            x.clear()
            return

    def on_press_vent(self):
        global fan_enabled, connected
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

app = App()
app.run()