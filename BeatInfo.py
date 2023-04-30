from MyClass import *
from log import *
from struct import unpack
from myByteBuffer import load_bytearray
from ReadContext import *
#from controller import smap
from StateMap import sData
from time import time_ns
import datetime
from json import loads

import re

def render_bit_map(raw_data):
    p = raw_data
    data_bit_map = {
        "clock": unpack(">Q", load_bytearray(p[8:24]))[0],
        "player1": {
            "beat": unpack(">d", load_bytearray(p[32:48]))[0],
            "beatTotal": unpack(">d", load_bytearray(p[48:64]))[0],
            "bpm": unpack(">d", load_bytearray(p[64:80]))[0],
            "timeline": unpack(">Q", load_bytearray(p[224:240]))[0]
        },
        "player2": {
            "beat": unpack(">d", load_bytearray(p[80:96]))[0],
            "beatTotal": unpack(">d", load_bytearray(p[96:112]))[0],
            "bpm": unpack(">d", load_bytearray(p[112:128]))[0],
            "timeline": unpack(">Q", load_bytearray(p[240:256]))[0]
        },
        "player3": {
            "beat": unpack(">d", load_bytearray(p[128:144]))[0],
            "beatTotal": unpack(">d", load_bytearray(p[144:160]))[0],
            "bpm": unpack(">d", load_bytearray(p[160:176]))[0],
            "timeline": unpack(">Q", load_bytearray(p[256:272]))[0]
        },
        "player4": {
            "beat": unpack(">d", load_bytearray(p[176:192]))[0],
            "beatTotal": unpack(">d", load_bytearray(p[192:208]))[0],
            "bpm": unpack(">d", load_bytearray(p[208:224]))[0],
            "timeline": unpack(">Q", load_bytearray(p[272:288]))[0]
        }
    }
    return data_bit_map


@dataclass
class TimeLine(MyDataClass):
  tempo : float = 0
  beatOrigin : float = 0
  timeOrigin: int = 0

@dataclass()
class TwoValueBuffer():
    buff: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.buff = [0,0]

    def add(self, value):
        self.buff.pop(1)
        self.buff.insert(0,value)

    def __str__(self):
        return self.buff[0]

    def __repr__(self):
        return self.buff[0]

@dataclass
class Beats(MyDataClass):
    mValue: int


    def _post_init_(self):
        pass

    def Beat(self,beats):
        if type(beats) == float:
            self.mValue = round(beats * 1e6)
        else:
            self.mValue = beats



