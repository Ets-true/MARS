KV = '''
#:import MeshLinePlot kivy_garden.graph.MeshLinePlot
<ContentError>:
    Label:
        text: "Не удалось подключиться к серверу"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top":1}

    Button:
        text: "OK"
        size_hint: 0.4, 0.2
        pos_hint: {"x":0.1, "y":0.1}
        on_press: app.close_popup()

<SetGraph>:
    graph : graph
    Graph:
        id: graph
        background_color: 1, 0.63, 0, 1
        plot: MeshLinePlot
        xlabel:'Time'
        x_tics_major: 25
        y_grid_label: True
        x_grid_label: True
        padding:5
        x_grid:True
        y_grid:True
        xmin:0
        xmax:25
        ymin:0
        pos: 0, root.height / 3.86
        size: root.width , root.height * 16 / 24
        
        
<ContentNavigationDrawer>

    ScrollView:

        MDList:

            OneLineListItem:
                text: "Tools"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Tools"
                    app.server_connect()
                    app.stop_receiving()
                    
            OneLineListItem:
                text: "Analitics"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Analitics"
                    app.start_receiving()
                    app.server_connect()


MDScreen:
    
    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "Menu"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        md_bg_color: 1, 0.63, 0, 1

    MDNavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            MDScreen:
                name: "Main"

                MDLabel:
                    text: "This is Main screen"
                    halign: "center"

            MDScreen:
                name: "Tools"

                MDIconButton:
                    id: fan
                    icon: "fan-off"
                    theme_text_color: "Custom"
                    pos_hint:{"top": 0.85, "right": 0.40}
                    text_color: 1, 0.63, 0, 1
                    user_font_size : '64dp'
                    on_press: app.on_press_vent()
                
                MDIconButton:
                    id: window
                    icon: "window-closed-variant"
                    theme_text_color: "Custom"
                    pos_hint:{"top": 0.65, "right": 0.40}
                    text_color: 1, 0.63, 0, 1
                    user_font_size : '64dp'
                    on_press: app.on_press_window()
                    
                MDIconButton:
                    id: door
                    icon: "door-closed"
                    theme_text_color: "Custom"
                    pos_hint:{"top": 0.45, "right": 0.40}
                    text_color: 1, 0.63, 0, 1
                    user_font_size : '64dp'
                    on_press: app.on_press_door()
                    
                MDIconButton:
                    id: led
                    icon: "led-off"
                    theme_text_color: "Custom"
                    pos_hint:{"top": 0.25, "right": 0.40}
                    text_color: 1, 0.63, 0, 1
                    user_font_size : '64dp'
                    on_press: app.led_enable()
                    
                MDSlider:
                    id: vent_speed
                    min: 0
                    max: 255
                    hint: True
                    color: 1, 0.63, 0, 1
                    pos_hint:{"top": 0.775, "right": 0.80}
                    size_hint: 0.4, 0.1
                    on_value: app.change_vent_speed()
                    
                MDSlider:
                    id: window_rotation
                    min: 0
                    max: 180
                    hint: True
                    color: 1, 0.63, 0, 1
                    pos_hint:{"top": 0.575, "right": 0.80}
                    size_hint: 0.4, 0.1
                    on_value: app.change_window_rotation()
                    
                MDSlider:
                    id: door_rotation
                    min: 0
                    max: 180
                    hint: True
                    color: 1, 0.63, 0, 1
                    pos_hint:{"top": 0.375, "right": 0.80}
                    size_hint: 0.4, 0.1
                    on_value: app.change_door_rotation()
                    
                MDSlider:
                    id: led_change
                    min: 0
                    max: 255
                    hint: True
                    color: 1, 0.63, 0, 1
                    pos_hint:{"top": 0.175, "right": 0.80}
                    size_hint: 0.4, 0.1
                    on_value: app.change_led()
                    
            MDScreen:
                name: "Analitics"
                id: analitics
                
                MDIconButton:
                    id: graph_swap_1
                    icon: "arrow-left-bold-outline"
                    theme_text_color: "Custom"
                    pos_hint:{"top": 0.2, "right": 0.4}
                    text_color: 1, 0.63, 0, 1
                    user_font_size : '64dp'
                    on_press: app.change_graph_left()
                    
                MDIconButton:
                    id: graph_swap_2
                    icon: "arrow-right-bold-outline"
                    theme_text_color: "Custom"
                    pos_hint:{"top": 0.2, "right": 1.1}
                    text_color: 1, 0.63, 0, 1
                    user_font_size : '64dp'
                    on_press: app.change_graph_right()
                    
                MDLabel:
                    id: stats
                    pos_hint:{"top": 0.220, "right": 0.85}
                    size_hint: 0.6, 0.1
                    font_size : '15dp'
                    font_name: "Machine_BT"
                    

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''