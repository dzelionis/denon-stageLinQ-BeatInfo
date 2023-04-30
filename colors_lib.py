import re
import random
import math
import webcolors
from dataclasses import dataclass, field, asdict, InitVar
from scipy.spatial import KDTree
from webcolors import (
  CSS3_NAMES_TO_HEX,
  hex_to_rgb,
)
import numpy as np
import pandas as pd

cMap = {'1': ' * Colors Only ',
 '10': ' Fire ',
 '11': ' Pink Candy ',
 '12': ' Rainbow ',
 '13': ' Splash ',
 '14': ' Rewhi ',
 '15': ' Blink Red ',
 '16': ' Rainbow Bands ',
 '17': ' Yelblu Hot ',
 '18': ' * Random Cycle ',
 '19': ' Sherbet ',
 '20': ' Party ',
 '21': ' Sunset ',
 '22': ' Beach ',
 '23': ' Toxy Reaf ',
 '24': ' Cyane ',
 '25': ' Jul ',
 '26': ' Autumn ',
 '27': ' Semi Blue ',
 '28': ' Grintage ',
 '29': ' Hult ',
 '3': ' * Color Gradient ',
 '30': ' Departure ',
 '31': ' Icefire ',
 '32': ' Forest ',
 '33': ' Retro Clown ',
 '34': ' Temperature ',
 '35': ' Fairy Reaf ',
 '36': ' Hult 64 ',
 '37': ' Cloud ',
 '38': ' Lava ',
 '39': ' Aurora 2 ',
 '4': ' * Color 1 ',
 '40': ' Lite Light ',
 '41': ' Magenta ',
 '42': ' Yellowout ',
 '43': ' Vintage ',
 '44': ' Ocean ',
 '45': ' Tertiary ',
 '46': ' Analogous ',
 '47': ' Orange &amp; Teal ',
 '48': ' Breeze ',
 '49': ' Rivendell ',
 '5': ' * Colors 1&amp;2 ',
 '50': ' Atlantica ',
 '51': ' Aqua Flash ',
 '52': ' C9 ',
 '53': ' C9 2 ',
 '54': ' Sunset 2 ',
 '55': ' Aurora ',
 '56': ' Red Tide ',
 '57': ' C9 New ',
 '58': ' Tiamat ',
 '59': ' Drywet ',
 '6': ' Orangery ',
 '60': ' Sakura ',
 '61': ' Pastel ',
 '62': ' Red Flash ',
 '63': ' April Night ',
 '64': ' Yelblu ',
 '65': ' Light Pink ',
 '66': ' Red &amp; Blue ',
 '67': ' Beech ',
 '68': ' Red Reaf ',
 '69': ' Red Shift ',
 '7': ' Candy2 ',
 '70': ' Candy ',
 '8': ' Landscape ',
 '9': ' Magred ',
 'unknown': ' Yelmag '}



