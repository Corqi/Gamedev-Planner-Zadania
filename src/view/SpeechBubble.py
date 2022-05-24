from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from SpeechBubblePopup import SpeechBubblePopup
from AnswerButton import AnswerButton

Builder.load_file("layouts/speechBubble.kv")


class SpeechBubble(RelativeLayout):
    # relative position of bubble to mouse
    relative_pos = (0, 0)

    def __init__(self, answers=None, utterance="", tags="", position=(100, 700), bubble_id=None, **kwargs):
        super().init(**kwargs)

        if answers is None:
            answers = {}

        self.bubble_id = bubble_id
        self.answer_id = 0
        self.answer_buttons = {}
        for answer_id, answer in answers.items():
            self.answer_buttons.update({answer_id: self.create_answer(answer, answer_id)})
            self.answer_id = answer_id + 1

        self.utterance = utterance
        self.tags = tags

        self.set_bubble_size()

        Window.bind(mouse_pos=self.hover)

        # background initialization
        with self.canvas.before:
            self.color = Color(0.3, 0.3, 0.3, 1)
            self.rect = RoundedRectangle(pos=(0, 0), size=self.size)

        self.input_button = self.ids.input_button
        self.input_button.bind(on_release=self.input_button_clicked)

        self.refresh_bubble()

        # compensate for note size
        size = self.rect.size
        position = (position[0] - size[0] / 2, position[1] - size[1] / 2)
        self.pos = position

    def hover(self, *args):
        # get the coords of SpeechBubble
        x1, y1 = self.to_window(self.x, self.y)
        x2, y2 = self.size
        x2 += x1
        y2 += y1

        # check if mouse is inside SpeechBubble
        garbage, mouse = args
        x_mouse, y_mouse = mouse

        # first check if mouse is inside SpeechBubble and assign it as currently used
        if x1 <= x_mouse <= x2 and y1 <= y_mouse <= y2 and self.parent.is_busy is False:
            self.parent.child = self
            self.parent.is_busy = True
        # if currently used SpeechBubble is hovered make click delay 0
        elif x1 <= x_mouse <= x2 and y1 <= y_mouse <= y2 and self.parent.child == self and self.parent.is_busy is True:
            self.parent.parent.scroll_timeout = 0
        # if currently used SpeechBubble is no longer hovered, deassign it and allow scrolling map
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

    def refresh_bubble(self):
        self.ids.utterance_label.text = self.utterance
        self.show_answer_buttons()
        self.set_bubble_size()
        self.unpressed()

    def set_bubble_size(self, width=None, height=None):
        if width is None or height is None:
            # should be ok when max size is 300x200
            min_width = 150
            min_height = 100

            width_from_answers = 50 * len(self.answer_buttons)

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

            self.size = (max(min_width, width_from_utterance, width_from_answers), max(min_height, height_from_utterance))
            return

        self.size = (width, height)

    def add_answer(self, ans):
        answer_button = self.create_answer(ans)
        self.answer_buttons.update({self.answer_id: answer_button})
        self.answer_id += 1
        self.show_answer_buttons()
        return answer_button

    def create_answer(self, answer_text=None, id=None):
        if id is None:
            id = self.answer_id
        return AnswerButton(id, answer_text, on_release=self.answer_button_clicked)

    def remove_answer(self, answer_id):
        button = self.answer_buttons.pop(answer_id)
        self.parent.check_connection(self, button)

        self.show_answer_buttons()

    def show_answer_buttons(self):
        self.ids.answers_box.clear_widgets()

        for button in self.answer_buttons.values():
            self.ids.answers_box.add_widget(button)

        if self.parent is not None:
            self.parent.refresh_connection(self)

    def answer_button_clicked(self, instance):
        if self.parent.check_connection(self, instance):
            return

        self.parent.make_connection(self, instance, "start")

    def disable_answer_buttons(self):
        for button in self.ids.answers_box.children:
            button.disabled = True

    def enable_answer_buttons(self):
        for button in self.ids.answers_box.children:
            button.disabled = False

    def get_answer_by_id(self, ans_id):
        return self.answer_buttons.get(ans_id)

    def input_button_clicked(self, instance):
        self.parent.make_connection(self, instance, "end")

    def disable_input_buttons(self):
        self.ids.input_button.disabled = True

    def enable_input_buttons(self):
        self.ids.input_button.disabled = False

    def on_touch_down(self, touch):
        if self.ids.bubble_info_box.collide_point(*self.to_local(*touch.pos)) \
                and not self.ids.input_button.collide_point(*self.to_local(*touch.pos)):

            if self.parent.deletion_enabled:
                self.remove()
                return True
            if touch.button == 'right':
                popup = SpeechBubblePopup(parent=self)
                popup.open()
                return True
            touch.grab(self)

            # calculate relative position
            self.relative_pos = (touch.pos[0] - self.pos[0], touch.pos[1] - self.pos[1])

            self.pressed()
            # by returning true, we show, that it should look no further for something to collide
            # eliminating moving few widgets at a time
            return True
        super(SpeechBubble, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # I received my grabbed touch
            self.pos = [touch.pos[0] - self.relative_pos[0], touch.pos[1] - self.relative_pos[1]]
            if self.parent is not None:
                self.parent.refresh_connection(self)
        else:
            # it's a normal touch
            super(SpeechBubble, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
            touch.ungrab(self)
            self.unpressed()
        else:
            # it's a normal touch
            super(SpeechBubble, self).on_touch_up(touch)

    def pressed(self):
        self.update_background((0.3, 0.3, 0.3))

    def unpressed(self):
        self.update_background((0.1, 0.1, 0.1))

    def remove(self):
        # connections_to_delete = list(self.connections)
        # for connection in connections_to_delete:
        #     connection.remove()

        self.parent.parent.scroll_timeout = float('inf')
        self.parent.is_busy = False
        self.parent.child = None

        for button in self.answer_buttons.values():
            self.parent.check_connection(self, button)
        self.parent.check_connection(self, self.input_button)

        Window.unbind(mouse_pos=self.hover)

        self.parent.remove_bubble(self.bubble_id)

    def get_data(self):
        answers = {}
        for answer_id, answer_button in self.answer_buttons.items():
            answers.update({answer_id: answer_button.text})
        data = {"bubble_id": self.bubble_id, "utterance": self.utterance, "tags": self.tags, "ans": answers, "position": (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2)}
        return data
