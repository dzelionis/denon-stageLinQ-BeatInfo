from myByteBuffer import *
from WriteContext import WriteContext
from socket import (socket,AF_INET, SOL_SOCKET, SOCK_DGRAM, SO_BROADCAST, SO_REUSEADDR,SOCK_STREAM, SOCK_RAW, IPPROTO_IP,  IP_HDRINCL,  IPPROTO_RAW, gethostbyname, gethostname)
from selectors import (EVENT_READ, EVENT_WRITE, DefaultSelector)
from analytics import *
from coloring_terminal import *
#from pygame import mixer
#mixer.init()
#from libclient import Message
import types
from struct import unpack, pack, pack_into
import sys
import time
import struct
import asyncio
from common import *
import threading
from StateMap import StateMap,sData
from time import sleep
from ReadContext import ReadContext
#from player_template import DenonPlayer,Prime4
#from mTCPIPConnection import cBufferedTCPIPConnection
from BeatInfo import BeatInfo
sel = DefaultSelector()





smap = StateMap()
bi = BeatInfo()






class Controller():

    services = {
        "StateMap": None,
        "FileTransfer": None,
        "BeatInfo": None,
    }
    servicePorts = {}
    serviceRequestAllowed = False
    udp = None
    tcp = None
    broadcast = None
    connectionInfo = {
        "token": None,
        "source": None,
        "action": None,
        "software": {
            "name": None,
             "version": None
        },
        "port": None,
        "address": None,
    }




    def readConnectionInfo(self, s):
        pass


    def CreateDataForServiceSubscription(self,ServiceName, localPort):
        buf = WriteContext(bytearray(128),0,128)
        buf.put_ULInt32(MessageId['ServicesAnnouncement'])
        buf.put(CLIENT_TOKEN)
        buf.writeNetworkStringUTF16(ServiceName)
        buf.put_ULInt16(localPort)
        newBuf = buf.get_buffer()
        return newBuf


    def init_broadcast_socket(self):
        if self.broadcast is not None:
            return self.broadcast

        try:
            sock = socket(AF_INET, SOCK_DGRAM)
        except:
            print("failed to init socket")
            return None

        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Enable Broadcast
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('', LISTEN_PORT))
        # sock.bind(('10.4.20.127', LISTEN_PORT))
        self.broadcast = sock
        return self.broadcast

    def init_udp_socket(self, ip, port):
        if self.udp is not None:
            return self.udp

        try:
            udp = socket(AF_INET, SOCK_DGRAM)
        except:
            return False

        udp.settimeout(MESSAGE_TIMEOUT)
        udp.setblocking(True)
        udp.connect((ip,port))
        self.udp = udp
        return udp

    def init_tcp_socket(self, ip, port):
        try:
            tcp = socket(AF_INET, SOCK_STREAM)
        except:
            return False

        tcp.setblocking(False)
        tcp.settimeout(MESSAGE_TIMEOUT)
        tcp.connect((ip, port))
        return tcp

    def discover(self):
        # buf = ReadContext(bytearray(256),0,256)
        print("Discovering...")

        lastTime = time.time() * 1000
        result = {}
        sock = self.init_broadcast_socket()

        while True:
            if time.time() * 1000 > lastTime + LISTEN_TIMEOUT:
                break
            raw, net = sock.recvfrom(1024)
            remoteip, remoteport = net
            buf = ReadContext(raw, 0, len(raw))

            magic = buf.getString(4)
            if magic != DISCOVERY_MESSAGE_MARKER:
                sleep(0.250)
                continue
            self.connectionInfo = {
                "token": buf.read(16),
                "source": buf.readNetworkStringUTF16(),
                "action": buf.readNetworkStringUTF16(),
                "software": {
                    "name": buf.readNetworkStringUTF16(),
                    "version": buf.readNetworkStringUTF16()
                },
                "port": buf.get_UBInt16(),
                "address": remoteip,
            }
            # if (result["source"] == ""  or result["source"] == "testing" or result['software']["name"] == "OfflineAnalyzer"):

            #   continue
            if self.connectionInfo["source"] == "prime4" and self.connectionInfo['software']['name'] != 'OfflineAnalyzer':
                sleep(0.250)
                print(f"Found Prime4 on {self.connectionInfo['address']}:{self.connectionInfo['port']}")
                #print(self.connectionInfo)
                break
            else:
                #print("Found:")
                #print(self.connectionInfo)
                #print("skiping...")
                sleep(0.250)
        self.broadcast.close()
        self.broadcast = None
        return self.connectionInfo

    def ConnectToService(self, serviceName):
        if self.services[serviceName] is None:
            
            tcp = socket(AF_INET, SOCK_STREAM)
            tcp.setblocking(False)
            tcp.settimeout(MESSAGE_TIMEOUT)
            print(f'Connecting to {serviceName} service on: {self.connectionInfo["address"]}, port: {self.servicePorts[serviceName]}')
            tcp.connect((self.connectionInfo["address"], self.servicePorts[serviceName]))
            lip, lport = tcp.getsockname()
            packet = self.CreateDataForServiceSubscription(serviceName, lport)
            sleep(0.150)
            #self.tcp.send(packet)
            tcp.send(packet)
            sleep(0.150)
            if serviceName == "BeatInfo":
                tcp.send(bytearray([0x0, 0x0, 0x0, 0x4, 0x0, 0x0, 0x0, 0x0]))

            self.services[serviceName] = tcp
            return tcp



    def generateServiceRequest(self):
        ctx = WriteContext(bytearray(128), 0, 128)
        ctx.put_UBInt32(MessageId['ServicesRequest'])
        ctx.put(CLIENT_TOKEN)
        return ctx.get_buffer()

    def requestAvailableServices(self):
        tcp = self.init_tcp_socket(self.connectionInfo['address'], self.connectionInfo['port'])
        tcp.send(self.generateServiceRequest())
        lastTime = time.time_ns()
        while True:

            if len(self.servicePorts) >= 5 and self.serviceRequestAllowed:
            #if time.time() * 1000 > lastTime + LISTEN_TIMEOUT:
                break
            service,port = self.MessageHandler(tcp)
            print(f'Found: "{service}" service on port: {port}')
        self.tcp = tcp
        return self.servicePorts


    def Connect(self,ip, port, service=True):
        if service:
            serviceFound = False
            for ServiceName in self.servicePorts.keys():
                ServicePort = self.servicePorts[ServiceName]
                if int(ServicePort) == int(port):
                    serviceFound = True
                    break

            if serviceFound:
                serviceName = self.servicePorts[port]
                c = socket(AF_INET, SOCK_STREAM)
                c.setblocking(True)
                c.settimeout(MESSAGE_TIMEOUT)
                c.connect((ip, port))
                self.services[serviceName] = c
                return c
            else:
                print("Error: no such service found")
                return False
        else:
            c = socket(AF_INET, SOCK_STREAM)
            c.setblocking(True)
            c.settimeout(MESSAGE_TIMEOUT)
            c.connect((ip, port))
            return c


    def Diconnect(self, all=True):
        for service in self.services.keys():
            s = self.services[service]
            s.disconnect()
            self.services[service] = None


    def MessageHandler(self, s):

        services = {}
        while True:
            data = s.recv(4)
            buff = ReadContext(data, 0, len(data))
            Magic = buff.get_UBInt32()
            data = s.recv(16)

            if Magic == MessageId['TimeStamp']:
                 data = s.recv(16)
                 data = s.recv(16)
                 buf = ReadContext(data, 0, len(data))
                 self.timeAlive = buf.get_UBInt64() / (1000 * 1000 * 1000)
                 return ("KeepAlive", self.timeAlive)
            elif Magic == MessageId['ServicesAnnouncement']:
                data = s.recv(4)
                buf = ReadContext(data,0,len(data))
                bytes = buf.get_UBInt32();
                # Should be 2 bytes per character; otherwise
                string = '';
                for i in range(0, int(bytes / 2)):
                    data = s.recv(2)
                    buff = ReadContext(data, 0, len(data))
                    string += chr(buff.get_UBInt16());

                service = string
                data = s.recv(2)
                buff = ReadContext(data, 0, len(data))
                port = buff.get_UBInt16()
                self.servicePorts[service] = port
                services[service] = None
                return (service, port)
            elif Magic == MessageId['ServicesRequest']:
                self.serviceRequestAllowed = True
                return ("ServicesRequest", True)
            else:
               print(f"unknown service {Magic}")
               return False




    def connect_services(self):
       srvName = "BeatInfo"
       if self.serviceRequestAllowed:
           if self.services[srvName] is None:
              if srvName in self.servicePorts.keys():
                 bi.tcp = self.ConnectToService("BeatInfo")
                 self.services[srvName] = bi.tcp
           if self.services["StateMap"] is None:
             if "StateMap" in self.servicePorts.keys():
                smap.s = self.ConnectToService("StateMap")
                self.services["StateMap"] = smap.s

                smap.loop()
                       #if len(data) <= 84:
            #    print(data)
            #    print(len(data))
            #    continue

    def __init__(self):
        self.discover()
        self.requestAvailableServices()
        #print(self.servicePorts)

