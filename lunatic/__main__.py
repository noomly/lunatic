import constants as c

from config import Config
from irc.session import Session
from lunatic import Lunatic


def main():
    c.write("Lunatic started")

    if c.DEBUG:
        config = Config("lunatic.yaml.debug")
    else:
        config = Config("lunatic.yaml")
    config.load()

    irc_session = Session(config)
    irc_session.connect()

    lunatic = Lunatic(irc_session, config)

    lunatic.loop()


if __name__ == "__main__":
    main()
