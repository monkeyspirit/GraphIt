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


def network_draw():
    n1 = network.read_network_from_json()
    graphic.draw_network_graphic(n1)
    return n1


def behavioral_space(filename, transitions):
    full_space = graphic.create_behavioral_space(filename, n1, transitions)
    comportamentalSpace.save_space_as_json(full_space)
    return full_space


def behavioral_space_renominated(filename, full_space):
    graphic.create_behavioral_space_renominated(filename, full_space)
    comportamentalSpace.save_space_as_json(full_space)
    return full_space


def observation(filename, cutted_space_for_obs, obs):
    obs_full_space = graphic.create_behavioral_space_from_obs(filename, obs, cutted_space_for_obs)
    comportamentalSpace.save_space_as_json(obs_full_space)
    return obs_full_space


def observation_renominated(filename, renominated_space_for_obs_and_cutting, obs):
    graphic.create_behavioral_space_observable_renominated(filename, renominated_space_for_obs_and_cutting, obs)
    comportamentalSpace.save_space_as_json(renominated_space_for_obs_and_cutting)
    return renominated_space_for_obs_and_cutting


def diagnosis(filename, space_for_diagnosis, obs):
    img = graphic.create_diagnosis_for_space_observable_renominated(filename, space_for_diagnosis, obs)
    comportamentalSpace.save_space_as_json(space_for_diagnosis)
    return img


