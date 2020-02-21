#!/usr/bin/env python3

from threading import Thread
import socket
import struct # to send `int` as  `4 bytes`
import time   # for test
import cv2



# --- constants ---

#address = ("192.168.1.158", 12801)
ADDRESS = ("localhost", 12801)

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 255,   0)

# --- classes ---

class Streaming(Thread):

    def __init__(self):
        Thread.__init__(self)

        self.cam = cv2.VideoCapture(0)

    def get_image(self):
        
        successs, self.image = self.cam.read()

        image2byte = self.image.tobytes()
        
        return image2byte
        
    def run(self):

        s = socket.socket()

        # solution for: "socket.error: [Errno 98] Address already in use"
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind(ADDRESS)
        s.listen(1)
        
        print("Wait for connection")

        try:
            sc, info = s.accept()
            print("Video client connected:", info)

            while True:
                
                img = self.get_image()

                len_img = struct.pack('!i', len(img))
                print('len:', len_img)

                # send string size
                sc.send(len_img)

                # send string image
                
                sc.send(img)

                # wait
                
                time.sleep(0.5)
                
        except Exception as e:
            print(e)
        finally:
            # exit
            print("Closing socket and exit")
            sc.close()
            s.close()
        

# --- main ---

Streaming().run()

