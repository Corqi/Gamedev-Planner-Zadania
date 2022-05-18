from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

Builder.load_file("layouts/projectPickWindow.kv")


class ProjectPickWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        open_project_button = self.ids.open_project_button
        open_project_button.bind(on_release=self.btn_click)

    def btn_click(self, instance):
        self.parent.current = "project_view_window"


