import PySimpleGUI as sg

from Class.Base import space, graphic, network, FSM


def load_fsm(pass_window, fsms, filename):
    try:
        f1 = FSM.read_fsm_from_txt()
        fsms.append(f1)
        graphic.draw_FSM_graphic(f1, filename)
        names = ""
        for fsm in fsms:
            names = names + fsm.name + ", "
        names = names[:-2]
        pass_window['output_fsms'].update(names)
        pass_window['show_fsms'].update(disabled=False)
        pass_window['delete_fsms'].update(disabled=False)
        pass_window['load_link'].update(disabled=False)
    except IndexError:
        sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
    except FileNotFoundError:
        pass
    except TypeError:
        pass


def remove_fsm(pass_window, fsms):
    fsms.clear()
    pass_window['output_fsms'].update("")
    pass_window['output_link'].update("")
    pass_window['output_transitions'].update("")

    pass_window['delete_fsms'].update(disabled=True)

    pass_window['load_link'].update(disabled=True)
    pass_window['load_transitions'].update(disabled=True)

    pass_window['show_fsms'].update(disabled=True)
    pass_window['create_network'].update(disabled=True)


def show_fsm_graph(fsms, filename):
    images = []
    text = []
    for i in range(int(len(fsms))):
        images.append(sg.Image(filename='Output/'+filename+'/FSM_graph/fsm' + fsms[i].name + '.png'))
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


def load_links(pass_window):
    try:
        links = network.read_link_from_txt()
        text = ""
        for l in links:
            text = text + str(l.name) + " " + str(l.source) + " " + str(l.destination) + " " + str(
                l.state) + "\n"

        pass_window['output_link'].update(text)
        pass_window['load_transitions'].update(disabled=False)
        return links
    except IndexError:
        sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
    except FileNotFoundError:
        pass
    except TypeError:
        pass


def load_transitions(pass_window):
    try:
        transitions = space.read_transitions_from_txt()
        print_T = ""
        for transition in transitions:
            print_T = print_T + str(transition.label) + ", " + str(transition.input) + ", " + str(
                transition.output) + ",  " + str(
                transition.relevance_label) + ", " + str(
                transition.observability_label) + "\n"

        pass_window['output_transitions'].update(print_T)
        pass_window['save_filename'].update(disabled=False)
        return transitions
    except IndexError:
        sg.Popup('Attenzione!', 'Il file potrebbe non essere quello corretto o avere degli errori di sintassi!')
    except FileNotFoundError:
        pass
    except TypeError:
        pass
