from os import listdir
from os.path import isfile, join, basename
import yaml

import constants as c


class Config:
    def __init__(self, lunatic_conf_path):
        self.lunatic_conf_path = lunatic_conf_path
        self.plugins_conf_path = "lunatic/plugins"

        self.lunatic_conf = None
        self.plugins_conf = {}

    def load(self):
        c.write("loading configuration files...")

        c.write("--loading \'%s\'..." % basename(self.lunatic_conf_path))
        lunatic_conf_str = ""
        with open(self.lunatic_conf_path, encoding='utf-8') as file_1:
            lunatic_conf_str = lunatic_conf_str + file_1.read()

        self.lunatic_conf = yaml.load(lunatic_conf_str)

        for plugin_conf_name in listdir(self.plugins_conf_path):
            plugin_conf_name_split = plugin_conf_name.split('.')

            if isfile(join(self.plugins_conf_path, plugin_conf_name)) and \
                    len(plugin_conf_name_split) == 2 and \
                    plugin_conf_name_split[1] == "yaml":
                c.write("--loading \'%s\'..." % plugin_conf_name)
                plugin_conf_str = ""
                with open(join(self.plugins_conf_path,
                               plugin_conf_name)) as file_1:
                    plugin_conf_str = plugin_conf_str + file_1.read()

                self.plugins_conf[plugin_conf_name_split[0]] = yaml.load(
                        plugin_conf_str)

        c.write("all configuration files loaded!")
