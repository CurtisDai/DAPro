#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time


# In[2]:


class Node:
    def __init__(self,ip, holder_ip_address=None, CS=False, token=False):
        self.ip = ip
        self.holder = holder_ip_address
        self.CS = CS
        self.token = token
        self.queue = []
        # listen to the request node
        self.request_server = None
        # listen to the receiver node
        self.receive_server = None
        # listen to the CS execution node
        self.CS_server = None
        
        
    # listen to the request node, will be a thread on port 60000    
    def receive_request_from_child(self, request_server_ip_address):
        # will establish a connection to receive request
        print(self.ip,'request from:',request_server_ip_address)
        # disconnect the connection
    
        self.queue.append(request_server_ip_address)
        if self.token:
            if not self.CS:
                first_node = self.queue.pop(0)
                self.holder = first_node
                self.send_token(self.holder)
                self.token = False
        else:
            self.send_reqeust_to_holder()
            
    # listen to the receiver node, will be a thread on port 60000    
    def send_reqeust_to_holder(self):
        # will establish a connection to send request
        print(self.ip,'sending request to holder: '+ str(self.holder))
        
        
    
    # will be a thread sending info on port 50000    
    def send_token(self, holder):
        # will establish a connection to send token
        print(self.ip,'sending token to holder: ' + str(self.holder))

    # will be a thread listening on port 50000    
    def receive_token(self, holder):
        # will establish a connection to send request   
        print(self.ip,'receiving token from:' +str(self.holder ))
        request_server_ip_address = self.queue.pop(0)
        self.token = True

        
        if request_server_ip_address.ip == self.ip:

            self.holder = self.ip
            self.enterCS()
        else:
            self.holder = request_server_ip_address
            self.token = False
            self.send_token(self.holder)
            if (len(self.queue) != 0):
                self.send_reqeust_to_holder()
    
    
    def enterCS(self):
        print(self.ip,'enter CS')
        self.CS = True
        time.sleep(2)

        self.exitCS()
        
    def exitCS(self):
        if len(self.queue) != 0:
        
            first_node = self.queue.pop(0)
            self.send_token(first_node)
            self.holder = first_node
            print(self.ip,'pass the holder to ', holder)
            
        self.CS = False
        print(self.ip,'exit cs')
        
    def get_queue(self):
        return [i for i in self.queue]
        
    def initial_request(self):
        self.queue.append(self)
        print(self.ip, 'request the token')
        
    def get_holder(self):
        return self.holder

    def __repr__(self):
        return str(self.ip)

    


# In[5]:


# scenario 1
a =  Node('a', holder_ip_address=None, CS=False, token=True)
b =  Node('b', holder_ip_address=a, CS=False, token=False)
c =  Node('c', holder_ip_address=b, CS=False, token=False)
d =  Node('d', holder_ip_address=c, CS=False, token=False)
e =  Node('e', holder_ip_address=d, CS=False, token=False)
f =  Node('f', holder_ip_address=d, CS=False, token=False)
g =  Node('g', holder_ip_address=c, CS=False, token=False)

d.initial_request()
assert(d.get_queue() == [d])

d.send_reqeust_to_holder()
c.receive_request_from_child(d)
assert(c.get_queue() == [d])

# c.send_reqeust_to_holder()
b.receive_request_from_child(c)
assert(b.get_queue()==[c])

# b.send_reqeust_to_holder()
a.receive_request_from_child(b)
assert(a.get_queue()==[])
assert(a.get_holder() == b)

assert(b.get_holder() == a)
b.receive_token(a)
assert(b.token == False)
assert(b.get_holder() == c)

# passing the token back
assert(c.get_holder() == b)
c.receive_token(b)
assert(c.token == False)
assert(c.get_holder() == d)

assert(d.token == False)
assert(d.get_holder() == c)
d.receive_token(c)

assert(d.token == True)


# In[4]:


# scenario 2
a =  Node('a', holder_ip_address=None, CS=False, token=True)
b =  Node('b', holder_ip_address=a, CS=False, token=False)
c =  Node('c', holder_ip_address=b, CS=False, token=False)
d =  Node('d', holder_ip_address=c, CS=False, token=False)
e =  Node('e', holder_ip_address=d, CS=False, token=False)
f =  Node('f', holder_ip_address=d, CS=False, token=False)
g =  Node('g', holder_ip_address=c, CS=False, token=False)

d.initial_request()
assert(d.get_queue() == [d])

d.send_reqeust_to_holder()
c.receive_request_from_child(d)
assert(c.get_queue() == [d])

c.send_reqeust_to_holder()
b.receive_request_from_child(c)
assert(b.get_queue()==[c])

# c request token after passing d's request to node b (parent node)
c.initial_request()
assert(c.get_queue() == [d,c])

b.send_reqeust_to_holder()
a.receive_request_from_child(b)
assert(a.get_queue()==[])
assert(a.get_holder() == b)

# passing the token back
assert(b.get_holder() == a)
b.receive_token(a)
assert(b.token == False)
assert(b.get_holder() == c)


c.receive_token(b)
d.receive_token(c)


d.receive_request_from_child(c)
c.receive_token(d)


# In[ ]:




