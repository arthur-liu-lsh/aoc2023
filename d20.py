from collections import deque
from typing import Deque, Dict, List, Set, Tuple
from math import lcm

from copy import deepcopy

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt
import re

class Gate():
    def __init__(self, name: str, inputs: List[str], outputs: List[str], queue: Deque, counter: Dict[bool, int]):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.state = False
        self.queue = queue
        self.counter = counter

    def update(self, input_name: str, signal: bool):
        pass

    def get_state(self, ):
        pass

    def set_state(self, state):
        pass

class Broadcast(Gate):
    def update(self, input_name: str, signal: bool):
        for output in self.outputs:
            self.counter[False] += 1
            self.queue.append((output, self.name, False))
    
    def get_state(self):
        return None
    
    def set_state(self, state):
        pass

class FlipFlop(Gate):
    def update(self, input_name: str, signal: bool):
        if not signal:
            self.state = not self.state
            for output in self.outputs:
                self.counter[self.state] += 1
                self.queue.append((output, self.name, self.state))
        
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

class Conjunction(Gate):
    def __init__(self, name: str, inputs: List[str], outputs: List['Gate'], queue: Deque, counter: Dict[bool, int]):
        super().__init__(name, inputs, outputs, queue, counter)
        self.state = True
        self.states = {}
        for input_name in self.inputs:
            self.states[input_name] = False

    def update(self, input_name: str, signal: bool):
        self.states[input_name] = signal
        for output in self.outputs:
            signal = not all(self.states.values())
            self.counter[signal] += 1
            self.queue.append((output, self.name, signal))

    def get_state(self):
        return tuple(self.states.values())

    def set_state(self, state):
        for key, value in state:
            self.states[key] = value

def get_state(world: Dict[str, Gate]):
    states = []
    for gate in world.values():
        states.append((gate.name, gate.get_state()))
    return tuple(states)

def set_state(world: Dict[str, Gate], states):
    for name, state in states:
        world[name].set_state(state)

lines_test = utils.parse("d20test.txt")
lines = utils.parse("d20.txt")

@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0

    types = {}
    gates = {}
    setag = {}

    world: Dict[str, Gate] = {}
    counter = {True: 0, False: 0}

    for line in lines:
        line = line.replace('->', '')
        line = line.replace(',', '')
        words = line.split()
        first = words[0]
        others = words[1:]
        name = first
        if first[0] == '%':
            name = first[1:]
            types[name] = 1
        elif first[0] == '&':
            name = first[1:]
            types[name] = 2
        else:
            types[name] = 0
        gates[name] = others

    for key, values in gates.items():
        for value in values:
            if value not in setag:
                setag[value] = []
            setag[value].append(key)
    
    queue = deque()

    for name, outputs in gates.items():
        if name in setag:
            inputs = setag[name]
        else:
            inputs = None
        if types[name] == 0:
            world[name] = Broadcast(name, inputs, outputs, queue, counter)
        elif types[name] == 1:
            world[name] = FlipFlop(name, inputs, outputs, queue, counter)
        elif types[name] == 2:
            world[name] = Conjunction(name, inputs, outputs, queue, counter)


    k = 0
    stop = False
    rs_counter = [None, None, None, None]
    while k < 10000:
        queue.append(('broadcaster', None, None))
        k+=1
        if k % 100000 == 0:
            print("iter", k)
        counter[False] += 1
        if stop:
            break
        while len(queue) != 0:
            target, origin, signal = queue.popleft()
            if target in world:
                world[target].update(origin, signal)
            rs_state = world['rs'].get_state()
            if any(rs_state):
                if rs_counter[0] is None and rs_state[0]:
                    rs_counter[0] = k
                if rs_counter[1] is None and rs_state[1]:
                    rs_counter[1] = k
                if rs_counter[2] is None and rs_state[2]:
                    rs_counter[2] = k
                if rs_counter[3] is None and rs_state[3]:
                    rs_counter[3] = k
        if k == 1000:
            result1 = counter[True] * counter[False]


    result2 = lcm(*rs_counter)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

# run(lines_test)
run(lines)