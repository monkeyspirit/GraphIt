from tkinter import filedialog
from graphviz import Digraph


def draw_graphic_from_txt_file(event=None):
    f = Digraph('finite_state_machine', filename='fsm', format='png')

    filename = filedialog.askopenfilename()

    i = open(filename, "r")
    name = i.readline()
    name = name[:-1]

    s = i.readline()
    s = s[:-1]
    states = s.split(",")
    for state in states:
        f.node(state, shape='circle')

    final_states = i.readline()
    if final_states != [] and final_states != "":
        final_states = final_states[:-1]
        f.node(final_states, shape='doublecircle')

    t = i.readline()
    edges = t.split("/")
    for edge in edges:
        array_edge = edge.split(",")
        f.edge(array_edge[0], array_edge[1], array_edge[2])
    i.close()

    f.render(directory="Output/FSM_graph")

    return name, states, final_states, edges


def draw_FSM_graphic(fsm, filename):
    f = Digraph('finite_state_machine', filename='fsm' + fsm.name, format='png')

    for state in fsm.states:
        f.node(state, shape='circle')

    for state in fsm.final_states:
        if state != "":
            f.node(state, shape='doublecircle')

    for edge_fsm in fsm.edges:
        f.edge(edge_fsm.source, edge_fsm.destination, edge_fsm.label)

    f.render(directory="Output/"+filename+"/FSM_graph")

    summary = open("Output/"+filename+"/FSM_graph/"+fsm.name+"_summary.txt", "w")
    summary.write("Numero di stati:"+str(len(fsm.states))+"\n")
    i = 1
    for state in fsm.states:
        summary.write(str(i)+") " + str(state) + "\n")
        i=i+1
    summary.write("Numero di transizioni:" + str(len(fsm.edges)) + "\n")
    i=1
    for e in fsm.edges:
        summary.write(str(i)+") " + str(e.source)+" -> "  +e.label+" -> "  +e.destination+ "\n")
        i=i+1
    summary.close()


def draw_network_graphic(network, filename):
    f = Digraph('network', filename='network_' + filename, format='png')

    for fsm in network.fsms:
        f.node(fsm.name, shape='box')

    for link in network.links:
        f.edge(link.source, link.destination, link.name)

    f.render(directory="Output/"+filename+"/Network_graph")

    summary = open("Output/"+filename+"/Network_graph/network_summary.txt", "w")
    summary.write("Numero di automi:" + str(len(network.fsms)) + "\n")
    i = 1
    for fsm in network.fsms:
        summary.write(str(i) + ") " + str(fsm.name) + "\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(network.links)) + "\n")
    i = 1
    for l in network.links:
        summary.write(str(i) + ") " + str(l.source) + " -> " + str(l.name) + " -> " + str(l.destination) + "\n")
        i = i + 1
    summary.close()


def draw_network_graphic_from_load_network(n1, names, filename):
    f = Digraph('network', filename='network_' + names, format='png')

    for fsm in n1.fsms:
        f.node(fsm.name, shape='box')

    for link in n1.links:
        f.edge(link.source, link.destination, link.name)

    f.render(directory="Output/"+filename+"/Network_graph")

    summary = open("Output/"+filename+"/Network_graph/network_summary.txt", "w")
    summary.write("Numero di automi:" + str(len(n1.fsms)) + "\n")
    i = 1
    for fsm in n1.fsms:
        summary.write(str(i) + ") " + str(fsm.name) + "\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(n1.links)) + "\n")
    i = 1
    for l in n1.links:
        summary.write(str(i) + ") " + str(l.source) + " -> " + str(l.name) + " -> " + str(l.destination) + "\n")
        i = i + 1
    summary.close()


def draw_comportamental_space(name, space):
    g = Digraph(name, format='png')

    for transition in space.transitions:
        g.edge(str(transition.source), str(transition.destination), transition.label)

    for node in space.nodes:
        if node.isFinal:
            g.node(str(node.id), shape="doublecircle")
        else:
            g.node(str(node.id), shape="circle")

    g.render(directory="Output/"+name+"/Behavioral_Space")
