import time
import random


class Lunatic():
    def __init__(self, irc_session, config):
        self.irc_session = irc_session
        self.config = config

    def loop(self):
        old_recv_data = self.irc_session.recv_data
        while True:
            time.sleep(0.5)

            if self.irc_session.recv_data != old_recv_data:
                old_recv_data = self.irc_session.recv_data

                for word in self.config.bot['hellowords']:
                    if word in old_recv_data.lower():
                        print("BBBBBBBBBBBBBBBBBBBBBBBBB", word)
                        # self.irc_session.send_msg(random.choice(
                        #     self.config.bot['hellowords']))
