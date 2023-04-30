from bytebuffer import ByteBuffer
from WriteContext import WriteContext
from socket import (socket, AF_INET, SOL_SOCKET, SOCK_DGRAM, SO_BROADCAST, SO_REUSEADDR)
from struct import unpack, pack, pack_into
import sys
import time
import asyncio
from common import *
#import threading
import logging
from threading import Thread,Event

from time import sleep
from ReadContext import ReadContext



def load_stream(data_str):
    data_list = []
    for i in range(0, len(data_str)-1, 2):
        tmp_str = f"0x{data_str[i]}{data_str[i + 1]}"
        tmp_int = int(tmp_str, 16)
        tmp_hex = hex(tmp_int)
        print(f'{tmp_str} -> {tmp_int} -> {tmp_hex}')
        data_list.append(tmp_int)
    return data_list



class StageLinqAnnounce(Thread):
    DiscoveryMessage = {
        "action": Action["Login"],
        "port": 0,
        "software": {
            "name": "dm StageLinq",
            "version": '0.0.1',
        },
        "source": 'testing',
        "token": CLIENT_TOKEN
    }

    announceClient = None
    announceTimer = None
    packet = bytearray(258)
    sock = object()
    core = object()

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.event = Event()
        self.keep_running = None

    def start(self):
        self.event.clear()
        self.keep_running = True
        super().start()

    def stop(self):
        self.keep_running = False
        self.event.set()


    def writeDiscoveryMessage(self):
        p_ctx = WriteContext(bytearray(124), 0, 124)
        p_message = self.DiscoveryMessage

        p_ctx.writeFixedSizedString(DISCOVERY_MESSAGE_MARKER)
        p_ctx.put(p_message["token"])
        p_ctx.writeNetworkStringUTF16(p_message["source"])
        print(p_ctx.lenght())
        p_ctx.writeNetworkStringUTF16(p_message["action"])
        print(p_ctx.lenght())
        p_ctx.writeNetworkStringUTF16(p_message["software"]["name"])
        print(p_ctx.lenght())
        p_ctx.writeNetworkStringUTF16(p_message["software"]["version"])
        print(p_ctx.lenght())
        p_ctx.put_ULInt16(p_message["port"])
        self.packet = p_ctx



    def init_socket(self):
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
        except:
            print("failed to init socket")

        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Enable Broadcast
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(('', LISTEN_PORT))
        #self.sock.bind(('10.4.20.127', LISTEN_PORT))
        #self.sock.bind(('10.4.20.90',0))


    def send_broadcast(self, packet):
        self.sock.sendto(packet, ('10.4.20.127', LISTEN_PORT))
        self.sock.sendto(packet, ('255.255.255.255', LISTEN_PORT))


    def run(self):
        lastTime = time.time() * 1000
        self.init_socket()
        self.writeDiscoveryMessage()

        while self.keep_running:
            if time.time() * 1000 > lastTime + ANNOUNCEMENT_INTERVAL:
                self.send_broadcast(self.packet.get_buffer())
                # print("Packets per second: %i"%(packetCount))
                announce_cb()
                lastTime = time.time()

            sleep(0.250)


def announce_cb():
    pass





if __name__ == "__main__":
    a = StageLinqAnnounce(object)
    a.start()
    while True:
        sleep(2)




#a = Announce()
#a.init_socket()
#a.writeDiscoveryMessage()



#def announce_worker():

#    lastTime = time.time() * 1000

#    while True:
#        if time.time() * 1000 > lastTime + ANNOUNCEMENT_INTERVAL:
#            a.send_broadcast(a.packet.get_buffer())
            #print("Packets per second: %i"%(packetCount))
#            announce_cb()
 #           lastTime = time.time()


#        sleep(0.250)

#aw  = threading.Thread(target=announce_worker, args=())
#aw.start()



