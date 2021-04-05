import io
import socket
import struct
import time
from picamera import PiCamera, Color
import datetime as dt
from time import sleep 
from fps import FPS
from frame_generator import FrameGenerator
import argparse
import signal
import sys

class SemblanceClient:
    def __init__(self, address='192.168.2.107', port=8000):
        signal.signal(signal.SIGINT, self._handle_signal)
        camera = PiCamera()
        camera.resolution = (800, 600)
        camera.framerate = 30
        camera.iso = 800
        self._camera = camera

        self._address = address
        self._port = port
        self._client = None
    
    
    def connect(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((self._address, self._port))
        self._conn = self._client.makefile('wb')


    def close(self):
        self._conn.write(struct.pack('<L', 0))
        self._conn.close()
        self._client.close()


    def start(self):
        connected = False
        while True:
            try:
                if not connected:
                    print( "Connecting...")
                    self.connect()
                    gen = FrameGenerator(self._conn)
                    connected = True
                
                print( "Streaming...")
                for _ in self._camera.capture_sequence(gen.frames(), 'jpeg', use_video_port=True):
                    pass

            except socket.error:
                connected = False
                print( "Connection lost..." )  
                sleep(3)
    
    def _handle_signal(self, signal, frame):
        print('Stopping Semblance Client, ciao!')
        self.close()
        sys.exit(0)


if __name__ == "__main__":
    SemblanceClient().start()             