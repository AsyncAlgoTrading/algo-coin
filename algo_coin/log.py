
import time
from datetime import datetime


class Log(object):
    def __init__(self):
        """ """
        self.logfile = open("logs/log-" + str(int(time.time())), "w")
        self.log("***LOG START***")
        pass

    def log(self, string):
        """ """
        self.logfile.write(str(datetime.now()) + "\t" + string + "\n")

    def logprint(self, string):
        """ """
        print(string)
        self.log(string)

    def close(self):
        """ """
        self.logfile.close()