cList =  {
    '1': ['black', 'lime'],
 '10': ['white',
        'yellow',
        'maroon',
        'black',
        'darkorange',
        'gold',
        'firebrick',
        'orange',
        'darkred',
        'orangered'],
 '11': ['mediumvioletred', 'blue', 'midnightblue', 'white'],
 '12': ['blue',
        'darkgoldenrod',
        'mediumblue',
        'seagreen',
        'firebrick',
        'saddlebrown',
        'lawngreen',
        'limegreen',
        'lime',
        'red',
        'indigo',
        'teal',
        'crimson',
        'purple'],
 '13': ['rosybrown', 'blueviolet', 'darkmagenta', 'firebrick'],
 '14': ['slategrey', 'brown', 'midnightblue', 'red', 'chocolate', 'sienna'],
 '15': ['salmon', 'darkmagenta', 'black', 'mediumblue', 'firebrick'],
 '16': ['blue',
        'black',
        'darkgoldenrod',
        'seagreen',
        'saddlebrown',
        'lime',
        'red',
        'indigo',
        'crimson'],
 '17': ['yellow', 'black', 'firebrick', 'darkred', 'chocolate'],
 '18': ['cornflowerblue', 'limegreen', 'darkturquoise', 'darkorchid'],
 '19': ['ivory', 'tomato', 'limegreen', 'lime', 'red', 'orangered'],
 '20': ['blue',
        'darkgoldenrod',
        'mediumblue',
        'saddlebrown',
        'red',
        'indigo',
        'crimson',
        'purple'],
 '21': ['navy', 'maroon', 'firebrick', 'darkblue', 'indigo', 'orangered'],
 '22': ['saddlebrown', 'black', 'darkorange', 'seagreen'],
 '23': ['limegreen', 'indigo'],
 '24': ['darkgreen',
        'indianred',
        'brown',
        'cadetblue',
        'darkcyan',
        'forestgreen',
        'khaki',
        'darkolivegreen'],
 '25': ['black', 'forestgreen', 'firebrick', 'maroon'],
 '26': ['saddlebrown', 'black', 'olivedrab', 'maroon'],
 '27': ['black', 'midnightblue', 'mediumblue'],
 '28': ['black', 'darkgoldenrod', 'darkgreen', 'maroon'],
 '29': ['teal', 'fuchsia', 'violet', 'plum'],
 '3': ['black', 'lime'],
 '30': ['burlywood',
        'darkgreen',
        'maroon',
        'black',
        'lime',
        'green',
        'sienna',
        'lightgreen',
        'white'],
 '31': ['blue', 'deepskyblue', 'dodgerblue', 'black', 'white', 'lightskyblue'],
 '32': ['mediumaquamarine',
        'darkgreen',
        'forestgreen',
        'seagreen',
        'lightgreen',
        'limegreen',
        'lawngreen',
        'olivedrab',
        'green',
        'yellowgreen',
        'darkolivegreen'],
 '33': ['chocolate', 'darkviolet', 'firebrick'],
 '34': ['dodgerblue',
        'darkcyan',
        'maroon',
        'gold',
        'darkorange',
        'royalblue',
        'orange',
        'midnightblue',
        'mediumseagreen',
        'darkred',
        'teal',
        'yellowgreen',
        'orangered'],
 '35': ['mediumvioletred', 'aquamarine', 'darkturquoise', 'white'],
 '36': ['teal', 'olive', 'darkgreen', 'darkslategray'],
 '37': ['blue', 'lightblue', 'darkblue', 'skyblue', 'white'],
 '38': ['maroon', 'black', 'orange', 'red', 'darkred', 'white'],
 '39': ['forestgreen',
        'mediumorchid',
        'lawngreen',
        'mediumseagreen',
        'palevioletred'],
 '4': ['lime'],
 '40': ['black'],
 '41': ['black', 'white', 'fuchsia', 'blue'],
 '42': ['darkgoldenrod', 'black'],
 '43': ['black', 'darkorange', 'olive', 'maroon'],
 '44': ['navy',
        'blue',
        'cornflowerblue',
        'aquamarine',
        'aqua',
        'darkcyan',
        'cadetblue',
        'mediumblue',
        'seagreen',
        'darkblue',
        'midnightblue',
        'teal',
        'lightskyblue'],
 '45': ['blue', 'darkgreen', 'saddlebrown', 'lime', 'red'],
 '46': ['blue', 'red', 'darkred'],
 '47': ['teal', 'orangered'],
 '48': ['teal', 'black', 'darkslategray', 'lightskyblue'],
 '49': ['black', 'grey', 'darkslategray'],
 '5': ['black', 'lime'],
 '50': ['seagreen',
        'royalblue',
        'lime',
        'midnightblue',
        'mediumseagreen',
        'darkslategray'],
 '51': ['black', 'turquoise', 'white', 'yellow'],
 '52': ['saddlebrown', 'midnightblue', 'darkgreen', 'darkred'],
 '53': ['firebrick', 'saddlebrown', 'midnightblue', 'red', 'green'],
 '54': ['black', 'darkorange', 'goldenrod', 'saddlebrown', 'darkslategray'],
 '55': ['black', 'green', 'lime', 'limegreen'],
 '56': ['maroon',
        'black',
        'gold',
        'goldenrod',
        'red',
        'sandybrown',
        'orangered'],
 '57': ['midnightblue', 'green', 'red', 'firebrick'],
 '58': ['darkviolet',
        'black',
        'springgreen',
        'lightblue',
        'seagreen',
        'fuchsia',
        'darkturquoise',
        'mediumspringgreen',
        'snow',
        'turquoise'],
 '59': ['navy',
        'black',
        'mediumblue',
        'goldenrod',
        'darkturquoise',
        'yellowgreen'],
 '6': ['darkorange', 'firebrick', 'saddlebrown', 'red', 'darkred', 'orangered'],
 '60': ['crimson', 'red', 'tomato', 'firebrick'],
 '61': ['coral',
        'yellow',
        'gold',
        'seagreen',
        'midnightblue',
        'yellowgreen',
        'tomato'],
 '62': ['sandybrown', 'black', 'red'],
 '63': ['black',
        'darkorange',
        'lightseagreen',
        'limegreen',
        'crimson',
        'orangered'],
 '64': ['blue', 'aqua', 'limegreen', 'yellow'],
 '65': ['darkorchid',
        'darkmagenta',
        'darkslateblue',
        'black',
        'slateblue',
        'lightblue',
        'lightcyan',
        'skyblue',
        'mediumpurple'],
 '66': ['black', 'midnightblue', 'red', 'maroon'],
 '67': ['aquamarine',
        'darkcyan',
        'teal',
        'darkturquoise',
        'midnightblue',
        'olivedrab',
        'darkslategray',
        'lightgoldenrodyellow',
        'darkkhaki',
        'turquoise'],
 '68': ['cornflowerblue', 'black', 'red'],
 '69': ['black', 'darkgoldenrod', 'darkred', 'firebrick'],
 '7': ['orange', 'black', 'darkorange', 'firebrick'],
 '70': ['midnightblue', 'chocolate', 'gold', 'black'],
 '8': ['black',
       'lightblue',
       'lightsteelblue',
       'mediumblue',
       'royalblue',
       'limegreen',
       'green',
       'yellowgreen'],
 '9': ['black', 'red', 'crimson', 'fuchsia'],
 'unknown': ['yellow', 'black', 'fuchsia', 'red', 'crimson', 'orangered']}




