from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivymd.uix.label import MDLabel

from utilities import MatrixLoader

EventCreationButton = MatrixLoader.build_utl("Assets/DPT_heatmap.utl")


class BasePopup:
    parent: Layout

    def __init__(self, *args, **kwargs):
        default_args = {"popup_image": "images/Event_Creation_Blur.png",
                        "background_shade": (0, 0, 0, 0.7),
                        "parent": None}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        self.parent = default_args["parent"]
        self.popupWidgets = []
        self.idRef = {"DEFAULT": 0, }
        self.popupWidgets.append(dict())
        self.popupWidgets[0]['Background'] = Button(background_color=default_args["background_shade"],
                                                    size=Window.size,
                                                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                    on_press=lambda a: self.CheckDestroy())

        self.popupWidgets[0]['Background_Image'] = Image(source=default_args["popup_image"],
                                                         pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                         size_hint=(0.8, 0.8),
                                                         allow_stretch=True,
                                                         keep_ratio=False)
        self.stackHeight = 0.8
        self.curStackID = 1

    def checkboxLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder",
                        "on_checkbox_check": None, "stack_id": self.curStackID}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        wFName = f"CheckBox"
        wPName = f"{default_args['id']}"
        self.idRef[wPName] = default_args['stack_id']
        self.popupWidgets.insert(default_args['stack_id'], dict())
        self.popupWidgets[default_args['stack_id']][wCName] = MDLabel(text=default_args["text"],
                                                                      pos_hint={"center_x": 0.35,
                                                                                "center_y": self.stackHeight},
                                                                      size_hint=(0.3, 0.06))
        self.popupWidgets[default_args['stack_id']][wFName] = CheckBox(
            pos_hint={"center_x": 0.75, "center_y": self.stackHeight},
            size_hint=(0.1, 0.06))

    def UpdateIdRef(self):
        items = list(self.idRef.items())
        indIns = int(items[-1][-1])
        items.insert(indIns, items[-1])
        items.pop(-1)
        lastInd = -1
        for x in range(len(items)):
            if items[x][1] - lastInd > 1:
                items[x] = (items[x][0], items[x][1] - 1)
            elif items[x][1] - lastInd <= 0:
                items[x] = (items[x][0], items[x][1] + 1)
            lastInd = items[x][1]
        self.idRef = dict(items)

    def UpdatePopupWidgets(self):
        stack_height = 0.8
        for x in range(1, len(self.popupWidgets)):
            for y in self.popupWidgets[x].keys():
                self.popupWidgets[x][y].pos_hint["center_y"] = stack_height
            stack_height -= 0.1
        self.stackHeight = stack_height

    def removeWidget(self, id):
        index = self.idRef[id]
        del self.idRef[id]
        RM = self.popupWidgets.pop(index)
        for x in RM.values():
            self.parent.remove_widget(x)
        self.UpdatePopupWidgets()
        self.UpdateIdRef()
        self.curStackID -= 1

    def _multilineIndex(self, List, sub_index, find):
        for n in range(len(List)):
            if List[n][sub_index] == find:
                return n

    def addWidget(self, type, pos=-1, *args, **kwargs):
        if pos == -1:
            pos = len(self.popupWidgets)
        if self.stackHeight < 0.2:
            return "Widget is full!"
        widgetDict = {"checkboxLabel": self.checkboxLabel, }
        widgetDict[type](stack_id=pos, *args, **kwargs)
        self.UpdatePopupWidgets()
        self.UpdateIdRef()
        self.curStackID += 1

    def build_self(self):
        for x in self.popupWidgets:
            for y in x.values():
                self.parent.add_widget(y)

    def CheckDestroy(self):
        choice = MatrixLoader.CheckAreaOnUtl(EventCreationButton, self.popupWidgets[0]["Background"]
                                             , Window.mouse_pos)
        if choice:
            self.destroy_self()

    def destroy_self(self):
        for x in self.popupWidgets:
            for y in x.values():
                self.parent.remove_widget(y)
