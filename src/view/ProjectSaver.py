import pickle


class ProjectSaver:
    def init(self, project):
        with open("../project.p", "wb") as f:
            pickle.dump(project, f, pickle.HIGHEST_PROTOCOL)


class Project:
    def init(self, board_data=None, table_data=None):
        self.board_data = board_data
        self.table_data = table_data


class ProjectReader:
    def init(self):
        try:
            with open("../project.p", "rb") as f:
                self.project = pickle.load(f)
        except FileNotFoundError:
            self.project = None
            print("Project file not found")
