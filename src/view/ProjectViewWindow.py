from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from DialogueCreatorWidget import DialogueCreatorWidget
from TableWidget import TableWidget
from ProjectSaver import *

Builder.load_file("layouts/projectViewWindow.kv")


class ProjectViewWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create buttons listeners
        self.ids.dialogue_creator_button.bind(on_release=self.open_dialogue_creator)
        self.ids.table_button.bind(on_release=self.open_table)
        self.ids.back_to_menu_button.bind(on_release=self.back_to_menu)

        self.ids.save_project_button.bind(on_release=self.save_project)

        self.table = None
        self.dialogue_creator = None

    def open_dialogue_creator(self, instance):
        self.ids.window.clear_widgets()
        if self.dialogue_creator is None:
            self.dialogue_creator = DialogueCreatorWidget()
        self.ids.window.add_widget(self.dialogue_creator)

    def open_table(self, instance):
        self.ids.window.clear_widgets()
        if self.table is None:
            self.table = TableWidget()
        self.ids.window.add_widget(self.table)

    def back_to_menu(self, instance):
        self.parent.current = "project_pick_window"

    def save_project(self, instance):
        board_data = None
        table_data = None

        if self.dialogue_creator is not None:
            board_data = self.dialogue_creator.board.get_data()
        if self.table is not None:
            table_data = self.table.table.get_data()
        project = Project(board_data, table_data)
        ps = ProjectSaver(project)

    def open_project(self, project):
        if project.board_data is None:
            self.dialogue_creator = None
        else:
            self.dialogue_creator = DialogueCreatorWidget()
            self.dialogue_creator.board.set_data(project.board_data)

        if project.table_data is None:
            self.table = None
        else:
            self.table = TableWidget()
            self.table.table.set_data(project.table_data)

        self.ids.window.clear_widgets()
        if self.dialogue_creator is not None:
            self.ids.window.add_widget(self.dialogue_creator)
        if self.table is not None:
            self.ids.window.add_widget(self.table)
