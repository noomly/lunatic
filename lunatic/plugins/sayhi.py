import random

import events


def load():
    pass


def event(event, irc_session, conf):
    if isinstance(event, events.EventReceivedMsg):
        for word in conf['hellowords']:
            if word in event.text.lower():
                irc_session.send_msg(random.choice(conf['hellowords']) + " " +
                                     event.nick)

    elif isinstance(event, events.EventQuit):
        irc_session.send_msg("and now %s is no more." % event.nick)
