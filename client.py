#!/usr/bin/env python
from threading import Thread
import socket
import struct

# --- constants ---

#address = ("192.168.1.158", 12801)
ADDRESS = ("localhost", 12801)

# --- classes ---

class Receiving(Thread):

    def __init__(self):
        Thread.__init__(self)


    def run(self):
        s = socket.socket()
        s.connect(ADDRESS)

        try:
            running = True
            while running:
                # receive size
                    
                len_img = s.recv(4)
                size = struct.unpack('!i', len_img)[0]

                # receive string

                img_str = b''

                while size > 0:
                    if size >= 4096:
                        data = s.recv(4096)
                    else:
                        data = s.recv(size)

                    if not data:
                        break
                    
                    size -= len(data)
                    img_str += data

                print('len:', len(img_str))

                # convert string to image

           
                        
        except Exception as e:
            print(e)
        finally:
            # exit
            print("Closing socket and exit")
            s.close()
            

# --- main ---

Receiving().run()
