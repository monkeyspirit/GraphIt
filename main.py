import copy
import json
import os
from doctest import master
from tkinter import ttk
from tkinter.tix import ScrolledWindow

from reportlab.lib.colors import white

from Class import network, comportamentalSpace, graphic, FSM
from Class.comportamentalSpace import Transition, Space
from Class.FSM import FiniteStateMachine
from Class.network import Network
from Class.FSM import Edge
import PySimpleGUI as sg
import webbrowser

def first():
    fsm = FiniteStateMachine("C2", ["20", "21"], "", [Edge("20", "t2a", "21"), Edge("21", "t2b", "20")])
    graphic.draw_FSM_graphic(fsm)

    # Save a fsm in a json file
    FSM.save_fsm_as_json(fsm)

    # Read a fsm from a json file and create the obj
    fsm_read = fsm = FiniteStateMachine("C3", ["20", "21"], "", [Edge("20", "t2a", "21"), Edge("21", "t2b", "20")])

    graphic.draw_FSM_graphic(fsm_read)

    transitions = comportamentalSpace.read_transitions_from_txt()

    fsms = [fsm, fsm_read]

    link = network.read_link_from_txt()
    n = Network(fsms, [link, network.Link("C2", "L3", "C3", "ϵ")], transitions)

    network.save_network_as_json(n)

    n1 = network_draw()

    full_space = behavioral_space(n1, transitions)

    full_space_r = behavioral_space_renominated(n1, full_space)

    obs = ["o3", "o2"]
    obs_full_space = observation(n1, full_space_r, obs)

    obs_space_r = observation_renominated(n1, obs_full_space, obs)

    diagnosis(n1, obs_space_r, obs)


def network_draw():
    n1 = network.read_network_from_json()
    graphic.draw_network_graphic(n1)
    return n1


def behavioral_space(n1, transitions):
    filename = 'full_space' + n1.fsms[0].name + n1.fsms[1].name
    full_space = graphic.create_behavioral_space(filename, n1, transitions)
    comportamentalSpace.save_space_as_json(full_space)
    return full_space


def behavioral_space_renominated(n1, full_space):
    filename = 'renominated_space' + n1.fsms[0].name + n1.fsms[1].name
    graphic.create_behavioral_space_renominated(filename, full_space)
    comportamentalSpace.save_space_as_json(full_space)
    return full_space


def observation(n1, cutted_space_for_obs, obs):
    filename = 'observable_space' + n1.fsms[0].name + n1.fsms[1].name + '_id_' + obs[0]
    obs_full_space = graphic.create_behavioral_space_from_obs(filename, obs, cutted_space_for_obs)
    comportamentalSpace.save_space_as_json(obs_full_space)
    return obs_full_space


def observation_renominated(n1, renominated_space_for_obs_and_cutting, obs):
    filename = 'renominated_space_obs' + n1.fsms[0].name
    graphic.create_behavioral_space_observable_renominated(filename, renominated_space_for_obs_and_cutting, obs)
    comportamentalSpace.save_space_as_json(renominated_space_for_obs_and_cutting)
    return renominated_space_for_obs_and_cutting


def diagnosis(n1, space_for_diagnosis, obs):
    filename = 'diagnosis_space_obs' + n1.fsms[0].name
    img = graphic.create_diagnosis_for_space_observable_renominated(filename, space_for_diagnosis, obs)
    comportamentalSpace.save_space_as_json(space_for_diagnosis)
    return img


