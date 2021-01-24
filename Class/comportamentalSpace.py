import json
from collections import namedtuple
from json import JSONEncoder
from tkinter import filedialog
from random import seed
from random import randint
from types import SimpleNamespace


class Transition:
    def __init__(self, fsm, label, input, output, relevance_label,
                 observability_label):
        self.fsm = fsm
        self.label = label
        self.input = input
        self.output = output
        self.relevance_label = relevance_label
        self.observability_label = observability_label


class Space:

    def __init__(self, nodes, transitions):
        seed(1)
        self.id = randint(0, 100)
        self.nodes = nodes
        self.nodes_after_cutting = []
        self.cutted_nodes = []
        self.transitions = transitions
        self.transitions_after_cutting = []
        self.cutted_transitions = []


class ObservableNode:
    def __init__(self, link_node, id, observation_index):
        self.link_node = link_node
        self.id = id
        self.direct_reachable = []
        self.reachable_nodes = []
        self.observation_index = observation_index
        self.isFinal = False


class ObservableTransition:
    def __init__(self, label, observation_index, source, destination, observability_label, relevance_label):
        self.label = label
        self.source = source
        self.destination = destination
        self.observation_index = observation_index
        self.observability_label = observability_label
        self.relevance_label = relevance_label


class E_transition:
    def __init__(self, label, source, destination):
        self.label = label
        self.source = source
        self.destination = destination
        self.list_label = []


class Node:
    count = -1

    def __init__(self, fsms_states, links_states, label, isFinal):
        self.fsms_states = fsms_states
        self.links_states = links_states
        self.label = label
        Node.count += 1
        self.id = Node.count
        self.reachable_nodes = []
        self.isFinal = isFinal
        self.isReachingFinal = 0
        self.edges = []
        self.renomination_label = ""
        self.old_id = ""


class SpaceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def save_space_as_json(space, filename):
    with open("JSON/" + filename + ".json", "w") as write_file:
        json.dump(space, write_file, indent=4, cls=SpaceEncoder)


# In this function the fsm is read from a JSON file
def read_space_from_json():
    filename = filedialog.askopenfilename()
    list_filename = filename.split("/")
    name_ext = list_filename[len(list_filename)-1]
    name_list = name_ext.split(".")
    name = name_list[0]
    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)

        space = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
        return space, name


def read_transitions_from_txt():
    # get file object
    filename = filedialog.askopenfilename()
    f = open(filename, "r")

    transitions = []

    while (True):
        fsm = ""
        label = ""
        input = []
        output = []
        obs_label = ""
        rel_label = ""
        line = f.readline()
        if not line:
            break
        # print(line)
        line = line[:-1]

        split_line = line.split(",")
        # print(split_line)
        list = []

        for el in split_line:
            list.append(el)

        fsm = list[0]
        label = list[1]
        obs_label = list[4]
        rel_label = list[5]

        input_list = list[2][1:-1]


        input_list = input_list.split("/")
        input_dic = {}
        if input_list != []:
            for input in input_list:
                if input != "":
                    split_input = input.split(":")
                    input_dic.update({split_input[0]: split_input[1]})

        output_list = list[3][1:-1]


        output_list = output_list.split("/")
        output_dic = {}
        if output_list != []:
            for output in output_list:
                if output != "":
                    split_output = output.split(":")
                    output_dic.update({split_output[0]: split_output[1]})


        # you can access the line
        # print(list)
        transition = Transition(fsm, label, input_dic, output_dic, obs_label, rel_label)
        transitions.append(transition)

    # close file
    f.close()
    return transitions
