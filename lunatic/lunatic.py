from os import listdir
from os.path import isfile, join
import time

import constants as c

import modules


class Lunatic():
    def __init__(self, irc_session, config):
        self.irc_session = irc_session
        self.config = config

        c.write("loading modules...")

        self.modules_ = []
        modules_name = []
        modules_path = "lunatic/modules"
        modules_path_import = "modules"

        for module in listdir(modules_path):
            if isfile(join(modules_path, module)) and module != "__init__.py":
                module_final = module.split('.')[0]

                modules_name.append(module_final)
                c.write("found module \'%s\'" % module_final)

        for module in modules_name:
            __import__(join(modules_path_import, module).replace('/', '.'))
            self.modules_.append(getattr(modules, module))

        for module in self.modules_:
            module.load()
            c.write("loaded module \'%s\'" % module)

        c.write("all modules loaded!")

    def loop(self):
        old_recv_data = self.irc_session.recv_data
        while True:
            time.sleep(0.5)

            if self.irc_session.recv_data != old_recv_data:
                old_recv_data = self.irc_session.recv_data

                for module in self.modules_:
                    module.received_data(self.irc_session, self.config,
                                         old_recv_data)
