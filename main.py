import os
import re

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from app_utils import PopupBuilder
from utilities import MatrixLoader
from utilities.Hashtools import *
from utilities.Modular_DB_creator import Assembler
from utilities.Timetools import *
from utilities.modular_DB_opener import Opener

Window.size = (700 / 1.8, 1560 / 2)

try:
    Runhash = open("runhash.dat", "r")

except FileNotFoundError:
    Runhash = InitHash("runhash", "FirstRun:int:0")

StartButton = MatrixLoader.build_utl("Assets/SB_heatmap.utl")


Datas = FormatHash(Runhash.read())
print(Datas)
APerm = Assembler("UserData", "a")
OPerm = Opener("UserData")


class ImageButton(ButtonBehavior, Image):
    pass


class User:

    def __init__(self):
        self.windows = {1: "start", 2: "main", 3: "planner", 4: "stats", 5: "facts", 6: "settings", 7: "user"}
        self.last_screen = 1
        self.hasUD = False

    def addBaseUserData(self, raw_data):
        self.hasUD = True
        BaseUD = raw_data
        self.refName = raw_data[0]
        self.name = raw_data[1]
        self.surname = raw_data[2]
        self.emaill = raw_data[3]
        self.ageGroup = raw_data[4]
        self.UID = raw_data[5]

    def AddActivities(self):
        activities = OPerm.GetData(f"{self.refName}_Activities", "activity_active=1")
        if len(activities) != 3:
            raise RuntimeError("Activities be real bad")
        self.activities = [(i[0], i[2]) for i in activities]
        self.activities.sort(key=lambda a: a[1])
        self.activities = [i[0] for i in activities]

    def GetActivities(self):
        return self.activities

    def set_last_screen(self, last_screen):
        self.last_screen = last_screen

    def get_last_screen(self):
        return self.last_screen

    def __getitem__(self, item):
        return self.windows.get(item, 1)


class BasicWidgetFunctions:

    def goto_window(self, window_id):
        U.set_last_screen(self.manager.current)
        self.manager.current = U[window_id]
        self.superWindowInit(U[window_id])

    def goto_last(self):
        self.manager.current = U.get_last_screen()
        self.superWindowInit(self.manager.current)

    def getWindowSize(self):
        return Window.size

    def getScreen(self, screen_name):
        return self.manager.get_screen(screen_name)

    def superWindowInit(self, window_name):
        # All init functions must contain this function!
        new_screen = self.manager.get_screen(window_name)
        new_screen.start_init()


class CommonWidgetVariables:
    default_bottom_menu_src = "images/Bottom_MenuNew.png"


class WindowManager(ScreenManager):
    pass


class StartWindow(Screen, BasicWidgetFunctions):
    WelcomeText = StringProperty("__NAME__")
    StartMotivationalLabel = StringProperty("Let's get some work done!")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.DemoVar = StringProperty("Test label")
        Clock.schedule_once(lambda a: self.check_first_login(), 0)

    def check_first_login(self):
        if Datas["FirstRun"] == 0:
            self.manager.current = "login"
        elif Datas["FirstRun"] == 1:
            self.manager.current = "second_form"
        else:
            self.start_init()

    def start_init(self):

        Data = OPerm.GetData("Users", "user_identifier=1")
        U.addBaseUserData(Data[0])
        self.initialize_vars()

    def initialize_vars(self):
        U.AddActivities()
        self.WelcomeText = f"{getLocTimeGreet()} {U.name}."

    def center_widget_clicked(self):
        choice = MatrixLoader.CheckAreaOnUtl(StartButton, self.ids.startPointerButton, Window.mouse_pos)
        if not choice:
            return
        acts = U.GetActivities()
        M = self.getScreen("main")
        M.setCurrentActivity(acts[choice - 1])
        self.goto_window(2)


