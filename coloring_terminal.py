import os
from datetime import datetime
import time
import sys
from termcolor import colored, cprint
from os import isatty
from fcntl import ioctl
#from curses import tigetstr, setupterm, tparm
from pyparsing import *

'''
#!/usr/bin/python

print "\\033[XXm"

for i in range(30,37+1):
    print "\033[%dm%d\t\t\033[%dm%d" % (i,i,i+60,i+60);

print "\033[39m\\033[39m - Reset colour"
print "\\033[2K - Clear Line"
print "\\033[<L>;<C>H OR \\033[<L>;<C>f puts the cursor at line L and column C."
print "\\033[<N>A Move the cursor up N lines"
print "\\033[<N>B Move the cursor down N lines"
print "\\033[<N>C Move the cursor forward N columns"
print "\\033[<N>D Move the cursor backward N columns"
print "\\033[2J Clear the screen, move to (0,0)"
print "\\033[K Erase to end of line"
print "\\033[s Save cursor position"
print "\\033[u Restore cursor position"
print " "
print "\\033[4m  Underline on"
print "\\033[24m Underline off"
print "\\033[1m  Bold on"
print "\\033[21m Bold off"
'''

class ColorHelper():
    RES_COL = 100
    RES_ROW = 24
    # COLUMNS=`set | grep COLUMNS | awk -F"=" '{print $2}'`

    # echo $COLUMNS
    # RES_COL=`expr $COLUMNS - 18`
    # terminal sequence to move to that column. You could change this
    # to something like "tput hpa ${RES_COL}" if your terminal supports it
    MOVE_TO_COL = "echo -en \\033[${RES_COL}G"
    # terminal sequence to set color to a 'success' color (currently: green)
    SETCOLOR_SUCCESS = "\033[0;32m"
    # terminal sequence to set color to a 'failure' color (currently: red)
    SETCOLOR_FAILURE = "\033[0;31m"
    # terminal sequence to set color to a 'warning' color (currently: yellow)
    SETCOLOR_WARNING = "\033[0;33m"
    # terminal sequence to reset to the default color.
    SETCOLOR_NORMAL = "\033[0;39m"

    # ANSI color codes

    RS = "\033[0m"  # reset
    HI = "\033[1m"  # hicolor
    LO = "\033[2m"  # hicolor
    IT = "\033[3m"  # hicolor
    UL = "\033[4m"  # underline
    BL = "\033[5m"  # underline

    INV = "\033[7m"  # inverse background and foreground
    FBLK = "\033[30m"  # foreground black
    FRED = "\033[31m"  # foreground red
    FGRN = "\033[32m"  # foreground green
    FYEL = "\033[33m"  # foreground yellow
    FBLE = "\033[34m"  # foreground blue
    FMAG = "\033[35m"  # foreground magenta
    FLMAG = "\033[35;1m"
    FDMAG = "\033[35;2m"
    FCYN = "\033[36m"  # foreground cyan
    FWHT = "\033[39m"  # foreground white
    BBLK = "\033[40m"  # background black
    BRED = "\033[41m"  # background red
    BGRN = "\033[42m"  # background green
    BYEL = "\033[43m"  # background yellow
    BBLE = "\033[44m"  # background blue
    BMAG = "\033[45m"  # background magenta
    BCYN = "\033[46m"  # background cyan
    BWHT = "\033[47m"  # background white

    ACT_COL = 37
    # RES_COL=60
    MOVE_TO_ACT = "echo -en \\033[${ACT_COL}G"

    def Pink(self,string):
        out = f'\033[38;5;206m{string}{self.RS}'
        return out

    def Fg(self,string,color):
        if string:
            out = f'\033[38;5;{color}m{string}{self.RS}'
        else:
            out = f'\033[38;5;{color}m'
        return out

    def get_x(self):
        try:
            columns, rows = os.get_terminal_size(0)
        except:
            columns = 80
            rows = 24
        self.RES_COL = columns
        return columns

    def get_y(self):
        try:
            columns, rows = os.get_terminal_size(0)
        except:
            columns = 80
            rows = 24
        self.RES_ROW = rows
        return rows



    def get_string_of_chars(self, char, count, start_pos):
        out = ""
        i = 0
        while i != count + start_pos:

            if i <= start_pos:
                out = out + " "
            else:
                out = out + char
            i = i + 1
        out = "[" + out
        return out



    def loading(self):
        for i in range(0, 100):
            time.sleep(0.1)
            width = (i + 1) / 4
            bar = "[" + "#" * width + " " * (25 - width) + "]"
            sys.stdout.write(u"\u001b[1000D" +  bar)
            sys.stdout.flush()



    def head(self, msg=None):

        x = self.get_x()
        out = "\033[35;1m"
        for i in range(0, x):
            out = out + "#"
        out = out + "\033[0;39m"
        self.p(out)
        if msg:
            msgLen = len(msg) + 4
            pos = int((x / 2) - ( msgLen /2))
            #pos = int(pos / 2)
            self.pos(pos)
            msgOut = "[ " + msg + " ]"
            self.n(msgOut)
            self.pos(x)
            self.sout("\r\n")

    def tail(self, msg=None, noNewLine=False, ansiCode=False):

        x = self.get_x()
        out = "\r\n\033[35m"
        for i in range(0, x):
            out = out + "-"
        out = out + "\033[0;39m"
        self.p(out)
        if msg:
            msgLen = len(msg) + 4
            pos = int((x / 2) - (msgLen /2))
            #pos = int(pos / 2)
            self.pos(pos)
            if ansiCode:
                msgOut = "[ " + ansiCode + msg + "\033[0;39m" + " ]\r"
            else:
                msgOut = "[ " + msg + " ]\r"
            self.n(msgOut)
        if not noNewLine:
            self.n("")

    def sout(self, text, flush=True):
        sys.stdout.write(text)
        if flush:
            sys.stdout.flush()


    def pos(self, pos, display=True):
        out = '\33[' + str(pos) + 'G'
        if display:
            self.sout(out)
        return out

    def p(self, msg):
        self.sout(msg)
    def n(self, msg=None):
        if msg:
            self.sout(msg)
        else:
            self.sout('\n')


    def time(self):
        now = datetime.now()
        #out = "{month}{day}.{h}:{m}:{s}".format(month=now.month,day=now.day,h=now.hour,m=now.minute,s=now.second)
        out = now.strftime("%m%d.%H:%M:%S")
        return out

    def s(self, status, msg1, msg2=None, msg3=None, msg4=None, msg5=None, s=True):
        timestamp = self.time()
        out = "[{FCYN}{timestamp}{FWHT}] {FYEL}{STATUS}{FWHT}: {msg1}".format(FCYN=self.FCYN, FYEL=self.FYEL, timestamp=timestamp, STATUS=status, FWHT=self.FWHT, msg1=msg1)

        msgs = ""
        if msg2:
            msgs = '{} \033[35m{}\033[0;39m'.format(msgs, msg2)
        if msg3:
            msgs = '{} \033[01;34m{}\033[0;39m'.format(msgs, msg3)
            #msgs = '{} {}'.format(msgs, msg3)
        if msg4:
            msgs = '{} \033[35m{}\033[0;39m'.format(msgs, msg4)
        if msg5:
            msgs = '{} \033[01;34m{}\033[0;39m'.format(msgs, msg5)

        out = out + msgs
        #self.p(out)

        self.p(out)
        if s:
            self.status()
        else:
            self.n("")
        #self.pos(10)
        #print('\33[33' + "m adsasd", end="")
        #self.pos(4)
        #self.p("asdasd")
        #self.pos(104)
        #self.p("a")

    def status(self, msg=None):
        x = self.get_x()


        if not msg:
            pos = x - 9
            self.pos(pos)
            msg = "[{:8}]".format("")
            self.p(msg)
            self.pos(20)
            self.p('\r')
        else:
            pos = x - 9
            self.pos(pos)
            msg = "[{:^10}]".format(msg)
            self.n(msg)

    def done(self):
        self.status("\033[0;32m" + "{:^8}".format("DONE") + "\033[0;39m")

    def fail(self):
        self.status("\033[0;31m" + "{:^8}".format("FAILED") + "\033[0;39m")

    def ok(self):
        self.status("\033[0;32m" + "{:^8}".format("OK") + "\033[0;39m")

    def yes(self):
        self.status("\033[0;32m" + "{:^8}".format("YES") + "\033[0;39m")

    def no(self):
        self.status("\033[0;33m" + "{:^8}".format("NO") + "\033[0;39m")

    def warning(self):
        self.status("\033[0;33m" + "{:^8}".format("WARNING") + "\033[0;39m")

    def passed(self):
        self.status("\033[0;33m" + "{:^8}".format("PASSED") + "\033[0;39m")

    def len(self, string):

        ESC = Literal('\x1b')
        integer = Word(nums)
        escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer, ';')) +
                            oneOf(list(alphas)))

        nonAnsiString = lambda s: Suppress(escapeSeq).transformString(s)

        unColorString = nonAnsiString(string)
        return len(unColorString)


