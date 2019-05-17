[README]

####Requirement:
Python Version >= 3.6.8 \
Python Tkinter >= 8.6


## Raymond Algorithm (in folder Raymond):
- CriticalSection.py \
Simulate a CS area in network, print the access information when some process enter
- Node.py \
Simulate a process running in reliable network
- raymondNode.py \
Coding the node's action based on Raymond algorithm
- raymondServer.py \
Simulate a monitor process which will logging all transmission in network, and visualize it on GUI
- UI.py \
Graph user interface for algorithm visualization

## Suzuki-Kasami Algorithm (in folder Suziki_Kasami):
- MainNode.py \
Simulate a process running in reliable network, it's action will based on suzuki- kasami algorithm
- MainServer.py \
Simulate a monitor process which will logging all transmission in network, and visualize it on GUI
- Storehouse.py \
Simulate a CS area in network, print the access information when some process enter


##User Guide:
###Raymond Algorithm
#####In Raymond Folder:
1.Run a CS:
```
     python3 criticalSection.py <port>
```
It will print the IP address and port of itself

2.Run the Visualization Monitor:
```
     python3 raymondServer.py <port> <CS IP address> <CS port>
```
It will open an UI interface

3.Run the Process:
```
     python3 Node.py <port> <raymondServer IP address> <raymondServer port>
```
You can run at most 5 processes in one time because of the UI settings(avoiding UI crash)

All paras could be chosen later because the program will ask you if you do not enter any para
###Suzuki-Kasami Algorithm
#####In Suzuki_Kasami Folder:
1.Run the MainServer.py:
```
     python3 MainServer.py
```

Input the server port information according to the tips. This program run as a monitor to reflect the running progress of the whole algorithm.

2.Run the Storehouse.py program:
```
     python3 Storehouse.py
```

The Storehouse program indicate the CS.

3.Run the MainNode.py program:
```
     python3 MainNode.py
```
According to the tips, input the server address and port. Input the node port. The program has a command line interface, which provide operation instruction, after running.