c = colorfull_table()


from json import loads

def stageChangeCB(id,key,value):

    x  = c.get_x()
    y = c.get_y() - 5

    c.clear_line(display=True)
    if key == "/Engine/Deck1/Play":
        #json = loads(value)
        state = value['state']
        if state == True:
            bi.p1.start()
        else:
            bi.p1.reset()
    c.goto(30,2, display=True)
    a = c.clear_line(display=False)
    c.sout(f'{a}{id},{key},{value}',flush=True)
    c.goto(x,y,display=True)

sData.add_onChangeCB(stageChangeCB)

##    print("boom\n")
#bi.add_beat_calback(on4beat_cb,4)
ctrl = Controller()

def BeatInfo_worker():
    headers = False
    while True:
        if ctrl.services["BeatInfo"] is None:
            sleep(0.2)
        else:
            if not headers:
                c.print_headers(["Clock", "Player1", "Player2"])
                headers = True


            #ata_hex = a.recv_size(a.services["BeatInfo"])
            #print(ctrl.services)
            data_hex = bi.read_stream(ctrl.services["BeatInfo"])
            #print(data_hex)
            bi.load_bitstram(data_hex)

            output = bi.render_for_output()
            c.print_data(output)

            bi.find_active_player()
            bi.onChangeTracking()

            p1 = sData.render_output(1)
            p2 = sData.render_output(2)

            items_to_remove=["TrackName"]
            #for i in range(0,len(p1)-2):
            #    key1,value1= p1[i]
            #    key2,value2 = p2[i]
            #    if key1 in items_to_remove or len(str(value1)) > 20:
             #       p1.pop(i)
           #     if key2 in items_to_remove or len(str(value2)) > 20:
             #       p2.pop(i)


            out = {
                "Clock": [],
                "Player1":p1,
                "Player2":p2,
            }

            #c.print_data(out)
            c.commit()