class MainWindow(Screen, BasicWidgetFunctions):
    popupEvents = {}
    CurrentActivity = ""
    ButtonStates = {"PauseButton": 1, }
    timer_time = StringProperty("00:00")
    Paus_Cont = StringProperty("Pause")
    TSCHD = TimerInstance()

    def start_init(self):
        print("Main window init")
        # Here the program loads activities

    def setCurrentActivity(self, activity):
        self.CurrentActivity = activity
        self.MainText = f"You have chosen: {self.CurrentActivity}"

    def UpdateTimer(self):
        tc = self.TSCHD.GetTicSecs()
        show = f"{fix_format(tc['m']) if not tc['h'] else fix_format(tc['h'])}:{fix_format(tc['s']) if not tc['h'] else fix_format(tc['m'])}"
        self.timer_time = show

    def PauseTimer(self):
        self.ButtonStates["PauseButton"] *= -1
        states = {-1: "Resume", 1: "Pause"}
        self.PauseButton.text = states[self.ButtonStates["PauseButton"]]
        if self.ButtonStates["PauseButton"] == -1:
            print("paused")
            self.TSCHD.freezeEvent()
            self.tick_event.cancel()
        else:
            print("resumed")
            self.TSCHD.unFreezeEvent()
            self.UpdateTimer()
            self.tick_event = Clock.schedule_interval(lambda a: self.UpdateTimer(), 1)

    def ResetTimer(self):
        self.tick_event.cancel()
        self.timer_time = "00:00"
        self.fLayout.add_widget(self.sButton)
        self.fLayout.remove_widget(self.PauseButton)
        self.fLayout.remove_widget(self.ResetButton)

    def ChangeWidgetState(self, widget, z):

        print(widget, z)
        if self.popupEvents[widget].disabled:
            self.popupEvents[widget].disabled = False
        else:
            self.popupEvents[widget].disabled = True

    def EventCreationTab(self):

        self.BuildEventPopup = PopupBuilder.BasePopup(parent=self.ids.FloatTimer)
        self.BuildEventPopup.addWidget("checkboxLabel", pos=-1, text="HelloItsMe", id="CL1")
        self.BuildEventPopup.addWidget("checkboxLabel", pos=-1, text="No, really", id="CL2")
        self.BuildEventPopup.addWidget("checkboxLabel", pos=1, text="But can you do this", id="CL3")
        self.BuildEventPopup.addWidget("testLabel", pos=1, id="C4")
        self.BuildEventPopup.addWidget("titleLabel", pos=1, text="Le title", id="T1")

        self.BuildEventPopup.build_self()

    def AddEvent(self):
        self.EventCreationTab()

    def ActivateTimer(self):
        # Startaj count
        self.fLayout = self.ids.FloatTimer
        self.TSCHD.StartTic()
        self.sButton = self.ids.StartTimerButton
        self.fLayout.remove_widget(self.sButton)
        self.PauseButton = MDFillRoundFlatButton(text=self.Paus_Cont, on_press=lambda a: self.PauseTimer(),
                                                 pos_hint={"center_x": .28, "center_y": .2}, size_hint=(.4, .07),
                                                 font_size="36dp")
        self.ResetButton = MDFillRoundFlatButton(text="Reset", on_press=lambda a: self.ResetTimer(),
                                                 pos_hint={"center_x": .72, "center_y": .2}, size_hint=(.4, .07),
                                                 font_size="36dp")
        self.fLayout.add_widget(self.PauseButton)
        self.fLayout.add_widget(self.ResetButton)
        self.tick_event = Clock.schedule_interval(lambda a: self.UpdateTimer(), 1)


