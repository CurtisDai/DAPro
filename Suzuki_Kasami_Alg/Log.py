# REQUESTMSG = "Request"
# TOKENMSG = "Token"
# ERRORMSG = "Eor"
# SENDREQ = "SRequest"
# SENDTOK = "SToken"
# WAITTOK = "Wait"
# TOKENRECV = "Recv"
# TIMEOUT = "Tout"
#
# def listenerLOG( type, addr='',id=''):
#     if type == ERRORMSG:
#         print("[Warn | ", ERRORMSG, "] <<< [From | ", addr, "]")
#     if type == REQUESTMSG:
#         print("[Recv | ", REQUESTMSG, "] <<< [From | ",id,' | ', addr, "]")
#     if type == TOKENMSG:
#         print("[Recv | ", TOKENMSG, "] <<< [From | ",id,' | ', addr, "]")
#
# def sendLOG(type,addr=''):
#
#     if type == SENDREQ:
#         print("[Send | ", SENDREQ, "] >>> [To | ",addr, "]")
#     if type == SENDTOK:
#         print("[Send | ", SENDTOK, "] >>> [To | ", addr, "]")
#
# def notifyLOG(type):
#     if type == TOKENRECV:
#         print("[State]: Receive token")
#
#     if type == WAITTOK:
#         print("[State]: Waiting for token")
#
#     if type == TIMEOUT:
#         print("[State]: No token response, waiting or retry")
#
import json
diction = (1,2)
diction2= [1,2]
print(str(diction) == str(diction2))
# data = {"head": 'update', "sd": diction}
# data = json.dumps(data)