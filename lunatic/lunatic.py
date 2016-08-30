from os import listdir
from os.path import isfile, join
import threading
import time

import constants as c

import events
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
        try:
            while True:
                time.sleep(0.5)

                recv_data = self.irc_session.get_last_recv_data()

                if recv_data is not None:
                    recv_data_split = recv_data.split(' ')

                    for plugin in self.plugins_:
                        event = None

                        if recv_data_split[1] == "JOIN":
                            event = events.EventJoin(
                                recv_data_split[2],
                                recv_data.split('!')[0][1:],
                                recv_data.split('!')[1].split('@')[0][1:])

                        elif recv_data_split[1] == "QUIT":
                            event = events.EventQuit(
                                recv_data_split[2],
                                recv_data.split('!')[0][1:],
                                recv_data.split('!')[1].split('@')[0][1:],
                                recv_data.split(':', maxsplit=2)[2])

                        elif recv_data_split[1] == "PRIVMSG":
                            event = events.EventReceivedMsg(
                                recv_data_split[2],
                                recv_data.split('!')[0][1:],
                                recv_data.split('!')[1].split('@')[0][1:],
                                recv_data.split(':', maxsplit=2)[2])

                        plugin_thread = threading.Thread(target=plugin.event,
                                args=(event, self.irc_session,
                                     self.config.plugins_conf[
                                         plugin.__name__.split('.')[1]]))
                        plugin_thread.start()
        except KeyboardInterrupt:
            self.config.save_changes()
            return
