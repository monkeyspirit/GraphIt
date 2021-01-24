import PySimpleGUI as sg

from Class import FSM, graphic, network, comportamentalSpace

def show_fsm_graph(n1, filename):
    global name_fsm_images

    name_fsm_images = []

    for fsm in n1.fsms:
        name_fsm_images.append(fsm.name)

    images = []
    text = []
    for i in range(len(name_fsm_images)):
        images.append(sg.Image(filename='Output'+filename+'FSM_graph/fsm' + name_fsm_images[i] + '.png'))
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
