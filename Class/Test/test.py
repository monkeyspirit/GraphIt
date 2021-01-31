import json
import tracemalloc
from datetime import datetime
from tkinter import filedialog
from types import SimpleNamespace
import timeit

from Class.Base.space import Transition
import Class.Spaces.create_behavioral_space_renominated
import Class.Spaces.create_behavioral_spaces
import Class.Spaces.create_observable_space
import Class.Spaces.create_observable_space_Renominated
import Class.Spaces.execute_diagnosi_observation

def read_transitions(filename):
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

def read_space(filename):
    list_filename = filename.split("/")
    name_ext = list_filename[len(list_filename)-1]
    name_list = name_ext.split(".")
    name = name_list[0]
    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)

        space = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
        return space, name

def read_network(filename):

    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)

        n = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
        return n

if __name__ == '__main__':

    SETUP = '''
from Class.Base.space import Transition
import Class.Spaces.create_behavioral_space_renominated
import Class.Spaces.create_behavioral_spaces
import Class.Spaces.create_observable_space
import Class.Spaces.create_observable_space_Renominated
import Class.Spaces.execute_diagnosi_observation
import json
from collections import namedtuple
from json import JSONEncoder
from tkinter import filedialog
from types import SimpleNamespace
import tracemalloc

    '''
    TEST_1 = '''
tracemalloc.start()
dir_filename = "test"
filename_network = "/home/maria/PycharmProjects/Algoritmi/Input/network_rete1.json"
filename_transition = "/home/maria/PycharmProjects/Algoritmi/Input/Rete1/input_transition.txt"

# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete1/space_2021-01-28_rete1_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete2/space_2021-01-28_rete2_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete3/space_2021-01-28_rete3_BS.json"
f = open(filename_transition, "r")

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

with open(filename_network, "r+") as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

    network = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
print("=========== USEFUL METHODS ===========")  
print("Traced Memory 1 (Current, Peak): ", tracemalloc.get_traced_memory())
full_space = Class.Spaces.create_behavioral_spaces.create_behavioral_space(dir_filename+'_BS', network, transitions,dir_filename)
print("Traced Memory 2 (Current, Peak): ", tracemalloc.get_traced_memory())
full_space_r = Class.Spaces.create_behavioral_space_renominated.create_behavioral_space_renominated(dir_filename+'_RE', full_space, 0, dir_filename)
print("Traced Memory 3 (Current, Peak): ", tracemalloc.get_traced_memory())
obs=["o3","o2"]
obs_full_space = Class.Spaces.create_observable_space.create_behavioral_space_from_obs(dir_filename+'_OS', obs, full_space_r, dir_filename)
print("Traced Memory 4 (Current, Peak): ", tracemalloc.get_traced_memory())
obs_space_r = Class.Spaces.create_observable_space_Renominated.create_behavioral_space_observable_renominated(dir_filename+'_ROS', obs_full_space, dir_filename)
print("Traced Memory 5 (Current, Peak): ", tracemalloc.get_traced_memory())
Class.Spaces.execute_diagnosi_observation.create_diagnosis_for_space_observable_renominated(dir_filename, obs_space_r)  
print("Traced Memory 6 (Current, Peak): ", tracemalloc.get_traced_memory())
print("======================")

tracemalloc.stop()
'''
    TEST_2 = '''
tracemalloc.start()
dir_filename = "test"
filename_transition = "/home/maria/PycharmProjects/Algoritmi/Input/Rete2/transition_SB.txt"
filename_network = "/home/maria/PycharmProjects/Algoritmi/Input/network_rete2.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete1/space_2021-01-28_rete1_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete2/space_2021-01-28_rete2_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete3/space_2021-01-28_rete3_BS.json"
f = open(filename_transition, "r")

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

with open(filename_network, "r+") as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

    network = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))

print("1,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
full_space = Class.Spaces.create_behavioral_spaces.create_behavioral_space(dir_filename+'_BS', network, transitions,dir_filename)
print("2,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
full_space_r = Class.Spaces.create_behavioral_space_renominated.create_behavioral_space_renominated(dir_filename+'_RE', full_space, 0, dir_filename)
print("3,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
obs=["act","sby","nop"]
obs_full_space = Class.Spaces.create_observable_space.create_behavioral_space_from_obs(dir_filename+'_OS', obs, full_space_r, dir_filename)
print("4,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
obs_space_r = Class.Spaces.create_observable_space_Renominated.create_behavioral_space_observable_renominated(dir_filename+'_ROS', obs_full_space, dir_filename)
print("5,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
Class.Spaces.execute_diagnosi_observation.create_diagnosis_for_space_observable_renominated(dir_filename, obs_space_r)  
print("6,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])

tracemalloc.stop()
'''
    TEST_3 = '''
tracemalloc.start()
dir_filename = "test"

filename_transition = "/home/maria/PycharmProjects/Algoritmi/Input/Rete3/transition_c123.txt"

filename_network = "/home/maria/PycharmProjects/Algoritmi/Input/network_rete3.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete1/space_2021-01-28_rete1_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete2/space_2021-01-28_rete2_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete3/space_2021-01-28_rete3_BS.json"
f = open(filename_transition, "r")

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

with open(filename_network, "r+") as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

    network = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))


print("1,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
full_space = Class.Spaces.create_behavioral_spaces.create_behavioral_space(dir_filename+'_BS', network, transitions,dir_filename)
print("2,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
full_space_r = Class.Spaces.create_behavioral_space_renominated.create_behavioral_space_renominated(dir_filename+'_RE', full_space, 0, dir_filename)
print("3,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
obs=["o1","o2"]
obs_full_space = Class.Spaces.create_observable_space.create_behavioral_space_from_obs(dir_filename+'_OS', obs, full_space_r, dir_filename)
print("4,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
obs_space_r = Class.Spaces.create_observable_space_Renominated.create_behavioral_space_observable_renominated(dir_filename+'_ROS', obs_full_space, dir_filename)
print("5,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
Class.Spaces.execute_diagnosi_observation.create_diagnosis_for_space_observable_renominated(dir_filename, obs_space_r)  
print("6,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])

tracemalloc.stop()
'''
    TEST_4 = '''
# tracemalloc.start()
dir_filename = "test"

filename_transition = "/home/maria/PycharmProjects/Algoritmi/transizioni.txt"

filename_network = "/home/maria/PycharmProjects/Algoritmi/Input/network_caso1.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete1/space_2021-01-28_rete1_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete2/space_2021-01-28_rete2_BS.json"
# filename = "/home/maria/PycharmProjects/Algoritmi/Output/rete3/space_2021-01-28_rete3_BS.json"
f = open(filename_transition, "r")

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

with open(filename_network, "r+") as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

    network = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))


# print("1,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
full_space = Class.Spaces.create_behavioral_spaces.create_behavioral_space(dir_filename+'_BS', network, transitions,dir_filename)
# print("2,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
full_space_r = Class.Spaces.create_behavioral_space_renominated.create_behavioral_space_renominated(dir_filename+'_RE', full_space, 0, dir_filename)
# print("3,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
obs=["ins","re"]
obs_full_space = Class.Spaces.create_observable_space.create_behavioral_space_from_obs(dir_filename+'_OS', obs, full_space_r, dir_filename)
# print("4,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
obs_space_r = Class.Spaces.create_observable_space_Renominated.create_behavioral_space_observable_renominated(dir_filename+'_ROS', obs_full_space, dir_filename)
# print("5,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
Class.Spaces.execute_diagnosi_observation.create_diagnosis_for_space_observable_renominated(dir_filename, obs_space_r)  
# print("6,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])

# tracemalloc.stop()
    '''
    r_date = open("/home/maria/PycharmProjects/Algoritmi/Output/Test/test_case_dia_no_img.txt", "w")

    # r_date.write("id,Tempo\n")

    # dates = timeit.repeat(setup=SETUP, stmt=TEST_1, repeat=10, number=1)
    # for date in dates:
    #     r_date.write("Rete1,"+str(date)+"\n")

    # dates = timeit.repeat(setup=SETUP, stmt=TEST_2, repeat=10, number=1)
    # for date in dates:
    #     r_date.write("Rete2," + str(date) + "\n")
    # #
    # dates = timeit.repeat(setup=SETUP, stmt=TEST_3, repeat=10, number=1)
    # for date in dates:
    #     r_date.write("Rete3," + str(date) + "\n")
    # dates = timeit.repeat(setup=SETUP, stmt=TEST_4, repeat=100, number=1)
    # i = 1
    # for date in dates:
    #     r_date.write(str(i)+"," + str(date) + "\n")
    #     i = i+1


    i = 0
    while(i<10):
        tracemalloc.start()
        dir_filename = "test"

        filename_network = "/home/maria/PycharmProjects/Algoritmi/Input/network_rete1.json"
        filename_transition = "/home/maria/PycharmProjects/Algoritmi/Input/Rete1/input_transition.txt"
        f = open(filename_transition, "r")

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

        with open(filename_network, "r+") as json_file:
            data = json.load(json_file)
            data_str = json.dumps(data)

            network = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))

        print("1,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
        full_space = Class.Spaces.create_behavioral_spaces.create_behavioral_space(dir_filename + '_BS', network,
                                                                                   transitions, dir_filename)
        print("2,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
        full_space_r = Class.Spaces.create_behavioral_space_renominated.create_behavioral_space_renominated(
            dir_filename + '_RE', full_space, 0, dir_filename)
        print("3,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
        obs = ["o3", "o2"]
        obs_full_space = Class.Spaces.create_observable_space.create_behavioral_space_from_obs(dir_filename + '_OS', obs,
                                                                                               full_space_r, dir_filename)
        print("4,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
        obs_space_r = Class.Spaces.create_observable_space_Renominated.create_behavioral_space_observable_renominated(
            dir_filename + '_ROS', obs_full_space, dir_filename)
        print("5,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])
        Class.Spaces.execute_diagnosi_observation.create_diagnosis_for_space_observable_renominated(dir_filename,
                                                                                                    obs_space_r)
        print("6,", tracemalloc.get_traced_memory()[0],tracemalloc.get_traced_memory()[1])

        tracemalloc.stop()
        i = i+1