@dataclass
class playerDataRaw(MyDataClass):
    id: int
    phase: float = 0
    phase4str: str = ""
    phase4buff: list = field(default_factory=list, repr=False)
    phase8str: str = ""
    phase8buff: list = field(default_factory=list, repr=False)
    phase16str: str= ""
    phase16buff: list = field(default_factory=list, repr=False)
    beat: float = 0
    beat_last: float = 0
    beat_buff: list = field(default_factory=list, repr=False)
    beat_diff_buff: list = field(default_factory=list, repr=False)
    beat_diff: float = 0
    beatTotal: float = 0
    bpm: float = 120
    bpm_buff: object = field(default_factory=object, repr=False)
    count: int = 0
    timeLine: int = 0
    timeLine_last: int = 0
    timeLine_diff: int = 0
    buffer: list = field(default_factory=list, repr=False)
    buffer_max: int = 512
    start_time: int = 0
    time_left: int = 0
    time_left_str: str = ""
    end_time: int = 0
    clock: int = 0
    quantumBins: int = 0

    def _make_player_name(self,id):
        return f'self.p{str(id)}'

    def reset(self):
        self.timeLine_last = 0
        self.timeLine = 0
        self.buffer = []
        self.beat_buff = []
        self.beat_diff_buff = []
        self.beat_last = 0
        self.beat_diff = 0
        self.count = 0
        self.beatTotal = 0
        self.beat = 0
        self.bpm = 120
        self.bpm_buff = TwoValueBuffer()
        self.phase4buff = TwoValueBuffer()
        self.phase8buff = TwoValueBuffer()
        self.phase16buff = TwoValueBuffer()
        self.start_time = 0
        self.time_left = 0
        self.time_left_str = ""
        self.end_time = 0

    def start(self):
        self.reset()
        self.start_time = self.clock

    def __post_init__(self):
        self.bpm_buff = TwoValueBuffer()
        self.phase4buff = TwoValueBuffer()
        self.phase8buff = TwoValueBuffer()
        self.phase16buff = TwoValueBuffer()

    def to_micros(self,value):
        return round(value * 1e6)

    def calc_phase(self,beats, quantum, as_string=False):
        quantumMicros = self.to_micros(quantum)
        quantumBins = int((abs(self.to_micros(beats)) + quantumMicros) / quantumMicros)
        self.quantumBins = quantumBins
        quantumBeats = quantumBins * quantumMicros
        phase = round((beats + quantumBeats) % quantum)
        if as_string:
            return self.calc_phase_str(phase,quantum)
        else:
            return phase

    def calc_phase_str(self, phase, quantum):
        phase_str = ''
        for x in range(0, quantum):
            if x < phase:
                phase_str += 'X'
            else:
                phase_str += '0'
        return phase_str

    def calc_endtime(self, in_micros=True):
        microsPerBeat =60. * 1e6 / self.bpm
        mictosTotalTillEnd = self.beatTotal * microsPerBeat
        if in_micros:
            return mictosTotalTillEnd
        else:
            return str(datetime.timedelta(microseconds=mictosTotalTillEnd))

    def calc_timeleft(self, in_micros=True):
        endtime = self.calc_endtime()
        microsPerBeat = 60. * 1e6 / self.bpm
        currposmicros = microsPerBeat * self.beat
        timeleft = endtime -  currposmicros
        if in_micros:
            return timeleft
        else:
            return str(datetime.timedelta(microseconds=timeleft))

    def append(self, raw_data):
        data = self._parse(raw_data,self.id)
        #data = self._parse(raw_data, 2)
        self.clock = data[1]
        data = data[0]
        self.beat = data['beat']
        self.beatTotal = data['beatTotal']
        self.bpm = data['bpm']
        self.bpm_buff.add(data['bpm'])
        self.timeLine = data['timeline']
        self.update_buffer()
        if len(self.buffer) >= 2:
            self.timeLine_last = self.buffer[1]
            self.timeLine_diff = self.timeLine - self.timeLine_last
        self.update_beat_buffer()
        self.phase = self.calc_phase(self.beat, 4)

        phase4 = self.calc_phase(self.beat, 4, as_string=False)
        self.phase4buff.add(phase4)
        self.phase4str = self.calc_phase_str(phase4, 4)
        phase8 = self.calc_phase(self.beat, 8, as_string=False)
        self.phase8buff.add(phase8)
        self.phase4str = self.calc_phase_str(phase4, 8)
        phase16 = self.calc_phase(self.beat, 16, as_string=False)
        self.phase16buff.add(phase16)
        self.phase16str = self.calc_phase_str(phase16, 16)
        self.phase8str = self.calc_phase(self.beat, 8, as_string=False)
        self.phase16str = self.calc_phase(self.beat, 16, as_string=False)
        if len(self.beat_buff) >= 2:
            self.beat_last = self.beat_buff[1]
            self.beat_diff = self.beat - self.beat_last
            #self.beat_diff_buff.append((self.phase,round(self.beat_diff * 1e4)))
        self.end_time = self.calc_endtime(in_micros=False)
        self.time_left_str = self.calc_timeleft(in_micros=False)
        self.count += 1

    def update_buffer(self):
        self.buffer.insert(0,self.timeLine)
        if len(self.buffer) > self.buffer_max:
            last_index = len(self.buffer) - 1
            self.buffer.pop(last_index)


    def update_beat_buffer(self):
        self.beat_buff.insert(0, self.beat)
        if len(self.beat_buff) > self.buffer_max:
            last_index = len(self.beat_buff) - 1
            self.beat_buff.pop(last_index)


    def _parse(self, raw_data, id):
        data = render_bit_map(raw_data=raw_data)
        data.pop("player4")
        data.pop("player3")
        #print(id, data)
        #print(self.to_tuple())
        return (data[f'player{str(id)}'], data['clock'])

    def render_for_output(self):
        data = self.to_dict()
        #output = {}
        output = []
        data.pop("buffer")
        id = data.pop("id")
        data.pop("beat_buff")
        for key in data.keys():
            value = data[key]
            output.append((key, value))
        #output[f'Player{id}'] = tmp_list
        return output


