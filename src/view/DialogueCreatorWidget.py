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
        self.test()

    def create_bubble(self, instance):
        offset = self.calculate_offset()

        self.board.add_bubble(SpeechBubble(offset=offset))

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

    def test(self):
        s1 = SpeechBubble(["1", "2", "3"], "Pierwszy")
        s2 = SpeechBubble(utterance="Drugi")
        s3 = SpeechBubble(["1"], "Trzeci")
        s4 = SpeechBubble(utterance="Czwarty")
        s = [s1, s2, s3, s4]
        for x in s:
            self.board.add_bubble(x)

        self.board.make_connection_between(s1, s1.get_answer_by_id(0), s2)
        self.board.make_connection_between(s1, s1.get_answer_by_id(1), s3)
        self.board.make_connection_between(s3, s3.get_answer_by_id(0), s4)

        self.board.refresh_canvas()

        self.board.export_to_INK()
