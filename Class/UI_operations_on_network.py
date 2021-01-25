import copy

import PySimpleGUI as sg
from graphviz import Digraph

from Class import FSM, graphic, network, comportamentalSpace


def calculate_behavioral_space(pass_window, filename, transitions, n):
    filename_be = filename + '_BS'
    full_space = graphic.create_behavioral_space(filename_be, n, transitions, filename)
    global old_full_space
    old_full_space = copy.deepcopy(full_space)
    pass_window['ren_be'].update(disabled=False)
    pass_window['be_diag'].update(disabled=False)
    pass_window['save_be_space'].update(disabled=False)
    return filename_be, full_space


def show_behavioral_space(filename_be, original_filename, type=0):
    behavioral_layout = [[]]
    if type == 0:
        column1 = [[sg.Text('Spazio con LABEL')],
                   [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space/' + filename_be + '.gv.png')]]
        column2 = [[sg.Text('Spazio con ID')],
                   [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space/' + filename_be + '_id.gv.png')]]
        behavioral_layout = [
            [
                sg.Column(column1, size=(600, 800), scrollable=True),
                sg.Column(column2, size=(600, 800), scrollable=True)
            ]
        ]
    elif type == 1:
        column2 = [[sg.Text('Spazio con ID')],
                   [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space/' + filename_be + '.gv.png')]]
        behavioral_layout = [
            [
                sg.Column(column2, size=(600, 800), scrollable=True)
            ]
        ]
    behavioral_window = sg.Window('Diagramma spazio comportamentale', behavioral_layout, resizable=True)
    while True:
        event, values = behavioral_window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break


def calculate_behavioral_space_renominated(pass_window, filename, full_space, loaded):
    filename_re_be = filename + '_RS'
    full_space_r = graphic.create_behavioral_space_renominated(filename_re_be, full_space, loaded, filename)
    global old_re_space
    old_re_space = copy.deepcopy(full_space_r)
    pass_window['be_re_diag'].update(disabled=False)
    pass_window['renomination_file_be'].update(disabled=False)
    pass_window['input_btn'].update(disabled=False)
    pass_window['refresh'].update(disabled=False)
    pass_window['save_be_re_space'].update(disabled=False)
    return filename_re_be, full_space_r


def show_re_be_space(filename_re_be, filename_be, original_filename, type=0):
    filename = ""

    column_re1 = [[sg.Text('Spazio con ID rinominati')],
                  [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space_Renominated/' + filename_re_be + '.gv.png')]]
    column_re2 = [[sg.Text('Spazio con ID vecchi')],
                  [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space_Renominated/' + filename_re_be + '_old_id.gv.png')]]

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
            show_renomination_file_be(filename_re_be, filename_be, original_filename,type)


def show_renomination_file_be(filename_re_be, filename_be, original_filename, type=0):
    file = open(file="Output/"+original_filename+"/Behavioral_Space_Renominated/RL_" + filename_re_be + ".txt")
    renomination_be_layout = [
        [
            sg.Button('Vedi diagramma', key='be_re_diag')
        ],
        [sg.Column([[sg.Text(file.read())]], scrollable=True)]
    ]

    show_re_be_window = sg.Window('File di renominazione dello spazio comportamentale',
                                  renomination_be_layout, resizable=True)
    while True:
        event, values = show_re_be_window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'be_re_diag':
            show_re_be_space(filename_re_be, filename_be,original_filename, type)

    show_re_be_window.close()


def check_obs_insert(string_obs, pass_window):
    try:
        obs = string_obs.split(",")
        pass_window['calc_obs'].update(disabled=False)
        pass_window['ren_obs'].update(disabled=True)
        pass_window['diag'].update(disabled=True)
        pass_window['obs_diag'].update(disabled=True)
        pass_window['obs_re_diag'].update(disabled=True)
        pass_window['renomination_file_obs'].update(disabled=True)
        return obs
    except IndexError:
        sg.Popup('Attenzione!', 'Controlla di aver inserito l\'osservazione in modo corretto.')


def check_obs_insert_dia(string_obs, pass_window):
    try:
        obs = string_obs.split(",")
        pass_window['diag'].update(disabled=False)
        return obs
    except IndexError:
        sg.Popup('Attenzione!', 'Controlla di aver inserito l\'osservazione in modo corretto.')


def refresh_obs(pass_window):
    pass_window['calc_obs'].update(disabled=True)
    pass_window['ren_obs'].update(disabled=True)
    pass_window['diag'].update(disabled=True)
    pass_window['obs_diag'].update(disabled=True)
    pass_window['obs_re_diag'].update(disabled=True)

    pass_window['renomination_file_obs'].update(disabled=True)
    pass_window['save_obs_space'].update(disabled=True)
    pass_window['save_obs_re_space'].update(disabled=True)


def refresh_obs_diagnosi(pass_window):
    pass_window['diag'].update(disabled=True)


def calculate_obs_space(pass_window, filename, full_space_r, obs):
    filename_obs = filename + '_OS'
    obs_full_space = graphic.create_behavioral_space_from_obs(filename_obs, obs, full_space_r, filename)
    global old_obs_space
    old_obs_space = copy.deepcopy(obs_full_space)
    pass_window['ren_obs'].update(disabled=False)
    pass_window['obs_diag'].update(disabled=False)
    pass_window['save_obs_space'].update(disabled=False)
    return obs_full_space, filename_obs


def show_obs_space(obs, filename_obs, original_filename,):
    obs_name = ""
    for o in obs:
        obs_name = obs_name + o + " "

    column_ob1 = [[sg.Text('Diagramma con id')],
                  [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space_Observable/' + filename_obs + '.gv.png')]]
    column_ob2 = [[sg.Text('Diagramma con stati')],
                  [sg.Image(filename='Output/'+original_filename+'/Behavioral_Space_Observable/' + filename_obs + '_state.gv.png')]]

    obs_layout = [

        [
            sg.Text("L'osservazione considerata è:\n" + obs_name)
        ],
        [
            sg.Column(column_ob1, size=(600, 800), scrollable=True),
            sg.Column(column_ob2, size=(600, 800), scrollable=True)
        ]
    ]
    obs_window = sg.Window('Diagramma spazio comportamentale data un\'osservazione', obs_layout)
    while True:
        event, values = obs_window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break


def calculate_obs_space_renominated(pass_window, filename, obs_full_space, obs):
    filename_re_obs = filename + '_ROS'
    obs_space_r = graphic.create_behavioral_space_observable_renominated(filename_re_obs, obs_full_space, obs, filename)
    global old_re_obs_space
    old_re_obs_space = copy.deepcopy(obs_space_r)
    pass_window['diag'].update(disabled=False)
    pass_window['obs_re_diag'].update(disabled=False)
    pass_window['renomination_file_obs'].update(disabled=False)
    pass_window['save_obs_re_space'].update(disabled=False)
    return obs_space_r, filename_re_obs


def show_re_obs_space(obs, filename_re_obs, original_filename):
    column_re_ob1 = [
        [sg.Image(
            filename='Output/'+original_filename+'/Behavioral_Space_Observable_Renominated/' + filename_re_obs + '.gv.png')]]

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
            show_renomination_file_obs(obs, filename_re_obs, original_filename)


def show_renomination_file_obs(obs, filename_re_obs,  original_filename):
    file = open(
        file="Output/"+original_filename+"/Behavioral_Space_Observable_Renominated/RL_" + filename_re_obs + ".txt")
    renomination_obs_layout = [
        [
            sg.Button('Vedi diagramma', key='obs_re_diag')
        ],
        [sg.Column([[sg.Text(file.read())]], scrollable=True)]
    ]

    show_re_obs_window = sg.Window('File di renominazione dello spazio comportamentale data osservazione',
                                   renomination_obs_layout,resizable=True)
    while True:
        event, values = show_re_obs_window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'obs_re_diag':
            show_re_obs_space(obs, filename_re_obs, original_filename)

    show_re_obs_window.close()


def calculate_diagnosi_space(pass_window, filename, obs_space_r, obs):
    n_img, exp = graphic.create_diagnosis_for_space_observable_renominated(filename, obs_space_r, obs)
    return n_img, exp


def save_be_space_as_JSON(filename, original_filename):
    comportamentalSpace.save_space_as_json(old_full_space, filename, original_filename)


def save_be_re_space_as_JSON(filename, original_filename):
    comportamentalSpace.save_space_as_json(old_re_space, filename, original_filename)


def save_obs_space_as_JSON(filename, original_filename):
    comportamentalSpace.save_space_as_json(old_obs_space, filename, original_filename)


def save_obs_re_space_as_JSON(filename, original_filename):
    comportamentalSpace.save_space_as_json(old_re_obs_space, filename, original_filename)


def load_comportamental_space(pass_window):
    full_space, filename_be = comportamentalSpace.read_space_from_json()
    graphic.draw_comportamental_space(filename_be, full_space)
    pass_window['input_btn'].update(disabled=False)
    pass_window['refresh'].update(disabled=False)
    return full_space, filename_be


def calculate_all(pass_window, full_space, filename, obs):
    filename_re_be = filename + '_RS'
    full_space_r = graphic.create_behavioral_space_renominated(filename_re_be, full_space, True, filename)
    filename_obs = filename + '_OS'
    obs_full_space = graphic.create_behavioral_space_from_obs(filename_obs, obs, full_space_r,filename)
    filename_re_obs = filename + '_ROS'
    obs_space_r = graphic.create_behavioral_space_observable_renominated(filename_re_obs, obs_full_space, obs,filename)
    filename_dia = filename + '_DS'
    n_img, exp = graphic.create_diagnosis_for_space_observable_renominated(filename, obs_space_r, obs)
    # pass_window['save_diagnosi_space'].update(disabled=False)
    return n_img, exp
