from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel

from app_utils.custom_widgets import *
from utilities import MatrixLoader

EventCreationButton = MatrixLoader.build_utl("Assets/DPT_heatmap.utl")


class BasePopup:
    parent: Layout

    def __init__(self, *args, **kwargs):
        default_args = {"parent": None}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        self.parent = default_args["parent"]
        self.controls = {}
        self.popupWidgets = []
        self.idRef = dict()
        self.AddBackground(args, kwargs)
        self.stackHeight = 0.8
        self.curStackID = 1

    def AddBackground(self, *args, **kwargs):
        self.idRef["DEFAULT"] = 0
        self.popupWidgets.append(dict())
        default_args = {"popup_image": "images/Event_Creation_Blur.png",
                        "background_shade": (0, 0, 0, 0.7), }
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        self.popupWidgets[0]['Background'] = Button(background_color=default_args["background_shade"],
                                                    size=Window.size,
                                                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                    on_press=lambda a: self.CheckDestroy())

        self.popupWidgets[0]['Background_Image'] = Image(source=default_args["popup_image"],
                                                         pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                         size_hint=(0.8, 0.8),
                                                         allow_stretch=True,
                                                         keep_ratio=False)

    def checkboxLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder",
                        "on_checkbox_check": None, "stack_id": self.curStackID}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        wFName = f"CheckBox"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        self.popupWidgets[default_args['stack_id']][wCName] = MDLabel(text=default_args["text"],
                                                                      pos_hint={"center_x": 0.35,
                                                                                "center_y": self.stackHeight},
                                                                      size_hint=(0.4, 0.06),
                                                                      halign="left"
                                                                      )
        self.popupWidgets[default_args['stack_id']][wFName] = CheckBox(
            pos_hint={"center_x": 0.75, "center_y": self.stackHeight},
            size_hint=(0.1, 0.06))

    def titleLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder", "stack_id": self.curStackID, "font_size": "36dp"}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        self.popupWidgets[default_args['stack_id']][wCName] = Label(text=default_args["text"],
                                                                    pos_hint={"center_x": 0.5,
                                                                              "center_y": self.stackHeight},
                                                                    size_hint=(0.3, 0.2), halign="center",
                                                                    font_size=default_args["font_size"],
                                                                    font_name="Fonts/Montserrat-Light.ttf",
                                                                    color="white")

    def inputLabel(self, *args, **kwargs):

        def saveText(self):
            self.controls["id"] = self.text

        default_args = {"id": "default", "text": "placeholder", "stack_id": self.curStackID, "font_size": "18dp"}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        self.popupWidgets[default_args['stack_id']][wCName] = TextInput(text=default_args["text"],
                                                                        pos_hint={"center_x": 0.5,
                                                                                  "center_y": self.stackHeight},
                                                                        size_hint=(0.6, 0.1), halign="center",
                                                                        font_size=default_args["font_size"],
                                                                        font_name="Fonts/Montserrat-Light.ttf", )
        self.popupWidgets[default_args['stack_id']][wCName].on_text = saveText
        self.controls["id"] = ""

    def scrollSelectorLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder", "stack_id": self.curStackID, "font_size": "12dp",
                        "dn_threshold": 0, "up_threshold": 31, "custom_list": None, "template": "date",
                        "current_month": 12, "current_day": 30, "current_year": 2022}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"

        # please for the love of god optimize this
        def dateTemplate():
            def dayUpdate():
                default_args["stack_id"] = self.idRef[default_args["id"]]
                self.controls[default_args['id']][0] = \
                    int(self.popupWidgets[default_args['stack_id']]['days'].text)

            def mntUpdate():
                default_args["stack_id"] = self.idRef[default_args["id"]]
                if not (default_args["current_month"] ==
                        constant_datas.year_months_en.index(
                            self.popupWidgets[default_args['stack_id']]['months'].text) + 1
                        and default_args["current_year"] ==
                        int(self.popupWidgets[default_args['stack_id']]['years'].text)):
                    self.popupWidgets[default_args['stack_id']]['days'].bindCustomArgs(
                        customAccList=None,
                        dn_threshold=1,
                        up_threshold=
                        constant_datas.days_per_month_calculator(
                            int(self.popupWidgets[default_args['stack_id']]['years'].text))[
                            constant_datas.year_months_en.index(
                                self.popupWidgets[default_args['stack_id']]['months'].text)], on_scroll=dayUpdate)
                else:
                    self.popupWidgets[default_args['stack_id']]['days'].bindCustomArgs(
                        customAccList=None,
                        dn_threshold=default_args["current_day"],
                        up_threshold=
                        constant_datas.days_per_month_calculator(
                            int(self.popupWidgets[default_args['stack_id']]['years'].text))[
                            constant_datas.year_months_en.index(
                                self.popupWidgets[default_args['stack_id']]['months'].text)], on_scroll=dayUpdate)
                self.controls[default_args['id']][1] = \
                    constant_datas.year_months_en.index(self.popupWidgets[default_args['stack_id']]['months'].text) + 1
                dayUpdate()

            def yrUpdate():
                default_args["stack_id"] = self.idRef[default_args["id"]]
                if default_args["current_year"] != int(self.popupWidgets[default_args['stack_id']]['years'].text):
                    self.popupWidgets[default_args['stack_id']]['months'].bindCustomArgs(
                        customAccList=constant_datas.year_months_en,
                        dn_threshold=default_args["dn_threshold"],
                        up_threshold=default_args["up_threshold"], on_scroll=mntUpdate)
                    self.popupWidgets[default_args['stack_id']]['days'].bindCustomArgs(
                        customAccList=None,
                        dn_threshold=1,
                        up_threshold=
                        constant_datas.days_per_month_calculator(
                            int(self.popupWidgets[default_args['stack_id']]['years'].text))[
                            constant_datas.year_months_en.index(
                                self.popupWidgets[default_args['stack_id']]['months'].text)], on_scroll=dayUpdate)
                else:
                    self.popupWidgets[default_args['stack_id']]['months'].bindCustomArgs(
                        customAccList=constant_datas.year_months_en[default_args['current_month'] - 1:],
                        dn_threshold=default_args["dn_threshold"],
                        up_threshold=default_args["up_threshold"], on_scroll=mntUpdate)
                    mntUpdate()
                self.controls[default_args['id']][2] = \
                    int(self.popupWidgets[default_args['stack_id']]['years'].text)

            self.popupWidgets[default_args['stack_id']]['years'] = ScrollSelector(text=default_args["text"],
                                                                                  size_hint=(0.2, 0.1), halign="center",
                                                                                  font_size=default_args["font_size"],
                                                                                  font_name="Fonts/Montserrat-Light.ttf",
                                                                                  color="black",
                                                                                  pos_hint={"center_x": 0.75,
                                                                                            "center_y": self.stackHeight}
                                                                                  )

            self.popupWidgets[default_args['stack_id']]['years'].bindCustomArgs(
                customAccList=None,
                dn_threshold=default_args["current_year"],
                up_threshold=2037, on_scroll=yrUpdate)

            self.popupWidgets[default_args['stack_id']]['months'] = ScrollSelector(text=default_args["text"],
                                                                                   size_hint=(0.2, 0.1),
                                                                                   halign="center",
                                                                                   font_size=default_args["font_size"],
                                                                                   font_name="Fonts/Montserrat-Light.ttf",
                                                                                   color="black",
                                                                                   pos_hint={"center_x": 0.5,
                                                                                             "center_y": self.stackHeight}
                                                                                   )
            self.popupWidgets[default_args['stack_id']]['months'].bindCustomArgs(
                customAccList=constant_datas.year_months_en[default_args['current_month'] - 1:],
                dn_threshold=default_args["dn_threshold"],
                up_threshold=default_args["up_threshold"], on_scroll=mntUpdate)

            self.popupWidgets[default_args['stack_id']]['days'] = ScrollSelector(text=default_args["text"],
                                                                                 size_hint=(0.2, 0.1), halign="center",
                                                                                 font_size=default_args["font_size"],
                                                                                 font_name="Fonts/Montserrat-Light.ttf",
                                                                                 color="black",
                                                                                 pos_hint={"center_x": 0.25,
                                                                                           "center_y": self.stackHeight}
                                                                                 )
            self.popupWidgets[default_args['stack_id']]['days'].bindCustomArgs(
                customAccList=None,
                dn_threshold=default_args["current_day"],
                up_threshold=
                constant_datas.days_per_month_calculator(default_args['current_year'])[
                    default_args['current_month'] - 1], on_scroll=dayUpdate)

            self.controls[default_args['id']] = [default_args["current_day"]
                , default_args["current_month"],
                                                 default_args["current_year"]]

        def timeTemplate():
            def updateT(index, key):
                default_args["stack_id"] = self.idRef[default_args["id"]]
                self.controls[default_args['id']][index] = \
                    int(self.popupWidgets[default_args['stack_id']][key].text)

            self.popupWidgets[default_args['stack_id']]['seconds'] = ScrollSelector(text=default_args["text"],
                                                                                    pos_hint={"center_x": 0.75,
                                                                                              "center_y": self.stackHeight},
                                                                                    size_hint=(0.2, 0.1),
                                                                                    halign="center",
                                                                                    font_size=default_args["font_size"],
                                                                                    font_name="Fonts/Montserrat-Light.ttf",
                                                                                    color="black")
            self.popupWidgets[default_args['stack_id']]['seconds'].bindCustomArgs(
                customAccList=None,
                dn_threshold=0,
                up_threshold=59, on_scroll=lambda: updateT(2, 'seconds'))
            self.popupWidgets[default_args['stack_id']]['minutes'] = ScrollSelector(text=default_args["text"],
                                                                                    pos_hint={"center_x": 0.5,
                                                                                              "center_y": self.stackHeight},
                                                                                    size_hint=(0.3, 0.1),
                                                                                    halign="center",
                                                                                    font_size=default_args["font_size"],
                                                                                    font_name="Fonts/Montserrat-Light.ttf",
                                                                                    color="black")
            self.popupWidgets[default_args['stack_id']]['minutes'].bindCustomArgs(
                customAccList=None,
                dn_threshold=0,
                up_threshold=59, on_scroll=lambda: updateT(1, 'minutes'))
            self.popupWidgets[default_args['stack_id']]['hours'] = ScrollSelector(text=default_args["text"],
                                                                                  pos_hint={"center_x": 0.25,
                                                                                            "center_y": self.stackHeight},
                                                                                  size_hint=(0.3, 0.1), halign="center",
                                                                                  font_size=default_args["font_size"],
                                                                                  font_name="Fonts/Montserrat-Light.ttf",
                                                                                  color="black")
            self.popupWidgets[default_args['stack_id']]['hours'].bindCustomArgs(
                customAccList=None,
                dn_threshold=0,
                up_threshold=23, on_scroll=lambda: updateT(0, 'hours'))
            self.controls[default_args['id']] = [0, 0, 0]

        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        templates = {"time": timeTemplate, "date": dateTemplate}
        templates[default_args["template"]]()

    def submitButton(self, *args, **kwargs):
        pass

    def AddToRefs(self, wPname, sID, ):
        if wPname in self.idRef:
            raise Warning("Widget with allocated ID already exists, aborting!")
        self.idRef[wPname] = sID
        self.popupWidgets.insert(sID, dict())

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

    def getDatas(self, key):
        return self.controls.get(key)

    def addWidget(self, type, pos=-1, *args, **kwargs):
        if pos == -1:
            pos = len(self.popupWidgets)
        if self.stackHeight < 0.2:
            return "Widget is full!"
        widgetDict = {"checkboxLabel": self.checkboxLabel, "titleLabel": self.titleLabel,
                      "inputLabel": self.inputLabel, "testLabel": self.scrollSelectorLabel}
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
        print(self.controls)
        for x in self.popupWidgets:
            for y in x.values():
                self.parent.remove_widget(y)