import json
from pprint import pprint

@dataclass
class MyDataClass():
    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(asdict(self))

#    def to_list(self):


def dist_3d(a,b):
  return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])+(a[2]-b[2])*(a[2]-b[2]))

def dist_3d_v2(r1,r2,g1,g2,b1,b2):
  return math.sqrt((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)




def sort_colors_old(colors, source):
    colorMap = []
    sortedColors = list()
    for i in range(len(colors)):
        dist = dist_3d(colors[i], source)
        #colorMap = colorMap + (dist, colors[i])
        colorMap.append((dist, colors[i]))

    sorted_by_dist = sorted(colorMap, key=lambda tup: tup[0])

    for (d, c) in sorted_by_dist:
        sortedColors.append(c)

    return sortedColors

def sort_colors(colors, source):
    result = sorted(colors, key=lambda color: dist_3d(color, source))
    return result

def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_NAMES_TO_HEX
    names = []
    rgb_values = []
    for color_name, color_hex in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'


def extract_colornames_from_string(string):
    resultList = []
    rr = re.compile(r'\(\d+,\s?\d+,\s?\d+\)')
    mm = rr.findall(string)
    if mm:
        for rgb in mm:
            tmp = rgb.lstrip("(")
            tmp = tmp.rstrip(")")
            tmp = tmp.split(", ")
            tmp = tuple(tmp)
            result = convert_rgb_to_names(tmp)
            resultList.append(result)
        tmp = set(resultList)
        tmp = list(tmp)
        return tmp
    else:
        return False

def phase_wled_html_for_colors(string):
    palleteList = {}
    palleteMap ={}
    #rr = re.compile(r"^' \\n ([a-zaA-Z -9&;]+) \\n<\/span>")
    palletes = string.split('<span class="lstIname">')
    #palletes = string.split('</span>')
    rr_id = re.compile(r'data-id="(\d+)"')
    for pallete in palletes:
        items = pallete.split("\n")
        pallete_name = items[1]

        colors_string = items[3]
        print(colors_string)
        list_of_colors = extract_colornames_from_string(colors_string)
        id_string = items[4]
        mm_id = rr_id.search(id_string)
        if mm_id:
            id = mm_id.groups()[0]
        else:
            id = "unknown"
        palleteMap[id] = pallete_name
        palleteList[id] = list_of_colors
        print(f'id: {id}, name: {pallete_name}, colors: {list_of_colors}')

    return (palleteMap, palleteList)

def rgb_hue(rgb, s=1):
  nrgb = rgb.astype(np.float64) / float(s)
  nmax = np.max(nrgb,1)
  ndelta = nmax - np.min(nrgb,1)
  return (np.where(ndelta == 0, 0
      , np.where(nmax == nrgb[:,0], nrgb[:,1]-nrgb[:,2]
      , np.where(nmax == nrgb[:,1], (nrgb[:,2]-nrgb[:,0])+2
      , (nrgb[:,0]-nrgb[:,1])+4))) / 6.) % 1.

def rgb_saturation(rgb, s=1):
  nrgb = rgb.astype(np.float64) / float(s)
  nmax = np.max(nrgb,1)
  ndelta = nmax - np.min(nrgb,1)
  return np.where(nmax == 0, 0, ndelta / nmax)

def rgb_value(rgb, s=1):
  nrgb = rgb.astype(np.float64) / float(s)
  nmax = np.max(nrgb,1)
  return nmax

def rgb_hsv(rgb, s=1, dhue=1, dsat=1, dval=1):
  nrgb = rgb.astype(np.float64) / float(s)
  nmax = np.max(nrgb,1)
  ndelta = nmax - np.min(nrgb,1)
  hue = (np.where(ndelta == 0, 0
      , np.where(nmax == nrgb[:,0], nrgb[:,1]-nrgb[:,2]
      , np.where(nmax == nrgb[:,1], (nrgb[:,2]-nrgb[:,0])+2
      , (nrgb[:,0]-nrgb[:,1])+4))) / 6.) % 1.
  sat = np.where(nmax == 0, 0, ndelta / nmax)
  val = nmax
  return np.column_stack((hue*dhue, sat*dsat, val*dval))

def get_dominant_color(list_of_rgb_colors):
  adv = np.array(list_of_rgb_colors)
  dom_color = []
  for channel_id in [0, 1, 2]:
    dom_color.append(np.argmax(np.histogram(adv[..., channel_id], bins=256, range=(0, 256))[0]))
  return dom_color

def get_nondominant_color(list_of_rgb_colors):
  adv = np.array(list_of_rgb_colors)
  dom_color = []
  for channel_id in [0, 1, 2]:
    dom_color.append(np.argmin(np.histogram(adv[..., channel_id], bins=256, range=(0, 256))[0]))
  return dom_color



@dataclass
class MyColors():
    color_list: list = field(default_factory=list)
    color_dict = {}
    color_use_dict = {}

    def get_pallete(self, mode="rgb"):

        color_list = self.populate_color_list(mode="name")
        color_dict = self.color_use_dict.copy()
        new_color_list = []
        for col in color_list:
            if col in color_dict.keys():
                if color_dict[col] != 0:
                    new_color_list.append(self.color_name_to_rgb(col))

        pri_col = self.get_pri_dominant_color(mode="rgb")
        results = sort_colors(new_color_list, pri_col)
        #if results is None:
        #    results = []
        #if [0,0,0] in results:
        #    results.remove([0,0,0])
        #    results.append([0,0,0])
        color_name_list  = []
        for col in results:
            color_name_list.append(convert_rgb_to_names(col))

        if mode == "rgb":
            return results
        elif mode == "name":
            return color_name_list
        elif mode == "hex":
            hexResults = []
            for item in color_name_list:
                hexResults.append(self.color_name_to_hex(item))
            return hexResults


    def get_random_color(self, mode="rgb", normalize=False):
        colorList = self.populate_color_list(mode="rgb")
        maxcol = len(colorList)
        randcol  = list(colorList)[random.randint(0, maxcol - 1)]
        if normalize == True:
            randcol = self.normalize_rgb_color(randcol)
        result =randcol
        color_name=convert_rgb_to_names(randcol)
        if mode == "rgb":
            result = self.color_name_to_rgb(color_name)
        elif mode == "hex":
            result = self.color_name_to_hex(color_name)
        elif mode == "name":
            result = color_name
        return result

    def normalize_rgb_color(self, col):
        max_value = max(col)
        col_add = 255 - max_value
        newCol = []
        for c in col:
            tmpCol = 0
            if c != 0:
                tmpCol = c + col_add
                newCol.append(tmpCol)
            else:
                newCol.append(0)
        return newCol

    def color_name_to_rgb(self, name):
        r,g,b = webcolors.name_to_rgb(name)
        Col = [r,g,b]
        return Col


    def color_name_to_hex(self, name):
        #Name = tcol.get_sec_dominant_color()
        Col = webcolors.name_to_rgb(name)
        hexcol = webcolors.rgb_to_hex(Col)
        return hexcol

    def colorlist_to_hex(self, namelist):
        result = []
        for name in namelist:
            result.append(self.color_name_to_hex(name))
        return result

    def colorlist_to_rgb(self, namelist):
        result = []
        for name in namelist:
            result.append(self.color_name_to_rgb(name))
        return result

    def reset_color_list(self):
        self.color_dict = {}
        self.color_use_dict = {}
        self.color_list = []



    def populate_color_list(self, mode="name"):
        color_list = []
        color_dict_copy = self.color_dict.copy()
        for key in color_dict_copy.keys():
            color_list.append(key)
        self.color_list = color_list
        if mode == "name":
            return self.color_list.copy()
        elif mode == "rgb":
            return self.colorlist_to_rgb(self.color_list)
        elif mode == "hex":
            return self.colorlist_to_hex(self.color_list)

    def reset_color_counters(self):
        for key in self.color_use_dict.keys():
            self.color_use_dict[key] = 0

    def expire_colors(self):
        expire_color_list = []
        for key in self.color_dict.keys():
            if self.color_dict[key] == 0:
                expire_color_list.append(key)
            else:
                self.color_dict[key] -= 1
        for color in expire_color_list:
            self.color_dict.pop(color)
            self.color_use_dict.pop(color)
        #self.reset_color_counters()


    def add_color(self, color, normalize=False):
        if normalize:
            if color != "black":
                rgb_color = self.color_name_to_rgb()
                rgb_color = self.normalize_rgb_color(rgb_color)
                color = convert_rgb_to_names(rgb_color)
        self.color_dict[color] = 30
        if color in self.color_use_dict.keys():
            self.color_use_dict[color] += 1
        else:
            self.color_use_dict[color] = 1


    def get_pri_dominant_color(self, mode="rgb", normalize=False):
        color_hit = 0
        color_name = "black"
        colore_list = self.populate_color_list()
        color_use_dict = self.color_use_dict.copy()
        #print(colore_list)
        #print(color_use_dict)
        #print(color_use_dict)
        if "black" in colore_list:
            colore_list.remove("black")
        for color in colore_list:
            if color not in color_use_dict.keys():
                continue
            if color_use_dict[color] > color_hit:
                color_hit = color_use_dict[color]
                color_name = color
        if color_name != "black" and normalize==True:
            rgb = self.color_name_to_rgb(color_name)
            rgb = self.normalize_rgb_color(rgb)
            color_name = convert_rgb_to_names(rgb)
        result = color_name
        if mode == "rgb":
            result = self.color_name_to_rgb(color_name)
        elif mode == "hex":
            result = self.color_name_to_hex(color_name)
        elif mode == "name":
            result = color_name
        return result


    def get_sec_dominant_color(self,mode="rgb", normalize=False):
        color = self.get_pri_dominant_color(mode="name")
        if color == "black":
            return color

        color_hit = 0
        color_name = "black"
        colore_list = self.populate_color_list()
        color_use_dict = self.color_use_dict.copy()

        if "black" in colore_list:
            colore_list.remove("black")
        if color in colore_list:
            colore_list.remove(color)
        for color in colore_list:
            if color not in color_use_dict.keys():
                continue
            if color_use_dict[color] > color_hit:
                color_hit = color_use_dict[color]
                color_name = color
        if color_name != "black" and normalize == True:
            rgb = self.color_name_to_rgb(color_name)
            rgb = self.normalize_rgb_color(rgb)
            color_name = convert_rgb_to_names(rgb)
        result = color_name
        if mode == "rgb":
            result = self.color_name_to_rgb(color_name)
        elif mode == "hex":
            result = self.color_name_to_hex(color_name)
        elif mode == "name":
            result = color_name
        return result

    def get_third_dominant_color(self, mode="rgb", normalize=False):
        sec_color = self.get_sec_dominant_color(mode="name")
        pri_color = self.get_pri_dominant_color(mode="name")

        if sec_color == "black":
            return pri_color

        color_hit = 0
        color_name = sec_color
        colore_list = self.populate_color_list()
        color_use_dict = self.color_use_dict.copy()

        if "black" in colore_list :
            colore_list.remove("black")
        if pri_color in colore_list:
            colore_list.remove(pri_color)
        if sec_color in colore_list:
            colore_list.remove(sec_color)
        for color in colore_list:
            if color not in color_use_dict.keys():
                continue
            if color_use_dict[color] > color_hit:
                color_hit = color_use_dict[color]
                color_name = color
        if color_name != "black" and normalize == True:
            rgb = self.color_name_to_rgb(color_name)
            rgb = self.normalize_rgb_color(rgb)
            color_name = convert_rgb_to_names(rgb)
        result = color_name
        if mode == "rgb":
            result = self.color_name_to_rgb(color_name)
        elif mode == "hex":
            result = self.color_name_to_hex(color_name)
        elif mode == "name":
            result = color_name
        return result
