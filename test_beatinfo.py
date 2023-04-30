#!/usr/bin/env python3
from log import *
setup_logging("ERROR")
import random
import os
import sys
import time
import copy
import threading
from colors_lib import MyColors
phase = 0
import sys
from controller import bi,Controller
from BeatInfo import TwoValueBuffer



ctrl = Controller()
from  controller import at
at.start()
ctrl.connect_services()
