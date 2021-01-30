from graphviz import Digraph

from Class.Utils.save_files import save_renomination_file_obs
from Class.Utils.utils import link_to_a_final_obs_re, remove_duplicated_transition_obs


# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space from an observation list and creates the renominated space
# - filename: this is the name to save the graph image
# - space: is the behavioral observable renominated space
def create_behavioral_space_observable_renominated(filename, space, original_filename):
    f = Digraph(filename, format='png')

    # count is the new "id" after the cut and the renomination, this is not an id, but a label
    count = 0
    # Create the list of the cutted nodes, add the nodes that were cutted
    cutted_id = []
    space.nodes_after_cutting = []
    space.cutted_nodes = []
    space.cutted_transitions = []
    space.transitions_after_cutting = []

    for node in space.nodes:
        if node.isFinal or link_to_a_final_obs_re(node, space.nodes):
            space.nodes_after_cutting.append(node)
        else:
            space.cutted_nodes.append(node)
            cutted_id.append((node.id, node.observation_index))

    for node in space.nodes_after_cutting:
        label = str(node.id) + ", " + str(node.observation_index)
        if node.isFinal:
            f.node(label, shape="doublecircle")
        else:
            f.node(label, shape="circle")

    for node in space.cutted_nodes:
        label = str(node.id) + ", " + str(node.observation_index)
        f.node(label, shape="circle")

    for transition in space.transitions:
        if (transition.source.id, transition.source.observation_index) in cutted_id:
            space.cutted_transitions.append(transition)
        elif (transition.destination.id, transition.destination.observation_index) in cutted_id:
            space.cutted_transitions.append(transition)
        else:
            space.transitions_after_cutting.append(transition)

    remove_duplicated_transition_obs(space.transitions_after_cutting)

    # This part is for graphviz, to print in a good style the graph
    for transition in space.transitions_after_cutting:
        source = str(transition.source.id) + ", " + str(transition.source.observation_index)
        destination = str(transition.destination.id) + ", " + str(transition.destination.observation_index)
        f.edge(source, destination,
               label='<' + transition.label + " " + '<FONT COLOR="grey">' + str(
                   transition.observation_index) + '</FONT>' + " " + '<FONT COLOR="blue">' + str(
                   transition.observability_label) + '</FONT>' + " " + '<FONT COLOR="red">' + str(
                   transition.relevance_label) + '</FONT>>')

    f.render(directory="Output/"+original_filename+"/Behavioral_Space_Observable_Renominated")
    save_renomination_file_obs(space, "Output/" + original_filename + "/Behavioral_Space_Observable_Renominated/RL_" + filename + ".txt")

    summary = open("Output/"+original_filename+"/Behavioral_Space_Observable_Renominated/space_summary.txt", "w")
    summary.write("Numero di nodi:" + str(len(space.nodes_after_cutting)) + "\n")
    i = 1
    for node in space.nodes_after_cutting:
        summary.write(str(i) + ") " + str(node.id)+", "+str(node.observation_index)+ "\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(space.transitions_after_cutting)) + "\n")
    i = 1
    for t in space.transitions_after_cutting:
        summary.write(
            str(i) + ") " + str(t.source.link_node.id) + ", " + str(t.source.observation_index) + " -> " + str(
                t.label) + "-> " + str(t.destination.link_node.id) + ", " + str(
                t.destination.observation_index) + "\n")
        i = i + 1
    summary.close()
    return space