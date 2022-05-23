from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ProjectPickWindow import ProjectPickWindow
from ProjectViewWindow import ProjectViewWindow


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ProjectPickWindow())
        return sm


if __name__ == '__main__':
    MainApp().run()