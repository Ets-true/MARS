import math
from datetime import datetime
import json
import socket

from kivy.graphics import Rectangle, Canvas
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window

from kivy_garden.graph import Graph, LinePlot

from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

from kv import KV

fan_enabled = False
window_opened = False
door_opened = False
led_enabled = False
buzzer_enabled = False

connected = False

current = "Moisture"

x = []
val = 0


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ContentError(FloatLayout):
    pass

class Button1(ButtonBehavior, Image):
    def on_press(self):
        self.source = "button1_pressed.png"

    def on_release(self):
        global connected, buzzer_enabled
        try:
            sock_server.send(b't')
            self.source = "button1.png"
            builder.ids.buzzer.icon = "volume-off"
        except ConnectionResetError:
            App.show_popup(self)
            connected = False
        buzzer_enabled = False


class Button2(ButtonBehavior, Image):
    def on_press(self):
        self.source = "button2_pressed.png"

    def on_release(self):
        global connected, buzzer_enabled
        try:
            sock_server.send(b't')
            self.source = "button2.png"
            builder.ids.buzzer.icon = "volume-off"
        except ConnectionResetError:
            App.show_popup(self)
            connected = False
        buzzer_enabled = False


class SetGraph(Widget):
    graph_test = ObjectProperty(None)

    def create_plot(self):
        global plot
        plot = LinePlot(color=[0.37, 0.98, 0.2, 1], line_width=1.25)
        self.ids["graph"].add_plot(plot)

    def update_graph(self, data):
        global current, plot, val
        if len(x) == 100:
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
        button1 = Button1(on_press=lambda frequency: app.button_action(200), pos_hint ={"top": 0.87, "left": 0.9} , size = ("380dp", "60dp"), size_hint = (None, None))
        button2 = Button1(on_press=lambda frequency: app.button_action(300), pos_hint ={"top": 0.76, "left": 0.9}, size = ("380dp", "60dp"), size_hint = (None, None))
        button3 = Button1(on_press=lambda frequency: app.button_action(400), pos_hint ={"top": 0.65, "left": 0.9}, size = ("380dp", "60dp"), size_hint = (None, None))
        button4 = Button1(on_press=lambda frequency: app.button_action(500), pos_hint ={"top": 0.54, "left": 0.9}, size = ("380dp", "60dp"), size_hint=(None, None))
        button5 = Button1(on_press=lambda frequency: app.button_action(600), pos_hint ={"top": 0.43, "left": 0.9}, size = ("380dp", "60dp"), size_hint=(None, None))
        button6 = Button1(on_press=lambda frequency: app.button_action(700), pos_hint ={"top": 0.32, "left": 0.9}, size = ("380dp", "60dp"), size_hint=(None, None))
        button7 = Button1(on_press=lambda frequency: app.button_action(800), pos_hint ={"top": 0.21, "left": 0.9}, size = ("380dp", "60dp"), size_hint=(None, None))
        button8 = Button1(on_press=lambda frequency: app.button_action(900), pos_hint={"top": 0.1, "left": 0.9}, size=("380dp", "60dp"), size_hint=(None, None))
        button13 = Button2(on_press=lambda frequency: app.button_action(250), pos_hint={"top": 0.815, "right": 0.98}, size=("200dp", "60dp"), size_hint=(None, None))
        button14 = Button2(on_press=lambda frequency: app.button_action(350), pos_hint={"top": 0.705, "right": 0.98}, size=("200dp", "60dp"), size_hint=(None, None))
        button15 = Button2(on_press=lambda frequency: app.button_action(450), pos_hint={"top": 0.595, "right": 0.98}, size=("200dp", "60dp"), size_hint=(None, None))
        button16 = Button2(on_press=lambda frequency: app.button_action(550), pos_hint={"top": 0.485, "right": 0.98}, size=("200dp", "60dp"), size_hint=(None, None))
        button17 = Button2(on_press=lambda frequency: app.button_action(650), pos_hint={"top": 0.375, "right": 0.98}, size=("200dp", "60dp"), size_hint=(None, None))
        button18 = Button2(on_press=lambda frequency: app.button_action(750), pos_hint={"top": 0.265, "right": 0.98}, size=("200dp", "60dp"), size_hint=(None, None))
        button19 = Button2(on_press=lambda frequency: app.button_action(850), pos_hint={"top": 0.155, "right": 0.98},  size=("200dp", "60dp"), size_hint=(None, None))

        builder.ids.Frequency_player.add_widget(button1)
        builder.ids.Frequency_player.add_widget(button2)
        builder.ids.Frequency_player.add_widget(button3)
        builder.ids.Frequency_player.add_widget(button4)
        builder.ids.Frequency_player.add_widget(button5)
        builder.ids.Frequency_player.add_widget(button6)
        builder.ids.Frequency_player.add_widget(button7)
        builder.ids.Frequency_player.add_widget(button8)
        builder.ids.Frequency_player.add_widget(button13)
        builder.ids.Frequency_player.add_widget(button14)
        builder.ids.Frequency_player.add_widget(button15)
        builder.ids.Frequency_player.add_widget(button16)
        builder.ids.Frequency_player.add_widget(button17)
        builder.ids.Frequency_player.add_widget(button18)
        builder.ids.Frequency_player.add_widget(button19)


        builder.ids.analitics.add_widget(graph)
        return builder

    def disconnect(self):
        global sock_server
        sock_server.close()

    def server_connect(self):
        global sock_server, connected
        if not connected:
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
        popupWindow = Popup(title="Ошибка", content=show, size_hint=(None, None), size=("400dp", "400dp"),
                            on_dismiss=App.reset_to_main)
        popupWindow.open()

    def close_popup(self):
        global popupWindow
        popupWindow.dismiss()

    def reset_to_main(self):
        builder.ids.screen_manager.current = "Main"

    def start_receiving(self):
        global event
        event = Clock.schedule_interval(App.receive_data, 0.1)

    def server_disconnect(self):
        global sock_server, connected
        if connected:
            sock_server.close()
            connected = False

    def stop_receiving(self):
        global event
        try:
            Clock.unschedule(event)
        except:
            pass

    def receive_data(self):
        global sock_server, data, graph, builder, avl, connected
        if connected == True:
            try:
                data = sock_server.recv(1024)
                data = data.decode()
                builder.ids.stats.text = current + ": " + str(val) + "\n\n" + "Time: " + str(
                    datetime.fromisoformat(str(datetime.now())))
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

    def buzzer_enable(self):
        global buzzer_enabled, connected
        if buzzer_enabled == False and connected == True:
            try:
                sock_server.send(b'u')
                builder.ids.buzzer.icon = "volume-high"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            buzzer_enabled = True
        else:
            try:
                sock_server.send(b't')
                builder.ids.buzzer.icon = "volume-off"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False
            buzzer_enabled = False

    def button_action(self, frequency):
        global connected
        if connected == True:
            try:
                sock_server.send(bytes("f" + str(math.ceil(frequency)) + "#", "utf-8"))
                self.source = "button1_pressed.png"
            except ConnectionResetError:
                App.show_popup(self)
                connected = False

    def disable_buzzer(self):
        global connected, buzzer_enabled
        try:
            sock_server.send(b't')
            builder.ids.buzzer.icon = "volume-off"
        except ConnectionResetError:
            App.show_popup(self)
            connected = False
        buzzer_enabled = False

    def change_vent_speed(self):
        global fan_enabled, connected
        try:
            if math.ceil(builder.ids.vent_speed.value) == 0:
                fan_enabled = False
                builder.ids.fan.icon = "fan-off"
            else:
                fan_enabled = True
                builder.ids.fan.icon = "fan"
            sock_server.send(bytes("a" + str(math.ceil(builder.ids.vent_speed.value)) + "#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def change_window_rotation(self):
        global window_opened, connected
        try:
            if math.ceil(builder.ids.window_rotation.value) == 0:
                window_opened = False
                builder.ids.window.icon = "window-closed-variant"
            else:
                window_opened = True
                builder.ids.window.icon = "window-open-variant"
            sock_server.send(bytes("r" + str(math.ceil(builder.ids.window_rotation.value)) + "#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def change_door_rotation(self):
        global door_opened, connected
        try:
            if math.ceil(builder.ids.door_rotation.value) == 0:
                door_opened = False
                builder.ids.door.icon = "door-closed"
            else:
                door_opened = True
                builder.ids.door.icon = "door-open"
            sock_server.send(bytes("v" + str(math.ceil(builder.ids.door_rotation.value)) + "#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def change_led(self):
        global led_enabled, connected
        try:
            if math.ceil(builder.ids.led_change.value) == 0:
                led_enabled = False
                builder.ids.led.icon = "led-off"
            else:
                led_enabled = True
                builder.ids.led.icon = "led-on"
            sock_server.send(bytes("l" + str(math.ceil(builder.ids.led_change.value)) + "#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def lcd_print(self):
        global connected
        try:
            sock_server.send(bytes(("q" + builder.ids.lcd_text.text + "#"), "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False

    def set_buzzer_frequency(self):
        global buzzer_enabled, connected
        try:
            if math.ceil(builder.ids.buzzer_frequency.value) == 0:
                sock_server.send(b't')
                buzzer_enabled = False
                builder.ids.buzzer.icon = "volume-off"
            else:
                buzzer_enabled = True
                builder.ids.buzzer.icon = "volume-high"
                sock_server.send(bytes("f" + str(math.ceil(builder.ids.buzzer_frequency.value)) + "#", "utf-8"))
        except ConnectionResetError:
            App.show_popup(self)
            connected = False


app = App()
app.run()