#
# def third():
#     fsm_1 = FiniteStateMachine("S", ["0", "1"], "", [Edge("0", "s1", "1"), Edge("1", "s2", "0"),
#                                                      Edge("0", "s3", "0"), Edge("1", "s4", "1")])
#     graphic.draw_FSM_graphic(fsm_1)
#     fsm_2 = FiniteStateMachine("B", ["0", "1"], "", [Edge("0", "b1", "1"), Edge("1", "b2", "0"),
#                                                      Edge("0", "b3", "0"), Edge("1", "b4", "1"),
#                                                      Edge("0", "b5", "0"), Edge("1", "b6", "1"),
#                                                      Edge("0", "b7", "1"), Edge("1", "b8", "0")])
#     graphic.draw_FSM_graphic(fsm_2)
#
#     transitions_2 = [Transition("S", "s1", {}, {"L": "op"}, "ϵ", "act"),
#                      Transition("S", "s2", {}, {"L": "cl"}, "ϵ", "sby"),
#                      Transition("S", "s3", {}, {"L": "cl"}, "f1", "ϵ"),
#                      Transition("S", "s4", {}, {"L": "op"}, "f2", "ϵ"),
#                      Transition("B", "b1", {"L": "op"}, {}, "ϵ", "opn"),
#                      Transition("B", "b2", {"L": "cl"}, {}, "ϵ", "cls"),
#                      Transition("B", "b3", {"L": "op"}, {}, "f3", "ϵ"),
#                      Transition("B", "b4", {"L": "cl"}, {}, "f4", "ϵ"),
#                      Transition("B", "b5", {"L": "cl"}, {}, "ϵ", "nop"),
#                      Transition("B", "b6", {"L": "op"}, {}, "ϵ", "nop"),
#                      Transition("B", "b7", {"L": "cl"}, {}, "f5", "opn"),
#                      Transition("B", "b8", {"L": "op"}, {}, "f6", "cls")
#                      ]
#
#     fsms_2 = [fsm_1, fsm_2]
#
#     n2 = Network(fsms_2, [network.Link("S", "L", "B", "ϵ")], transitions_2)
#     network.save_network_as_json(n2)
#
#     graphic.draw_network_graphic(n2)
#
#     filename = 'full_space' + n2.fsms[0].name
#
#     full_space = graphic.create_behavioral_space(filename, n2, transitions_2)
#
#     comportamentalSpace.save_space_as_json(full_space)
#
#     full_space_for_renomination = copy.deepcopy(full_space)
#
#     filename = 'rinominated_space' + n2.fsms[0].name
#     graphic.create_behavioral_space_renominated(filename, full_space_for_renomination)
#
#     cutted_space_for_obs = copy.deepcopy(full_space_for_renomination)
#     # comportamental space relative to obs
#     obs = ["act", "sby", "nop"]
#     filename = 'observable_space' + n2.fsms[0].name + '_' + obs[0]
#     obs_full_space = graphic.create_behavioral_space_from_obs(filename, obs, cutted_space_for_obs)
#
#     renominated_space_for_obs_and_cutting = copy.deepcopy(obs_full_space)
#     filename = 'renominated_space_obs' + n2.fsms[0].name
#     graphic.create_behavioral_space_observable_renominated(filename, renominated_space_for_obs_and_cutting, obs)
#
#     space_for_diagnosis = copy.deepcopy(renominated_space_for_obs_and_cutting)
#     filename = 'diagnosis_space_obs' + n2.fsms[0].name
#     graphic.create_diagnosis_for_space_observable_renominated(filename, space_for_diagnosis, obs)
#

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
            except Exception:
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
                images.append(sg.Image(filename='Output/FSM_graph/fsm' + fsms[i].name + '.png'))
                text.append(sg.Text(fsms[i].name), )

            # Define the window's contents
            show_fsms = [
                images,
                text
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
                if event == sg.WINDOW_CLOSED:
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
            except Exception:
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
                create_window['save_filename'].update(disabled=False)
            except IndexError:
                sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
            except Exception:
                pass

        def save_filename():
            global filename
            filename = values['input_filename']+"_"
            create_window['create_network'].update(disabled=False)

        def create_net():

            global n1
            try:
                n1 = Network(fsms, links, transitions)
                graphic.draw_network_graphic(n1)
                network.save_network_as_json(n1, filename)

                operations_on_network()
                # show_net_btn['state'] = tk.NORMAL
                # behavioral_space_btn['state'] = tk.NORMAL
            except IndexError:
                sg.Popup('Attenzione!',
                         'Controlla di aver inserito tutti gli automi previsti dai link e dalle transizioni inserite!')

        def operations_on_network():

            def calculate_behavioral_space():
                global full_space, filename_be
                network_window['output_network_op'].update(values['output_network_op']+"--- Calcolo in corso ... ---")
                filename_be = filename + 'full_space'
                full_space = behavioral_space(filename_be, transitions)

                network_window['output_network_op'].update(values['output_network_op'] + '> Completato\n '
                                                                                         'Diagramma salvato in: Output/Behavioral_Space/' + filename_be)
                network_window['ren_be'].update(disabled=False)
                network_window['be_diag'].update(disabled=False)

            def show_behavioral_space():
                column1 = [[sg.Text('Spazio con LABEL')],
                           [sg.Image(filename='Output/Behavioral_Space/' + filename_be + '.gv.png')]]
                column2 = [[sg.Text('Spazio con ID')],
                           [sg.Image(filename='Output/Behavioral_Space/' + filename_be + '_id.gv.png')]]
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
                network_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")
                filename_re_be = filename + 'renominated_space'
                full_space_r = behavioral_space_renominated(filename_re_be, full_space)
                network_window['output_network_op'].update(values['output_network_op'] + '> Completato\n '
                                                                                         'Diagramma salvato in: Output/Behavioral_Space_Renominated/'
                                                           + filename_re_be  + "\nFile di "
                                                                                         "ridenominazione spazio comportamentale salvato in:\n"
                                                                                         "Output/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")


                network_window['be_re_diag'].update(disabled=False)
                network_window['renomination_file_be'].update(disabled=False)
                network_window['input_btn'].update(disabled=False)
                network_window['refresh'].update(disabled=False)

            def show_re_be_space():
                column_re1 = [[sg.Text('Spazio con ID rinominati')],
                              [sg.Image(filename='Output/Behavioral_Space_Renominated/' + filename_re_be + '.gv.png')]]
                column_re2 = [[sg.Text('Spazio con ID vecchi')],
                              [sg.Image(filename='Output/Behavioral_Space_Renominated/' + filename_re_be + '_id.gv.png')]]

                re_behavioral_layout = [
                    [
                        sg.Button('Vedi file ridenominazione', key='renomination_file_be_in_diag'),
                    ],
                    [
                        sg.Column(column_re1, size=(600, 800), scrollable=True),
                        sg.Column(column_re2, size=(600, 800), scrollable=True)
                    ]
                ]
                re_behavioral_window = sg.Window('Diagramma spazio comportamentale rinominato', re_behavioral_layout,
                                                 resizable=True)
                while True:
                    event, values = re_behavioral_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'renomination_file_be_in_diag':
                        show_renomination_file_be()

            def show_renomination_file_be():
                file = open(file="Output/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")
                renomination_be_layout = [
                    [
                        sg.Button('Vedi diagramma', key='be_re_diag')
                    ],
                    [sg.Column([[sg.Text(file.read())]], scrollable=True)]
                ]

                show_re_be_window = sg.Window('File di renominazione dello spazio comportamentale',
                                              renomination_be_layout)
                while True:
                    event, values = show_re_be_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'be_re_diag':
                        show_re_be_space()

                show_re_be_window.close()

            def check_obs_insert():
                global obs

                # obs = ["act", "sby", "nop"]
                try:
                    string_obs = values['input_obs']
                    obs = string_obs.split(",")
                    network_window['calc_obs'].update(disabled=False)
                    network_window['ren_obs'].update(disabled=True)
                    network_window['diag'].update(disabled=True)
                    network_window['obs_diag'].update(disabled=True)
                    network_window['obs_re_diag'].update(disabled=True)
                    network_window['diag_diag'].update(disabled=True)
                    network_window['renomination_file_obs'].update(disabled=True)
                    network_window['output_network_op'].update(values['output_network_op'] + "> Osservazione inserita:\n"+string_obs)
                except Exception:
                    sg.Popup('Attenzione!', 'Controlla di aver inserito l\'osservazione in modo corretto.')

            def refresh_obs():
                network_window['input_obs'].update("")
                network_window['calc_obs'].update(disabled=True)
                network_window['ren_obs'].update(disabled=True)
                network_window['diag'].update(disabled=True)
                network_window['obs_diag'].update(disabled=True)
                network_window['obs_re_diag'].update(disabled=True)
                network_window['diag_diag'].update(disabled=True)
                network_window['renomination_file_obs'].update(disabled=True)

            def calculate_obs_space():
                global obs_full_space, filename_obs
                network_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")

                filename_obs = filename + 'observable_space'
                obs_full_space = observation(filename_obs, full_space_r, obs)
                network_window['output_network_op'].update(
                    values['output_network_op'] + '> Completato\n '
                                                  'Diagramma salvato in: Output/Behavioral_Space_Observable/' + filename_obs)

                network_window['ren_obs'].update(disabled=False)
                network_window['obs_diag'].update(disabled=False)

            def show_obs_space():
                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "

                column_ob1 = [[sg.Image(filename='Output/Behavioral_Space_Observable/' + filename_obs + '.gv.png')]]
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
                network_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")
                filename_re_obs = filename + 'renominated_space_obs'
                obs_space_r = observation_renominated(filename_re_obs, obs_full_space, obs)

                network_window['output_network_op'].update(values[
                                                               'output_network_op'] + '> Completato\n'
                                                                                      'Diagramma salvato in: Output/Behavioral_Space_Observable_Renominated/' + filename_re_obs + "\nFile di "
                                                                                         "ridenominazione dello spazio data l'osservazione salvato in:\n"
                                                                                         "Output/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")

                network_window['diag'].update(disabled=False)
                network_window['obs_re_diag'].update(disabled=False)
                network_window['renomination_file_obs'].update(disabled=False)

            def show_re_obs_space():
                column_re_ob1 = [
                    [sg.Image(filename='Output/Behavioral_Space_Observable_Renominated/' + filename_re_obs + '.gv.png')]]

                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "

                re_obs_layout = [
                    [
                        sg.Text("L'osservazione considerata è:\n" + obs_name)
                    ],
                    [
                        sg.Button('Vedi file ridenominazione', key='renomination_file_obs_in_diag'),
                    ],
                    [
                        sg.Column(column_re_ob1, size=(600, 800), scrollable=True)
                    ]
                ]
                re_obs_window = sg.Window('Diagramma spazio comportamentale rinominato data l\'osservazione',
                                          re_obs_layout)
                while True:
                    event, values = re_obs_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'renomination_file_obs_in_diag':
                        show_renomination_file_obs()

            def show_renomination_file_obs():
                file = open(
                    file="Output/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")
                renomination_obs_layout = [
                    [
                        sg.Button('Vedi diagramma', key='obs_re_diag')
                    ],
                    [sg.Column([[sg.Text(file.read())]], scrollable=True)]
                ]

                show_re_obs_window = sg.Window('File di renominazione dello spazio comportamentale data osservazione',
                                               renomination_obs_layout)
                while True:
                    event, values = show_re_obs_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'obs_re_diag':
                        show_re_obs_space()

                show_re_obs_window.close()

            def calculate_diagnosi_space():
                network_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")
                global n_img, exp
                filename_dia = filename + 'diagnosis_space_obs'
                n_img, exp = diagnosis(filename_dia, obs_space_r, obs)

                network_window['output_network_op'].update(values['output_network_op'] + '> Completato\n'
                                                                                         'Diagramma salvato in: '
                                                                                         'Output/Diagnosi_steps/\n'+
                                                           '> Espressione regolare: '+exp)


                network_window['diag_diag'].update(disabled=False)

            def show_diagnosi():
                images_diagnosis = []
                for i in range(int(n_img) + 1):
                    images_diagnosis.append(sg.Image(filename='Output/Diagnosi_steps/' + str(i + 1) + '.gv.png'))

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
                    sg.Button('Calcola lo spazio comportamentale', key='calc_be'),
                    sg.Button('Vedi diagramma', key='be_diag', disabled=True)
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale', key='ren_be', disabled=True),
                    sg.Button('Vedi diagramma', key='be_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_be', disabled=True),
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Text('Inserire un\'osservazione valida:\n(separare gli elementi con una ","\n e senza spazi)'),
                    sg.InputText(key='input_obs'),
                    sg.Button('Inserisci', key='input_btn', disabled=True),
                    sg.Button('⟲', key='refresh', disabled=True)
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Calcola lo spazio comportamentale data un\'osservazione', key='calc_obs', disabled=True),
                    sg.Button('Vedi diagramma', key='obs_diag', disabled=True)
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale con l\'osservazione data', key='ren_obs',
                              disabled=True),
                    sg.Button('Vedi diagramma', key='obs_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_obs', disabled=True),
                ],
                [
                    sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True),
                    sg.Button('Vedi diagrammi', key='diag_diag', disabled=True)
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Indietro')
                ]
            ]

            network_diagram_plot = [
                [
                    sg.Text('Diagramma della rete')
                ],
                [
                    sg.Image(filename='Output/Network_graph/network' + n1.fsms[0].name + n1.fsms[1].name + '.png')
                ]
            ]

            network_plot = [
                [
                    sg.Multiline("", size=(40, 30), disabled=True, key="output_network_op")
                ]
            ]

            network_layout = [
                [
                    sg.Column(network_diagram_plot),
                    sg.Column(network_buttons),
                    sg.VSeparator(),
                    sg.Column(network_plot)
                ]
            ]

            network_window = sg.Window('Operazioni sulla rete', network_layout)

            while True:
                event, values = network_window.read()
                # See if user wants to quit or window was closed
                if event == sg.WINDOW_CLOSED or event == 'Indietro':
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
                elif event == 'renomination_file_be':
                    show_renomination_file_be()
                elif event == 'renomination_file_obs':
                    show_renomination_file_obs()
                elif event == 'input_btn':
                    check_obs_insert()
                elif event == 'refresh':
                    refresh_obs()

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
              sg.Text('Nome identificativo\ndel file:'),
              sg.Input(key='input_filename', size=(20, 1)),
              sg.Button('Salva', key='save_filename', disabled=True,)
            ],
            [
                sg.Button('Crea la rete', disabled=True, key='create_network')
            ],
            [
                sg.HSeparator()
            ],
            [
                sg.Button('Indietro')
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
            if event == sg.WINDOW_CLOSED or event == 'Indietro':
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
            elif event == 'save_filename':
                save_filename()
            elif event == 'create_network':
                create_net()

        # Finish up by removing from the screen
        create_window.close()


    def load_network_window():
        global load_window
        global n1

        try:
            n1 = network_draw() #  Read the netwrok json
            for fsm in n1.fsms:
                graphic.draw_FSM_graphic(fsm)

            names = ""
            for fsm in n1.fsms:
                names = names + str(fsm.name)

            def show_fsm_graph():
                global name_fsm_images

                name_fsm_images = []

                for fsm in n1.fsms:
                    name_fsm_images.append(fsm.name)

                images = []
                text = []
                for i in range(len(name_fsm_images)):
                    images.append(sg.Image(filename='Output/FSM_graph/fsm' + name_fsm_images[i] + '.png'))
                    text.append(sg.Text(name_fsm_images[i]), )

                # Define the window's contents
                show_fsms = [
                    images,
                    text
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
                    if event == sg.WINDOW_CLOSED:
                        break
                # Finish up by removing from the screen
                show_fsms_window.close()

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

                    load_window['output_transitions'].update(print_T)
                    load_window['save_filename'].update(disabled=False)
                except IndexError:
                    sg.Popup('Attenzione!',
                             'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
                except Exception:
                    pass

            def save_filename():
                global filename
                filename = values['input_filename'] + "_"
                load_window['calc_be'].update(disabled=False)


            def calculate_behavioral_space():
                global full_space, filename_be
                load_window['output_network_op'].update(values['output_network_op']+"--- Calcolo in corso ... ---")
                filename_be = filename + 'full_space'
                full_space = behavioral_space(filename_be, transitions)

                load_window['output_network_op'].update(values['output_network_op'] + '> Completato\n '
                                                                                         'Diagramma salvato in: Output/Behavioral_Space/' + filename_be)
                load_window['ren_be'].update(disabled=False)
                load_window['be_diag'].update(disabled=False)

            def show_behavioral_space():
                column1 = [[sg.Text('Spazio con LABEL')],
                           [sg.Image(filename='Output/Behavioral_Space/' + filename_be + '.gv.png')]]
                column2 = [[sg.Text('Spazio con ID')],
                           [sg.Image(filename='Output/Behavioral_Space/' + filename_be + '_id.gv.png')]]
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
                load_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")
                filename_re_be = filename + 'renominated_space'
                full_space_r = behavioral_space_renominated(filename_re_be, full_space)
                load_window['output_network_op'].update(values['output_network_op'] + '> Completato\n '
                                                                                         'Diagramma salvato in: Output/Behavioral_Space_Renominated/'
                                                           + filename_re_be  + "\nFile di "
                                                                                         "ridenominazione spazio comportamentale salvato in:\n"
                                                                                         "Output/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")


                load_window['be_re_diag'].update(disabled=False)
                load_window['renomination_file_be'].update(disabled=False)
                load_window['input_btn'].update(disabled=False)
                load_window['refresh'].update(disabled=False)

            def show_re_be_space():
                column_re1 = [[sg.Text('Spazio con ID rinominati')],
                              [sg.Image(filename='Output/Behavioral_Space_Renominated/' + filename_re_be + '.gv.png')]]
                column_re2 = [[sg.Text('Spazio con ID vecchi')],
                              [sg.Image(filename='Output/Behavioral_Space_Renominated/' + filename_re_be + '_id.gv.png')]]

                re_behavioral_layout = [
                    [
                        sg.Button('Vedi file ridenominazione', key='renomination_file_be_in_diag'),
                    ],
                    [
                        sg.Column(column_re1, size=(600, 800), scrollable=True),
                        sg.Column(column_re2, size=(600, 800), scrollable=True)
                    ]
                ]
                re_behavioral_window = sg.Window('Diagramma spazio comportamentale rinominato', re_behavioral_layout,
                                                 resizable=True)
                while True:
                    event, values = re_behavioral_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'renomination_file_be_in_diag':
                        show_renomination_file_be()

            def show_renomination_file_be():
                file = open(file="Output/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")
                renomination_be_layout = [
                    [
                        sg.Button('Vedi diagramma', key='be_re_diag')
                    ],
                    [sg.Column([[sg.Text(file.read())]], scrollable=True)]
                ]

                show_re_be_window = sg.Window('File di renominazione dello spazio comportamentale',
                                              renomination_be_layout)
                while True:
                    event, values = show_re_be_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'be_re_diag':
                        show_re_be_space()

                show_re_be_window.close()

            def check_obs_insert():
                global obs

                # obs = ["act", "sby", "nop"]
                try:
                    string_obs = values['input_obs']
                    obs = string_obs.split(",")
                    load_window['calc_obs'].update(disabled=False)
                    load_window['ren_obs'].update(disabled=True)
                    load_window['diag'].update(disabled=True)
                    load_window['obs_diag'].update(disabled=True)
                    load_window['obs_re_diag'].update(disabled=True)
                    load_window['diag_diag'].update(disabled=True)
                    load_window['renomination_file_obs'].update(disabled=True)
                    load_window['output_network_op'].update(values['output_network_op'] + "> Osservazione inserita:\n"+string_obs)
                except Exception:
                    sg.Popup('Attenzione!', 'Controlla di aver inserito l\'osservazione in modo corretto.')

            def refresh_obs():
                load_window['input_obs'].update("")
                load_window['calc_obs'].update(disabled=True)
                load_window['ren_obs'].update(disabled=True)
                load_window['diag'].update(disabled=True)
                load_window['obs_diag'].update(disabled=True)
                load_window['obs_re_diag'].update(disabled=True)
                load_window['diag_diag'].update(disabled=True)
                load_window['renomination_file_obs'].update(disabled=True)

            def calculate_obs_space():
                global obs_full_space, filename_obs
                load_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")

                filename_obs = filename + 'observable_space'
                obs_full_space = observation(filename_obs, full_space_r, obs)
                load_window['output_network_op'].update(
                    values['output_network_op'] + '> Completato\n '
                                                  'Diagramma salvato in: Output/Behavioral_Space_Observable/' + filename_obs)

                load_window['ren_obs'].update(disabled=False)
                load_window['obs_diag'].update(disabled=False)

            def show_obs_space():
                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "

                column_ob1 = [[sg.Image(filename='Output/Behavioral_Space_Observable/' + filename_obs + '.gv.png')]]
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
                load_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")
                filename_re_obs = filename +  'renominated_space_obs'
                obs_space_r = observation_renominated(filename_re_obs, obs_full_space, obs)

                load_window['output_network_op'].update(values[
                                                               'output_network_op'] + '> Completato\n'
                                                                                      'Diagramma salvato in: Output/Behavioral_Space_Observable_Renominated/' + filename_re_obs + "\nFile di "
                                                                                         "ridenominazione dello spazio data l'osservazione salvato in:\n"
                                                                                         "Output/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")

                load_window['diag'].update(disabled=False)
                load_window['obs_re_diag'].update(disabled=False)
                load_window['renomination_file_obs'].update(disabled=False)

            def show_re_obs_space():
                column_re_ob1 = [
                    [sg.Image(filename='Output/Behavioral_Space_Observable_Renominated/' + filename_re_obs + '.gv.png')]]

                obs_name = ""
                for o in obs:
                    obs_name = obs_name + o + " "

                re_obs_layout = [
                    [
                        sg.Text("L'osservazione considerata è:\n" + obs_name)
                    ],
                    [
                        sg.Button('Vedi file ridenominazione', key='renomination_file_obs_in_diag'),
                    ],
                    [
                        sg.Column(column_re_ob1, size=(600, 800), scrollable=True)
                    ]
                ]
                re_obs_window = sg.Window('Diagramma spazio comportamentale rinominato data l\'osservazione',
                                          re_obs_layout)
                while True:
                    event, values = re_obs_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'renomination_file_obs_in_diag':
                        show_renomination_file_obs()

            def show_renomination_file_obs():
                file = open(
                    file="Output/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")
                renomination_obs_layout = [
                    [
                        sg.Button('Vedi diagramma', key='obs_re_diag')
                    ],
                    [sg.Column([[sg.Text(file.read())]], scrollable=True)]
                ]

                show_re_obs_window = sg.Window('File di renominazione dello spazio comportamentale data osservazione',
                                               renomination_obs_layout)
                while True:
                    event, values = show_re_obs_window.read()
                    # See if user wants to quit or window was closed
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == 'obs_re_diag':
                        show_re_obs_space()

                show_re_obs_window.close()

            def calculate_diagnosi_space():
                load_window['output_network_op'].update(values['output_network_op'] + "--- Calcolo in corso ... ---")
                global n_img, exp
                filename_dia = filename + 'diagnosis_space_obs'
                n_img, exp = diagnosis(filename_dia, obs_space_r, obs)
                load_window['output_network_op'].update(values['output_network_op'] + '> Completato\n'
                                                                                         'Diagramma salvato in: '
                                                                                         'Output/Diagnosi_steps\n'+
                                                           '> Espressione regolare: '+exp)


                load_window['diag_diag'].update(disabled=False)

            def show_diagnosi():
                images_diagnosis = []
                for i in range(int(n_img) + 1):
                    images_diagnosis.append(sg.Image(filename='Output/Diagnosi_steps/' + str(i + 1) + '.gv.png'))

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



            load_net_buttons = [
                [
                    sg.Text('Diagramma della rete'),
                    sg.Image(filename="Output/Network_graph/network" + names + ".png")
                ],
                [
                    sg.Button('Mostra i diagrammi degli automi', key='show_fsms'),

                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Carica transizioni', key='load_transitions')
                ],

                [
                    sg.HSeparator()
                ],

                [
                    sg.Text('Nome identificativo\ndel file:'),
                    sg.Input(key='input_filename', size=(20, 1)),
                    sg.Button('Salva', key='save_filename', disabled=True, )
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Calcola lo spazio comportamentale', disabled=True, key='calc_be'),
                    sg.Button('Vedi diagramma', key='be_diag', disabled=True)
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale', key='ren_be', disabled=True),
                    sg.Button('Vedi diagramma', key='be_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_be', disabled=True),
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Text('Inserire un\'osservazione valida:\n(separare gli elementi con una ","\n e senza spazi)'),
                    sg.InputText(key='input_obs'),
                    sg.Button('Inserisci', key='input_btn', disabled=True),
                    sg.Button('⟲', key='refresh', disabled=True)
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Calcola lo spazio comportamentale data un\'osservazione', key='calc_obs', disabled=True),
                    sg.Button('Vedi diagramma', key='obs_diag', disabled=True)
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale con l\'osservazione data', key='ren_obs',
                              disabled=True),
                    sg.Button('Vedi diagramma', key='obs_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_obs', disabled=True),
                ],
                [
                    sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True),
                    sg.Button('Vedi diagrammi', key='diag_diag', disabled=True)
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Indietro')
                ]
            ]

            load_net_plot = [
                [
                    sg.Text("Transizioni inserite")
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Multiline("", size=(30, 10), disabled=True, key="output_transitions")
                ],
                [
                    sg.Multiline("", size=(40, 30), disabled=True, key="output_network_op")
                ]
            ]

            load_layout = [
                [
                    sg.Column(load_net_buttons),
                    sg.VSeparator(),
                    sg.Column(load_net_plot)
                ]
            ]

            # Create the window
            load_window = sg.Window('Carica rete', load_layout)

            # Display and interact with the Window using an Event Loop
            while True:
                event, values = load_window.read()
                # See if user wants to quit or window was closed
                if event == sg.WINDOW_CLOSED or event == 'Indietro':
                    break
                elif event == 'load_transitions':
                    load_transitions()
                elif event == 'show_fsms':
                    show_fsm_graph()
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
                elif event == 'renomination_file_be':
                    show_renomination_file_be()
                elif event == 'renomination_file_obs':
                    show_renomination_file_obs()
                elif event == 'input_btn':
                    check_obs_insert()
                elif event == 'refresh':
                    refresh_obs()
                elif event == 'save_filename':
                    save_filename()

            # Finish up by removing from the screen
            load_window.close()

        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except IndexError:
            pass


    def help():
        webbrowser.open("Help/html/index_home.html")

    def cs_window():
        cs_layout = [
            [
                sg.Button('Indietro')
            ]
        ]

        # Create the window
        cs_window = sg.Window('Carica rete', cs_layout)
        while True:
            event, values = cs_window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Indietro':
                break


        # Finish up by removing from the screen
        cs_window.close()

    def diagnosi_window():
        dia_layout = [
            [
                sg.Button('Indietro')
            ]
        ]

        # Create the window
        dia_window = sg.Window('Carica rete', dia_layout)
        while True:
            event, values = dia_window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Indietro':
                break


        # Finish up by removing from the screen
        dia_window.close()

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
              [sg.Button('Crea una rete'), sg.Button('Carica una rete'), sg.Button('Carica spazio comportamentale'), sg.Button('Esegui diagnosi')],
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
        elif event == 'Carica spazio comportamentale':
            cs_window()
        elif event == 'Esegui diagnosi':
            diagnosi_window()

    # Finish up by removing from the screen
    window.close()

    # f1 = FSM.read_fsm_from_txt()
    # graphic.draw_FSM_graphic(f1)
    # first()
    # second()
    # third()
