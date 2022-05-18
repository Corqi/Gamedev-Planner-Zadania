from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color
from Connection import Connection


class Board(RelativeLayout):
    # TODO The size should be dynamically set depending on the size of the window and the placement of the sticky notes.
    is_busy = False
    child = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deletion_enabled = False
        self.is_making_connection = False
        self.connection_start = []
        self.connection_end = []

        self.bubbles = []
        self.connections = []


    def make_connection_between(self, speech_bubble_out, answer_button, speech_bubble_in):
        connection_start = [speech_bubble_out, answer_button]
        connection_end = [speech_bubble_in, speech_bubble_in.input_button]
        connection = Connection(*connection_start, *connection_end, self)
        self.add_connection(connection)

    # TODO move logic to Connection class maybe
    def make_connection(self, speech_bubble, button, button_type):
        if self.connection_start == [speech_bubble, button] or self.connection_end == [speech_bubble, button]:
            # brake making connection after click on the same button

            for bubble in self.bubbles:
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

            for bubble in self.bubbles:
                bubble.disable_answer_buttons()
                bubble.enable_input_buttons()

            button.disabled = False     # enable current button
            # change current button appearance
            button.background_normal = "atlas://data/images/defaulttheme/button_pressed"

        elif button_type == "end":  # on click input button
            self.connection_end = [speech_bubble, button]

            for bubble in self.bubbles:
                bubble.enable_answer_buttons()
                bubble.disable_input_buttons()

            button.disabled = False
            button.background_normal = "atlas://data/images/defaulttheme/button_pressed"

        else:
            # TODO raise exception maybe
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

            for bubble in self.bubbles:
                bubble.enable_answer_buttons()
                bubble.enable_input_buttons()

            self.refresh_canvas()

            # clear self.line_start, self.line_end
            self.connection_start = []
            self.connection_end = []

    def add_bubble(self, bubble):
        self.bubbles.append(bubble)
        self.add_widget(bubble)

    def remove_bubble(self, bubble):
        self.bubbles.remove(bubble)
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
        self.canvas.add(Color(0.5, 0, 1, 1))
        for connection in self.connections:
            self.canvas.add(connection)

        for bubble in self.bubbles:
            self.add_widget(bubble)

    # noinspection PyPep8Naming
    def export_to_INK(self):
        bubbles = []
        # generate better bubbles >:)
        for bubble in self.bubbles:
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

        # find starting node
        for bubble in bubbles:
            if bubble.input is None:
                # change id and output to be accepted by .INK files
                temp = str(bubble.id)
                temp = temp.replace('.', '').replace('<', '').replace('>', '').replace(' ', '')

                file.write('-> ' + temp + '\n')
                break

        # convert rest of bubbles into dialogue
        for bubble in bubbles:
            temp = bubble.create_dialogue()
            file.write(temp)

        file.close()


class BetterBubbles:
    def __init__(self, bubble):
        self.id = bubble
        self.utterance = bubble.utterance
        self.tags = bubble.tags
        self.answers = bubble.answers
        self.output = []
        self.input = None
        self.has_answers = True

        # check if SpeechBubble is has text with no output
        if len(self.answers) == 1 and self.answers == 'output':
            self.answers = False

    def __repr__(self):
        string = str(print(self.id, self.input, self.utterance, self.tags, self.output, self.answers, self.has_answers))
        return string

    def create_dialogue(self):
        # change id and output to be accepted by .INK files
        id_stripped = str(self.id)
        id_stripped = id_stripped.replace('.', '').replace('<', '').replace('>', '').replace(' ', '')
        output_stripped = [str(out) for out in self.output]
        output_stripped = [out.replace('.', '').replace('<', '').replace('>', '').replace(' ', '') for out in output_stripped]

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