@dataclass
class clockRaw(MyDataClass):
    clock: int = 0
    count: int = 0
    clock_last: int = 0
    clock_diff: int = 0
    buffer: list = field(default_factory=list,repr=False)
    buffer_max: int = 512
    last_error: str = ""

    def append(self, raw_data):
        clock = self._parse(raw_data)
        self.clock = clock
        self.buffer.insert(0,clock)
        if len(self.buffer) > self.buffer_max:
            last_index = len(self.buffer) - 1
            self.buffer.pop(last_index)
        if len(self.buffer) >=2:
            self.clock_last = self.buffer[1]
            self.clock_diff = self.clock - self.clock_last
        self.count += 1


    def _parse(self, raw_data):
        data = render_bit_map(raw_data)
        return data["clock"]

    def render_for_output(self):
        data = self.to_dict()
        output = []
        data.pop("buffer")
        #id = data.pop("id")
        for key in data.keys():
            value = data[key]
            output.append((key, value))
        #output["Clock"] = tmp_list
        return output


@dataclass(order=True)
class PlayerState:
    playing: bool = False
    ExternalMixerVolume: float = 0
    faderPosition: float = 0
#    def __gt__(self, other):
#        if self.playing == True and other.playing == False:
#            return True
#        else:
#            if self.ExternalMixerVolume > other.ExternalMixerVolume:
#                return True
#            elif self.ExternalMixerVolume == other.ExternalMixerVolume:
#                if self.faderPosition > other.faderPosition:
#                    return True
#                else:
#                    return False
#            else:
#                return False

#    def __le__(self, other):
#        if self.playing == False and other.playing == True:
#           return False
#       else:
#           if self.ExternalMixerVolume < other.ExternalMixerVolume:
#               return True
#           elif self.ExternalMixerVolume == other.ExternalMixerVolume:
#               if self.faderPosition < other.faderPosition:
#                   return True
#               else:
#                   return False
##              return False



