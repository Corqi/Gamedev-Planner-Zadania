from kivy.uix.button import Button


class AnswerButton(Button):
    def __init__(self, answer_id, text,  **kwargs):
        super(AnswerButton, self).__init__(**kwargs)
        self.id = answer_id
        self.text = text
