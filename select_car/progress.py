import wx
import wx.adv
import os
import yaml

default_yaml_filename = "config.yaml"


########################################
# 処理中画面を表示するコンポーネント
########################################
class ProgressComponent(wx.Frame):

    def __init__(self, parent):
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + default_yaml_filename, "r", encoding="utf-8") as f:
            y = yaml.load(stream=f, Loader=yaml.SafeLoader)
            self.progress = y.get("resource").get("path") + y.get("resource").get("progress")
            self.logo = y.get("resource").get("path") + y.get("resource").get("logo")
        wx.Frame.__init__(self, parent, -1, '処理中', size=(285, 190))
        # アイコン
        icon = wx.Icon(self.logo, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        # gif
        self.animation = wx.adv.Animation(self.progress)
        self.ctrl = wx.adv.AnimationCtrl(self, anim=self.animation)
        self.ctrl.Play()
