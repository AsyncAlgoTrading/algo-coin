
import time

s_name = "ConnectionMonitor"


class ConnectionMonitor(object):
    def __init__(self, conn_engine, log):
        self.conn_engine = conn_engine
        self.conn_engine.init_processes()
        self.log = log

    def start_exchange_processes(self):
        self.log.log(s_name, "Starting Exchange Processes")
        self.conn_engine.run_processes()

    def run(self):
        self.monitor_connections()
        pass

    def terminate(self):
        print("ConnectionMonitor going down")
        self.conn_engine.terminate()
        self.log.log(s_name, "Going down...")


    def monitor_connections(self):
        while(True):
            self.log.log(s_name, "Monitoring Connections (HEARTBEAT)")
            if not self.conn_engine.monitor_processes():
                self.conn_engine.restart_down()
            time.sleep(1)
            print("HEARTBEAT")
