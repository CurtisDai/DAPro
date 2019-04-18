from NodeProg import *

def testNode(id,nip,nport):
    node = NodeProg(id, nip, nport)
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
                leave = node.csLeave()
                if leave is None:
                    print("[State]: I don't have token")
                if leave == False:
                    print("[Hold]: ","No Request, let me hold it")
                if counter > 50:
                    break

                time.sleep(1)
            # else:
            #     print("[Result]: Enter Failed")
    except KeyboardInterrupt:
        print("<<< Terminated by user >>>")
        node.close()
        sys.exit(1)

def testNode2(id,nip,nport,sip,sport):
    node = NodeProg(id, nip, nport,sip,sport)
    node.start()

    try:
        while True:
            stdin = input()
            if stdin == '':
                if node.csEnter():
                    with open("output.txt", 'a') as file:
                        file.write('[Enter]: ' + id + '\n')
                        print('[Enter | '+id+']')
                    time.sleep(0.5)
                    with open("output.txt", 'a') as file:
                        file.write('[Leave]: ' + id + '\n')
                    print('[Leave | '+id+']')
                    leave = node.csLeave()
                    if leave is None:
                        print("[State]: I don't have token")
                    if leave == False:
                        print("[Hold]: ","No Request, let me hold it")
            elif stdin == 'exit':
                node.close()
                node.join()

            else:
                print("[Result]: Enter Failed, try again")
    except KeyboardInterrupt:
        print("<<< Terminated by user >>>")
        node.close()
        sys.exit(1)


if __name__ == '__main__':
    import sys
    import getopt

    try:
        options,args = getopt.getopt(sys.argv[1:],"hs:l:", ["help","nodeip=","nodeport="])
    except getopt.GetoptError:
        sys.exit(1)

    sip = None
    sport = None
    nip = '127.0.0.1'
    nport = None

    for name,value in options:
        if name in ("-h", "--help"):
            pass
        # if name in ("-i", "--ip"):
        #     ip = value
        # if name in ("-p", "--port"):
        #     port = value
        if name in ("-s","--nodeip"):
            nip = value
        if name in ("-l","--nodeport"):
            nport = value
        # if name in ("-d","--id"):
        #     id = value
    id = nip+":"+nport
    testNode2(id,nip,nport,sip,sport)

