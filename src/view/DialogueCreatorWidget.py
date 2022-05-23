from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from SpeechBubble import SpeechBubble
from Board import Board

Builder.load_file("layouts/dialogueCreatorWidget.kv")


class DialogueCreatorWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deletion_enabled = False

        # in Python code
        self.board = Board(size_hint=(None, None), size=(1000, 1000))
        self.ids.scroll_view.add_widget(self.board)

        self.new_bubble_button = self.ids.add_new_bubble_button
        self.new_bubble_button.bind(on_release=self.create_bubble)
        self.ids.remove_bubble_button.bind(on_release=self.remove_button_clicked)
        self.ids.export_dialogue_button.bind(on_release=self.export_dialogue)
        #self.test()

    def create_bubble(self, instance):
        offset = self.calculate_offset()

        self.board.add_bubble(position=offset)

    def remove_button_clicked(self, instance):
        if self.board.deletion_enabled:
            self.board.deletion_enabled = False
            self.ids.remove_bubble_button.background_normal = "atlas://data/images/defaulttheme/button"
        else:
            self.board.deletion_enabled = True
            self.ids.remove_bubble_button.background_normal = "atlas://data/images/defaulttheme/button_pressed"

    def calculate_offset(self):
        # calculate where is our screen relative on the table
        offset = self.ids.scroll_view.to_local(self.x, self.y)
        # add 1/2 of screen size to make it center
        offset = (offset[0] + self.width / 2, offset[1] + self.height / 2)

        return offset

    def export_dialogue(self, instance):
        self.board.export_to_INK()

    def test(self):
        self.board.add_bubble(answers=['output'], utterance='Do you want to listen music with me?', tags='#speaker:Ghost #portrait:ghost_neutral #layout:right')
        self.board.add_bubble(answers=['output'], utterance='VAR play_music = false')
        self.board.add_bubble(answers=['No', 'Yes'], utterance='Listen to music with ghost?', tags='#speaker:Death #portrait:death_neutral #layout:left')
        self.board.add_bubble(answers=['output'], utterance='~ play_music = false')
        self.board.add_bubble(answers=['output'], utterance='~ play_music = true')
        self.board.add_bubble(utterance="Maybe next time, <color=\#323EA8>right</color>?", tags="#speaker:Ghost #portrait:ghost_sad #layout:right")
        self.board.add_bubble(utterance="I'm <b><color=\#C63636>glad</color></b>", tags="#speaker:Ghost #portrait:ghost_happy #layout:right")

        self.board.make_connection_between(0, 1, 1)
        self.board.make_connection_between(1, 1, 2)
        self.board.make_connection_between(2, 1, 3)
        self.board.make_connection_between(2, 2, 4)
        self.board.make_connection_between(3, 1, 5)
        self.board.make_connection_between(4, 1, 6)

        self.board.refresh_canvas()
