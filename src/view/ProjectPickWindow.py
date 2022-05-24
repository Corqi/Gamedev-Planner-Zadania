from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from ProjectViewWindow import ProjectViewWindow
from ProjectSaver import *

Builder.load_file("layouts/projectPickWindow.kv")


class ProjectPickWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        create_project_button = self.ids.create_project_button
        create_project_button.bind(on_release=self.create_new_project)

        open_project_button = self.ids.open_project_button
        open_project_button.bind(on_release=self.open_project)
        self.project_view_window = None

    def create_new_project(self, instance):
        if self.project_view_window is None:
            self.project_view_window = ProjectViewWindow()
            self.parent.add_widget(self.project_view_window)
            self.parent.current = "project_view_window"
        else:
            self.parent.remove_widget(self.project_view_window)
            self.project_view_window = ProjectViewWindow()
            self.parent.add_widget(self.project_view_window)
            self.parent.current = "project_view_window"

    def open_project(self, instance):
        if self.project_view_window is None:
            self.project_view_window = ProjectViewWindow()
            self.parent.add_widget(self.project_view_window)
            project = ProjectReader().project
            if project is not None:
                self.project_view_window.open_project(project)
                self.parent.current = "project_view_window"
        else:
            self.parent.remove_widget(self.project_view_window)
            self.project_view_window = ProjectViewWindow()
            self.parent.add_widget(self.project_view_window)
            project = ProjectReader().project
            if project is not None:
                self.project_view_window.open_project(project)
                self.parent.current = "project_view_window"
