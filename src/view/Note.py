from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, InstructionGroup
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.image import Image

Builder.load_file("layouts/note.kv")


class Note(RelativeLayout):
    # relative position of note to mouse
    relative_pos = (0, 0)

    def __init__(self, offset, **kwargs):
        super().__init__(**kwargs)

        # TODO it will be necessary to load this data from a special dialogue class
        self.utterance = ""
        # temporary

        self.set_note_size()

        Window.bind(mouse_pos=self.hover)

        # background initialization
        with self.canvas.before:
            self.color = Color(248/255, 229/255, 144/255, 1)
            self.rect = Rectangle(pos=(0, 0), size=self.size)

        self.refresh_note()

        # compensate for note size
        offset = (offset[0] - self.width/2, offset[1] - self.height/2)
        self.pos = offset

    def hover(self, *args):
        # get the coords of Note
        x1, y1 = self.to_window(self.x, self.y)
        x2, y2 = self.size
        x2 += x1
        y2 += y1

        # check if mouse is inside Note
        garbage, mouse = args
        x_mouse, y_mouse = mouse

        # first check if mouse is inside Note and assign it as currently used
        if x1 <= x_mouse <= x2 and y1 <= y_mouse <= y2 and self.parent.is_busy is False:
            self.parent.child = self
            self.parent.is_busy = True
        # if currently used Note is hovered make click delay 0
        elif x1 <= x_mouse <= x2 and y1 <= y_mouse <= y2 and self.parent.child == self and self.parent.is_busy is True:
            self.parent.parent.scroll_timeout = 0
        # if currently used Note is no longer hovered, deassign it and allow scrolling map
        elif self.parent.child == self and self.parent.is_busy is True:
            self.parent.parent.scroll_timeout = float('inf')
            self.parent.is_busy = False
            self.parent.child = None

    def update_background(self, color):
        self.rect.size = self.size
        if color[0] is not None:
            self.color.r = color[0]
        if color[1] is not None:
            self.color.g = color[1]
        if color[2] is not None:
            self.color.b = color[2]

    def refresh_note(self):
        self.set_text()
        self.set_note_size()
        self.unpressed()

    def set_note_size(self, width=None, height=None):
        if width is None or height is None:
            # should be ok when max size is 300x200
            min_width = 150
            min_height = 100


            width_from_utterance = 0
            height_from_utterance = 0
            if len(self.utterance) < 30:
                width_from_utterance = 150
            elif len(self.utterance) < 150:
                height_from_utterance = 150
                width_from_utterance = 200
            else:
                width_from_utterance = 300
                height_from_utterance = 200

            self.size = (max(min_width, width_from_utterance), max(min_height, height_from_utterance))
            return

        self.size = (width, height)

    def set_text(self):
        self.ids.utterance_label.text = self.utterance
        self.ids.utterance_label.color = (0.1, 0.1, 0.1, 1)

    def on_touch_down(self, touch):
        if self.ids.note_info_box.collide_point(*self.to_local(*touch.pos)):
            if touch.button == 'right':
                print("Right")
                popup = NotePopup(parent=self)
                popup.open()
                return True
            touch.grab(self)

            # calculate relative position
            self.relative_pos = (touch.pos[0] - self.pos[0], touch.pos[1] - self.pos[1])

            self.pressed()
            # by returning true, we show, that it should look no further for something to collide
            # eliminating moving few widgets at a time
            return True
        super(Note, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # I received my grabbed touch
            self.pos = [touch.pos[0] - self.relative_pos[0], touch.pos[1] - self.relative_pos[1]]
        else:
            # it's a normal touch
            super(Note, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
            touch.ungrab(self)
            self.unpressed()
        else:
            # it's a normal touch
            super(Note, self).on_touch_up(touch)

    def pressed(self):
        self.update_background((247/255, 221/255, 97/255))

    def unpressed(self):
        self.update_background((248/255, 229/255, 144/255))


class NotePopup(Popup):
    def __init__(self, parent, **kwargs):
        super(NotePopup, self).__init__(**kwargs)
        self.parenttt = parent
        self.utterance = parent.utterance

        self.ids.utterance_text_input.text = self.utterance

        self.ids.back_button.bind(on_release=self.close_popup)
        self.bind(on_dismiss=self.closed_popup)

    def close_popup(self, instance):
        self.parenttt.utterance = self.ids.utterance_text_input.text
        self.parenttt.refresh_note()
        self.dismiss()

    def closed_popup(self, instance):
        self.parenttt.utterance = self.ids.utterance_text_input.text
        self.parenttt.refresh_note()


class NoteImage(RelativeLayout):
    def __init__(self, source, offset, **kwargs):
        super().__init__(**kwargs)

        # TODO it will be necessary to load this data from a special dialogue class

        Window.bind(mouse_pos=self.hover)
        self.ids.image.source = source

        self.ids.image.size = self.ids.image.texture.size
        # background initialization
        with self.canvas.before:
            self.color = Color(248/255, 229/255, 144/255, 1)
            self.rect = Rectangle(pos=(0, 0), size=(self.ids.image.width + 20, self.ids.image.height + 20))

        self.ids.image_info_box.size = self.rect.size
        self.refresh_note()

        # compensate for note size
        size = self.rect.size
        offset = (offset[0] - size[0] / 2, offset[1] - size[1] / 2)
        self.pos = offset

    def hover(self, *args):
        # get the coords of NoteImage
        x1, y1 = self.to_window(self.x, self.y)
        x2, y2 = self.rect.size
        x2 += x1
        y2 += y1

        # check if mouse is inside NoteImage
        garbage, mouse = args
        x_mouse, y_mouse = mouse

        # first check if mouse is inside NoteImage and assign it as currently used
        if x1 <= x_mouse <= x2 and y1 <= y_mouse <= y2 and self.parent.is_busy is False:
            self.parent.child = self
            self.parent.is_busy = True
        # if currently used NoteImage is hovered make click delay 0
        elif x1 <= x_mouse <= x2 and y1 <= y_mouse <= y2 and self.parent.child == self and self.parent.is_busy is True:
            self.parent.parent.scroll_timeout = 0
        # if currently used NoteImage is no longer hovered, deassign it and allow scrolling map
        elif self.parent.child == self and self.parent.is_busy is True:
            self.parent.parent.scroll_timeout = float('inf')
            self.parent.is_busy = False
            self.parent.child = None

    def update_background(self, color):
        if color[0] is not None:
            self.color.r = color[0]
        if color[1] is not None:
            self.color.g = color[1]
        if color[2] is not None:
            self.color.b = color[2]

    def refresh_note(self):
        self.unpressed()

    def on_touch_down(self, touch):
        if self.ids.image_info_box.collide_point(*self.to_local(*touch.pos)):
            touch.grab(self)

            # calculate relative position
            self.relative_pos = (touch.pos[0] - self.pos[0], touch.pos[1] - self.pos[1])

            self.pressed()
            # by returning true, we show, that it should look no further for something to collide
            # eliminating moving few widgets at a time
            return True
        super(NoteImage, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # I received my grabbed touch
            self.pos = [touch.pos[0] - self.relative_pos[0], touch.pos[1] - self.relative_pos[1]]
        else:
            # it's a normal touch
            super(NoteImage, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
            touch.ungrab(self)
            self.unpressed()
        else:
            # it's a normal touch
            super(NoteImage, self).on_touch_up(touch)

    def pressed(self):
        self.update_background((247/255, 221/255, 97/255))
        self.ids.image.opacity = 0.8

    def unpressed(self):
        self.update_background((248/255, 229/255, 144/255))
        self.ids.image.opacity = 1