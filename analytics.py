import time
import dataclasses
from typing import NamedTuple


def nsTOms(ns):
    return  round(ns / 1000000)

def nsTOs(ns):
    return round((ns / 1000000) / 1000)
def nsTos_v2(ns):
    return round(ns / 1e9)

class FixedSizeList():

    def __init__(self, size):
        self.size = size
        self.data = []

    def __repr__(self):
        result = f'[{",".join(self.data)}]'
        return result

    def append(self, item):
        if len(self.data) == self.size:
            self.data.pop(self.size - 1 )
        self.data.insert(0, item)

    def diff_between_current_and_most_recent_value(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0]
        else:
            if self.data[0] > self.data[1]:
                return self.data[0] - self.data[1]
            elif self.data[0] < self.data[1]:
                return self.data[1] - self.data[0]
            else:
                return 0

    def diff_between_current_and_oldest_value(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0]
        else:
            oldest_index = len(self.data) - 1
            if self.data[0] > self.data[oldest_index]:
                return self.data[0] - self.data[oldest_index]
            elif self.data[0] < self.data[oldest_index]:
                return self.data[oldest_index] - self.data[0]
            else:
                return 0


    def calculate_avg(self):
        if len(self.data) == 0:
            return None
        elif len(self.data) == 1:
            return self.data[0]
        else:
            result = 0
            for i in range(0, len(self.data)):
                result += self.data[i]
            result = result / len(self.data)
            return result


