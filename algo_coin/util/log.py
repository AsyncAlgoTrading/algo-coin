
import time
from datetime import datetime


class Log(object):
    def __init__(self):
        """ """
        self.logstart = False
        pass

    def log(self, s_name, string):
        """Log message STRING from S_NAME"""
        if not self.logstart:
            self.logfile = open("logs/log-" + s_name +
                                "-" + str(int(time.time())), "w")
            self.logfile.write(str(datetime.now()) +
                               "***LOG START***")
            self.logstart = True

        self.logfile.write(str(datetime.now()) + "\t" +
                           s_name + "\t" + string + "\n")

    def logprint(self, s_name, string):
        """Log message STRING from S_NAME and print to stdout"""
        if not self.logstart:
            self.logfile = open("logs/log-" + s_name +
                                "-" + str(int(time.time())), "w")
            self.logfile.write(str(datetime.now()) +
                               "***LOG START***")
            self.logstart = True

        print(string)
        self.log(string)

    def close(self):
        """Close logfile"""
        self.logfile.close()