def second():
    # Create a fsm from an input file (text)
    fsm_1 = FiniteStateMachine("C1", ["10", "11"], "",
                               [Edge("10", "t1a", "11"), Edge("11", "t1b", "10"), Edge("10", "t1c", "11")])
    graphic.draw_FSM_graphic(fsm_1)
    fsm = FiniteStateMachine("C2", ["20", "21"], "", [Edge("20", "t2a", "21"), Edge("21", "t2b", "20")])
    graphic.draw_FSM_graphic(fsm)

    # Save a fsm in a json file
    FSM.save_fsm_as_json(fsm)

    # Read a fsm from a json file and create the obj
    fsm_read = FSM.read_fsm_from_json()
    graphic.draw_FSM_graphic(fsm_read)

    transitions = [Transition("C1", "t1a", {"L1": "e1"}, {}, "ϵ", "ϵ"),
                   Transition("C1", "t1b", {"L3": "e2"}, {}, "ϵ", "ϵ"),
                   Transition("C1", "t1c", {}, {}, "f1", "ϵ"),
                   Transition("C2", "t2a", {}, {"L1": "e1", "L2": "e3"}, "ϵ", "o1"),
                   Transition("C2", "t2b", {}, {"L1": "e1"}, "ϵ", "o2"),
                   Transition("C3", "t3a", {}, {"L3": "e2"}, "ϵ", "ϵ"),
                   Transition("C3", "t3b", {"L2": "e3"}, {}, "ϵ", "ϵ"),
                   Transition("C3", "t3c", {"L2": "e3"}, {}, "f3", "ϵ")]

    fsms = [fsm_1, fsm, fsm_read]

    n1 = Network(fsms, [network.Link("C1", "L3", "C3", "ϵ"), network.Link("C3", "L1", "C1", "ϵ"),
                        network.Link("C2", "L2", "C3", "ϵ")])

    network.save_network_as_json(n1)

    graphic.draw_network_graphic(n1)

    filename = 'full_space' + n1.fsms[0].name + n1.fsms[1].name

    full_space = graphic.create_behavioral_space(filename, n1, transitions)

    comportamentalSpace.save_space_as_json(full_space)

    filename = 'renominated_space' + n1.fsms[0].name + n1.fsms[1].name
    graphic.create_behavioral_space_renominated(filename, full_space)

    # comportamental space relative to obs
    obs = ["o3", "o2"]
    filename = 'observable_space' + n1.fsms[0].name + n1.fsms[1].name + '_id_' + obs[0]
    obs_full_space = graphic.create_behavioral_space_from_obs(filename, obs, full_space)

    filename = 'renominated_space_obs' + n1.fsms[0].name
    graphic.create_behavioral_space_observable_renominated(filename, obs_full_space)


def third():
    fsm_1 = FiniteStateMachine("S", ["0", "1"], "", [Edge("0", "s1", "1"), Edge("1", "s2", "0"),
                                                     Edge("0", "s3", "0"), Edge("1", "s4", "1")])
    graphic.draw_FSM_graphic(fsm_1)
    fsm_2 = FiniteStateMachine("B", ["0", "1"], "", [Edge("0", "b1", "1"), Edge("1", "b2", "0"),
                                                     Edge("0", "b3", "0"), Edge("1", "b4", "1"),
                                                     Edge("0", "b5", "0"), Edge("1", "b6", "1"),
                                                     Edge("0", "b7", "1"), Edge("1", "b8", "0")])
    graphic.draw_FSM_graphic(fsm_2)

    transitions_2 = [Transition("S", "s1", {}, {"L": "op"}, "ϵ", "act"),
                     Transition("S", "s2", {}, {"L": "cl"}, "ϵ", "sby"),
                     Transition("S", "s3", {}, {"L": "cl"}, "f1", "ϵ"),
                     Transition("S", "s4", {}, {"L": "op"}, "f2", "ϵ"),
                     Transition("B", "b1", {"L": "op"}, {}, "ϵ", "opn"),
                     Transition("B", "b2", {"L": "cl"}, {}, "ϵ", "cls"),
                     Transition("B", "b3", {"L": "op"}, {}, "f3", "ϵ"),
                     Transition("B", "b4", {"L": "cl"}, {}, "f4", "ϵ"),
                     Transition("B", "b5", {"L": "cl"}, {}, "ϵ", "nop"),
                     Transition("B", "b6", {"L": "op"}, {}, "ϵ", "nop"),
                     Transition("B", "b7", {"L": "cl"}, {}, "f5", "opn"),
                     Transition("B", "b8", {"L": "op"}, {}, "f6", "cls")
                     ]

    fsms_2 = [fsm_1, fsm_2]

    n2 = Network(fsms_2, [network.Link("S", "L", "B", "ϵ")], transitions_2)
    network.save_network_as_json(n2)

    graphic.draw_network_graphic(n2)

    filename = 'full_space' + n2.fsms[0].name

    full_space = graphic.create_behavioral_space(filename, n2, transitions_2)

    comportamentalSpace.save_space_as_json(full_space)

    full_space_for_renomination = copy.deepcopy(full_space)

    filename = 'rinominated_space' + n2.fsms[0].name
    graphic.create_behavioral_space_renominated(filename, full_space_for_renomination)

    cutted_space_for_obs = copy.deepcopy(full_space_for_renomination)
    # comportamental space relative to obs
    obs = ["act", "sby", "nop"]
    filename = 'observable_space' + n2.fsms[0].name + '_' + obs[0]
    obs_full_space = graphic.create_behavioral_space_from_obs(filename, obs, cutted_space_for_obs)

    renominated_space_for_obs_and_cutting = copy.deepcopy(obs_full_space)
    filename = 'renominated_space_obs' + n2.fsms[0].name
    graphic.create_behavioral_space_observable_renominated(filename, renominated_space_for_obs_and_cutting, obs)

    space_for_diagnosis = copy.deepcopy(renominated_space_for_obs_and_cutting)
    filename = 'diagnosis_space_obs' + n2.fsms[0].name
    graphic.create_diagnosis_for_space_observable_renominated(filename, space_for_diagnosis, obs)


