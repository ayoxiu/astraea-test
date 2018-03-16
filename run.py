"""Usage: run.py (--host <mq_host>) (--user <mq_user>) (--pass <mq_pass>) (--sys_name <sys_name>) [--debug]
       run.py (--help | -h)
Options:
  -h --help
  -v --debug        verbose mode
  --host            RabbitMQ host
  --user            RabbitMQ user
  --pass            RabbitMQ pass
  --sys_name        System Name
"""
from rpc.synapse.astraea import Synapse

import json
from docopt import docopt

arguments = docopt(__doc__)


def event_test(params, props):
    print("**收到EVENT: %s@%s %s" % (props.type, props.reply_to, json.dumps(params)))
    return True


def rpc_test(params, props):
    print("**RPC请求:", params)
    return {"from": "python", "m": params["msg"], "number": 5233}


server = Synapse()
# 定义事件回调
server.event_callback = {
    "java.test": event_test,
    "dotnet.test": event_test,
    "python.test": event_test,
    "php.test": event_test,
    "ruby.test": event_test,
    "node.test": event_test,
}
# #定义RPC服务方法
server.rpc_callback = {
    "test": rpc_test,
}
server.sys_name = arguments["<sys_name>"]
server.app_name = "python"
server.mq_host = arguments["<mq_host>"]
server.mq_user = arguments["<mq_user>"]
server.mq_pass = arguments["<mq_pass>"]
if arguments["--debug"]:
    server.debug = True
server.serve()


def show_help():
    print("----------------------------------------------")
    print("|   event usage:                             |")
    print("|     > event [event] [msg]                  |")
    print("|   rpc usage:                               |")
    print("|     > rpc [app] [method] [msg]             |")
    print("----------------------------------------------")


show_help()
while True:
    try:
        info = input("input >> ")
        inputs = info.split(' ')
        if inputs[0] == "rpc":
            if len(inputs) != 4:
                show_help()
                continue
            print(server.send_rpc(inputs[1], inputs[2], {"msg": inputs[3]}))
        elif inputs[0] == "event":
            if len(inputs) != 3:
                show_help()
                continue
            server.send_event(inputs[1], {"msg": inputs[2]})
        else:
            show_help()
    except KeyboardInterrupt:
        exit()
