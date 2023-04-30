from MyClass import *
from log import *
from common import *
from socket import socket
from ReadContext import ReadContext, load_stream
from WriteContext import WriteContext
from json import loads,dumps
from struct import unpack, pack
from time import sleep
from pprint import pprint
from socket import (socket,AF_INET, SOL_SOCKET, SOCK_DGRAM, SO_BROADCAST, SO_REUSEADDR,SOCK_STREAM, SOCK_RAW, IPPROTO_IP,  IP_HDRINCL,  IPPROTO_RAW, gethostbyname, gethostname)
from typing import get_type_hints
import codecs

STATES = [
        #Mixer
        "StageLinqValue.MixerCH1faderPosition",
        "StageLinqValue.MixerCH2faderPosition",
        "StageLinqValue.MixerCrossfaderPosition",
        "StageLinqValue.EngineDeckCount",
        "StageLinqValue.ClientLibrarianDevicesControllerCurrentDevice",
        "StageLinqValue.ClientPreferencesPlayer",
        "StageLinqValue.ClientPreferencesLayerB",
        # Decks
        "StageLinqValue.EngineDeck1Play",
        "StageLinqValue.EngineDeck1PlayState",
        "StageLinqValue.EngineDeck1PlayStatePath",
        "StageLinqValue.EngineDeck1TrackArtistName",
        "StageLinqValue.EngineDeck1TrackTrackNetworkPath",
        "StageLinqValue.EngineDeck1TrackSongLoaded",
        "StageLinqValue.EngineDeck1TrackSongName",
        "StageLinqValue.EngineDeck1TrackTrackData",
        "StageLinqValue.EngineDeck1TrackTrackName",
        "StageLinqValue.EngineDeck1CurrentBPM",
        "StageLinqValue.EngineDeck1ExternalMixerVolume",

        "StageLinqValue.EngineDeck2Play",
        "StageLinqValue.EngineDeck2PlayState",
        "StageLinqValue.EngineDeck2PlayStatePath",
        "StageLinqValue.EngineDeck2TrackArtistName",
        "StageLinqValue.EngineDeck2TrackTrackNetworkPath",
        "StageLinqValue.EngineDeck2TrackSongLoaded",
        "StageLinqValue.EngineDeck2TrackSongName",
        "StageLinqValue.EngineDeck2TrackTrackData",
        "StageLinqValue.EngineDeck2TrackTrackName",
        "StageLinqValue.EngineDeck2CurrentBPM",
        "StageLinqValue.EngineDeck2ExternalMixerVolume",

        "StageLinqValue.EngineDeck3Play",
        "StageLinqValue.EngineDeck3PlayState",
        "StageLinqValue.EngineDeck3PlayStatePath",
        "StageLinqValue.EngineDeck3TrackArtistName",
        "StageLinqValue.EngineDeck3TrackTrackNetworkPath",
        "StageLinqValue.EngineDeck3TrackSongLoaded",
        "StageLinqValue.EngineDeck3TrackSongName",
        "StageLinqValue.EngineDeck3TrackTrackData",
        "StageLinqValue.EngineDeck3TrackTrackName",
        "StageLinqValue.EngineDeck3CurrentBPM",
        "StageLinqValue.EngineDeck3ExternalMixerVolume",

        "StageLinqValue.EngineDeck4Play",
        "StageLinqValue.EngineDeck4PlayState",
        "StageLinqValue.EngineDeck4PlayStatePath",
        "StageLinqValue.EngineDeck4TrackArtistName",
        "StageLinqValue.EngineDeck4TrackTrackNetworkPath",
        "StageLinqValue.EngineDeck4TrackSongLoaded",
        "StageLinqValue.EngineDeck4TrackSongName",
        "StageLinqValue.EngineDeck4TrackTrackData",
        "StageLinqValue.EngineDeck4TrackTrackName",
        "StageLinqValue.EngineDeck4CurrentBPM",
        "StageLinqValue.EngineDeck4ExternalMixerVolume",
]





@dataclass()
class StateJsonMsg:
    key: str = ""
    type: int = 0
    string: str = ""
    value: int = 0
    interval: int = 0

@dataclass()
class EngineMixer(MyDataClass):
    CH1faderPosition: str = 0
    CH2faderPosition: str = 0
    CH3faderPosition: str = 0
    CH4faderPosition: str = 0
    CrossfaderPosition: str= 0

    def _render_map_for_subscription(self):

        result = []
       # fullName = f'{s}{str(self.EngineDeckID)}'

        for item in STAGE_LINQ_MAP.keys():
            if "Mixer" in item:
                result.append(STAGE_LINQ_MAP[item])
        return result


