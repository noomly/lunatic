from config import Config
from irc.session import Session
from lunatic import Lunatic


def main():
    config = Config("lunatic.yaml")
    config.load()

    irc_session = Session(config)
    irc_session.connect()

    lunatic = Lunatic(irc_session, config)
    lunatic.loop()


if __name__ == "__main__":
    main()
