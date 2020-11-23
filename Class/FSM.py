import json
from collections import namedtuple
from json import JSONEncoder
from tkinter import filedialog
from types import SimpleNamespace


class Edge:
    def __init__(self, source, label, destination):
        self.source = source
        self.label = label
        self.destination = destination
        self.transition_link = []


#  This is the Finite state machine constructor, where we have:
#  - the name of the fsm
#  - the states' array, there we have the acceptable states
#  - the final state
#  - the edges, that are the link between states
class FiniteStateMachine:
    def __init__(self, name, states, final_states, edges):
        self.name = name
        self.states = states
        self.final_states = final_states
        self.edges = edges


class FSMEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def read_fsm_from_json():
    # filename = filedialog.askopenfilename()
    filename = "JSON/C3.json"
    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)

        fsm = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))

        return fsm


# In this function the fsm is saved as a JSON file whose name is made with
# the current time and date.
def save_fsm_as_json(fsm):
    with open("JSON/" + fsm.name + ".json", "w") as write_file:
        json.dump(fsm, write_file, indent=4, cls=FSMEncoder)

# In this function the fsm is read from a JSON file

def read_fsm_from_txt():
    # get file object
    f = open("input.txt", "r")
    c = 0
    name = ""
    states = []
    final_states = []
    edges = []

    while (True):
        # read next line
        if c == 0:
            line = f.readline()
            name = line[:-1]
        elif c == 1:
            line = f.readline()
            line = line[:-1]
            split_states = line.split(",")
            for state in split_states:
                states.append(state)
        elif c == 2:
            line = f.readline()
            line = line[:-1]
            split_states = line.split(",")
            for state in split_states:
                final_states.append(state)
        else:
            line = f.readline()
            split_line = line.split("/")
            split_line.remove(split_line[len(split_line)-1])
            for edge_full in split_line:
                # print(edge_full)
                edge_split = edge_full.split(",")
                list = []
                for e in edge_split:
                    list.append(e)

                edge = Edge(list[0], list[2], list[1])
                edges.append(edge)


        # if line is empty, you are done with all lines in the file
        c += 1
        if not line:
            break
        # you can access the line
    fsm = FiniteStateMachine(name, states, final_states, edges)

    # close file
    f.close()
    return fsm