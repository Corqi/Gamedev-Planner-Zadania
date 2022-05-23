import pickle


class ProjectSaver:
    def __init__(self, project):
        with open("project.p", "wb") as f:
            pickle.dump(project, f, pickle.HIGHEST_PROTOCOL)


class Project:
    def __init__(self, board_data=None, table_data=None):
        self.board_data = board_data
        self.table_data = table_data


class ProjectReader:
    def __init__(self):
        with open("project.p", "rb") as f:
            self.project = pickle.load(f)

