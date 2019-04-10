from NodeProg import *

def testNode(id,ip,port,nip,nport):
    node = NodeProg(id, ip, port, nip, nport)
    node.run()
    counter = 0
    try:
        while True:
            # stdin = input()
            # if stdin == '':
            while node.csEnter():
                counter += 1
                with open("output.txt", 'a') as file:
                    file.write('[Enter]: ' + id + '\n')
                    print('[Enter | '+id+']')
                time.sleep(0.5)
                with open("output.txt", 'a') as file:
                    file.write('[Leave]: ' + id + '\n')
                print('[Leave | '+id+']')
                if not node.csLeave():
                    print("[Hold]: ","No Request, let me hold it")
                if counter > 25:
                    break

                time.sleep(1)
            else:
                print("[Result]: Enter Failed")
    except KeyboardInterrupt:
        print("<<< Terminated by user >>>")
        node.close()
        sys.exit(1)

if __name__ == '__main__':
    import sys
    import getopt

    try:
        options,args = getopt.getopt(sys.argv[1:],"hp:i:s:l:d:", ["help","ip=","port=","nodeip=","nodeport=","id="])
    except getopt.GetoptError:
        sys.exit(1)

    ip = '127.0.0.1'
    port = 9999
    nip = '127.0.0.1'
    nport = None
    id = None
    for name,value in options:
        if name in ("-h", "--help"):
            pass
        if name in ("-i", "--ip"):
            ip = value
        if name in ("-p", "--port"):
            port = value
        if name in ("-s","--nodeip"):
            nip = value
        if name in ("-l","--nodeport"):
            nport = value
        if name in ("-d","--id"):
            id = value

    testNode(id,ip,port,nip,nport)