@dataclass()
class EngineDeckState(MyDataClass):
    EngineDeckID: int
    EngineDeckName: str = "EngineDeck"
    ExternalMixerVolume: int = 0
    ExternalScratchWheelTouch: int = 0
    PadsView: int = 0
    Play: str = ""
    PlayState: str = ""
    PlayStatePath:  str = ""
    Speed: int = 0
    SpeedNeutral: int = 0
    SpeedOffsetDown: int = 0
    SpeedOffsetUp: int = 0
    SpeedRange: int = 0
    SpeedState: int = 0
    SyncMode: int = 0
    ArtistName: str = ""
    Bleep: int = 0
    CuePosition: int = 0
    CurrentBPM: float = 0
    CurrentKeyIndex: int = 0
    CurrentLoopInPosition: int = 0
    CurrentLoopOutPosition: int = 0
    CurrentLoopSizeInBeats: int = 0
    KeyLock: int = 0
    LoopEnableState: int = 0
    LoopQuickLoop1: str = ""
    LoopQuickLoop2: int = 0
    LoopQuickLoop3: int = 0
    LoopQuickLoop4: int = 0
    LoopQuickLoop5: int = 0
    LoopQuickLoop6: int = 0
    LoopQuickLoop7: str = ""
    LoopQuickLoop8: int = 0
    PlayPauseLEDState: int = 0
    SampleRate: str = ""
    SongAnalyzed: str = ""
    SongLoaded: str = ""
    SongName: str = ""
    SoundSwitchGUID: str = ""
    TrackBytes: int = 0
    TrackData: bool = False
    TrackLength: int = 0
    TrackName: str = field(repr=False,default="")
    TrackNetworkPath: str = ""
    TrackURI: str = ""
    TrackWasPlayed: str = ""

    def __post_init(self):

        self.EngineDeckName = f'EngineDeck{id}'

    def _render_map_for_subscription(self):

        result = []
        fullName = f'{self.EngineDeckName}{str(self.EngineDeckID)}'

        for item in STAGE_LINQ_MAP.keys():
            if fullName in item:
                result.append(STAGE_LINQ_MAP[item])
        return result