class FixedTimeSizeList():
    def __init__(self, timeWindowIn_ms):
        self.data = []
        self.beat = 0
        self.size = None
        self.avgSize = None
        self.phase = 0
        self.beatTime = time.time_ns()
        self.timeWindowIn_ns = timeWindowIn_ms * 1000000
        self.sizesList = FixedSizeList(5)
        self.beatTotalTime = 0
        self.bufferStartTime = time.time_ns()
        self.bufferTotalTime = 0


    def __repr__(self):
        self.expire_data()
        result = ""
        for item, timestamp in self.data:
            if not result:
                result = f'[{item}'
            else:
                result += f', {item}'
        if result:
            result += "]"
        else:
            result = "[]"
        return result

    def expire_data(self):
        data_expired = False
        last_index = len(self.data) - 1
        while True:
            if last_index <= -1:
                break
            item, timestamp = self.data[last_index]
            if time.time_ns() > timestamp + self.timeWindowIn_ns + 100:
                data_expired = True
                self.data.pop(last_index)
                last_index -= 1
            last_index -= 1
        if data_expired:
            self.sizesList.append(len(self.data))

    def current_size(self):
        self.expire_data()
        return len(self.data)
    def avg_size(self):
        result = self.sizesList.calculate_avg()
        self.expire_data()
        return result
    def populate_list(self):
        result = []
        for value, timestamp in self.data:
            result.append(value)
        return result

    def append(self, item):
        timestamp = time.time_ns()
        data = self.populate_list()
        if data:
            max_value = max(data)
            min_value = min(data)
            last_value = data[len(data) -1]

            if item == 0 and last_value != 0:
                self.beat += 1
                self.phase = 0
                self.beatTotalTime = 0
                self.beatTime = time.time_ns()
            elif item == 0 and last_value == 0:
                pass
            elif item > 0:
                self.beatTime += 1

            #if time.time_ns() > timestamp + self.timeWindowIn_ns


        aaa = """
            if min_value >= 0:
                if last_value == min_value:
                    if item > last_value >= max_value:
                    #if item >= min_value
                        self.phase = 0
                #elif last_value <= min_value:
                #    if last_value == item:
                #        self.phase = 0
                elif last_value < item:
                    #if last_value == item:
                    self.phase += 1

                #elif last_value != item < 0:
                #    #if last_value == item:
                #    self.phase += 1
            elif min_value < 0:
                if last_value == min_value:
                    if last_value != item > 0:
                    #if item >= min_value
                        self.phase = 0
                #elif last_value <= min_value:
                #    if last_value == item:
                #        self.phase = 0
                elif last_value != item:
                    #if last_value == item:
                    self.phase += 1


            if self.phase >= 16:
                self.phase = 0

                #elif last_value <= min_value:
                #    if last_value < item:
                #        if item >= min_value:
                #            self.phase = 0
                ##elif last_value > min_value:
                 ##   if last_value > item:
                  #      self.phase += 1
"""
        self.data.insert(0, (item, timestamp))
        self.expire_data()


    def diff_between_current_and_most_recent_value(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            #if self.data[0][0] > self.data[1][0]:
            return self.data[0][0] - self.data[1][0]
            #elif self.data[0][0] < self.data[1][0]:
            #    return self.data[1][0] - self.data[0][0]
            #else:
            #    return 0

    def diff_between_current_and_oldest_value(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            oldest_index = len(self.data) - 1
            if self.data[0][0] > self.data[oldest_index][0]:
                return self.data[0][0] - self.data[oldest_index][0]
            elif self.data[0][0] < self.data[oldest_index][0]:
                return self.data[oldest_index][0] - self.data[0][0]
            else:
                return 0

    def get_ratio(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            oldest_index = len(self.data) - 1
            if self.data[0][0] > self.data[oldest_index][0]:
                return self.data[0][0] / self.data[oldest_index][0]
            elif self.data[0][0] < self.data[oldest_index][0]:
                return self.data[oldest_index][0] / self.data[0][0]
            else:
                return 0

    def print_all_unique(self):
        self.expire_data()
        result = set()
        for value,name in self.data:
            result.add(str(value))
        return ",".join(list(result))

    def print_all_values(self):

        result = []
        for value,name in self.data:
            result.append(str(value))
        self.expire_data()
        #
        return result

#         return ",".join(result)

    def calculate_avg(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            result = 0
            for i in range(0, len(self.data)):
                result += self.data[i][0]
            result = result / len(self.data)
            return result








class BeatBuffer():
    def __init__(self):
        self.data = []
        self.beat = 0
        self.size = None
        self.avgSize = None
        self.phase = 0
        self.beatTime = time.time_ns()
        self.sizesList = FixedSizeList(5)
        self.beatTotalTime = 0
        self.bufferStartTime = time.time_ns()
        self.bufferTotalTime = 0
        self.phase_data = 0

    def __repr__(self):
        self.expire_data()
        result = ""
        for item, timestamp in self.data:
            if not result:
                result = f'[{item}'
            else:
                result += f', {item}'
        if result:
            result += "]"
        else:
            result = "[]"
        return result

    def phase(self, beats,quantum):
        #if quantum == Beats{INT64_C(0)})
        pass

    def expire_data(self):

        data_expired = False
        last_index = len(self.data) - 1
        item, timestamp = self.data[last_index]
        if time.time_ns() > timestamp + item + 1:
            if len(self.data) > 2:
              #data_expired = True
              self.data.pop(last_index)
              last_index -= 1
              self.phase_data += 1
              self.sizesList.append(len(self.data))


#    def expire_data(self):
#        data_expired = False
#        last_index = len(self.data) - 1
#        while True:
#            if last_index <= -1:
#                break
#            item, timestamp = self.data[last_index]
#            if time.time_ns() > timestamp + self.timeWindowIn_ns + 100:
#                data_expired = True
#                self.data.pop(last_index)
#                last_index -= 1
#            last_index -= 1
#        if data_expired:
#            self.sizesList.append(len(self.data))

    def current_size(self):
        self.expire_data()
        return len(self.data)
    def avg_size(self):
        result = self.sizesList.calculate_avg()
        self.expire_data()
        return result
    def populate_list(self):
        result = []
        for value, timestamp in self.data:
            result.append(value)
        return result

    def append(self, item):
        timestamp = time.time_ns()
        data = self.populate_list()
        if data:
            max_value = max(data)
            min_value = min(data)
            last_value = data[len(data) -1]

            if item == 0 and last_value != 0:
                self.beat += 1
                self.phase = 0
                self.beatTotalTime = 0
                self.beatTime = time.time_ns()
            elif item == 0 and last_value == 0:
                pass
            #elif item > 0:
            #    self.beatTime

            #if time.time_ns() > timestamp + self.timeWindowIn_ns

        self.data.insert(0, (item, timestamp))
        self.expire_data()


    def diff_between_current_and_most_recent_value(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            #if self.data[0][0] > self.data[1][0]:
            return self.data[0][0] - self.data[1][0]
            #elif self.data[0][0] < self.data[1][0]:
            #    return self.data[1][0] - self.data[0][0]
            #else:
            #    return 0

    def diff_between_current_and_oldest_value(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            oldest_index = len(self.data) - 1
            if self.data[0][0] > self.data[oldest_index][0]:
                return self.data[0][0] - self.data[oldest_index][0]
            elif self.data[0][0] < self.data[oldest_index][0]:
                return self.data[oldest_index][0] - self.data[0][0]
            else:
                return 0

    def get_ratio(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            oldest_index = len(self.data) - 1
            if self.data[0][0] > self.data[oldest_index][0]:
                return self.data[0][0] / self.data[oldest_index][0]
            elif self.data[0][0] < self.data[oldest_index][0]:
                return self.data[oldest_index][0] / self.data[0][0]
            else:
                return 0

    def print_all_unique(self):
        self.expire_data()
        result = set()
        for value,name in self.data:
            result.add(str(value))
        return ",".join(list(result))

    def print_all_values(self):

        result = []
        for value,name in self.data:
            result.append(str(nsTOms(value)))
        self.expire_data()
        #
        return result

#         return ",".join(result)

    def calculate_avg(self):
        if len(self.data) == 0:
            return 0
        elif len(self.data) == 1:
            return self.data[0][0]
        else:
            result = 0
            for i in range(0, len(self.data)):
                result += self.data[i][0]
            result = result / len(self.data)
            return result
