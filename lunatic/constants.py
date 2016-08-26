from time import gmtime, strftime


DEBUG = True


def write(text):
    if DEBUG:
        print("[%s] %s" % (strftime("%H:%M:%S", gmtime()), text))
