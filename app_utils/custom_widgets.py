import math

from kivy.core.window import Window
from kivy.uix.behaviors import *
from kivy.uix.label import Label

from app_utils import constant_datas


def clamp(x, max0, min0):
    if x > max0:
        return max0
    elif x < min0:
        return min0
    return x


class ScrollSelector(Label, ButtonBehavior):
    touched = False
    upThreshold = 2030
    dnThreshold = 2023
    accList = [i for i in range(dnThreshold, upThreshold + 1)]
    startTouch = 0
    change = 0
    scrollRatio = math.tanh(Window.size[1] / 100) * 10
    Ind = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = str(self.accList[0])
        self.on_scroll = self.placeholder

    def bindCustomArgs(self, up_threshold=31, dn_threshold=0, customAccList=None, on_scroll=None):
        if customAccList:
            self.accList = customAccList
        else:
            self.upThreshold = up_threshold
            self.dnThreshold = dn_threshold
            self.accList = [i for i in range(self.dnThreshold, self.upThreshold + 1)]
        self.text = str(self.accList[0])
        if on_scroll:
            self.on_scroll = on_scroll

    def placeholder(self):
        pass

    def on_touch_down(self, touch):
        self.startTouch = touch.pos[1]
        if self.calcAvgDist(touch.pos, self.pos, self.size):
            self.touched = True

    def calcAvgDist(self, pos1, pos2, size):
        return (abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2) < (
                    (size[0] // 2) ** 2 + (size[1] // 2) ** 2) // 1.5

    def set_up_for_days(self, current_date, month_num, year, currentMY=True):
        self.upThreshold = constant_datas.days_per_month_calculator(year)[month_num]
        if currentMY:
            self.dnThreshold = current_date
        else:
            self.dnThreshold = 0
        self.accList = [i for i in range(self.dnThreshold, self.upThreshold + 1)]
        self.text = str(self.accList[0])

    def on_touch_move(self, touch):
        if not self.touched:
            return
        self.DeltaTouch = int(touch.pos[1] - self.startTouch)
        self.change += self.DeltaTouch
        self.startTouch = touch.pos[1]
        if self.change > self.scrollRatio:
            self.Ind = round(clamp(int(self.Ind) + 1, len(self.accList) - 1, 0))
            c = self.text
            self.text = str(self.accList[self.Ind])
            if c != self.text:
                self.on_scroll()
            self.change = 0
        elif self.change < -self.scrollRatio:
            self.Ind = round(clamp(int(self.Ind) - 1, len(self.accList) - 1, 0))
            c = self.text
            self.text = str(self.accList[self.Ind])
            if c != self.text:
                self.on_scroll()
            self.change = 0

    def on_touch_up(self, touch):
        self.touched = False
