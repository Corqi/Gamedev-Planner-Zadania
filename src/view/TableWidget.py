from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from Note import Note
from Note import NoteImage
from kivy.core.window import Window

Builder.load_file("layouts/tableWidget.kv")


class TableWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deletion_enabled = False

        self.table = Table(size_hint=(None, None), size=(1000, 1000))
        self.ids.scroll_view.add_widget(self.table)

        self.new_note_button = self.ids.add_new_note_button
        self.new_note_button.bind(on_release=self.create_note)

        self.remove_note_button = self.ids.remove_note_button
        self.remove_note_button.bind(on_release=self.remove_button_clicked)

        Window.bind(on_dropfile=self.drop_image)

    def drop_image(self, window, filename):
        # correct file extension list
        correct_ext = ['png', 'jpg', 'jpeg', 'bmp', 'tif', 'webp']

        # delete b' and ' from file_path
        filename = str(filename)
        filename = filename[2:-1]
        # check if file extension is correct
        extension = filename.split('.')[1]
        if extension not in correct_ext:
            filename = 'res/missing_texture.webp'

        self.create_image(filename)

    def create_note(self, instance):
        offset = self.calculate_offset()

        self.table.add_note(Note("", offset))

    def create_image(self, filename):
        offset = self.calculate_offset()
        self.table.add_note_image(NoteImage(filename, offset))

    def calculate_offset(self):
        # calculate where is our screen relative on the table
        offset = self.ids.scroll_view.to_local(self.x, self.y)
        # add 1/2 of screen size to make it center
        offset = (offset[0] + self.width / 2, offset[1] + self.height / 2)

        return offset

    def remove_button_clicked(self, instance):
        if self.table.deletion_enabled:
            self.table.deletion_enabled = False
            self.ids.remove_note_button.background_normal = "atlas://data/images/defaulttheme/button"
        else:
            self.table.deletion_enabled = True
            self.ids.remove_note_button.background_normal = "atlas://data/images/defaulttheme/button_pressed"


class Table(RelativeLayout):
    is_busy = False
    child = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deletion_enabled = False
        self.notes = []
        self.note_images = []

    def refresh_canvas(self):
        self.canvas.clear()
        self.clear_widgets()
        # self.canvas.add(Color(0.5, 0, 1, 1))

        for note in self.notes:
            self.add_widget(note)

        for note_image in self.note_images:
            self.add_widget(note_image)

    def add_note(self, note):
        self.notes.append(note)
        self.add_widget(note)

    def add_note_image(self, note_image):
        self.note_images.append(note_image)
        self.add_widget(note_image)

    def remove_note(self, note):
        self.notes.remove(note)
        self.refresh_canvas()

    def remove_note_image(self, note_image):
        self.note_images.remove(note_image)
        self.refresh_canvas()

    def get_data(self):
        notes_data = []
        for note in self.notes:
            notes_data.append(note.get_data())

        return {"notes": notes_data}

    def set_data(self, table_data):
        notes_data = table_data["notes"]

        for note in notes_data:
            temp_note = Note(note["text"], note["position"])
            self.add_note(temp_note)

        self.refresh_canvas()

