class EventJoin():
    def __init__(self, channel, nick, username):
        self.channel = channel
        self.nick = nick
        self.username = username


class EventQuit():
    def __init__(self, channel, nick, username, text):
        self.channel = channel
        self.nick = nick
        self.username = username
        self.text = text


class EventReceivedMsg():
    def __init__(self, channel, nick, username, text):
        self.event = "received_msg"

        self.channel = channel
        self.nick = nick
        self.username = username
        self.text = text
