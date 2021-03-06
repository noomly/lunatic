import constants as c

import socket
import threading


class Session:
    def __init__(self, config):
        self.config = config

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.settimeout(0.5)

        self.recv_data = None

    def connect(self):
        self.irc.connect((self.config.lunatic_conf['server'],
                          self.config.lunatic_conf['port']))

        listen_thread = threading.Thread(target=self.__listen)
        listen_thread.start()

        if self.config.lunatic_conf['password'] != "":
            self.__send("PASS %s" % self.config.lunatic_conf['password'])

        self.__send("NICK %s" % self.config.lunatic_conf['username'])
        self.__send("USER %s %s %s :%s" %
                    (self.config.lunatic_conf['username'],
                     self.config.lunatic_conf['hostname'],
                     self.config.lunatic_conf['servername'],
                     self.config.lunatic_conf['realname']))

        for channel in self.config.lunatic_conf['channels']:
            self.__send("JOIN %s" % channel)

    def __listen(self):
        while threading.main_thread().is_alive():
            try:
                self.recv_data = self.irc.recv(4096).decode('utf-8')
            except socket.timeout:
                pass

            if self.recv_data is not None:
                c.write("RECEIVED : \"%s\"" % self.recv_data)

                recv_data_split = self.recv_data.split(' ')

                if recv_data_split[0] == "PING":
                    self.__send("PONG %s" % recv_data_split[1])

    def __send(self, data):
        c.write("SENT : \"%s\"" % data)
        self.irc.send((data + "\r\n").encode('utf-8'))

    def get_last_recv_data(self):
        recv_data_save = self.recv_data
        self.recv_data = None

        return recv_data_save

    def send_msg(self, receiver, data):
        self.__send("PRIVMSG %s :%s" % (receiver, data))
