from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from DialogueCreatorWidget import DialogueCreatorWidget
from TableWidget import TableWidget

Builder.load_file("layouts/projectViewWindow.kv")


class ProjectViewWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create buttons listeners
        self.ids.dialogue_creator_button.bind(on_release=self.open_dialogue_creator)
        self.ids.table_button.bind(on_release=self.open_table)
        self.ids.back_to_menu_button.bind(on_release=self.back_to_menu)

    def open_dialogue_creator(self, instance):
        self.ids.window.clear_widgets()
        self.ids.window.add_widget(DialogueCreatorWidget())

    def open_table(self, instance):
        self.ids.window.clear_widgets()
        self.ids.window.add_widget(TableWidget())

    def back_to_menu(self, instance):
        self.parent.current = "project_pick_window"
