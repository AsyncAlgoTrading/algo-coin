import sys
import time

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, connectWS
from twisted.python import log
from twisted.internet import reactor

from multiprocessing import Queue, Process

from algo_coin.util.settings import parse_settings

import algo_coin.recrouter as rr
import algo_coin.sendeng as se
import algo_coin.strategy as strats
import algo_coin.compliance as comp


def main(*args):
    log.startLogging(sys.stdout)

    #Construct Socket
    active = parse_settings("config/config.cfg")
    active = [key for key in active.keys() if active[key].strip() == "yes"]
    print(active)

    endpoints = parse_settings("config/endpoints.cfg")
    print(endpoints)

    rr_config = "config/recrouter.cfg"
    se_config = "config/sendeng.cfg"
    sm_config = "config/strats.cfg"
    c_config = "config/compliance.cfg"

    rr_settings = parse_settings(rr_config)
    se_settings = parse_settings(se_config)
    sm_settings = parse_settings(sm_config)
    c_settings = parse_settings(c_config)

    recrouter = rr.ReceiverRouter(rr_settings, active, endpoints)
    sendeng = se.SendEngine(se_settings, active)
    stratman = strats.StrategyManager(sm_settings, active)
    compliance = comp.Compliance(c_settings, active)

    connect_inbound(recrouter, stratman, compliance)
    connect_outbound(sendeng, stratman, compliance)

    run()


def connect_inbound(recrouter, stratman, compliance):
    pass


def connect_outbound(sendeng, stratman, compliance):
    pass


def run():
    pass


if __name__ == "__main__":
    main(sys.argv)
