import re

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

from utilities.Hashtools import *
from utilities.Modular_DB_creator import Assembler
from utilities.Timetools import *
from utilities.modular_DB_opener import Opener

Window.size = (700 / 1.8, 1560 / 2)

O = Opener


try:
    Runhash = open("runhash.dat", "r")
    print("opened")

except FileNotFoundError:
    Runhash = open("runhash.dat", "w")
    Runhash.write("FirstRun:bool:True")
    Runhash.close()
    Runhash = open("runhash.dat", "r")

Datas = FormatHash(Runhash.read())
print(Datas)


class User:

    def __init__(self):
        self.windows = {1: "start", 2: "main", 3: "blank", 4: "stats", 5: "facts", 6: "settings"}
        self.last_screen = 1
        self.hasUD = False

    def addBaseUserData(self,raw_data):
        self.hasUD = True
        BaseUD = raw_data
        self.name = raw_data[0]
        self.surname = raw_data[1]
        self.emaill = raw_data[2]
        self.ageGroup = raw_data[3]
        self.UID = raw_data[4]

    def set_last_screen(self, last_screen):
        self.last_screen = last_screen

    def get_last_screen(self):
        return self.last_screen

    def __getitem__(self, item):
        return self.windows.get(item, 1)


class BasicFunctions:

    def goto_window(self, window_id):
        U.set_last_screen(self.manager.current)
        self.manager.current = U[window_id]

    def goto_last(self):
        self.manager.current = U.get_last_screen()


class WindowManager(ScreenManager):
    pass


class StartWindow(Screen, BasicFunctions):
    WelcomeText = StringProperty("__NAME__")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.DemoVar = StringProperty("Test label")
        Clock.schedule_once(lambda a: self.check_first_login(), 0)

    def check_first_login(self):
        if Datas["FirstRun"]:
            self.manager.current = "login"
        else:
            self.start_init()

    def start_init(self):
        Otemp = O("UserData")
        Data = Otemp.GetData("Users", "user_identifier=1")
        U.addBaseUserData(Data[0])
        self.initialize_vars()

    def initialize_vars(self):
        self.WelcomeText = f"{getLocTimeGreet()} {U.name}."


    def center_widget_clicked(self):
        sz = (Window.size[0] / 2, Window.size[1] / 2)
        mp = Window.mouse_pos
        if ((sz[0] - mp[0]) * (sz[0] - mp[0]) + (sz[1] - mp[1]) * (sz[1] - mp[1])) ** 0.5 < 25:
            self.goto_window(2)
        elif mp[1] > sz[1]:
            self.goto_window(3)
        else:
            if mp[0] < sz[0]:
                self.goto_window(4)
            elif mp[0] >= sz[0]:
                self.goto_window(5)

    def UtilLogin(self):
        self.goto_window(2)


class MainWindow(Screen, BasicFunctions):
    pass


#Login je mostly gotov
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
        D = Assembler("UserData")
        D.create_tables(["Users", f"{NameAndSurname}_Events", f"{NameAndSurname}_Functionality"],
                        [["name", "surname", "email", "age_group", "user_identifier"],
                         ["event_name", "event_desc", "start_time", "end_time", "event_score", "event_priority", "EID"],
                         ["projects", "goals", "personalization_temp", "misc"]])
        D.AddToTable("Users", [NameAndSurname.split("_")[0], NameAndSurname.split("_")[1], Email, AgeGroup,1])
        Datas["FirstRun"] = False
        WriteToHash(Datas)
        start_screen = self.manager.get_screen("start")
        start_screen.start_init()

        self.manager.current = "start"


class SubWindowBlank(Screen, BasicFunctions):
    pass


class SubWindowStats(Screen, BasicFunctions):
    pass

class SecondFormWindow(Screen,BasicFunctions):
    pass

class SubWindowFacts(Screen, BasicFunctions):
    pass


class SettingsWindow(Screen, BasicFunctions):
    pass


class MainApp(MDApp):

    def build(self):
        Start_Screen = Builder.load_file("core.kv")
        return Start_Screen


U = User()
X = MainApp()
X.run()