class colorfull_table(ColorHelper):

    max_x = None
    max_y = None
    current_row = 0
    refresh_from_row = 0
    main_node = None
    dataList = []
    dataDict = {}

    ARROW_DL = "\u2BA8"
    ARROW_UR = "\u2BAB"



    def __init__(self):
        self.max_x = self.get_x()
        self.max_y = self.get_y()
        self.clear_screen()
        #self.dataDict = {}
        self.dataList = []
        #self.print_headers(dataDict)
#        self.print_data()

    def clear_screen(self,display=True):
        out ='\033[2J'
        if display:
            self.sout(out)
        else:
            return out

    def goto(self,x,y,display=True):
        out = f'\033[{y};{x}H'
        #out = f'\\033[{y};{x}f'
        if display:
            self.sout(out)
        else:
            return out

    def print_headers(self,dataList):
        #self.dataDict = dataDict
        available_lenght = int(self.max_x / len(dataList))
        current_pos=0

        self.goto(0,self.current_row)

        out = ""

        current_pos = 1
        for key in dataList:
            out += f'{self.goto(current_pos, 0, display=False)}'
            spaced_str = self.center_str(key, available_lenght)
            spaced_str = self.Pink(spaced_str)
            out += self.center_str(spaced_str, available_lenght)
            current_pos += available_lenght
        # print(out)
        self.sout(out)

        current_pos = 0
        template_str = ""
        for key in dataList:
            template_str += self.goto(current_pos,0,display=False)
            template_str += '['
            if current_pos + available_lenght == self.max_x:
                template_str += self.goto(current_pos + available_lenght, 0, display=False)
            else:
                template_str += self.goto(current_pos+available_lenght -1 ,0,display=False)
            template_str += ']'

            current_pos += available_lenght

        self.sout(template_str)
        self.current_row += 2
        self.refresh_from_row = self.current_row

        #

    def commit(self):
        self.current_row = self.refresh_from_row
        self.goto(0, self.max_y)

    def print_data(self, dataDict):
        self.dataDict = dataDict
        available_lenght = int(self.max_x / len(self.dataDict.keys()))
        current_pos = 0
        start_row = 1
        current_row = self.current_row
        self.goto(current_pos, current_row)
        out = ""
        max_dict_rows = 0
        max_name_length = 0
        max_value_length = 0
        for key in self.dataDict.keys():
            if max_dict_rows < len(self.dataDict[key]):
                max_dict_rows = len(self.dataDict[key])
            for name,value in self.dataDict[key]:
                if max_name_length < len(name):
                    max_name_length = len(name)
                if max_value_length < len(str(value)):
                    max_value_length = len(str(value))

        for i in range(0, max_dict_rows):
            current_row = start_row + i + self.current_row
            current_pos = 0
            data = []
            for key in self.dataDict.keys():
                col_data = self.dataDict[key]

                if len(col_data) > i:
                    name, value = self.dataDict[key][i]
                else:
                    name, value = ("","")
                data.append((name, str(value)))
            out = self.goto(current_pos,current_row,display=False)
            out += self.clear_line()
            for name,value in data:
                #name_pos =  int((available_lenght / 2) - (self.len(name)))
                #value_pos = int(available_lenght / 2)
                if name:
                    out += self.goto(current_pos+ max_name_length - len(name) +4,current_row,display=False)
                    out += self.col(name, self.FGRN)
                    out += f':'
                #current_pos += value_pos
                if value:
                    out += self.goto(current_pos+4+max_name_length +1, current_row, display=False)
                    out += self.col(value, self.FBLE)
                    out += self.goto(current_pos + 4 + max_name_length + max_value_length + 1, current_row, display=False)
                    out += f"[{self.col(len(value), self.FYEL)}]"
                current_pos += available_lenght


                self.sout(out)
        self.current_row += current_row
        #self.goto(0, self.max_y-2)

    def thead(self, lenght, msg=None):

        x = lenght
        #out = "\033[35;1m+"
        out = self.Fg("", 5)
        for i in range(0, x):
            out = out + "#"
        out = f'{out}\033[0;39m'
        self.p(out)
        if msg:
            msgLen = self.len(msg) + 4
            pos = int((x / 2) - (msgLen / 2))
            # pos = int(pos / 2)
            self.pos(pos)
            msgOut = self.Fg("[ ",13) + msg + self.Fg(" ]", 13)
            self.n(msgOut)
            self.pos(x)
            self.sout("\r\n")

    def clear_line(self, display=False):
        if display:
            self.sout("\033[2K")
        else:
            return "\033[2K"

    def center_str(self, dataString, available_lenght):
        padding = int((available_lenght / 2) - (self.len(dataString) / 2))
        spaces = ""
        for i in range(0, padding):
            spaces = f'{spaces} '
        dataString = f'{spaces}{dataString}{spaces}'
        if self.len(dataString) < available_lenght:
            dataString = f'{dataString} '
        return dataString

    def col(self, dataString, col, mod=1):
        if type(mod) == int:
            out = f'{col}\033[{str(mod)}m{dataString}{self.RS}'
        else:
            out = f'{col}{mod}{dataString}{self.RS}'
        return out

    def add_rnode(self, rnode, list_rint, list_lint):
        intStr = ""
        max_col = 0
        for rint, lint in zip(list_rint, list_lint):
            if intStr:
                intStr += self.Pink("|")

            intStr += f'{self.col(lint,self.FWHT,2)} {self.Fg(f"{self.ARROW_DL} {self.ARROW_UR}",92)} {self.col(rint,self.FWHT,2)}'

        # will represent longest int or node name
        max_col = self.len(intStr)
        # Node is longer
        if self.len(rnode) > max_col:
            max_col = self.len(rnode)
            # format int to center
            intStr = self.center_str(intStr, self.len(rnode))
        # int is longer
        elif self.len(rnode) < max_col:
            # format node to center
            rnode = self.center_str(rnode, self.len(intStr))

        self.dataList.append((rnode, intStr))

    def thead(self, lenght, msg=None):

        x = lenght
        #out = "\033[35;1m+"
        out = self.Fg("", 5)
        for i in range(0, x):
            out = out + "#"
        out = f'{out}\033[0;39m'
        self.p(out)
        if msg:
            msgLen = self.len(msg) + 4
            pos = int((x / 2) - (msgLen / 2))
            # pos = int(pos / 2)
            self.pos(pos)
            msgOut = self.Fg("[ ",13) + msg + self.Fg(" ]", 13)
            self.n(msgOut)
            self.pos(x)
            self.sout("\r\n")

    def ttail(self, lenght, msg=None, noNewLine=False, ansiCode=False):

        x = lenght
        out = "\033[35m"
        for i in range(0, x):
            out = out + "-"
        out = out + "\033[0;39m"
        self.p(out)
        if msg:
            msgLen = len(msg) + 4
            pos = int((x / 2) - (msgLen / 2))
            # pos = int(pos / 2)
            self.pos(pos)
            if ansiCode:
                msgOut = "[ " + ansiCode + msg + "\033[0;39m" + " ]\r"
            else:
                msgOut = "[ " + msg + " ]\r"
            self.n(msgOut)
        if not noNewLine:
            self.n("")


    def print(self):
        lineList = []
        #lineIndex = None
        intLineCont = ""
        nodeLineCont = ""
        linePos = 0
        self.max_x = self.get_x()


        for rnode, intStr in self.dataList:
            if linePos + self.len(intStr) + 1 >= self.max_x:
                lineList.append((intLineCont, nodeLineCont))
                intLineCont = ""
                nodeLineCont = ""
                linePos = 0

            intLineCont += f'{self.Fg("|",5)}{intStr}'
            nodeLineCont += f'{self.Fg("|",5)}{rnode}'
            linePos += self.len(intStr) + 1

        lineList.append((intLineCont, nodeLineCont))
        intLineCont = ""
        nodeLineCont = ""
        linePos = 0

        longest_line = 0
        for intLineCont, nodeLineCont in lineList:
            if self.len(intLineCont) > longest_line:
                longest_line = self.len(intLineCont) + 1

        self.thead(longest_line,self.Fg(self.main_node, 93))
        line_count = 0
        for intLineCont, nodeLineCont in lineList:
            self.p(f'{intLineCont}{self.Fg("|",5)}')
            self.pos(longest_line)
            print(self.Fg("|",5))
            self.p(f'{nodeLineCont}{self.Fg("|",5)}')
            self.pos(longest_line)
            print(self.Fg("|", 5))
            self.ttail(longest_line)

        print()
        print()

