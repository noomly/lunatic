import random

import constants as c


def load():
    print("HEYYY I'M LOOOAAAADED")


def received_data(data, irc_session, config):
    print("RECEIVED SOMETHING YAYA TA YATA %s" % data)
    #for word in config.bot['hellowords']:
    #    if word in data.lower():
    #        c.write("BBBBBBBBBBBBBBBBBBBBBBBBB %s" % word)
    #        irc_session.send_msg(random.choice(config.bot['hellowords']))
