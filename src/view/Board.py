from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color
from Connection import Connection
from SpeechBubble import SpeechBubble


class Board(RelativeLayout):
    is_busy = False
    child = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deletion_enabled = False
        self.is_making_connection = False
        self.connection_start = []
        self.connection_end = []

        self.bubble_id = 0

        self.bubbles = {}
        self.connections = []

    def make_connection_between(self, output_bubble_id, answer_id, input_bubble_id, start_points=None):
        connection_start = [self.bubbles[output_bubble_id], self.bubbles[output_bubble_id].get_answer_by_id(answer_id)]
        connection_end = [self.bubbles[input_bubble_id], self.bubbles[input_bubble_id].input_button]
        connection = Connection(*connection_start, *connection_end, self)
        if start_points is not None:
            connection.points = [*start_points, *connection.end_points]
        self.add_connection(connection)

    def make_connection(self, speech_bubble, button, button_type):
        if self.connection_start == [speech_bubble, button] or self.connection_end == [speech_bubble, button]:
            # brake making connection after click on the same button

            for bubble in self.bubbles.values():
                bubble.enable_answer_buttons()
                bubble.enable_input_buttons()
            try:
                self.connection_start[1].background_normal = "atlas://data/images/defaulttheme/button"
            except IndexError:
                pass
            try:
                self.connection_end[1].background_normal = "atlas://data/images/defaulttheme/button"
            except IndexError:
                pass
            self.connection_start = []
            self.connection_end = []
            return

        if button_type == "start":  # on click answer button
            self.connection_start = [speech_bubble, button]

            for bubble in self.bubbles.values():
                bubble.disable_answer_buttons()
                bubble.enable_input_buttons()

            button.disabled = False     # enable current button
            # change current button appearance
            button.background_normal = "atlas://data/images/defaulttheme/button_pressed"

        elif button_type == "end":  # on click input button
            self.connection_end = [speech_bubble, button]

            for bubble in self.bubbles.values():
                bubble.enable_answer_buttons()
                bubble.disable_input_buttons()

            button.disabled = False
            button.background_normal = "atlas://data/images/defaulttheme/button_pressed"

        else:
            print("ERROR unknown button_type")

        if not(self.connection_start == [] or self.connection_end == []):
            # make connection and add connection to list of connections
            connection = Connection(*self.connection_start, *self.connection_end, self)
            self.add_connection(connection)

            try:
                self.connection_start[1].background_normal = "atlas://data/images/defaulttheme/button"
                self.connection_end[1].background_normal = "atlas://data/images/defaulttheme/button"
            except IndexError:
                print("ERROR button does not exist (Table class)")

            for bubble in self.bubbles.values():
                bubble.enable_answer_buttons()
                bubble.enable_input_buttons()

            self.refresh_canvas()

            # clear self.line_start, self.line_end
            self.connection_start = []
            self.connection_end = []

    def add_bubble(self, answers=None, utterance="", tags="", position=(100, 700), bubble_id=None):
        if bubble_id is None:
            self.bubble_id += 1
            bubble_id = self.bubble_id

        bubble = SpeechBubble(answers, utterance, tags, bubble_id=bubble_id, position=position)
        self.bubbles.update({bubble_id: bubble})
        self.add_widget(bubble)

    def remove_bubble(self, bubble_id):
        self.bubbles.pop(bubble_id)
        self.refresh_canvas()

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)
        self.refresh_canvas()

    def check_connection(self, bubble, answer_button):
        flag = False
        connections = list(self.connections)
        for connection in connections:
            if connection.start_bubble == bubble or connection.end_bubble == bubble:
                if connection.start_button == answer_button or connection.end_button == answer_button:
                    connection.remove()
                    flag = True
        if flag:
            return True
        return False

    def refresh_connection(self, bubble):
        for connection in self.connections:
            if connection.start_bubble == bubble or connection.end_bubble == bubble:
                connection.update_points(bubble)

    def refresh_canvas(self):
        self.canvas.clear()
        self.clear_widgets()
        self.canvas.add(Color(0.7, 0.7, 0.7, 1))
        for connection in self.connections:
            self.canvas.add(connection)

        for bubble in self.bubbles.values():
            self.add_widget(bubble)

    # noinspection PyPep8Naming
    def export_to_INK(self):
        # do dupy to
        bubbles = []
        # generate better bubbles >:)
        for bubble in self.bubbles.values():
            temp = BetterBubbles(bubble)
            bubbles.append(temp)

        # add connections to better bubbles
        for connection in self.connections:
            for bubble in bubbles:
                if bubble.id == connection.start_bubble:
                    bubble.output.append(connection.end_bubble)

                if bubble.id == connection.end_bubble:
                    bubble.input = connection.start_bubble

        # create/overwrite file
        file = open('dialogue.ink', 'w')
        file.close()
        file = open('dialogue.ink', 'a')

        # TODO:
        #   Zadanie 1 - Konwersja do .INK
        #   Programiści przez przypadek wykasowali część kodu potrzebnej do eksportowania dialogu do plików .ink.
        #   Uzupełnij ten kod, tak aby funkcja znowu działała poprawnie.
        #   .
        #   Zacznij od tego aby znaleźć w tablicy bubbles element, od którego zacznie się dialog.
        #   Gdy go znajdziesz dopisz do pliku poniższy kod:
        #   file.write('-> ' + strip_id(znaleziony_element.id) + '\n')
        #   Następnie dodaj każdy element tablicy bubbles do pliku (skorzystaj z funkcji element.create_dialogue())
        #   Żeby zobaczyć czy działa uruchom inklewriter, przekonwertuj plik dialogue.ink na dialogue.json
        #   Wrzuć plik do folderu '\JPWP\Nameless #1_Data' i uruchom aplikację 'Nameless #1.exe'

        file.close()

    def get_data(self):
        bubbles_data = []
        for bubble in self.bubbles.values():
            bubbles_data.append(bubble.get_data())

        connections_data = []
        for connection in self.connections:
            connections_data.append(connection.get_data())
        data = {"bubbles": bubbles_data, "connections": connections_data}

        return data

    def set_data(self, board_data):
        bubbles_data = board_data["bubbles"]
        connections_data = board_data["connections"]

        max_id = -1
        for bubble in bubbles_data:
            self.add_bubble(bubble["ans"].values(), bubble["utterance"], bubble["tags"], bubble["position"], bubble["bubble_id"])
            if max_id < bubble["bubble_id"]:
                max_id = bubble["bubble_id"]

        self.bubble_id = max_id + 1

        for connection in connections_data:
            self.make_connection_between(connection["start_bubble_id"], connection["answer_id"], connection["end_bubble_id"], connection["start_points"])

        self.refresh_canvas()


