from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.layout import Layout

from utilities import MatrixLoader

EventCreationButton = MatrixLoader.build_utl("Assets/DPT_heatmap.utl")


class BasePopup:
    parent: Layout

    def __init__(self, *args, **kwargs):
        print(kwargs)
        default_args = {"popup_image": "images/Event_Creation_Blur.png",
                        "background_shade": (0, 0, 0, 0.7),
                        "parent": None}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        self.parent = default_args["parent"]
        self.popupWidgets = dict()
        self.popupWidgets["Background"] = Button(background_color=default_args["background_shade"], size=Window.size,
                                                 pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                 on_press=lambda a: self.CheckDestroy())

        self.popupWidgets["MainFill"] = Image(source=default_args["popup_image"],
                                              pos_hint={"center_x": 0.5, "center_y": 0.5},
                                              size_hint=(0.8, 0.8),
                                              allow_stretch=True,
                                              keep_ratio=False)

    def build_self(self):
        for x in self.popupWidgets.values():
            self.parent.add_widget(x)

    def CheckDestroy(self):
        choice = MatrixLoader.CheckAreaOnUtl(EventCreationButton, self.popupWidgets["Background"]
                                             , Window.mouse_pos)
        if choice:
            self.destroy_self()

    def destroy_self(self):
        for x in self.popupWidgets.values():
            self.parent.remove_widget(x)
