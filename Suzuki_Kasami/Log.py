import socket
import json

LOG_SERVERADDR = None

REQUESTMSG = "Request"
TOKENMSG = "Token"
ERRORMSG = "Eor"
SENDREQ = "SRequest"
SENDTOK = "SToken"
WAITTOK = "Wait"
TOKENRECV = "Recv"
TIMEOUT = "Tout"

def listenerLOG( type, addr='',id=''):
    if type == ERRORMSG:
        print("[Warn | ", ERRORMSG, "] <<< [From | ", addr, "]")
    if type == REQUESTMSG:
        print("[Recv | ", REQUESTMSG, "] <<< [From | ",id,' | ', addr, "]")
    if type == TOKENMSG:
        print("[Recv | ", TOKENMSG, "] <<< [From | ",id,' | ', addr, "]")

def sendLOG(type,addr=''):

    if type == SENDREQ:
        print("[Send | ", SENDREQ, "] >>> [To | ",addr, "]")
    if type == SENDTOK:
        print("[Send | ", SENDTOK, "] >>> [To | ", addr, "]")

def notifyLOG(type):
    if type == TOKENRECV:
        print("[State]: Receive token")

    if type == WAITTOK:
        print("[State]: Waiting for token")

    if type == TIMEOUT:
        print("[State]: No token response, waiting or retry")

# report all the information before make a move
def report(act,result,id=''):
    msg = None
    if act == 'token':
        msg = {'head':'log','type':'recvtoken','content':id,'result':result}
    # result: to which id
    if act == 'sendToken':
        msg = {'head': 'log', 'type': 'send', 'content': id,'result':result}
    if act == 'pass':
        msg = {'head': 'log','type':'pass', 'content': id,'result':result}

    if act == 'request':
        msg = {'head': 'log','type':'request', 'content': id}
    # result: from which id
    if act == 'recvRequest':
        msg = {'head': 'log', 'type': 'recvrqt', 'content': id, 'result': result}

    if act == 'enter':
        msg = {'head': 'log','type':'enter', 'content': id}
    if act == 'leave':
        msg = {'head': 'log','type':'leave', 'content': id}





    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(json.dumps(msg).encode(),LOG_SERVERADDR)
    return msg
