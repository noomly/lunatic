from os import listdir
from os.path import isfile, join
import time

import constants as c

import plugins


class Lunatic():
    def __init__(self, irc_session, config):
        self.irc_session = irc_session
        self.config = config

        c.write("loading plugins...")

        self.plugins_ = []
        plugins_name = []
        plugins_path = "lunatic/plugins"
        plugins_path_import = "plugins"

        for plugin_name in listdir(plugins_path):
            plugin_name_split = plugin_name.split('.')

            if isfile(join(plugins_path, plugin_name)) and \
                    len(plugin_name_split) == 2 and \
                    plugin_name_split[1] == "py" and \
                    plugin_name != "__init__.py":

                plugins_name.append(plugin_name_split[0])
                c.write("--found plugin \'%s\'" % plugin_name)

        for plugin_name in plugins_name:
            c.write("--loading plugin \'%s\'..." % plugin_name)
            __import__(join(plugins_path_import,
                            plugin_name).replace('/', '.'))
            self.plugins_.append(getattr(plugins, plugin_name))

        for plugin in self.plugins_:
            plugin.load()

        c.write("all plugins loaded!")

    def loop(self):
        old_recv_data = self.irc_session.recv_data
        while True:
            time.sleep(0.5)

            if self.irc_session.recv_data != old_recv_data:
                old_recv_data = self.irc_session.recv_data

                for plugin in self.plugins_:
                    plugin.received_data(self.irc_session, self.config,
                                         old_recv_data)
        # TODO: complete events