class BetterBubbles:
    def __init__(self, bubble):
        self.id = bubble
        self.utterance = bubble.utterance
        self.tags = bubble.tags
        self.answers = []
        for answer in list(bubble.answer_buttons.values()):
            self.answers.append(answer.text)
        print(self.answers)
        self.output = []
        self.input = None
        self.has_answers = True

        # check if SpeechBubble is has text with no output
        if len(self.answers) == 1:
            if self.answers[0] == 'output':
                self.has_answers = False

    def __repr__(self):
        string = str(print(self.id, self.input, self.utterance, self.tags, self.output, self.answers, self.has_answers))
        return string

    def create_dialogue(self):
        # change id and output to be accepted by .INK files
        id_stripped = strip_id(self.id)
        output_stripped = [strip_id(out) for out in self.output]

        # create bubble header
        dialogue = '=== ' + id_stripped + ' ===' + '\n'

        # add utterance and tags
        dialogue += str(self.utterance) + ' ' + str(self.tags) + '\n'

        # check for dialogue end
        if len(self.output) == 0:
            dialogue += '-> END' + '\n'
            return dialogue

        # check if dialogue has no answers
        if self.has_answers is False:
            dialogue += '-> ' + output_stripped[0] + '\n'
            return dialogue

        # add answers
        for i in range(len(self.output)):
            dialogue += '\t' + '+ ' + '[' + str(self.answers[i]) + '] '
            dialogue += '-> ' + output_stripped[i] + '\n'

        return dialogue


def strip_id(bubble_id):
    id_stripped = str(bubble_id)
    id_stripped = id_stripped.replace('.', '').replace('<', '').replace('>', '').replace(' ', '')

    return id_stripped