@dataclass()
class StateData(MyDataClass):
    EngineDeck1: object = field(default_factory=object)
    EngineDeck2: object = field(default_factory=object)
    EngineDeck3: object = field(default_factory=object)
    EngineDeck4: object = field(default_factory=object)
    Mixer: object = field(default_factory=object)
    EngineDeckCount: int =0
    ClientDevicesController: dict = field(default_factory=dict)
    ClientPreferences: dict = field(default_factory=dict)
    stateSubscriptions: dict = field(default_factory=dict)

    onChange: list =  field(default_factory=list)

    _map = {
        "ClientDevicesController": "/Client/Librarian/DevicesController/",
        "ClientPreferences": "/Client/Preferences/Profile/Application/",
        "EngineDeck4": "/Engine/Deck4/",
        "EngineDeck3": "/Engine/Deck3/",
        "EngineDeck2": "/Engine/Deck2/",
        "EngineDeck1": "/Engine/Deck1/",
        "EngineDeckCount": "/Engine/DeckCount",
        "Mixer": "/Mixer/"
    }
    _lookup_map = {

    }
    _reverse_lookup_map = {

    }




    def render_output(self,id):
        output=[]
        blacklist = ["TrackName"]
        if id == 1:
            data = self.EngineDeck1.to_dict()
            for key in data.keys():
                value = data[key]
                if key not in blacklist:
                    output.append((key,value))
        elif id == 2:
            data = self.EngineDeck2.to_dict()
            for key in data.keys():
                value = data[key]
                if key not in blacklist:
                    output.append((key,value))
        return output


   # def __repr__(self):
   #     return self.to_dict()

    def __post_init__(self):
        self.EngineDeck1 = EngineDeckState(1)
        self.EngineDeck2 = EngineDeckState(2)
        self.EngineDeck3 = EngineDeckState(3)
        self.EngineDeck4 = EngineDeckState(4)
        self.Mixer = EngineMixer()

        for stage in STAGE_LINQ_MAP.keys():
            link = STAGE_LINQ_MAP[stage]
            lookupname,lookupkey = self.lookup(link)
            self._lookup_map[link] = (lookupname,lookupkey)
            self._reverse_lookup_map[(lookupname,lookupkey)] = link



    def add_onChangeCB(self, f):
        self.onChange.append(f)

    def add_stateCB(self, f):
        self.onChange.append(f)


    def cb_call(self, id, key, value):
        try:
            json = loads(value)
        except:
            json = ""
        for cb in self.onChange:
            if json:
                cb(id,key, json)
            else:
                cb(id, key,value)



    def load_data(self, key, data="", isJson=True):
        if key in self._lookup_map.keys():
            #if isJson:
              #  json = loads(data)
               # if "string" in json.keys():
                #    data = json["string"]
                #elif "state" in json.keys():
                #    data = json['state']
                #else:
                #    data = json


            lookupname, lookupkey = self._lookup_map[key]
            if lookupkey == "1":
                setattr(self.EngineDeck1, lookupname, data)
               # self.cb_call(1, lookupname,data)

            elif lookupkey == "2":
                setattr(self.EngineDeck2, lookupname, data)
                #self.cb_call(2, lookupname,data)

            elif lookupkey == "3":
                setattr(self.EngineDeck3, lookupname, data)
               # self.cb_call(3, lookupname,data)

            elif lookupkey == "4":
                setattr(self.EngineDeck4, lookupname, data)
              #  self.cb_call(4, lookupname, data)

            elif lookupkey == "5":
                setattr(self.Mixer, key, data)
                #self.cb_call(5, lookupname,data)

            elif lookupkey == "0" and lookupname == "DeckCount":
                setattr(self.EngineDeckCount, key, data)
               # self.cb_call(0, lookupname,data)

                # print(json)



    def update_data(self, key, data, isjson=True):
        pass


    def lookup(self, name):
        id =0
        iname = ""
        parts = str(name).split("/")
        part = "".join(parts)
        part = part.replace("TrackTrack", "Track")
        if "DeckCount" in part:
            id = 0
            iname = part.replace("Engine", "")
        elif "EngineDeck" in part:
            iname = part.replace("EngineDeck", "")
            id = iname[:1]
            if id in ["1","2","3","4"]:
                iname = iname[1:]
            else:
                id = 0
        elif "ClientLibrarianDevicesController" in part:
            id = 0
            #iname = "ClientLibrarianDevicesController"
            iname = part.replace("ClientLibrarianDevicesController", "ClientDevicesController")

        elif "ClientPreferencesProfileApplication" in part:
            id = 0
            #iname = "ClientPreferencesProfileApplication"
            iname = part.replace("ClientPreferencesProfileApplication", "ClientPreferences")
        elif "Mixer" in part:
            iname = part.replace("Mixer", "")
            id = 5

        return (iname, id)

    def _reverse_lookup(self,key):
        if key in self._lookup_map.keys():
            return self._lookup_map[key]



    def _render_map_for_subscription(self):
        self.stateSubscriptions ={ }        ##self.stateSubscriptions['Mixer'] =
        self.stateSubscriptions['Mixer'] = self.Mixer._render_map_for_subscription()
        self.stateSubscriptions["EngineDeck2"] = self.EngineDeck2._render_map_for_subscription()
        self.stateSubscriptions["EngineDeck1"] = self.EngineDeck1._render_map_for_subscription()

        return self.stateSubscriptions

    #        if DECK_COUNT == 2:
    #    result = []
    #    for item in STAGE_LINQ_MAP.keys():
    #        if DECK_COUNT < 4 and "EngineDeck4" in item:
    #            continue
    #        elif DECK_COUNT < 3:
    #            if "EngineDeck3" in item or "EngineDeck4" in item:
    #                continue
    #        result.append(STAGE_LINQ_MAP[item])
    #    return result


    #states: dict = field(default_factory=dict)
    #iterator: int = 0
    #stateMap: dict = field(default_factory=dict)
    #def append(self,json):
    #        self.json.append(json)

    #def __setitem__(self, id, data):
    #        self.json[id] = data

    #def __getitem__(self, id):
    #        return self.json[id]

    #def __post_init__(self):
    #    self.json = [None] * self._max_states
        #for state in STATES:
            #stateName, stateKey = self.translate_state(state)
            #self.states[stateName] = StateJsonMsg(key=stateKey)
            #self.stateMap[stateKey] = stateName



    def translate_state(self, state):
        state = str(state).split(".")
        return (state[1] ,globals()[state[0]][state[1]])



sData = StateData()



