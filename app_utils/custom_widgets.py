import math

from kivy.core.window import Window
from kivy.uix.behaviors import *
from kivy.uix.label import Label


def clamp(x, max0, min0):
    if x > max0:
        return max0
    elif x < min0:
        return min0
    return x


class ScrollSelector(Label, ButtonBehavior):
    touched = False
    custom_acc_list = [i for i in range(2023, 2031)]
    startTouch = 0
    change = 0
    scrollRatio = math.tanh(Window.size[1] / 100) * 10
    Ind = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = str(self.custom_acc_list[0])
        self.on_scroll = self.placeholder

    def reset_val(self):
        self.text = str(self.custom_acc_list[0])

    def bindCustomArgs(self, **kwargs):
        if "custom_acc_list" in kwargs:
            self.custom_acc_list = kwargs["custom_acc_list"]
        else:
            self.custom_acc_list = [i for i in range(kwargs["dn_threshold"], kwargs["up_threshold"] + 1)]
        self.text = str(self.custom_acc_list[0])
        if "on_scroll" in kwargs:
            self.on_scroll = kwargs["on_scroll"]

    def placeholder(self):
        pass

    def on_touch_down(self, touch):
        self.startTouch = touch.pos[1]
        if self.calcAvgDist(touch.pos, self.pos, self.size):
            self.touched = True

    def calcAvgDist(self, pos1, pos2, size):
        return (abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2) < (
                    (size[0] // 2) ** 2 + (size[1] // 2) ** 2) // 1.5

    def on_touch_move(self, touch):
        if not self.touched:
            return
        self.DeltaTouch = int(touch.pos[1] - self.startTouch)
        self.change += self.DeltaTouch
        self.startTouch = touch.pos[1]
        if self.change > self.scrollRatio:
            self.Ind = round(clamp(int(self.Ind) + 1, len(self.custom_acc_list) - 1, 0))
            c = self.text
            self.text = str(self.custom_acc_list[self.Ind])
            if c != self.text:
                self.on_scroll()
            self.change = 0
        elif self.change < -self.scrollRatio:
            self.Ind = round(clamp(int(self.Ind) - 1, len(self.custom_acc_list) - 1, 0))
            c = self.text
            self.text = str(self.custom_acc_list[self.Ind])
            if c != self.text:
                self.on_scroll()
            self.change = 0

    def on_touch_up(self, touch):
        self.touched = False
