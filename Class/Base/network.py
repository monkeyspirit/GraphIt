import json
from collections import namedtuple
from json import JSONEncoder
from tkinter import filedialog
from types import SimpleNamespace


class Link:
    def __init__(self, source, name, destination, state):
        self.source = source
        self.name = name
        self.destination = destination
        self.state = state


class Network:
    def __init__(self, fsms, links, transitions):
        self.fsms = fsms
        self.links = links



class NetworkEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def save_network_as_json(network, dir_filename):
    with open("Output/"+dir_filename+"/network_" + dir_filename + ".json", "w") as write_file:
        json.dump(network, write_file, indent=4, cls=NetworkEncoder)


# In this function the fsm is read from a JSON file
def read_network_from_json():
    filename = filedialog.askopenfilename()

    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)

        n = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
        return n

def read_link_from_txt():
    # get file object
    filename = filedialog.askopenfilename()
    f = open(filename, "r")
    c = 0

    links = []

    # read next line
    while(True):
        source = ""
        name = ""
        destination = ""
        state = ""
        line = f.readline()
        if not line:
            break
        line = line[:-1]
        split_line = line.split(",")
        el = []
        for i in split_line:
            el.append(i)

        if len(el)>4:
            raise IndexError
        # you can access the line
        link = Link(el[0], el[1], el[2], el[3])
        links.append(link)

    # close file
    f.close()

    return links