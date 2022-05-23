from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from AnswerButton import AnswerButton

Builder.load_file("layouts/speechBubblePopup.kv")


class SpeechBubblePopup(Popup):
    def __init__(self, parent, **kwargs):
        super(SpeechBubblePopup, self).__init__(**kwargs)
        self.parenttt = parent
        self.utterance = parent.utterance
        self.tags = parent.tags

        self.answers = []
        for answer_id, answer in parent.answer_buttons.items():
            self.answers.append(AnswerButton(answer_id, answer.text, on_release=self.remove_answer_button_clicked))
        self.show_answers_buttons()

        self.ids.utterance_text_input.text = self.utterance
        self.ids.tags_text_input.text = self.tags

        self.ids.add_answer_button.bind(on_release=self.add_answer_button_clicked)
        self.ids.back_button.bind(on_release=self.close_popup)

    def add_answer(self, answer_text):
        answer = self.parenttt.add_answer(answer_text)
        self.answers.append(AnswerButton(answer.id, answer.text, on_release=self.remove_answer_button_clicked))
        self.show_answers_buttons()

    def add_answer_button_clicked(self, instance):
        answer_popup = AnswerPopup(self)
        answer_popup.open()

    def remove_answer_button_clicked(self, instance):
        self.parenttt.remove_answer(instance.id)
        self.answers.remove(instance)
        self.show_answers_buttons()

    def show_answers_buttons(self):
        self.ids.answers_box.clear_widgets()
        if len(self.answers) == 0:
            self.ids.answers_box.add_widget(Label(text='No answers yet'))
        for ans in self.answers:
            self.ids.answers_box.add_widget(ans)

    def close_popup(self, instance):
        self.parenttt.utterance = self.ids.utterance_text_input.text
        self.parenttt.tags = self.ids.tags_text_input.text

        self.parenttt.refresh_bubble()
        self.dismiss()


class AnswerPopup(ModalView):
    def __init__(self, parent, **kwargs):
        super(AnswerPopup, self).__init__(**kwargs)
        self.parenttt = parent
        self.bind(on_dismiss=self.close)

    def close(self, instance):
        if self.ids.answer_input_text.text == "":
            return
        self.parenttt.add_answer(self.ids.answer_input_text.text)
