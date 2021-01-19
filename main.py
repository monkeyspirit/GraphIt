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
                create_window['output_fsms'].update(names)
                create_window['show_fsms'].update(disabled=False)
                create_window['delete_fsms'].update(disabled=False)
                create_window['load_link'].update(disabled=False)
            except IndexError:
                sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            except TypeError:
                pass

        def remove_fsm():
            fsms.clear()
            create_window['output_fsms'].update("")
            create_window['output_link'].update("")
            create_window['output_transitions'].update("")

            create_window['delete_fsms'].update(disabled=True)

            create_window['load_link'].update(disabled=True)
            create_window['load_transitions'].update(disabled=True)

            create_window['show_fsms'].update(disabled=True)
            create_window['create_network'].update(disabled=True)

        def show_fsm_graph():

            images = []
            text = []
            for i in range(int(len(fsms))):
                images.append(sg.Image(filename='FSM_graph/fsm' + fsms[i].name + '.png'))
                text.append(sg.Text(fsms[i].name), )

            # Define the window's contents
            show_fsms = [
                images,
                text,
                [
                    sg.Button('Esci')
                ]
            ]

            show_fsms_layout = [
                [
                    sg.Column(show_fsms)
                ]
            ]
            # Create the window
            show_fsms_window = sg.Window('Diagrammi automi a stati finiti', show_fsms_layout)

            # Display and interact with the Window using an Event Loop
            while True:
                event, values = show_fsms_window.read()
                # See if user wants to quit or window was closed
                if event == sg.WINDOW_CLOSED or event == 'Esci':
                    break
            # Finish up by removing from the screen
            show_fsms_window.close()

        def load_links():

            global links
            try:
                links = network.read_link_from_txt()
                text = ""
                for l in links:
                    text = text + str(l.name) + " " + str(l.source) + " " + str(l.destination) + " " + str(
                        l.state) + "\n"

                create_window['output_link'].update(text)
                create_window['load_transitions'].update(disabled=False)
            except IndexError:
                sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            except FileNotFoundError:
                pass

        def load_transitions():

            global transitions
            try:
                transitions = comportamentalSpace.read_transitions_from_txt()
                print_T = ""
                for transition in transitions:
                    print_T = print_T + str(transition.label) + ", " + str(transition.input) + ", " + str(
                        transition.output) + ",  " + str(
                        transition.observability_label) + ", " + str(
                        transition.relevance_label) + "\n"

                create_window['output_transitions'].update(print_T)
                create_window['create_network'].update(disabled=False)
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

                operations_on_network()
                # show_net_btn['state'] = tk.NORMAL
                # behavioral_space_btn['state'] = tk.NORMAL
            except IndexError:
                sg.Popup('Attenzione!',
                         'Controlla di aver inserito tutti gli automi previsti dai link e dalle transizioni inserite!')

        def operations_on_network():

            def calculate_behavioral_space():
                global full_space, filename_be

                filename_be = 'full_space' + n1.fsms[0].name + n1.fsms[1].name
                full_space = behavioral_space(n1, transitions)

                network_window['output_network_op'].update(values['output_network_op'] + '> Fatto! Salvato in '
                                                                                         'Behavioral_Space/' + filename_be)
                network_window['ren_be'].update(disabled=False)
                network_window['be_diag'].update(disabled=False)

            def show_behavioral_space():
                column1 = [[sg.Text('Spazio con LABEL')], [sg.Image(filename='Behavioral_Space/' + filename_be + '.gv.png')]]
                column2 =[[sg.Text('Spazio con ID')], [sg.Image(filename='Behavioral_Space/' + filename_be + '_id.gv.png')]]
                behavioral_layout = [
                    [
                        sg.Column(column1, size=(600, 800), scrollable=True),
                        sg.Column(column2, size=(600, 800), scrollable=True)
                    ]
                ]
                behavioral_window = sg.Window('Diagramma spazio comportamentale', behavioral_layout, resizable=True)
                while True:
                    event, values = behavioral_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break

            def calculate_behavioral_space_renominated():
                global full_space_r, filename_re_be

                filename_re_be = 'renominated_space' + n1.fsms[0].name + n1.fsms[1].name
                full_space_r = behavioral_space_renominated(n1, full_space)
                network_window['output_network_op'].update(values['output_network_op'] + '> Fatto! Salvato in '
                                                                                         'Behavioral_Space_Renominated/'
                                                           + filename_re_be)

                network_window['calc_obs'].update(disabled=False)
                network_window['be_re_diag'].update(disabled=False)

            def show_re_be_space():
                column_re1 = [[sg.Text('Spazio con ID vecchi')], [sg.Image(filename='Behavioral_Space_Renominated/' + filename_re_be + '.gv.png')]]
                column_re2 = [[sg.Text('Spazio con ID rinominati')], [sg.Image(filename='Behavioral_Space_Renominated/' + filename_re_be + '_id.gv.png')]]

                re_behavioral_layout = [

                    [
                        sg.Text(
                            "File di ridenominazione:\nBehavioral_Space_Renominated\n/renomination_list_" + filename_re_be + ".txt")
                    ],
                    [
                        sg.Column(column_re1, size=(600, 800), scrollable=True),
                        sg.Column(column_re2, size=(600, 800), scrollable=True)
                    ]
                ]
                re_behavioral_window = sg.Window('Diagramma spazio comportamentale rinominato', re_behavioral_layout, resizable=True)
                while True:
                    event, values = re_behavioral_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break

            def calculate_obs_space():
                global obs, obs_full_space, filename_obs
                obs = ["o3", "o2"]
                # obs = ["act", "sby", "nop"]
                filename_obs = 'observable_space' + n1.fsms[0].name + n1.fsms[1].name + '_id_' + obs[0]
                obs_full_space = observation(n1, full_space_r, obs)
                network_window['output_network_op'].update(values['output_network_op'] + '> Fatto! Salvato in Behavioral_Space_Observable/' + filename_obs)

                network_window['ren_obs'].update(disabled=False)
                network_window['obs_diag'].update(disabled=False)

            def show_obs_space():
                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "

                column_ob1 = [[sg.Image(filename='Behavioral_Space_Observable/' + filename_obs + '.gv.png')]]
                obs_layout = [

                    [
                        sg.Text("L'osservazione considerata è:\n" + obs_name)
                    ],
                    [
                        sg.Column(column_ob1, size=(600, 800), scrollable=True)
                    ]
                ]
                obs_window = sg.Window('Diagramma spazio comportamentale data un\'osservazione', obs_layout)
                while True:
                    event, values = obs_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break

            def calculate_obs_space_renominated():
                global obs_space_r, filename_re_obs
                filename_re_obs = 'renominated_space_obs' + n1.fsms[0].name
                obs_space_r = observation_renominated(n1, obs_full_space, obs)

                network_window['output_network_op'].update(values['output_network_op'] + '> Fatto! Salvato in Behavioral_Space_Observable_Renominated/'+ filename_re_obs)

                network_window['diag'].update(disabled=False)
                network_window['obs_re_diag'].update(disabled=False)


            def show_re_obs_space():
                column_re_ob1 = [[sg.Image(filename='Behavioral_Space_Observable_Renominated/' + filename_re_obs + '.gv.png')]]

                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "

                re_obs_layout = [
                    [
                        sg.Text("L'osservazione considerata è:\n" + obs_name)
                    ],
                    [
                        sg.Text("File di ridenominazione:\nBehavioral_Space_Observable_Renominated\n/renomination_list_" + filename_re_obs + ".txt")
                    ],
                    [
                        sg.Column(column_re_ob1, size=(600, 800), scrollable=True)
                    ]
                ]
                re_obs_window = sg.Window('Diagramma spazio comportamentale rinominato data l\'osservazione', re_obs_layout)
                while True:
                    event, values = re_obs_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break

            def calculate_diagnosi_space():
                global n_img, exp
                network_window['output_network_op'].update(values['output_network_op'] + '> Fatto! Salvato in '
                                                                                         'Diagnosi_steps/')

                n_img, exp = diagnosis(n1, obs_space_r, obs)
                network_window['diag_diag'].update(disabled=False)

            def show_diagnosi():
                images_diagnosis = []
                for i in range(int(n_img) + 1):
                    images_diagnosis.append(sg.Image(filename='Diagnosi_steps/' + str(i + 1) + '.gv.png'))

                diagnosi_layout = [
                    [
                        sg.Column([images_diagnosis], scrollable=True)
                    ],
                    [
                        sg.Text("Espressione regolare:\n" + exp)
                    ]

                ]
                diagnosi_window = sg.Window('Passaggi individuazione espressione regolare', diagnosi_layout)
                while True:
                    event, values = diagnosi_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break

            network_buttons = [
                [
                    sg.Button('Calcola lo spazio comportamentale', key='calc_be')
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale', key='ren_be', disabled=True)
                ],
                [
                    sg.Button('Calcola lo spazio comportamentale data un\'osservazione', key='calc_obs', disabled=True)
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale con l\'osservazione data', key='ren_obs',
                              disabled=True)
                ],
                [
                    sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True)
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Esci')
                ]
            ]
            see_buttons = [
                [
                    sg.Button('Vedi', key='be_diag', disabled=True)
                ],
                [
                    sg.Button('Vedi', key='be_re_diag', disabled=True)
                ],
                [
                    sg.Button('Vedi', key='obs_diag', disabled=True)
                ],
                [
                    sg.Button('Vedi', key='obs_re_diag', disabled=True)
                ],
                [
                    sg.Button('Vedi', key='diag_diag', disabled=True)
                ],
                [
                    sg.HSeparator()
                ],
                [

                ]
            ]

            network_diagram_plot = [
                [
                    sg.Text('Diagramma della rete')
                ],
                [
                    sg.Image(filename='Network_graph/network' + n1.fsms[0].name + n1.fsms[1].name + '.png')
                ]
            ]

            network_plot = [
                [
                    sg.Multiline("", size=(30, 30), disabled=True, key="output_network_op")
                ]
            ]

            network_layout = [
                [
                    sg.Column(network_diagram_plot),
                    sg.Column(network_buttons),
                    sg.Column(see_buttons),
                    sg.VSeparator(),
                    sg.Column(network_plot)
                ]
            ]

            network_window = sg.Window('Operazioni sulla rete', network_layout)

            while True:
                event, values = network_window.read()
                # See if user wants to quit or window was closed
                if event == sg.WINDOW_CLOSED or event == 'Esci':
                    break
                elif event == 'be_diag':
                    show_behavioral_space()
                elif event == 'be_re_diag':
                    show_re_be_space()
                elif event == 'obs_diag':
                    show_obs_space()
                elif event == 'obs_re_diag':
                    show_re_obs_space()
                elif event == 'diag_diag':
                    show_diagnosi()
                elif event == 'calc_be':
                    calculate_behavioral_space()
                elif event == 'ren_be':
                    calculate_behavioral_space_renominated()
                elif event == 'calc_obs':
                    calculate_obs_space()
                elif event == 'ren_obs':
                    calculate_obs_space_renominated()
                elif event == 'diag':
                    calculate_diagnosi_space()

            # Finish up by removing from the screen
            network_window.close()

        # Define the window's contents

        buttons = [
            [
                sg.Button('Carica automi'),
                sg.Button('Carica link', key='load_link', disabled=True),
                sg.Button('Carica transizioni', key='load_transitions', disabled=True)
            ],
            [
                sg.Button('Elimina automi', disabled=True, key='delete_fsms')
            ],
            [
                sg.HSeparator()
            ],
            [
                sg.Button('Mostra i diagrammi degli automi', disabled=True, key='show_fsms'),
            ],
            [
                sg.HSeparator()
            ],
            [
                sg.Button('Crea la rete', disabled=True, key='create_network')
            ],
            [
                sg.HSeparator()
            ],
            [
                sg.Button('Esci')
            ]
        ]

        plot = [
            [
                sg.Text("Automi inseriti")
            ],
            [
                sg.Multiline("", size=(30, 1), disabled=True, key="output_fsms")
            ],
            [
                sg.Text("Link inseriti")
            ],
            [
                sg.Multiline("", size=(30, 5), disabled=True, key="output_link")
            ],
            [
                sg.Text("Transizioni inserite")
            ],
            [
                sg.Multiline("", size=(30, 10), disabled=True, key="output_transitions")
            ]

        ]

        create_layout = [
            [
                sg.Column(buttons),
                sg.VSeparator(),
                sg.Column(plot)
            ]
        ]

        # Create the window
        create_window = sg.Window('Crea rete', create_layout)

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = create_window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Esci':
                break
            elif event == 'Carica automi':
                load_fsm()
            elif event == 'load_link':
                load_links()
            elif event == 'load_transitions':
                load_transitions()
            elif event == 'show_fsms':
                show_fsm_graph()
            elif event == 'delete_fsms':
                remove_fsm()
            elif event == 'create_network':
                create_net()

        # Finish up by removing from the screen
        create_window.close()

        # show_net_btn = tk.Button(create, text="Mostra il diagramma della rete", state=tk.DISABLED,
        #                          command=show_net_graph)
        # show_net_btn.grid(row=7, pady=10, padx=10, column=3, columnspan=2)


    # behavioral_space_btn = tk.Button(create, text="Calcola lo spazio comportamentale",
    #                                  command=calculate_behavioral_space, state=tk.DISABLED)
    # behavioral_space_btn.grid(row=8, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
    # behavioral_space_ren_btn = tk.Button(create, text="Rinomina lo spazio comportamentale", state=tk.DISABLED,
    #                                      command=calculate_behavioral_space_renominated)
    # behavioral_space_ren_btn.grid(row=9, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
    # behavioral_space_obs_btn = tk.Button(create, text="Calcola lo spazio comportamentale data un'osservazione",
    #                                      state=tk.DISABLED, command=calculate_obs_space)
    # behavioral_space_obs_btn.grid(row=10, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
    # behavioral_space_obs_ren_btn = tk.Button(create, text="Rinomina lo spazio comportamentale data un'osservazione",
    #                                          state=tk.DISABLED, command=calculate_obs_space_renominated)
    # behavioral_space_obs_ren_btn.grid(row=11, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
    # diagnosi_btn = tk.Button(create, text="Diagnosi data un'osservazione", command=calculate_diagnosi_space,
    #                          state=tk.DISABLED)
    # diagnosi_btn.grid(row=12, pady=10, padx=10, column=1, columnspan=len(name_fsm_images))
    #
    # create.mainloop()

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
                    sg.Popup('Attenzione!',
                             'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
                except FileNotFoundError:
                    pass

            load_transitions_btn = tk.Button(load_n, text="Carica le transizioni",
                                             command=load_transitions)
            load_transitions_btn.grid(row=4, column=3, columnspan=3)

            def calculate_behavioral_space():
                global full_space

                filename = 'full_space' + n1.fsms[0].name + n1.fsms[1].name
                full_space = behavioral_space(n1, transitions)
                tk.Label(load_n, text="Fatto! Salvato in Behavioral_Space/" + filename, fg='green').grid(row=6,
                                                                                                         column=3)
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
                tk.Label(load_n, text="Fatto! Salvato in Behavioral_Space_Renominated/" + filename, fg='green').grid(
                    row=7,
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
                tk.Label(load_n, text="Fatto!  Salvato in Behavioral_Space_Observable/" + filename, fg='green').grid(
                    row=8,
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
            behavioral_space_obs_ren_btn = tk.Button(load_n,
                                                     text="Rinomina lo spazio comportamentale data un'osservazione",
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


    # Define the window's contents
    layout = [[sg.Text("Benvenuto nel programma per la creazione e la visualizzazione di reti di automi finiti. \n"
                       "In questo programma è possibile caricare degli automi a stati finiti già esistenti,\n "
                       "associati al file dei link e delle transizioni, oppure caricare direttamente una\n"
                       "rete di automi a stati finiti e il file relativo alle transizioni.\n\n"
                       "Il pulsante 'Crea una rete' permette di creare una rete caricando i file .TXT degli \n"
                       "automi a stati finiti, dei link e delle transizioni. "
                       "\n\nCliccando sul pulsante 'Aiuto' è possibile visionare la documentazione\n"
                       "(caldamente consigliato farlo per capire come funziona il programma).")],

              [sg.Button('Aiuto')],
              [sg.Button('Crea una rete'), sg.Button('Carica una rete')],
              [sg.Button('Esci')]]

    # Create the window
    window = sg.Window('Benvenuto', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Esci':
            break
        elif event == 'Aiuto':
            help()
        elif event == 'Crea una rete':
            create_network_window()
        elif event == 'Carica una rete':
            load_network_window()

    # Finish up by removing from the screen
    window.close()

    # f1 = FSM.read_fsm_from_txt()
    # graphic.draw_FSM_graphic(f1)
    # first()
    # second()
    # third()