import tkinter as tk

if __name__ == '__main__':

    def create_network_window():
        global fsms

        fsms = []

        def load_fsm():
            try:
                f1 = FSM.read_fsm_from_txt()
                fsms.append(f1)
                graphic.draw_FSM_graphic(f1)
                names = ""
                for fsm in fsms:
                    names = names + fsm.name + ", "
                names = names[:-2]
                fsm_label['text'] = names
                show_fsm_btn['state'] = tk.NORMAL
                load_link_btn['state'] = tk.NORMAL
                remove_fsm_btn['state'] = tk.NORMAL
                load_fsm_btn['text'] = "Carica un altro automa"
            except IndexError:
                sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            except TypeError:
                pass

        def remove_fsm():
            fsms.clear()
            load_fsm_btn['text'] = "Carica un automa"
            fsm_label['text'] = ""
            remove_fsm_btn['state'] = tk.DISABLED
            create_net_btn['state'] = tk.DISABLED
            load_link_btn['state'] = tk.DISABLED
            load_transitions_btn['state'] = tk.DISABLED
            show_net_btn['state'] = tk.DISABLED
            behavioral_space_btn['state'] = tk.DISABLED
            behavioral_space_ren_btn['state'] = tk.DISABLED
            behavioral_space_obs_btn['state'] = tk.DISABLED
            behavioral_space_obs_ren_btn['state'] = tk.DISABLED
            diagnosi_btn['state'] = tk.DISABLED
            transitions_lbl['text'] = ""
            show_fsm_btn['state'] = tk.DISABLED
            link_lbl['text'] = ""
            load_transitions_btn['text'] = "Carica il file delle transizioni"
            load_link_btn['text'] = "Carica il file dei link"


        def show_fsm_graph():
            figure_fsm = tk.Toplevel(create)
            figure_fsm.geometry("500x300")
            figure_fsm.title("Diagrammi automi a stati finiti")
            frame = tk.Frame(figure_fsm, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)
            photo_step = [0] * (len(fsms))
            for i in range(int(len(fsms))):
                photo_step[i] = tk.PhotoImage(file='FSM_graph/fsm' + fsms[i].name + '.png')
                canvas.create_image((i) * 300, 30, image=photo_step[i], anchor="nw")
                canvas.create_text((i) * 300, 0, font="bold", text=fsms[i].name)

            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)

            frame.pack()

            figure_fsm.mainloop()

        def load_transitions():

            global transitions
            try:
                transitions = comportamentalSpace.read_transitions_from_txt()
                print_T = "Label - input - output - o label - r label \n"
                print_T = print_T + "------------------------------------- \n"
                for transition in transitions:
                    print_T = print_T + str(transition.label) + " " + str(transition.input) + " " + str(
                        transition.output) + "  " + str(
                        transition.observability_label) + " " + str(
                        transition.relevance_label) + "\n"

                transitions_lbl['text'] = print_T
                create_net_btn['state'] = tk.NORMAL
                load_transitions_btn['text'] = "Carica un altro file di transizioni"
            except IndexError:
                sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            except FileNotFoundError:
                pass

        def load_links():

            global links
            try:
                links = network.read_link_from_txt()
                text = ""
                for l in links:
                    text = text + str(l.name) + " " + str(l.source) + " " + str(l.destination) + " " + str(l.state) + "\n"

                link_lbl['text'] = text
                load_transitions_btn['state'] = tk.NORMAL
                load_link_btn['text'] = "Carica un altro file di link"
            except IndexError:
                sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            except FileNotFoundError:
                pass

        def create_net():
            global n1
            try:
                n1 = Network(fsms, links, transitions)
                graphic.draw_network_graphic(n1)
                network.save_network_as_json(n1)
                show_net_btn['state'] = tk.NORMAL
                behavioral_space_btn['state'] = tk.NORMAL
            except IndexError:
                sg.Popup('Attenzione!', 'Controlla di aver inserito tutti gli automi previsti dai link e dalle transizioni inserite!')



        def show_net_graph():
            figure_net = tk.Toplevel(create)
            figure_net.geometry("500x300")
            figure_net.title("Diagrammi della rete")
            frame = tk.Frame(figure_net, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)

            photo_step = tk.PhotoImage(file='Network_graph/network' + n1.fsms[0].name + n1.fsms[1].name + '.png')
            canvas.create_image(0, 30, image=photo_step, anchor="nw")
            canvas.create_text(0, 0, font="bold", text=n1.fsms[0].name + n1.fsms[1].name)

            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)

            frame.pack()

            figure_net.mainloop()

        create = tk.Toplevel(root)
        name_fsm_images = [2, 1]
        load_fsm_btn = tk.Button(create, text="Carica un automa", command=load_fsm)
        load_fsm_btn.grid(row=2, pady=10, padx=10, column=1, columnspan=2)

        fsm_label = tk.Label(create, text="")
        fsm_label.grid(row=4, column=1)

        remove_fsm_btn = tk.Button(create, text="Elimina i diagrammi", command=remove_fsm, state=tk.DISABLED)
        remove_fsm_btn.grid(row=3, pady=10, padx=10, column=1, columnspan=2)

        show_fsm_btn = tk.Button(create, text="Mostra i diagrammi degli automi", command=show_fsm_graph,
                                 state=tk.DISABLED)
        show_fsm_btn.grid(row=5, pady=10, padx=10, column=1, columnspan=2)

        load_link_btn = tk.Button(create, text="Carica il file dei link", command=load_links, state=tk.DISABLED)
        load_link_btn.grid(row=2, pady=10, padx=10, column=3, columnspan=2)
        link_lbl = tk.Label(create, text="")
        link_lbl.grid(row=3, column=4)

        load_transitions_btn = tk.Button(create, text="Carica il file delle transizioni", command=load_transitions,
                                         state=tk.DISABLED)
        load_transitions_btn.grid(row=2, column=5, columnspan=2)

        transitions_lbl = tk.Label(create, text="")
        transitions_lbl.grid(row=3, column=5)

        create_net_btn = tk.Button(create, text="Crea la rete", state=tk.DISABLED, command=create_net)
        create_net_btn.grid(row=7, pady=10, padx=10, column=1, columnspan=2)

        show_net_btn = tk.Button(create, text="Mostra il diagramma della rete", state=tk.DISABLED,
                                 command=show_net_graph)
        show_net_btn.grid(row=7, pady=10, padx=10, column=3, columnspan=2)

        def calculate_behavioral_space():
            global full_space

            filename = 'full_space' + n1.fsms[0].name + n1.fsms[1].name
            full_space = behavioral_space(n1, transitions)
            tk.Label(create, text="Fatto! Salvato in Behavioral_Space/" + filename, fg='green').grid(row=8, column=3)
            behavioral_space_ren_btn['state'] = tk.NORMAL

            figure1 = tk.Toplevel(create)
            figure1.geometry("720x720")
            figure1.title("Spazio comportamentale")
            frame = tk.Frame(figure1, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)

            photo1 = tk.PhotoImage(file='Behavioral_Space/' + filename + '.gv.png')
            photo2 = tk.PhotoImage(file='Behavioral_Space/' + filename + '_id.gv.png')
            photo1_small = photo1.subsample(2, 2)
            canvas.create_text(100, 10, font="bold",
                               text="Spazio con LABEL")
            canvas.create_image(0, 50, image=photo1_small, anchor="nw")
            canvas.create_text(500, 10, font="bold",
                               text="Spazio con ID")
            canvas.create_image(400, 50, image=photo2, anchor="nw")
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)

            frame.pack()

            figure1.mainloop()

        def calculate_behavioral_space_renominated():
            global full_space_r
            filename = 'renominated_space' + n1.fsms[0].name + n1.fsms[1].name
            full_space_r = behavioral_space_renominated(n1, full_space)
            tk.Label(create, text="Fatto! Salvato in Behavioral_Space_Renominated/" + filename, fg='green').grid(row=9,
                                                                                                                 column=3)
            behavioral_space_obs_btn['state'] = tk.NORMAL

            figure2 = tk.Toplevel(create)
            figure2.geometry("720x720")
            figure2.title("Spazio comportamentale rinominato")
            frame = tk.Frame(figure2, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)

            photo1 = tk.PhotoImage(file='Behavioral_Space_Renominated/' + filename + '.gv.png')
            photo2 = tk.PhotoImage(file='Behavioral_Space_Renominated/' + filename + '_id.gv.png')

            canvas.create_text(100, 10, font="bold",
                               text="Spazio con ID vecchi")
            canvas.create_image(0, 100, image=photo2, anchor="nw")
            canvas.create_text(500, 10, font="bold",
                               text="Spazio con ID rinominati")
            canvas.create_image(400, 100, image=photo1, anchor="nw")
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)
            canvas.create_text(350, 50, font="bold",
                               text="File di ridenominazione:\nBehavioral_Space_Renominated\n/renomination_list_" + filename + ".txt")

            frame.pack()

            figure2.mainloop()

        def calculate_obs_space():
            global obs
            global obs_full_space
            # obs = ["o3", "o2"]
            obs = ["act", "sby", "nop"]
            filename = 'observable_space' + n1.fsms[0].name + n1.fsms[1].name + '_id_' + obs[0]
            obs_full_space = observation(n1, full_space_r, obs)
            tk.Label(create, text="Fatto!  Salvato in Behavioral_Space_Observable/" + filename, fg='green').grid(row=10,
                                                                                                                 column=3)
            behavioral_space_obs_ren_btn['state'] = tk.NORMAL

            figure3 = tk.Toplevel(load)
            figure3.geometry("720x720")
            figure3.title("Spazio comportamentale data l'osservazione")
            frame = tk.Frame(figure3, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)

            photo1 = tk.PhotoImage(file='Behavioral_Space_Observable/' + filename + '.gv.png')
            canvas.create_image(0, 50, image=photo1, anchor="nw")
            obs_name = ""
            for o in obs:
                obs_name = obs_name + o + " "
            canvas.create_text(500, 300, font="bold",
                               text="L'osservazione considerata è:\n" + obs_name)
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)

            frame.pack()

            figure3.mainloop()

        def calculate_obs_space_renominated():
            global obs_space_r
            filename = 'renominated_space_obs' + n1.fsms[0].name
            obs_space_r = observation_renominated(n1, obs_full_space, obs)
            tk.Label(create, text="Fatto! Salvato in Behavioral_Space_Observable_Renominated/" + filename,
                     fg='green').grid(row=11, column=3)
            diagnosi_btn['state'] = tk.NORMAL

            figure4 = tk.Toplevel(load)
            figure4.geometry("720x720")
            figure4.title("Spazio comportamentale data l'osservazione")
            frame = tk.Frame(figure4, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)

            photo1 = tk.PhotoImage(file='Behavioral_Space_Observable_Renominated/' + filename + '.gv.png')
            canvas.create_image(0, 50, image=photo1, anchor="nw")
            obs_name = ""
            for o in obs:
                obs_name = obs_name + o + " "
            canvas.create_text(500, 300, font="bold",
                               text="L'osservazione considerata è:\n" + obs_name)
            canvas.create_text(500, 400, font="bold",
                               text="File di ridenominazione:\nBehavioral_Space_Observable_Renominated\n/renomination_list_" + filename + ".txt")
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)

            frame.pack()

            figure4.mainloop()

        def calculate_diagnosi_space():
            tk.Label(create, text="Fatto! Salvati i passaggi in Diagnosi_steps/", fg='green').grid(row=12, column=3)
            n_img, exp = diagnosis(n1, obs_space_r, obs)

            figure5 = tk.Toplevel(create)
            figure5.geometry("1420x720")
            figure5.title("Passaggi individuazione espressione regolare")
            frame = tk.Frame(figure5, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.BOTH, expand=True)

            xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

            yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

            canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                               yscrollcommand=yscrollbar.set)
            canvas.pack(fill="both", expand=True)
            photo_step = [0] * (n_img + 2)
            for i in range(int(n_img) + 1):
                photo_step[i] = tk.PhotoImage(file='Diagnosi_steps/' + str(i + 1) + '.gv.png')
                canvas.create_image((i) * 300, 0, image=photo_step[i], anchor="nw")

            canvas.create_text(300 * (n_img) + 50, 300, font="bold",
                               text="Espressione regolare:\n" + exp)
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            xscrollbar.config(command=canvas.xview)
            yscrollbar.config(command=canvas.yview)

            frame.pack()

            figure5.mainloop()

        behavioral_space_btn = tk.Button(create, text="Calcola lo spazio comportamentale",
                                         command=calculate_behavioral_space, state=tk.DISABLED)
        behavioral_space_btn.grid(row=8, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
        behavioral_space_ren_btn = tk.Button(create, text="Rinomina lo spazio comportamentale", state=tk.DISABLED,
                                             command=calculate_behavioral_space_renominated)
        behavioral_space_ren_btn.grid(row=9, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
        behavioral_space_obs_btn = tk.Button(create, text="Calcola lo spazio comportamentale data un'osservazione",
                                             state=tk.DISABLED, command=calculate_obs_space)
        behavioral_space_obs_btn.grid(row=10, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
        behavioral_space_obs_ren_btn = tk.Button(create, text="Rinomina lo spazio comportamentale data un'osservazione",
                                                 state=tk.DISABLED, command=calculate_obs_space_renominated)
        behavioral_space_obs_ren_btn.grid(row=11, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
        diagnosi_btn = tk.Button(create, text="Diagnosi data un'osservazione", command=calculate_diagnosi_space,
                                 state=tk.DISABLED)
        diagnosi_btn.grid(row=12, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))

        create.mainloop()

    def load_network_window():
        load_n = tk.Toplevel(root)
        load_n.title("Caricamento ...")
        load_n.geometry("1100x700")

        try:
            n1 = network_draw()
            for fsm in n1.fsms:
                graphic.draw_FSM_graphic(fsm)
            filename = 'full_space' + n1.fsms[0].name + n1.fsms[1].name
            load_n.title(filename)

            def show_fsm_graph():
                global name_fsm_images
                figure_fsm = tk.Toplevel(load_n)
                figure_fsm.geometry("720x720")
                figure_fsm.title("Diagrammi degli automi")

                name_fsm_images = []

                for fsm in n1.fsms:
                    name_fsm_images.append(fsm.name)

                frame = tk.Frame(figure_fsm, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True)

                xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

                yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                                   yscrollcommand=yscrollbar.set)
                canvas.pack(fill="both", expand=True)

                photo_fsm = [0] * len(name_fsm_images)

                for i in range(len(name_fsm_images)):
                    photo_fsm[i] = tk.PhotoImage(file='FSM_graph/fsm' + name_fsm_images[i] + '.png')
                    canvas.create_text(200 * i, 10, font="bold", text=name_fsm_images[i])
                    canvas.create_image(0 + 200 * i, 50, image=photo_fsm[i], anchor="nw")

                canvas.config(scrollregion=canvas.bbox(tk.ALL))
                xscrollbar.config(command=canvas.xview)
                yscrollbar.config(command=canvas.yview)

                frame.pack()
                figure_fsm.mainloop()

            names = ""
            for fsm in n1.fsms:
                names = names + str(fsm.name)

            show_fsm_graph_btn = tk.Button(load_n, text="Mostra i grafi degli automi",
                                           command=show_fsm_graph)
            show_fsm_graph_btn.grid(row=3, column=1, columnspan=2)
            tk.Label(load_n, text='Diagramma della rete').grid(row=4, column=1, columnspan=2)
            image_net = tk.PhotoImage(file="Network_graph/network" + names + ".png")
            tk.Label(load_n, image=image_net).grid(row=5, column=1, columnspan=2)

            def load_transitions():
                try:
                    global transitions
                    transitions = comportamentalSpace.read_transitions_from_txt()
                    print_T = "Label - input - output - o label - r label \n"
                    print_T = print_T + "------------------------------------- \n"
                    for transition in transitions:
                        print_T = print_T + str(transition.label) + " " + str(transition.input) + " " + str(
                            transition.output) + "  " + str(
                            transition.observability_label) + " " + str(
                            transition.relevance_label) + "\n"

                    tk.Label(load_n, text=print_T).grid(row=5, column=3)

                    behavioral_space_btn['state'] = tk.NORMAL
                except IndexError:
                    sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
                except FileNotFoundError:
                    pass

            load_transitions_btn = tk.Button(load_n, text="Carica le transizioni",
                                             command=load_transitions)
            load_transitions_btn.grid(row=4, column=3, columnspan=3)

            def calculate_behavioral_space():
                global full_space

                filename = 'full_space' + n1.fsms[0].name + n1.fsms[1].name
                full_space = behavioral_space(n1, transitions)
                tk.Label(load_n, text="Fatto! Salvato in Behavioral_Space/" + filename, fg='green').grid(row=6, column=3)
                behavioral_space_ren_btn['state'] = tk.NORMAL

                figure1 = tk.Toplevel(load_n)
                figure1.geometry("720x720")
                figure1.title("Spazio comportamentale")
                frame = tk.Frame(figure1, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True)

                xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

                yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                                   yscrollcommand=yscrollbar.set)
                canvas.pack(fill="both", expand=True)

                photo1 = tk.PhotoImage(file='Behavioral_Space/' + filename + '.gv.png')
                photo2 = tk.PhotoImage(file='Behavioral_Space/' + filename + '_id.gv.png')
                photo1_small = photo1.subsample(2, 2)
                canvas.create_text(100, 10, font="bold",
                                   text="Spazio con LABEL")
                canvas.create_image(0, 50, image=photo1_small, anchor="nw")
                canvas.create_text(500, 10, font="bold",
                                   text="Spazio con ID")
                canvas.create_image(400, 50, image=photo2, anchor="nw")
                canvas.config(scrollregion=canvas.bbox(tk.ALL))
                xscrollbar.config(command=canvas.xview)
                yscrollbar.config(command=canvas.yview)

                frame.pack()

                figure1.mainloop()

            def calculate_behavioral_space_renominated():
                global full_space_r
                filename = 'renominated_space' + n1.fsms[0].name + n1.fsms[1].name
                full_space_r = behavioral_space_renominated(n1, full_space)
                tk.Label(load_n, text="Fatto! Salvato in Behavioral_Space_Renominated/" + filename, fg='green').grid(row=7,
                                                                                                                     column=3)
                behavioral_space_obs_btn['state'] = tk.NORMAL

                figure2 = tk.Toplevel(load_n)
                figure2.geometry("720x720")
                figure2.title("Spazio comportamentale rinominato")
                frame = tk.Frame(figure2, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True)

                xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

                yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                                   yscrollcommand=yscrollbar.set)
                canvas.pack(fill="both", expand=True)

                photo1 = tk.PhotoImage(file='Behavioral_Space_Renominated/' + filename + '.gv.png')
                photo2 = tk.PhotoImage(file='Behavioral_Space_Renominated/' + filename + '_id.gv.png')

                canvas.create_text(100, 10, font="bold",
                                   text="Spazio con ID vecchi")
                canvas.create_image(0, 100, image=photo2, anchor="nw")
                canvas.create_text(500, 10, font="bold",
                                   text="Spazio con ID rinominati")
                canvas.create_image(400, 100, image=photo1, anchor="nw")
                canvas.config(scrollregion=canvas.bbox(tk.ALL))
                xscrollbar.config(command=canvas.xview)
                yscrollbar.config(command=canvas.yview)
                canvas.create_text(350, 50, font="bold",
                                   text="File di ridenominazione:\nBehavioral_Space_Renominated\n/renomination_list_" + filename + ".txt")

                frame.pack()

                figure2.mainloop()

            def calculate_obs_space():
                global obs
                global obs_full_space
                obs = ["o3", "o2"]
                filename = 'observable_space' + n1.fsms[0].name + n1.fsms[1].name + '_id_' + obs[0]
                obs_full_space = observation(n1, full_space_r, obs)
                tk.Label(load_n, text="Fatto!  Salvato in Behavioral_Space_Observable/" + filename, fg='green').grid(row=8,
                                                                                                                     column=3)
                behavioral_space_obs_ren_btn['state'] = tk.NORMAL

                figure3 = tk.Toplevel(load_n)
                figure3.geometry("720x720")
                figure3.title("Spazio comportamentale data l'osservazione")
                frame = tk.Frame(figure3, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True)

                xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

                yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                                   yscrollcommand=yscrollbar.set)
                canvas.pack(fill="both", expand=True)

                photo1 = tk.PhotoImage(file='Behavioral_Space_Observable/' + filename + '.gv.png')
                canvas.create_image(0, 50, image=photo1, anchor="nw")
                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "
                canvas.create_text(500, 300, font="bold",
                                   text="L'osservazione considerata è:\n" + obs_name)
                canvas.config(scrollregion=canvas.bbox(tk.ALL))
                xscrollbar.config(command=canvas.xview)
                yscrollbar.config(command=canvas.yview)

                frame.pack()

                figure3.mainloop()

            def calculate_obs_space_renominated():
                global obs_space_r
                filename = 'renominated_space_obs' + n1.fsms[0].name
                obs_space_r = observation_renominated(n1, obs_full_space, obs)
                tk.Label(load_n, text="Fatto! Salvato in Behavioral_Space_Observable_Renominated/" + filename,
                         fg='green').grid(row=9, column=3)
                diagnosi_btn['state'] = tk.NORMAL

                figure4 = tk.Toplevel(load_n)
                figure4.geometry("720x720")
                figure4.title("Spazio comportamentale data l'osservazione")
                frame = tk.Frame(figure4, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True)

                xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

                yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                                   yscrollcommand=yscrollbar.set)
                canvas.pack(fill="both", expand=True)

                photo1 = tk.PhotoImage(file='Behavioral_Space_Observable_Renominated/' + filename + '.gv.png')
                canvas.create_image(0, 50, image=photo1, anchor="nw")
                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "
                canvas.create_text(500, 300, font="bold",
                                   text="L'osservazione considerata è:\n" + obs_name)
                canvas.create_text(500, 400, font="bold",
                                   text="File di ridenominazione:\nBehavioral_Space_Observable_Renominated\n/renomination_list_" + filename + ".txt")
                canvas.config(scrollregion=canvas.bbox(tk.ALL))
                xscrollbar.config(command=canvas.xview)
                yscrollbar.config(command=canvas.yview)

                frame.pack()

                figure4.mainloop()

            def calculate_diagnosi_space():
                tk.Label(load_n, text="Fatto! Salvati i passaggi in Diagnosi_steps/", fg='green').grid(row=10, column=3)
                n_img, exp = diagnosis(n1, obs_space_r, obs)

                figure5 = tk.Toplevel(load_n)
                figure5.geometry("1420x720")
                figure5.title("Passaggi individuazione espressione regolare")
                frame = tk.Frame(figure5, bd=2, relief=tk.SUNKEN)
                frame.pack(fill=tk.BOTH, expand=True)

                xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

                yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                canvas = tk.Canvas(frame, bd=0, width=700, height=700, xscrollcommand=xscrollbar.set,
                                   yscrollcommand=yscrollbar.set)
                canvas.pack(fill="both", expand=True)
                photo_step = [0] * (n_img + 2)
                for i in range(int(n_img) + 1):
                    photo_step[i] = tk.PhotoImage(file='Diagnosi_steps/' + str(i + 1) + '.gv.png')
                    canvas.create_image((i) * 300, 0, image=photo_step[i], anchor="nw")

                canvas.create_text(300 * (n_img) + 50, 300, font="bold",
                                   text="Espressione regolare:\n" + exp)
                canvas.config(scrollregion=canvas.bbox(tk.ALL))
                xscrollbar.config(command=canvas.xview)
                yscrollbar.config(command=canvas.yview)

                frame.pack()

                figure5.mainloop()

            behavioral_space_btn = tk.Button(load_n, text="Calcola lo spazio comportamentale",
                                             command=calculate_behavioral_space, state=tk.DISABLED)
            behavioral_space_btn.grid(row=6, pady=10, padx=10, column=1, columnspan=len(n1.fsms))
            behavioral_space_ren_btn = tk.Button(load_n, text="Rinomina lo spazio comportamentale", state=tk.DISABLED,
                                                 command=calculate_behavioral_space_renominated)
            behavioral_space_ren_btn.grid(row=7, pady=10, padx=10, column=1, columnspan=len(n1.fsms))
            behavioral_space_obs_btn = tk.Button(load_n, text="Calcola lo spazio comportamentale data un'osservazione",
                                                 state=tk.DISABLED, command=calculate_obs_space)
            behavioral_space_obs_btn.grid(row=8, pady=10, padx=10, column=1, columnspan=len(n1.fsms))
            behavioral_space_obs_ren_btn = tk.Button(load_n, text="Rinomina lo spazio comportamentale data un'osservazione",
                                                     state=tk.DISABLED, command=calculate_obs_space_renominated)
            behavioral_space_obs_ren_btn.grid(row=9, pady=10, padx=10, column=1, columnspan=len(n1.fsms))
            diagnosi_btn = tk.Button(load_n, text="Diagnosi data un'osservazione", command=calculate_diagnosi_space,
                                     state=tk.DISABLED)
            diagnosi_btn.grid(row=10, pady=10, padx=10, column=1, columnspan=len(n1.fsms))

            load_n.mainloop()
        except FileNotFoundError:
            load_n.destroy()
        except Exception:
            sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            load_n.destroy()


    def help():
        webbrowser.open("Help/html/index_home.html")


    root = tk.Tk()
    root.title("Benvenuto")
    root.geometry("450x400")
    tk.Label(root, text="Benvenuto nel programma per la creazione \ne la visualizzazione di reti di automi finiti."
                        "\n\nIn questo programma è possibile caricare degli automi"
                        "\n a stati finiti già esistenti, associati al file dei link"
                        "\n e delle transizioni, oppure caricare direttamente una "
                        "\nrete di automi a stati finiti e il file relativo alle transizioni.\n"
                        "\nIl pulsante 'Crea una rete' permette di creare una rete"
                        "\n caricando i file .TXT degli automi a stati finiti, dei link e delle \n"
                        "transizioni. Cliccando sul pulsante 'Help' è possibile visionare la \n"
                        "documentazione (caldamente consigliato farlo per capire\n come funziona il programma).").pack()



    create = tk.Button(root, text="Crea una rete", command=create_network_window)
    load = tk.Button(root, text="Carica una rete", command=load_network_window)
    create.pack(side=tk.LEFT, expand=True)
    load.pack(side=tk.RIGHT, expand=True)

    help = tk.Button(root, text="Help", command=help)



    help.pack()

    root.mainloop()

    # f1 = FSM.read_fsm_from_txt()
    # graphic.draw_FSM_graphic(f1)
    # first()
    # second()
    # third()
