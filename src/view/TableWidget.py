from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from Note import Note
from Note import NoteImage

Builder.load_file("layouts/tableWidget.kv")


class TableWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO The size should be dynamically set depending on the size of the window and the placement of the sticky notes.
        # in Python code
        self.table = Table(size_hint=(None, None), size=(1000, 1000))
        self.ids.scroll_view.add_widget(self.table)

        self.new_note_button = self.ids.add_new_note
        self.new_note_button.bind(on_release=self.create_note)

        self.new_image_button = self.ids.add_new_image
        self.new_image_button.bind(on_release=self.create_image)

    def create_note(self, instance):
        offset = self.calculate_offset()

        self.table.add_widget(Note(offset))

    def create_image(self, instance):
        x = input()
        offset = self.calculate_offset()

        self.table.add_widget(NoteImage(x, offset))

    def calculate_offset(self):
        # calculate where is our screen relative on the table
        offset = self.ids.scroll_view.to_local(self.x, self.y)
        # add 1/2 of screen size to make it center
        offset = (offset[0] + self.width / 2, offset[1] + self.height / 2)

        return offset


class Table(RelativeLayout):
    is_busy = False
    child = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