class StateMap:

    serviceName = None
    MAGIC_MARKER = 'smaa'
    MAGIC_MARKER_BIT = bytearray([0x73,0x6d,0x61,0x61])
    MAGIC_MARKER_HEX = "736d6161"
    #// FIXME: Is this thing really an interval?
    MAGIC_MARKER_INTERVAL = 0x000007d2;
    MAGIC_MARKER_JSON = 0x00000000;
    s = object
    stateData = object

    def _get_sname(self):
        name = type(self).__name__
        return name


    def __init__(self):
        self.serviceName = self._get_sname()
        self.jsonMsgs = []
        self.stateData = sData
        #self.s = sock
        #self.loop()





    def _parse_data(self):
        raw_data = self.s.recv(4)
        size = unpack('>i', raw_data[:4])[0]
        raw_data = self.s.recv(size)
        data_hex = raw_data.hex()
        buff = load_stream(data_hex)
        while True:
            tmp_marker = buff.getString(4)
            if self.MAGIC_MARKER == tmp_marker:

                msgType = buff.get_UBInt32()
                if msgType == self.MAGIC_MARKER_JSON:
                    mType = msgType
                    mKey =  buff.readNetworkStringUTF16()
                    mValue = buff.readNetworkStringUTF16()
                    l.info(f'[{mKey}] ---[{mType}]--> {mValue}')
                    self.stateData.load_data(key=mKey,data=mValue, isJson=True)
                    self.stateData.cb_call(mType,mKey,mValue)
                elif msgType == self.MAGIC_MARKER_INTERVAL:
                    mType = msgType
                    mKey = buff.readNetworkStringUTF16()
                    mValue = buff.get_UBInt32()
                    l.info(f'[{mKey}] ---[{mType}]--> {mValue}')
                    self.stateData.cb_call(mType, mKey, mValue)
                    self.stateData.load_data(key=mKey, data=mValue, isJson=False)
                else:
                    break
            else:
                if msgType != 0:
                    l.error(f"unhandled type {msgType}")
                    l.error(buff.get_remaining(), buff._position, buff._length)
                return None


    def subscribeStateMsg(self, state, interval):

        #print(f'Subscribe to state {state}')
        getMessage = WriteContext(bytearray(1024), 0, 1024)
        getMessage.writeFixedSizedString(self.MAGIC_MARKER)
        getMessage.put_UBInt32(self.MAGIC_MARKER_INTERVAL)
        getMessage.writeNetworkStringUTF16(state)
        getMessage.put_UBInt32(interval)
        return getMessage

    def translate_state(self, state):
        state = str(state).split(".")
        return globals()[state[0]][state[1]]

    def subscribeState(self):
        counter = 0
        _state_data = self.stateData._render_map_for_subscription()
        for key in _state_data.keys():
            for ss in _state_data[key]:
                getMessage = self.subscribeStateMsg(ss, 0)
                l = getMessage.lenght()
                buff = getMessage.get_buffer()
                length_buff = WriteContext(bytearray(4), 0, 4)
                length_buff.put_UBInt32(l)

                if counter == 0:
                    status = self.s.send(length_buff.get_buffer())
                else:
                    status = self.s.send(buff + length_buff.get_buffer())
                counter += 1


            sleep(0.200)
            self._parse_data()


    def loop(self):
        self.subscribeState()
        a = False
        while(True):
            self._parse_data()
            if a == False:
                self.subscribeState()
                a = True


a = """
    def recv_size(self, max_recv_size=8192):
        # data length is packed into 4 bytes
        total_len = 0
        total_data = []
        recv_size = max_recv_size
        size = max_recv_size
        size_data = ""
        sock_data = ""
        the_socket = self.s
        while total_len < size:

            sock_data = the_socket.recv(8192)
            #sock_data = self.recv_size(sock_data)

            if not total_data:
                if len(sock_data) > 4 or len(size_data) > 4:
                    sock_bites = sock_data
                    size_data += sock_data.hex()
                    size = unpack('>i', sock_bites[:4])[0]
                    recv_size = size
                    if recv_size > 524288: recv_size = 524288
                    total_data.append(size_data[4:])
                else:
                    size_data += sock_data.hex()
            else:
                total_data.append(sock_data.hex())
            total_len = sum([len(i) for i in total_data])
        result =  ''.join(total_data)
        return result

"""

aaa = """
    def connect(self, ip,port):
        if self.s is None:
            self.s = socket(AF_INET, SOCK_STREAM)
            self.s.setblocking(True)
            self.s.settimeout(MESSAGE_TIMEOUT)
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
            #packet = self.CreateDataForServiceSubscription("BeatInfo",0)
            #self.s.connect((result["address"],self.servicePorts["BeatInfo"]))
            self.s.connect((ip, port))
            sleep(0.250)
            #tcp.send(packet)
            #tcp.send(bytearray([0x0,0x0,0x0,0x4,0x0,0x0,0x0,0x0]))
"""