at = threading.Thread(target=BeatInfo_worker, args=())
#ctrl = Controller()

#def Controller_worker():

    #ctrl.DiscoverAllServices()


#ct = threading.Thread(target=Controller_worker, args=())
#ctrl = Controller()
#at.start()
#ctrl.connect_services()
if __name__ == "__main__":
    #pass
    at.start()
    ctrl.connect_services()
    #ctrl.DiscoverAllServices()
    #sleep(0.500)
    #ctrl.connect_services()

    #at.start()
    #ct.start()




old = """
    def BeatInfoOld(self):
        packetCount = 0
        lastTime = time.time()

        if self.services['BeatInfo'] is None:
            tcp = socket(AF_INET, SOCK_STREAM)
            tcp.setblocking(True)
            tcp.settimeout(MESSAGE_TIMEOUT)
            #tcp.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
            #tcp.bind(('localhost', 50000))
            #tcp.listen(1)
            #conn, addr = tcp.accept()
            #tcp.connect(())
            #while 1:
               # data = conn.recv(1024)
               # print(data)
               # if not data:
               #     break

                #conn.sendall(data)
            packet = self.CreateDataForServiceSubscription("BeatInfo",0)
            tcp.connect((result["address"],self.servicePorts["BeatInfo"]))
            sleep(0.250)
            tcp.send(packet)
            sleep(0.250)
            tcp.send(bytearray([0x0,0x0,0x0,0x4,0x0,0x0,0x0,0x0]))
            aa1 = load_stream("0000000c00000001000009445f944bf0")
            aa2 = load_stream("00000001000009445f944bf0")

            #tcp.send(aa1._array)

            self.services["BeatInfo"] = tcp


        else:

            while True:


                data_hex = self.recv_size(self.services["BeatInfo"])

                data_hex = "" + data_hex
                h = data_hex
                if time.time() > lastTime + 1:
                    lastTime = time.time()

                p = [
                    h[0:4], #0 Packet Lenght
                    h[4:12], #1 id 0x2
                    h[12:28], #2 Clock
                    h[28:36], #3 ????
                    h, #4 Player1 Current position time
                    h, #5 Player1 end time
                    h, #6 Player1 Pitch ?
                    h, #7 Player2 Current position time
                    h, #8 Player2 end time
                    h[116:132], #9 Player 2 Pitch ?
                    h, #10 Plater 3 Current posstion
                    h, #11 Player 3 end time
                    h, #12 Player 3 Pitch ?
                    h[180:196], #13 Plater 4 Current Position Time
                    h[196:212], #14 Player 4 end time
                    h[212:228], #15 Player 4 Pitch ?
                    h[228:244], #16 Player 1 ?
                    h[244:260], #17 Player 2 ?
                    h, #18 Player 3 ?
                    h[276:292], #19 layer 4 ?
                ]

                ds = []

                ds.append("") #unpack(">L", load_bytearray(p[1]))) #1 unsigned long 4

                ds.append("")#unpack(">Q",load_bytearray(p[3]))) #3 unsigned long 8  - Clock



                ds.append("") #unpack(">L", load_bytearray(p[0]))) #0 unsigned long 4
                ds.append(unpack(">Q",load_bytearray(p[2]))[0])  #2 unsigned long 8

                ds.append(unpack(">d",load_bytearray(p[36:52]))[0]) #4 float 8 - Player 1 - quantum
                ds.append(unpack(">d",load_bytearray(p[52:68]))[0]) #5 float 8 - Player 1 - total quantums
                ds.append(unpack(">d", load_bytearray(p[68:84]))[0]) #6 float 8 - Player 1 - BPM
                ds.append(unpack(">d", load_bytearray(p[84:100]))[0])  # 7 float 8 - Player 2 - quantum
                ds.append(unpack(">d", load_bytearray(p[100:116]))[0])  # 8 float 8 - Player 2 - total quantums
                ds.append(unpack(">d", load_bytearray(p[116:132]))[0])  # 9 float 8 - Player 2 - BPM
                ds.append(unpack(">d", load_bytearray(p[132:148]))[0])  # 10 float 8 - Player 3 - quantum
                ds.append(unpack(">d", load_bytearray(p[148:164]))[0])  # 11 float 8 - Player 3 - total quantums
                ds.append(unpack(">d", load_bytearray(p[164:180]))[0])  # 12 float 8 - Player 3 - BPM
                ds.append(unpack(">d", load_bytearray(p[180:196]))[0])  # 13 float 8 - Player 4 - quantum
                ds.append(unpack(">d", load_bytearray(p[196:212]))[0])  # 14 float 8 - Player 4 - total quantums
                ds.append(unpack(">d", load_bytearray(p[212:228]))[0])  # 15 float 8 - Player 4 - BPM
                ds.append(unpack(">Q", load_bytearray(p[228:244]))[0])  # 16 unsigned long 8 - Player 1 - TimeLine
                ds.append(unpack(">Q", load_bytearray(p[244:260]))[0])  # 17 unsigned long 8 - Player 2 - TimeLine
                ds.append(unpack(">Q", load_bytearray(p[260:276]))[0])  # 18 unsigned long 8 - Player 3 - TimeLine
                ds.append(unpack(">Q", load_bytearray(p[276:292]))[0])  # 19 unsigned long 8 - Player 4 - TimeLine




                prime.populate_data(ds)
                prime.render_output()

"""