# Login je mostly gotov
class LoginWindow(Screen):
    ErrNameText = StringProperty("")
    ErrMailText = StringProperty("")
    DisabledSubmit = BooleanProperty(True)
    DoneForms = {"NameSurname": False, "Email": False, "AgeGroup": False}

    def __init__(self, **kw):
        super().__init__(**kw)
        self.AgeText = StringProperty()
        self.AgeText = "Select your age group:"
        self.ages = {1: "Youth: 0-19",
                     2: "Adult: 20-39",
                     3: "Middle Aged: 40-59",
                     4: "Old: 60-99"}

    def verify_name(self, widget):
        ver_exp = "^[\w]{2,20}\s[\w]{2,20}$"
        if re.match(ver_exp, widget.text):
            self.ErrNameText = ""
            self.DoneForms["NameSurname"] = True
        else:
            self.ErrNameText = "Name/Surname invalid!"
            self.DoneForms["NameSurname"] = False
        self.ChkDone()

    def verify_email(self, widget):
        ver_exp = "^[\w.]*?@(gmail|webmail|yahoo|skole).[a-z]{2,3}$"
        if re.match(ver_exp, widget.text):
            self.ErrMailText = ""
            self.DoneForms["Email"] = True
        else:
            self.ErrMailText = "Mail invalid!"
            self.DoneForms["Email"] = False
        self.ChkDone()

    def OpenAgeGroup(self):

        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": self.ages[1],
                "on_release": lambda: self.AgeSelect(1)
            }
            ,
            {
                "viewclass": "OneLineListItem",
                "text": self.ages[2],
                "on_release": lambda: self.AgeSelect(2)
            }
            ,
            {
                "viewclass": "OneLineListItem",
                "text": self.ages[3],
                "on_release": lambda: self.AgeSelect(3)
            }
            ,
            {
                "viewclass": "OneLineListItem",
                "text": self.ages[4],
                "on_release": lambda: self.AgeSelect(4)
            }

        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.ageButton,
            width_mult=4,
            items=self.menu_list,
            max_height=dp(112 * 1.8),

        )
        self.menu.open()

    def AgeSelect(self, age):
        print(self.ages[age])
        self.ids.ageButton.text = self.ages[age]
        self.menu.dismiss()
        self.DoneForms["AgeGroup"] = True
        self.ChkDone()

    def ChkDone(self):
        if not False in self.DoneForms.values():
            self.DisabledSubmit = False
        else:
            self.DisabledSubmit = True

    def submitLogin(self):
        dct = dict()
        for x in self.ages.items():
            dct[x[1]] = x[0]
        AgeGroup = dct[self.ids.ageButton.text]
        NameAndSurname = self.ids.nameSurname.text.replace(" ", "_")
        Email = self.ids.Email.text
        APerm.create_tables(["Users", f"{NameAndSurname}_Events", f"{NameAndSurname}_Projects",
                             f"{NameAndSurname}_Goals", f"{NameAndSurname}_Activities"],
                            [["ref_name", "name", "surname", "email", "age_group", "user_identifier"],
                             ["event_name", "event_desc", "event_time", "event_repetitions", "event_cooldown",
                              "event_score", "event_active",
                              "event_priority", "EID"],
                             ["project_name", "project_desc", "start_date", "end_date", "project_active",
                              "project_score", "project_priority", "project_goal", "PID"],
                             ["goal_name", "goal_desc", "goal_ref", "goal_score", "GID"],
                             ["activity_name", "activity_active", "activity_slot", "activity_misc"]])

        APerm.AddToTable("Users", [NameAndSurname, NameAndSurname.split("_")[0],
                                   NameAndSurname.split("_")[1], Email, AgeGroup, 1])
        Datas["FirstRun"] = 1
        WriteToHash(Datas)

        self.manager.current = "second_form"


class SubWindowPlanner(Screen, BasicWidgetFunctions):
    def start_init(self):
        print("Planner init")


class SubWindowStats(Screen, BasicWidgetFunctions):
    def start_init(self):
        print("stats init")


# second form je mostly gotov
class SecondFormWindow(Screen):
    textVerTot = 1

    def txtChk(self):
        L = (self.ids.act1, self.ids.act2, self.ids.act3)
        self.textVerTot = 1
        for i in range(3):
            if len(L[i].text) > 15 or not L[i].text:
                self.textVerTot = 0
        if self.textVerTot:
            self.ids.submitAct.disabled = False
        else:
            self.ids.submitAct.disabled = True

    def addActivityData(self):
        Datas = {"activity_one": self.ids.act1.text,
                 "activity_two": self.ids.act2.text,
                 "activity_three": self.ids.act3.text}

        Data = OPerm.GetData("Users", "user_identifier=1")
        print(Data)
        Uname = Data[0][0]
        ain = 1
        for x in Datas.items():
            APerm.AddToTable(f"{Uname}_Activities", [x[1], 1, ain, None])
            ain += 1

    def SubmitArrangement(self):
        self.addActivityData()
        start_screen = self.manager.get_screen("start")
        Datas["FirstRun"] = 2
        WriteToHash(Datas)

        start_screen.start_init()
        self.manager.current = "start"


class SubWindowFacts(Screen, BasicWidgetFunctions):
    def start_init(self):
        print("Facts window init")


class SettingsWindow(Screen, BasicWidgetFunctions):
    def start_init(self):
        print("Settings window init")

    def WipeUserQuery(self):
        self.show_alert_dialog()
        return

    def WipeUserConfirm(self):
        APerm.closeConn()
        OPerm.closeConn()
        Runhash.close()
        os.remove("UserData.db")
        os.remove("runhash.dat")
        quit(0)

    def show_alert_dialog(self):
        self.del_data_dialog = MDDialog(
            text="Are you sure? \n ..there is no going back",
            buttons=[
                MDFlatButton(
                    text="YES",
                    on_release=lambda a: self.WipeUserConfirm()

                ),
                MDFlatButton(
                    text="NO",
                    on_release=lambda a: self.close_alert_dialog()

                ),
            ],
        )
        self.del_data_dialog.open()

    def close_alert_dialog(self):
        self.del_data_dialog.dismiss()


class SubWindowUser(Screen, BasicWidgetFunctions):
    def start_init(self):
        print("User window init")


class MainApp(MDApp):
    def build(self):
        Start_Screen = Builder.load_file("core.kv")
        return Start_Screen


U = User()
X = MainApp()
X.run()
