import yaml


class Config:
    def __init__(self, file_path):
        self.file_path = file_path

        self.bot = None

    def load(self):
        bot_str = ""
        with open(self.file_path, encoding='utf-8') as file_1:
            bot_str = bot_str + file_1.read()

        self.bot = yaml.load(bot_str)
