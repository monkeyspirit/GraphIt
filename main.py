import json
from datetime import datetime

import Class.UI.UI_operations_on_network
from Class.Base import space, graphic, network
from Class.UI import UI_create_network, UI_operations_on_network
from Class.Base.network import Network
import PySimpleGUI as sg
import webbrowser



if __name__ == '__main__':

    def create_network_window():
        global fsms, links, transitions

        fsms = []
        links = []
        transitions = []

        def save_filename():
            global filename
            if values['input_filename'] != "":
                filename = values['input_filename']
                create_window['load_fsm'].update(disabled=False)
            else:
                sg.Popup('Attenzione!',
                         'Inserire un nome valido!')

        def create_net():
            global n1
            try:
                n1 = Network(fsms, links, transitions)
                graphic.draw_network_graphic(n1, filename)
                network.save_network_as_json(n1, filename)

                operations_on_network()
            except IndexError:
                sg.Popup('Attenzione!',
                         'Controlla di aver inserito tutti gli automi previsti dai link e dalle transizioni inserite!')

        def operations_on_network():
            global filename_be, filename_re_be, filename_obs, filename_re_obs, filename_dia
            global full_space, full_space_r, obs_full_space, obs_space_r
            global obs, n_img, exp

            network_buttons = [
                [
                    sg.Button('Calcola lo spazio comportamentale', key='calc_be'),
                    sg.Button('Vedi diagramma', key='be_diag', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_be_space')
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale', key='ren_be', disabled=True),
                    sg.Button('Vedi diagramma', key='be_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_be', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_be_re_space')
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
                    sg.Button('Vedi diagramma', key='obs_diag', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_obs_space')
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale con l\'osservazione data', key='ren_obs',
                              disabled=True),
                    sg.Button('Vedi diagramma', key='obs_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_obs', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_obs_re_space')
                ],
                [
                    sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True)

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
                    sg.Image(filename='Output/'+filename+'/Network_graph/network_' + filename+'.png')
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
                    UI_operations_on_network.show_behavioral_space(filename_be, filename)
                elif event == 'be_re_diag':
                    UI_operations_on_network.show_re_be_space(filename_re_be, filename_be, filename)
                elif event == 'obs_diag':
                    UI_operations_on_network.show_obs_space(obs, filename_obs, filename)
                elif event == 'obs_re_diag':
                    UI_operations_on_network.show_re_obs_space(obs, filename_re_obs, filename)
                elif event == 'calc_be':
                    network_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    filename_be, full_space = UI_operations_on_network.calculate_behavioral_space(network_window,
                                                                                                  filename, transitions,
                                                                                                  n1)
                    summary = open("Output/"+filename+"/Behavioral_Space/space_summary.txt", "r")
                    file = summary.read()
                    summary.close()
                    network_window['output_network_op'].update(values['output_network_op'] + '> Completato\nRiassunto:\n' + file +'\n'
                                                                                             'Diagramma salvato in: Output/'+filename+'/Behavioral_Space/' + filename_be)
                elif event == 'ren_be':
                    network_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    filename_re_be, full_space_r = UI_operations_on_network.calculate_behavioral_space_renominated(
                        network_window, filename, full_space, False)
                    summary = open("Output/" + filename + "/Behavioral_Space_Renominated/space_summary.txt", "r")
                    file = summary.read()
                    summary.close()
                    network_window['output_network_op'].update(values[
                                                                   'output_network_op'] + '> Completato\nRiassunto:\n'+ file +'\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space_Renominated/'
                                                               + filename_re_be + "\nFile di ridenominazione spazio comportamentale salvato in:\n"
                                                                                  "Output/'+filename+'/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")
                elif event == 'calc_obs':
                    network_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    obs_full_space, filename_obs = UI_operations_on_network.calculate_obs_space(network_window,
                                                                                                filename, full_space_r,
                                                                                                obs)
                    summary = open("Output/" + filename + "/Behavioral_Space_Observable/space_summary.txt", "r")
                    file = summary.read()
                    summary.close()

                    network_window['output_network_op'].update(
                        values['output_network_op'] + '> Completato\nRiassunto:\n'+file+
                                                      '\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space_Observable/' + filename_obs)
                elif event == 'ren_obs':
                    network_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    obs_space_r, filename_re_obs = UI_operations_on_network.calculate_obs_space_renominated(
                        network_window, filename, obs_full_space, obs)
                    summary = open("Output/" + filename + "/Behavioral_Space_Observable_Renominated/space_summary.txt", "r")
                    file = summary.read()
                    summary.close()
                    network_window['output_network_op'].update(values[
                                                                   'output_network_op'] + '> Completato\nRiassunto:\n'+file+
                                                                                          '\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space_Observable_Renominated/' + filename_re_obs + "\nFile di "
                                                                                                                                                                                      "ridenominazione dello spazio data l'osservazione salvato in:\n"
                                                                                                                                                                                      "Output/"+filename+"/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")
                elif event == 'diag':
                    try:
                        network_window['output_network_op'].update(
                            values['output_network_op'] + "--- Calcolo in corso ... ---")
                        n_img, exp = UI_operations_on_network.calculate_diagnosi_space(network_window, filename,
                                                                                       obs_space_r, obs)
                        network_window['output_network_op'].update(values['output_network_op'] + '> Completato\n'
                                                                                                 'Diagrammi salvati in: '
                                                                                              'Output/'+filename+'/Diagnosi_steps/'+filename+'\n' +
                                                                   '> Espressione regolare: ' + exp)
                    except IndexError:
                        sg.Popup(
                            'Attenzione, l\'osservazione produce uno spazio comportamentale vuoto. Quindi non ha senso fare un diagnosi.')
                        network_window['output_network_op'].update(
                            values['output_network_op'] + "--- Calcolo annullato ---")
                elif event == 'renomination_file_be':
                    UI_operations_on_network.show_renomination_file_be(filename_re_be, filename_be, filename)
                elif event == 'renomination_file_obs':
                    UI_operations_on_network.show_renomination_file_obs(obs, filename_re_obs, filename)
                elif event == 'input_btn':
                    string_obs = values['input_obs']
                    obs = UI_operations_on_network.check_obs_insert(string_obs, network_window)
                    network_window['output_network_op'].update(
                        values['output_network_op'] + "> Osservazione inserita:\n" + string_obs)
                elif event == 'refresh':
                    UI_operations_on_network.refresh_obs(network_window)
                elif event == 'save_be_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_be
                    UI_operations_on_network.save_be_space_as_JSON(dt_string, filename)
                    network_window['output_network_op'].update(
                        values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                      'Il percorso del file è\n: Output/'
                                                      + filename+'/' + dt_string + '.json')
                elif event == 'save_be_re_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_re_be
                    UI_operations_on_network.save_be_re_space_as_JSON(dt_string, filename)
                    network_window['output_network_op'].update(
                        values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                      'Il percorso del file è\n: Output/'
                                                      + filename+'/' + dt_string + '.json')
                elif event == 'save_obs_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_obs
                    UI_operations_on_network.save_obs_space_as_JSON(dt_string, filename)
                    network_window['output_network_op'].update(
                        values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                      'Il percorso del file è\n: Output/'
                                                      + filename+'/' + dt_string + '.json')
                elif event == 'save_obs_re_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_re_obs
                    UI_operations_on_network.save_obs_re_space_as_JSON(dt_string, filename)
                    network_window['output_network_op'].update(
                        values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                      'Il percorso del file è\n: Output/'
                                                       + filename+'/' + dt_string + '.json')

            # Finish up by removing from the screen
            network_window.close()

        # Define the window's contents

        buttons = [
            [
                sg.Text('Nome identificativo\ndel file:'),
                sg.Input(key='input_filename', size=(20, 1)),
                sg.Button('Salva', key='save_filename')
            ],
            [
                sg.HSeparator()
            ],
            [
                sg.Button('Carica automi', key='load_fsm', disabled=True),
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
            elif event == 'load_fsm':
                UI_create_network.load_fsm(create_window, fsms, filename)
            elif event == 'load_link':
                links = UI_create_network.load_links(create_window)
            elif event == 'load_transitions':
                transitions = UI_create_network.load_transitions(create_window)
                create_window['create_network'].update(disabled=False)
            elif event == 'show_fsms':
                UI_create_network.show_fsm_graph(fsms, filename)
            elif event == 'delete_fsms':
                UI_create_network.remove_fsm(create_window, fsms)
            elif event == 'save_filename':
                save_filename()
            elif event == 'create_network':
                create_net()

        # Finish up by removing from the screen
        create_window.close()


    def load_network_window():
        global n1, transition
        global filename_be, filename_re_be, filename_obs, filename_re_obs, filename_dia
        global full_space, full_space_r, obs_full_space, obs_space_r
        global obs, n_img, exp

        try:
            n1 = network.read_network_from_json() # Read the network json

            for fsm in n1.fsms:
                graphic.draw_FSM_graphic(fsm, "loaded_network")

            names = ""
            for fsm in n1.fsms:
                names = names + str(fsm.name)

            graphic.draw_network_graphic_from_load_network(n1, names, "loaded_network")

            def save_filename():
                global filename
                if values['input_filename'] != "":
                    filename = values['input_filename']
                    load_window['calc_be'].update(disabled=False)
                else:
                    sg.Popup('Attenzione!',
                             'Inserire un nome valido!')


            load_net_buttons = [
                [
                    sg.Text('Diagramma della rete'),
                    sg.Image(filename="Output/loaded_network/Network_graph/network_" + names + ".png")
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
                    sg.Button('Vedi diagramma', key='be_diag', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_be_space')
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale', key='ren_be', disabled=True),
                    sg.Button('Vedi diagramma', key='be_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_be', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_be_re_space')
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
                    sg.Button('Vedi diagramma', key='obs_diag', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_obs_space')
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale con l\'osservazione data', key='ren_obs',
                              disabled=True),
                    sg.Button('Vedi diagramma', key='obs_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_obs', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_obs_re_space')
                ],
                [
                    sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True)
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
                    transitions = UI_create_network.load_transitions(load_window)
                elif event == 'show_fsms':
                    Class.UI.UI_operations_on_network.show_fsm_graph(n1, "loaded_network")
                elif event == 'be_diag':
                    UI_operations_on_network.show_behavioral_space(filename_be, filename)
                elif event == 'be_re_diag':
                    UI_operations_on_network.show_re_be_space(filename_re_be, filename_be, filename)
                elif event == 'obs_diag':
                    UI_operations_on_network.show_obs_space(obs, filename_obs, filename)
                elif event == 'obs_re_diag':
                    UI_operations_on_network.show_re_obs_space(obs, filename_re_obs, filename)
                elif event == 'calc_be':
                    load_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    filename_be, full_space = UI_operations_on_network.calculate_behavioral_space(load_window,
                                                                                                  filename, transitions,
                                                                                                  n1)
                    summary = open("Output/" + filename + "/Behavioral_Space/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    load_window['output_network_op'].update(values['output_network_op'] + '> Completato\nRiassunto:\n'+file+
                                                                                          '\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space/' + filename_be)
                elif event == 'ren_be':
                    load_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    filename_re_be, full_space_r = UI_operations_on_network.calculate_behavioral_space_renominated(
                        load_window, filename, full_space, False)
                    summary = open("Output/" + filename + "/Behavioral_Space_Renominated/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    load_window['output_network_op'].update(values[
                                                                'output_network_op'] + '> Completato\nRiassunto:\n'+file+ '\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space_Renominated/'
                                                            + filename_re_be + "\nFile di ridenominazione spazio comportamentale salvato in:\n"
                                                                               "Output/"+filename+"/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")
                elif event == 'calc_obs':
                    load_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    obs_full_space, filename_obs = UI_operations_on_network.calculate_obs_space(load_window,
                                                                                                filename, full_space_r,
                                                                                                obs)
                    summary = open("Output/" + filename + "/Behavioral_Space_Observable/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    load_window['output_network_op'].update(
                        values['output_network_op'] + '> Completato\nRiassunto:\n'+file+
                                                      '\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space_Observable/' + filename_obs)
                elif event == 'ren_obs':
                    load_window['output_network_op'].update(
                        values['output_network_op'] + "--- Calcolo in corso ... ---")
                    obs_space_r, filename_re_obs = UI_operations_on_network.calculate_obs_space_renominated(
                        load_window, filename, obs_full_space, obs)
                    summary = open("Output/" + filename + "/Behavioral_Space_Observable_Renominated/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    load_window['output_network_op'].update(values[
                                                                'output_network_op'] + '> Completato\nRiassunto:\n'+file+
                                                                                       '\nDiagramma salvato in: Output/'+filename+'/Behavioral_Space_Observable_Renominated/' + filename_re_obs + "\nFile di "
                                                                                                                                                                                   "ridenominazione dello spazio data l'osservazione salvato in:\n"
                                                                                                                                                                                   "Output/"+filename+"/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")
                elif event == 'diag':
                    try:
                        load_window['output_network_op'].update(
                            values['output_network_op'] + "--- Calcolo in corso ... ---")
                        n_img, exp = UI_operations_on_network.calculate_diagnosi_space(load_window, filename,
                                                                                       obs_space_r, obs)
                        load_window['output_network_op'].update(values['output_network_op'] + '> Completato\n'
                                                                                              'Diagrammi salvati in: '
                                                                                              'Output/'+filename+'/Diagnosi_steps/'+filename+'\n' +
                                                                '> Espressione regolare: ' + exp)
                    except IndexError:
                        sg.Popup(
                            'Attenzione, l\'osservazione produce uno spazio comportamentale vuoto. Quindi non ha senso fare un diagnosi.')
                        load_window['output_network_op'].update(
                            values['output_network_op'] + "--- Calcolo annullato ---")
                elif event == 'renomination_file_be':
                    UI_operations_on_network.show_renomination_file_be(filename_re_be, filename_be, filename)
                elif event == 'renomination_file_obs':
                    UI_operations_on_network.show_renomination_file_obs(obs, filename_re_obs, filename)
                elif event == 'input_btn':
                    string_obs = values['input_obs']
                    obs = UI_operations_on_network.check_obs_insert(string_obs, load_window)
                    load_window['output_network_op'].update(
                        values['output_network_op'] + "> Osservazione inserita:\n" + string_obs)
                elif event == 'refresh':
                    UI_operations_on_network.refresh_obs(load_window)
                elif event == 'save_filename':
                    save_filename()

                elif event == 'save_be_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_be
                    UI_operations_on_network.save_be_space_as_JSON(dt_string, filename)
                    load_window['output_network_op'].update(values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                                                          'Il percorso del file è\n: Output/'
                                                                                         +filename+'/' + dt_string + '.json')
                elif event == 'save_be_re_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_re_be
                    UI_operations_on_network.save_be_re_space_as_JSON(dt_string, filename)
                    load_window['output_network_op'].update(values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                                                          'Il percorso del file è\n:  Output/'
                                                                                         +filename+'/' + dt_string + '.json')
                elif event == 'save_obs_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_obs
                    UI_operations_on_network.save_obs_space_as_JSON(dt_string, filename)
                    load_window['output_network_op'].update(values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                                                          'Il percorso del file è\n:  Output/'
                                                                                         +filename+'/' + dt_string + '.json')
                elif event == 'save_obs_re_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_re_obs
                    UI_operations_on_network.save_obs_re_space_as_JSON(dt_string, filename)
                    load_window['output_network_op'].update(values['output_network_op'] + '> Salvataggio effettuato!\n'
                                                                                          'Il percorso del file è\n:  Output/'
                                                                                         +filename+'/' + dt_string + '.json')

            # Finish up by removing from the screen
            load_window.close()

        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except json.decoder.JSONDecodeError:
            sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')
        # except AttributeError:
        #     sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')


    def help():
        webbrowser.open("Help\html\index_home.html")


    def load_comportamentalspace_window():

        global filename_be, filename_re_be, filename_obs, filename_re_obs, filename_dia
        global full_space, full_space_r, obs_full_space, obs_space_r
        global obs, n_img, exp

        try:
            full_space, filename_be = space.read_space_from_json()
            graphic.draw_comportamental_space(filename_be, full_space)

            comportamentalSpace_buttons = [
                [
                    sg.Button('Vedi diagramma spazio comportamentale caricato', key='be_diag'),
                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale', key='ren_be'),
                    sg.Button('Vedi diagramma', key='be_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_be', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_be_re_space')
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
                    sg.Button('Vedi diagramma', key='obs_diag', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_obs_space')
                ],
                [
                    sg.Button('Rinomina lo spazio comportamentale con l\'osservazione data', key='ren_obs',
                              disabled=True),
                    sg.Button('Vedi diagramma', key='obs_re_diag', disabled=True),
                    sg.Button('Vedi file ridenominazione', key='renomination_file_obs', disabled=True),
                    sg.Button('Salva lo spazio come JSON', disabled=True, key='save_obs_re_space')
                ],
                [
                    sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True)

                ],
                [
                    sg.HSeparator()
                ],
                [
                    sg.Button('Indietro')
                ]
            ]

            comportamentalspace_plot = [

                [
                    sg.Multiline("", size=(40, 30), disabled=True, key="output_op")
                ]
            ]

            comportamentalspace_layout = [
                [
                    sg.Column(comportamentalSpace_buttons),
                    sg.VSeparator(),
                    sg.Column(comportamentalspace_plot)
                ]
            ]

            # Create the window
            comportamentalspace_window = sg.Window('Spazio comportamentale', comportamentalspace_layout)
            while True:
                event, values = comportamentalspace_window.read()
                # See if user wants to quit or window was closed
                if event == sg.WINDOW_CLOSED or event == 'Indietro':
                    break
                elif event == 'be_diag':
                    UI_operations_on_network.show_behavioral_space(filename_be, filename_be, type=1)
                elif event == 'be_re_diag':
                    UI_operations_on_network.show_re_be_space(filename_re_be, filename_be, filename_be, type=1)
                elif event == 'obs_diag':
                    UI_operations_on_network.show_obs_space(obs, filename_obs, filename_be)
                elif event == 'obs_re_diag':
                    UI_operations_on_network.show_re_obs_space(obs, filename_re_obs, filename_be)
                elif event == 'ren_be':
                    comportamentalspace_window['output_op'].update(values['output_op'] + "--- Calcolo in corso ... ---")
                    filename_re_be, full_space_r = UI_operations_on_network.calculate_behavioral_space_renominated(
                        comportamentalspace_window, filename_be, full_space, True)
                    summary = open("Output/" + filename_be + "/Behavioral_Space_Renominated/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    comportamentalspace_window['output_op'].update(values[
                                                                       'output_op'] + '> Completato\nRiassunto:\n'+file+'\nDiagramma salvato in: Output/'+filename_be+'/Behavioral_Space_Renominated/'
                                                                   + filename_re_be + "\nFile di ridenominazione spazio comportamentale salvato in:\n"
                                                                                      "Output/"+filename_be+"/Behavioral_Space_Renominated/renomination_list_" + filename_re_be + ".txt")

                elif event == 'calc_obs':
                    comportamentalspace_window['output_op'].update(
                        values['output_op'] + "--- Calcolo in corso ... ---")
                    obs_full_space, filename_obs = UI_operations_on_network.calculate_obs_space(
                        comportamentalspace_window,
                        filename_be, full_space_r,
                        obs)
                    summary = open("Output/" + filename_be + "/Behavioral_Space_Observable/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    comportamentalspace_window['output_op'].update(
                        values['output_op'] + '> Completato\nRiassunto:\n'+file+
                                              '\nDiagramma salvato in: Output/'+filename_be+'/Behavioral_Space_Observable/' + filename_obs)
                elif event == 'ren_obs':
                    comportamentalspace_window['output_op'].update(
                        values['output_op'] + "--- Calcolo in corso ... ---")
                    obs_space_r, filename_re_obs = UI_operations_on_network.calculate_obs_space_renominated(
                        comportamentalspace_window, filename_be, obs_full_space, obs)
                    summary = open("Output/" + filename_be + "/Behavioral_Space_Observable_Renominated/space_summary.txt",
                                   "r")
                    file = summary.read()
                    summary.close()
                    comportamentalspace_window['output_op'].update(values[
                                                                       'output_op'] + '> Completato\nRiassunto:\n'+file+
                                                                                      '\nDiagramma salvato in: Output/'+filename_be+'/Behavioral_Space_Observable_Renominated/' + filename_re_obs + "\nFile di "
                                                                                                                                                                                  "ridenominazione dello spazio data l'osservazione salvato in:\n"
                                                                                                                                                                                  "Output/"+filename_be+"/Behavioral_Space_Observable_Renominated/renomination_list_" + filename_re_obs + ".txt")
                elif event == 'diag':
                    try:
                        comportamentalspace_window['output_op'].update(
                            values['output_op'] + "--- Calcolo in corso ... ---")
                        n_img, exp = UI_operations_on_network.calculate_diagnosi_space(comportamentalspace_window,
                                                                                       filename_be,
                                                                                       obs_space_r, obs)
                        comportamentalspace_window['output_op'].update(values['output_op'] + '> Completato\n'
                                                                                             'Diagrammi salvati in: '
                                                                                             'Output/'+filename_be+'/Diagnosi_steps/'+filename_be+'\n' +
                                                                       '> Espressione regolare: ' + exp)
                    except IndexError:
                        sg.Popup(
                            'Attenzione, l\'osservazione produce uno spazio comportamentale vuoto. Quindi non ha senso fare un diagnosi.')
                        comportamentalspace_window['output_op'].update(values['output_op'] + "--- Calcolo annullato ---")
                elif event == 'renomination_file_be':
                    UI_operations_on_network.show_renomination_file_be(filename_re_be, filename_be, filename_be, type=1)
                elif event == 'renomination_file_obs':
                    UI_operations_on_network.show_renomination_file_obs(obs, filename_re_obs, filename_be)
                elif event == 'input_btn':
                    string_obs = values['input_obs']
                    obs = UI_operations_on_network.check_obs_insert(string_obs, comportamentalspace_window)
                    comportamentalspace_window['output_op'].update(
                        values['output_op'] + "> Osservazione inserita:\n" + string_obs)
                elif event == 'refresh':
                    UI_operations_on_network.refresh_obs(comportamentalspace_window)
                elif event == 'save_be_re_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_re_be
                    UI_operations_on_network.save_be_re_space_as_JSON(dt_string, filename_be)
                    comportamentalspace_window['output_op'].update(values['output_op'] + '> Salvataggio effettuato!\n'
                                                                                         'Il percorso del file è\n: Output/'
                                                                                         +filename_be+'/' + dt_string + '.json')
                elif event == 'save_obs_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_obs
                    UI_operations_on_network.save_obs_space_as_JSON(dt_string, filename_be)
                    comportamentalspace_window['output_op'].update(values['output_op'] + '> Salvataggio effettuato!\n'
                                                                                         'Il percorso del file è\n: Output/'
                                                                                         +filename_be+'/' + dt_string + '.json')
                elif event == 'save_obs_re_space':
                    now = datetime.now()
                    dt_string = str(now.date()) + "_" + filename_re_obs
                    UI_operations_on_network.save_obs_re_space_as_JSON(dt_string, filename_be)
                    comportamentalspace_window['output_op'].update(values['output_op'] + '> Salvataggio effettuato!\n'
                                                                                         'Il percorso del file è\n: Output/'
                                                                                         +filename_be+'/' + dt_string + '.json')

            # Finish up by removing from the screen
            comportamentalspace_window.close()
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except json.decoder.JSONDecodeError:
            sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')
        except AttributeError:
            sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')


    def do_diagnosi_window():
        global full_space, filename_be, obs

        do_diagnosi_buttons = [
            [
                sg.Button('Carica lo spazio comportamentale', key='load')
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
                sg.Button('Calcola la diagnosi con l\'osservazione data', key='diag', disabled=True)
            ],
            [
                sg.HSeparator()
            ],
            [
                sg.Button('Indietro')
            ]

        ]


        do_diagnosi_plot = [
            [
                sg.Multiline("", size=(40, 10), disabled=True, key="output_dia")
            ]
        ]

        do_diagnosi_layout = [
            [
                sg.Column(do_diagnosi_buttons),
                sg.VSeparator(),
                sg.Column(do_diagnosi_plot)
            ]
        ]

        # Create the window
        do_diagnosi_window = sg.Window('Diagnosi', do_diagnosi_layout)
        while True:
            event, values = do_diagnosi_window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Indietro':
                break
            elif event == 'load':
                try:
                    full_space, filename_be = UI_operations_on_network.load_comportamental_space(do_diagnosi_window)
                    do_diagnosi_window['output_dia'].update(values['output_dia'] +"> Caricamento riuscito!")
                except FileNotFoundError:
                    pass
                except TypeError:
                    pass
                except json.decoder.JSONDecodeError:
                    sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')
                except AttributeError:
                    sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')
            elif event == 'input_btn':
                string_obs = values['input_obs']
                obs = UI_operations_on_network.check_obs_insert_dia(string_obs, do_diagnosi_window)
                do_diagnosi_window['output_dia'].update(
                    values['output_dia'] + "> Osservazione inserita:\n" + string_obs)
            elif event == 'refresh':
                UI_operations_on_network.refresh_obs_diagnosi(do_diagnosi_window)
            elif event == 'diag':
                try:
                    do_diagnosi_window['output_dia'].update(
                        values['output_dia'] + "--- Calcolo in corso ... ---")
                    n_img, exp = UI_operations_on_network.calculate_all(do_diagnosi_window, full_space, filename_be, obs)
                    do_diagnosi_window['output_dia'].update(values['output_dia'] + '> Completato\n'
                                                                                         'Diagrammi salvati in: '
                                                                                         'Output/'+filename_be+'/Diagnosi_steps/'+filename_be+'\n' +
                                                            '> Espressione regolare: ' + exp)
                except IndexError:
                    sg.Popup(
                        'Attenzione, l\'osservazione produce uno spazio comportamentale vuoto. Quindi non ha senso fare un diagnosi.')
                    do_diagnosi_window['output_dia'].update(
                        values['output_dia'] + "--- Calcolo annullato ---")

        # Finish up by removing from the screen
        do_diagnosi_window.close()


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
              [sg.Button('Crea una rete', key='create_net', size=(35, 2)),
               sg.Button('Carica una rete', key='load_net', size=(35, 2))],
              [sg.Button('Carica spazio comportamentale\n(Solo spazi completi)', key='load_space', size=(35, 2)),
               sg.Button('Esegui diagnosi\n(Solo spazi completi)', key='go_diagnosi', size=(35, 2))
               ],
              [sg.Button('Esci')]
              ]

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
        elif event == 'create_net':
            create_network_window()
        elif event == 'load_net':
            try:
                load_network_window()
            except AttributeError:
                sg.Popup('Attenzione!', 'Controlla di aver selezionato il file corretto.')
        elif event == 'load_space':
            load_comportamentalspace_window()
        elif event == 'go_diagnosi':
            do_diagnosi_window()

    # Finish up by removing from the screen
    window.close()
