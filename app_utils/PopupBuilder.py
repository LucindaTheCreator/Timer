from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch

from app_utils import constant_datas
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
                        "on_checkbox_check": None, "stack_id": self.curStackID, "additional_bind": None}

        def update_state(selfT, instance):
            self.controls[default_args["id"]] = selfT.active
            if default_args["additional_bind"]:
                default_args["additional_bind"](selfT.active)

        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        wFName = f"CheckBox"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        reference_widget: dict = self.popupWidgets[default_args["stack_id"]]
        reference_widget[wCName] = MDLabel(text=default_args["text"],
                                           pos_hint={"center_x": 0.35,
                                                     "center_y": self.stackHeight},
                                           size_hint=(0.4, 0.06),
                                           halign="left"
                                           )
        reference_widget[wFName] = MDSwitch(
            pos_hint={"center_x": 0.75, "center_y": self.stackHeight},
            size_hint=(0.1, 0.06))
        reference_widget[wFName].bind(active=update_state)
        self.controls[default_args["id"]] = 0

    def titleLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder", "stack_id": self.curStackID, "font_size": "36dp"}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        reference_widget: dict = self.popupWidgets[default_args["stack_id"]]
        reference_widget[wCName] = Label(text=default_args["text"],
                                         pos_hint={"center_x": 0.5,
                                                   "center_y": self.stackHeight},
                                         size_hint=(0.3, 0.2), halign="center",
                                         font_size=default_args["font_size"],
                                         font_name="Fonts/Montserrat-Light.ttf",
                                         color="white")

    def inputLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder", "stack_id": self.curStackID, "font_size": "18dp",
                        "background_color": (1, 1, 1, 1)}

        def saveText(selfT, instance):
            self.controls[default_args["id"]] = selfT.text

        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        reference_widget: dict = self.popupWidgets[default_args["stack_id"]]
        reference_widget[wCName] = TextInput(text=default_args["text"],
                                             pos_hint={"center_x": 0.5,
                                                       "center_y": self.stackHeight},
                                             size_hint=(0.6, 0.08), halign="center",
                                             font_size=default_args["font_size"],
                                             font_name="Fonts/Montserrat-Light.ttf",
                                             background_color=default_args["background_color"], )
        reference_widget[wCName].bind(text=saveText)
        self.controls[default_args["id"]] = ""

    def scrollSelectorLabel(self, *args, **kwargs):

        default_args = {"id": "default", "text": "placeholder", "stack_id": self.curStackID, "font_size": "12dp",
                        "dn_threshold": 0, "up_threshold": 31, "custom_list": None, "template": "date",
                        "current_month": 12, "current_day": 30, "current_year": 2022}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Label"

        def base_template(keys):
            default_kwargs = {"size_hint": (0.2, 0.1), "halign": "center", "font_size": default_args["font_size"],
                              "font_name": "Fonts/Montserrat-Light.ttf", "color": "black", "text": "NULL"}
            reference_widget: dict = self.popupWidgets[default_args["stack_id"]]
            for iterator in range(1, 4):
                reference_widget[keys[iterator - 1]] = ScrollSelector(**default_kwargs,
                                                                      pos_hint={"center_x": iterator / 4,
                                                                                "center_y": self.stackHeight})


        def dateTemplate():

            reference_widget: dict = self.popupWidgets[default_args["stack_id"]]

            def dayUpdate():
                default_args["stack_id"] = self.idRef[default_args["id"]]
                self.controls[default_args['id']][0] = \
                    int(reference_widget['days'].text)

            # please for the love of god optimize this
            def mntUpdate():
                default_args["stack_id"] = self.idRef[default_args["id"]]
                if not (default_args["current_month"] ==
                        constant_datas.year_months_en.index(
                            reference_widget['months'].text) + 1
                        and default_args["current_year"] ==
                        int(reference_widget['years'].text)):
                    reference_widget['days'].bindCustomArgs(
                        customAccList=None,
                        dn_threshold=1,
                        up_threshold=
                        constant_datas.days_per_month_calculator(
                            int(reference_widget['years'].text))[
                            constant_datas.year_months_en.index(
                                reference_widget['months'].text)], on_scroll=dayUpdate)
                else:
                    reference_widget['days'].bindCustomArgs(
                        customAccList=None,
                        dn_threshold=default_args["current_day"],
                        up_threshold=
                        constant_datas.days_per_month_calculator(
                            int(reference_widget['years'].text))[
                            constant_datas.year_months_en.index(
                                reference_widget['months'].text)], on_scroll=dayUpdate)
                self.controls[default_args['id']][1] = \
                    constant_datas.year_months_en.index(reference_widget['months'].text) + 1
                dayUpdate()

            def yrUpdate():

                if default_args["current_year"] != int(reference_widget['years'].text):
                    reference_widget['months'].bindCustomArgs(custom_acc_list=constant_datas.year_months_en)
                else:
                    reference_widget['months'].bindCustomArgs(
                        custom_acc_list=constant_datas.year_months_en[default_args['current_month'] - 1:])
                mntUpdate()
                self.controls[default_args['id']][2] = \
                    int(reference_widget['years'].text)

            reference_widget['years'].bindCustomArgs(
                dn_threshold=default_args["current_year"],
                up_threshold=2037, on_scroll=yrUpdate)

            reference_widget['months'].bindCustomArgs(
                custom_acc_list=constant_datas.year_months_en[default_args['current_month'] - 1:], on_scroll=mntUpdate)

            reference_widget['days'].bindCustomArgs(
                dn_threshold=default_args["current_day"],
                up_threshold=
                constant_datas.days_per_month_calculator(default_args['current_year'])[
                    default_args['current_month'] - 1], on_scroll=dayUpdate)

            self.controls[default_args['id']] = [default_args["current_day"]
                , default_args["current_month"],
                                                 default_args["current_year"]]

        def timeTemplate():
            reference_widget: dict = self.popupWidgets[default_args["stack_id"]]

            def updateT(index, key):
                self.controls[default_args['id']][index] = int(reference_widget[key].text)

            reference_widget['seconds'].bindCustomArgs(
                customAccList=None,
                dn_threshold=0,
                up_threshold=59, on_scroll=lambda: updateT(2, 'seconds'))

            reference_widget['minutes'].bindCustomArgs(
                dn_threshold=0,
                up_threshold=59, on_scroll=lambda: updateT(1, 'minutes'))

            reference_widget['hours'].bindCustomArgs(
                dn_threshold=0,
                up_threshold=23, on_scroll=lambda: updateT(0, 'hours'))

            self.controls[default_args['id']] = [0, 0, 0]

        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        templates = {"time": timeTemplate, "date": dateTemplate}
        template_keys = {"time": ["seconds", "minutes", "hours"], "date": ["days", "months", "years"]}
        base_template(template_keys[default_args["template"]])
        templates[default_args["template"]]()

    def submitButton(self, *args, **kwargs):
        default_args = {"id": "default", "text_1": "placeholder", "text_2": "placeholder_2"
            , "stack_id": self.curStackID, "bind_event_1": None, "bind_event_2": None}
        for x in kwargs.items():
            default_args[x[0]] = x[1]
        wCName = f"Button"
        try:
            self.AddToRefs(f"{default_args['id']}", default_args['stack_id'])
        except Warning:
            return
        reference_widget: dict = self.popupWidgets[default_args["stack_id"]]
        reference_widget[f"{wCName}_1"] = MDFillRoundFlatButton(text=default_args["text_1"],
                                                                on_release=default_args[
                                                                    "bind_event_1"],
                                                                pos_hint={"center_x": 0.7,
                                                                          "center_y": self.stackHeight},
                                                                size_hint=(0.25, 0.05)
                                                                )
        reference_widget[f"{wCName}_2"] = MDFillRoundFlatButton(text=default_args["text_2"],
                                                                on_release=default_args[
                                                                    "bind_event_2"],
                                                                pos_hint={"center_x": 0.3,
                                                                          "center_y": self.stackHeight},
                                                                size_hint=(0.25, 0.05)
                                                                )

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
            stack_height -= 0.08
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

    def getDatas(self, key=None):
        if not key:
            return self.controls.items()
        return self.controls.get(key)

    def addWidget(self, type, pos=-1, *args, **kwargs):
        if pos == -1:
            pos = len(self.popupWidgets)
        if self.stackHeight < 0.2:
            return "Widget is full!"
        widgetDict = {"checkboxLabel": self.checkboxLabel, "titleLabel": self.titleLabel,
                      "inputLabel": self.inputLabel, "scrollSelectorLabel": self.scrollSelectorLabel,
                      "control_buttons": self.submitButton}
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