class BeatInfo():

    clock = object
    p1 = object
    p2 = object
    p3 = object
    p4 = object
    p1state = object
    p2state = object

    player_list = []
    tcp = object
    active_player = ""
    _on_beat_cb = []

    def __init__(self, player_count=3):
        self.clock = clockRaw()
        self.p1 = playerDataRaw(1)
        self.p2 = playerDataRaw(2)
        self.p1state = PlayerState()
        self.p2state = PlayerState()
        #self.p3 = playerDataRaw(3)
        #self.p4 = playerDataRaw(4)
        for i in range(1,player_count):
            #setattr(self, f"p{i}.id", i)
            #setattr(self, self.get_pName(i), playerDataRaw(i))
            self.player_list.append(self.get_pObj(i))
            sData.add_stateCB(self.stateCB)

    def get_pName(self, id):
        return f'p{str(id)}'

    def get_pObj(self,id):
        return getattr(self, self.get_pName(id))

    def load_bitstram(self, binstream):
        self.clock.append(binstream)
        for player in self.player_list:
            player.append(binstream)

    def get_state_value(self, id, vName):
        if 0 < id < 5:
            iName = f"EngineDeck{str(id)}"
            sinst = getattr(sData, iName)
            pinst = getattr(sinst, vName)
            if pinst:
                value = ""
                string = ""
                type = ""
                json = loads(pinst)
                if "type" in json.keys():
                    jtype = json['type']
                    if jtype in [1, 2]:
                        state = json['state']
                        return state
                    elif jtype in [0,10]:
                        value = json['value']
                        return value
                    else:
                        return False
                    #if "string" in json.keys():
                    #string = json['string']
             #   if "value" in json.keys():

              #  if "state" in json.keys():

    def find_active_player(self):

        p1playState = self.get_state_value(1, "PlayState")
        self.active_player = getattr(self, "p1")

    def add_beat_calback(self, f, q):
        self._on_beat_cb.append((f,q))

    def phare_state_key(self , key):
        rr = re.compile(r'\/\w+\/(\w+)(\d)(\/|)(\w+)')
        result = rr.match(key)
        if result:
            dev, id, tmp, func = result.groups()

            return (dev, id, func)

        return (False, False,False)

    def stateCB(self, id, key, value):
       #print()
        l.info(f'{id}, {key}, {value}')
        print()
        dev, id, func = self.phare_state_key(key)
        if dev == "Deck" and func == "Play":
            tmp_class = getattr(self, f'p{id}state')
            tmp_class.playing = value['state']
        elif dev == "Mixer" and func == "faderPosition":
            tmp_class = getattr(self, f'p{id}state')
            tmp_class.faderPosition = value['value']
    #       if key == "/Engine/Deck1/Play" 0,/Engine/Deck1/Play,{'state': True, 'type': 1}
        if dev == "Deck" and func == "":
            tmp_class = getattr(self, f'p{id}state')
            tmp_class.ExternalMixerVolume = value['value']
        #print(self.p1state > self.p2state)


    def onChangeTracking(self):
        p = self.active_player
        ### Bpm
        #print("on chgeck")
        #if p.bpm_buff[0] != p.bpm_buff[1]:
        for cb, q in self._on_beat_cb:
#            if q == 4 and self.p1.phase4buff.buff[0] == 0 != self.p1.phase4buff.buff[1]:
             if q == 4:
                 cb((self.p1.phase4buff.buff[0], self.p1.phase4buff.buff[1]))
 #           elif q == 8 and self.p1.phase8buff.buff[0] == 0 != self.p1.phase8buff.buff[1]:
             if q == 8:
                cb((self.p1.phase8buff.buff[0], self.p1.phase8buff.buff[1]))
  #          elif q == 16 and self.p1.phase16buff.buff[0] == 0 != self.p1.phase16buff.buff[1]:
             if q == 16:
               cb((self.p1.phase16buff.buff[0], self.p1.phase16buff.buff[1]))
   #         elif q == 0 and 0 == self.p1.phase4buff.buff[0] != self.p1.phase4buff.buff[1]:
             #cb((self.p1.phase4buff.buff[0],0))
             #cb((self.p1.phase4buff.buff[0],0))


    def render_for_output(self):
        output = {
            "Clock": self.clock.render_for_output(),
            "Player1": self.p1.render_for_output(),
            "Player2": self.p2.render_for_output(),
        }

        return output

    def read_stream(self, ss):

        while True:
            raw_data = ss.recv(4)
            size = unpack('>i', raw_data[:4])[0]
            if size != 0:
                break
        raw_data = ss.recv(size)
        data_hex = raw_data.hex()
        if len(data_hex) > 288:
            self.clock.last_error = f"size {len(data_hex)} more 288 "
        buff = load_stream(data_hex)
        if "00000002" != data_hex[0:8]:
            self.clock.last_error = f"unkonwn marker {data_hex[0:8]}"
            return False
        return data_hex