#my = MyLLDPtable("core.ballybane.sw1")
#my.add_rnode("gal_7750-SR7_an01", ['ge-0/0/10.0', 'ge-0/0/22.0', 'ge-0/0/23.0'], ['ge-0/0/23', 'ge-0/0/21.0', 'ge-0/0/5.0'])
#my.add_rnode("gal_7750-SR7_an01", ['ae0'], ['ae1'])
#my.add_rnode("core.cellcom.urlingford.sw1", ['ae0',"ge-0/0/22.0"], ['ae1',"ge-0/0/21.0"])

#my.print()
#for rnode, intStr in my.dataList:
#    print(f'|{intStr}|')
 #   print(f'|{rnode}|')

#my = MyLLDPtable("core.cellcom.urlingford.sw1")
#for rnode, intStr in my.dataList:
#    print(f'|{intStr}|')
#    print(f'|{rnode}|')


'''
    def head(self, msg=None):

        x = self.get_x()
        out = "\033[35;1m"
        for i in range(0, x):
            out = out + "#"
        out = out + "\033[0;39m"
        self.p(out)
        if msg:
            msgLen = len(msg) + 4
            pos = int((x / 2) - ( msgLen /2))
            #pos = int(pos / 2)
            self.pos(pos)
            msgOut = "[ " + msg + " ]"
            self.n(msgOut)
            self.pos(x)
            self.sout("\r\n")
'''




#b = Bar()
#b.head("asd")

#b.s("asd", "Asd")
#b.status()
#b.done()

data_model = {
    "Player1": [
        ("name1", "value1"),
        ("name22", "value22"),
        ("name333", "value333"),
        ("name4444", "value4444"),
    ],
    "Player2": [
        ("name1", "value1"),
        ("name2", "value2"),
        ("name3", "value3"),
        ("name4", "value4"),
    ],
    "Player3": [
        ("name1", "value1"),
        ("name2", "value2"),
        ("name3", "value3"),
        ("name4", "value4"),
    ],
    "Player4": [
        ("name1", "value1"),
        ("name2", "value2"),
        ("name3", "value3"),
        ("name4", "value4"),
        ("name5", "value5"),

    ],
}

if __name__ == "__main__":

    a = colorfull_table()
    a.print_headers(data_model)
    a.print_data(data_model)
    a.print_data(data_model)
