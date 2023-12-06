#!/usr/bin/env python3

class Race:
    def __init__(self, time, record):
        self.time = time
        self.record = record

    def distance_with_speed(self, speed):
        return speed * (self.time - speed)

    def beat_record(self):
        nb_records = 0
        for speed in range(1, self.time):
            if self.distance_with_speed(speed) > self.record:
                nb_records = nb_records + 1
        return nb_records

sample = [
    Race(7, 9),
    Race(15, 40),
    Race(30, 200)
]

challenge = [
    Race(35, 212),
    Race(93, 2060),
    Race(73, 1201),
    Race(66, 1044)
]

challenge2 = [
    Race(35937366, 212206012011044)
]

from functools import reduce

records = [ race.beat_record() for race in challenge2 ]
print(reduce((lambda x, y: x * y), records))