from kivy.graphics import Line


class Connection(Line):
    def __init__(self, start_bubble, start_button, end_bubble, end_button, parent, **kwargs):
        super(Connection, self).__init__(**kwargs)

        self.start_bubble = start_bubble
        self.start_button = start_button
        self.end_bubble = end_bubble
        self.end_button = end_button

        self.parent = parent

        self.start_points = self.start_bubble.to_parent(self.start_button.pos[0] + self.start_button.width / 2,
                                                        self.start_button.pos[1])
        self.end_points = self.end_bubble.to_parent(self.end_button.pos[0] + self.end_button.width / 2,
                                                    self.end_button.pos[1] + self.end_button.height)
        self.points = [*self.start_points, *self.end_points]

        #self.start_bubble.add_connection(self)
        #self.end_bubble.add_connection(self)

    def update_points(self, speech_bubble):
        # a method to allow line movement
        if speech_bubble == self.start_bubble:
            self.start_points = self.start_bubble.to_parent(
                self.start_button.pos[0] + self.start_button.width / 2, self.start_button.pos[1])

        if speech_bubble == self.end_bubble:
            self.end_points = self.end_bubble.to_parent(self.end_button.pos[0] + self.end_button.width / 2,
                                                        self.end_button.pos[1] + self.end_button.height)
        # update the position of points
        self.points = [*self.start_points, *self.end_points]

    def remove(self):
        #self.start_bubble.remove_connection(self)
        #self.end_bubble.remove_connection(self)
        self.parent.remove_connection(self)
