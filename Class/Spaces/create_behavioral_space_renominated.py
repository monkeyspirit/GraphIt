from graphviz import Digraph

from Class.Utils.save_files import save_renomination_file
from Class.Utils.utils import link_to_a_final, remove_duplicate, find_node_by_id, get_new_id_by_old_id

# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space renominated and creates the renominated space
# - filename: this is the name to save the graph image
# - space: is the behavioral space
def create_behavioral_space_renominated(filename, space, loaded, original_filename):
    # f is the graphviz component to plot the graph
    f = Digraph(filename, format='png')

    # count is the new "id" after the cut and the renomination, this is not an id, but a label
    count = 0
    # Create the list of the cutted nodes, add the nodes that were cutted
    cutted_id = []
    # For each node in the space
    for node in space.nodes:
        # If the node is a final node or from the node it is possible to reach a final node than keep it
        if node.isFinal or link_to_a_final(node, space.nodes):
            # Set the renomination label
            node.renomination_label = count
            # nodes_after_cutting is the list of the nodes that are keeped
            # Add the node to the list of node that are keeped
            space.nodes_after_cutting.append(node)
            count += 1
        else:
            # If the node is not a final node or not reach a final node
            # cutted_nodes is the list of node that are cutted from the space after renomination
            # Add the node to the list of nodes that are cutted
            space.cutted_nodes.append(node)
            # Add the id of the node that is cutted to the list of the ids of the nodes that are cutted
            cutted_id.append(node.id)

    # Remove duplicated transitions from the space
    space.transitions = remove_duplicate(space.transitions)
    space.nodes = remove_duplicate(space.nodes)
    space.nodes_after_cutting = remove_duplicate(space.nodes_after_cutting)

    # For each transition in the space
    for transition in space.transitions:
        # cutted_transitions is the list of the cutted transitions
        if (transition.source in cutted_id) or (transition.destination in cutted_id):
            # If the source of the transition or the destination is in the list of cutted ids nodes, add the transition of the list of the cutted transitions
            space.cutted_transitions.append(transition)
        else:
            # Else keep the transition and add that to the list of transitions that are keeped
            transition.source = find_node_by_id(transition.source, space.nodes_after_cutting).renomination_label
            transition.destination = find_node_by_id(transition.destination, space.nodes_after_cutting).renomination_label
            space.transitions_after_cutting.append(transition)

    space.transitions_after_cutting = remove_duplicate(space.transitions_after_cutting)

    for node in space.nodes_after_cutting:
        node.old_id = node.id
        node.id = node.renomination_label

    if loaded:
        for node in space.nodes_after_cutting:
            edges = node.edges
            new_edges = []
            for edge in edges:
                if edge.source not in cutted_id and edge.destination not in cutted_id:
                    edge.source = get_new_id_by_old_id(edge.source, space.nodes)
                    edge.destination = get_new_id_by_old_id(edge.destination, space.nodes)
                    new_edges.append(edge)
            node.edges = new_edges



    # This part is for graphviz, to print the graph well
    # For each transition that was keeped
    for transition_after in space.transitions_after_cutting:

        # In this part the code is only for the printing on the graph of the observability and relevance label
        if transition_after.transition_link.observability_label == "ϵ" and transition_after.transition_link.relevance_label == "ϵ":
            f.edge(str(transition_after.source), str(transition_after.destination), label=str(transition_after.label))

        elif transition_after.transition_link.observability_label != "ϵ" and transition_after.transition_link.relevance_label == "ϵ":
            f.edge(str(transition_after.source), str(transition_after.destination), label='<' + str(
                transition_after.label) + " " + '<FONT COLOR="green">' + str(
                transition_after.transition_link.observability_label) + '</FONT>>')

        elif transition_after.transition_link.observability_label == "ϵ" and transition_after.transition_link.relevance_label != "ϵ":
            f.edge(str(transition_after.source), str(transition_after.destination), label='<' + str(
                transition_after.label) + " " + '<FONT COLOR="red">' + str(
                transition_after.transition_link.relevance_label) + '</FONT>>')

        else:
            f.edge(str(transition_after.source), str(transition_after.destination), label='<' + str(
                transition_after.label) + " " + '<FONT COLOR="red">' + str(
                transition_after.transition_link.relevance_label) + '</FONT>' + '<FONT COLOR="green">' + str(
                transition_after.transition_link.observability_label) + '</FONT>>')

    # This part is for graphviz, to print the graph well
    # For each node that was keeped
    for node in space.nodes_after_cutting:
        if node.isFinal:
            f.node(str(node.id), shape="doublecircle")
        else:
            f.node(str(node.id), shape="circle")

    for node in space.cutted_nodes:
        f.node(str(node.id), shape="circle")
    # Print the graph
    f.render(directory="Output/"+original_filename+"/Behavioral_Space_Renominated")
    # Save the file with the list of the renomination label, the old id, the nodes that are keeped and not

    save_renomination_file(space, "Output/" + original_filename + "/Behavioral_Space_Renominated/RL_" + filename + ".txt")

    g = Digraph(filename+'_old_id', format='png')
    for node in space.nodes_after_cutting:
        if node.isFinal:
            g.node(str(node.old_id), shape="doublecircle")
        else:
            g.node(str(node.old_id), shape="circle")

    for node in space.cutted_nodes:
        g.node(str(node.id), shape="circle")

    for transition_after in space.transitions_after_cutting:
        source = find_node_by_id(transition_after.source, space.nodes_after_cutting).old_id
        destination = find_node_by_id(transition_after.destination, space.nodes_after_cutting).old_id
        # In this part the code is only for the printing on the graph of the observability and relevance label
        if transition_after.transition_link.observability_label == "ϵ" and transition_after.transition_link.relevance_label == "ϵ":
            g.edge(str(source), str(destination), label=str(transition_after.label))

        elif transition_after.transition_link.observability_label != "ϵ" and transition_after.transition_link.relevance_label == "ϵ":
            g.edge(str(source), str(destination), label='<' + str(
                transition_after.label) + " " + '<FONT COLOR="green">' + str(
                transition_after.transition_link.observability_label) + '</FONT>>')

        elif transition_after.transition_link.observability_label == "ϵ" and transition_after.transition_link.relevance_label != "ϵ":
            g.edge(str(source), str(destination), label='<' + str(
                transition_after.label) + " " + '<FONT COLOR="red">' + str(
                transition_after.transition_link.relevance_label) + '</FONT>>')

        else:
            g.edge(str(source), str(destination), label='<' + str(
                transition_after.label) + " " + '<FONT COLOR="red">' + str(
                transition_after.transition_link.relevance_label) + '</FONT>' + '<FONT COLOR="green">' + str(
                transition_after.transition_link.observability_label) + '</FONT>>')
    g.render(directory="Output/"+original_filename+"/Behavioral_Space_Renominated")

    summary = open("Output/"+original_filename+"/Behavioral_Space_Renominated/space_summary.txt", "w")
    summary.write("Numero di nodi:" + str(len(space.nodes_after_cutting)) + "\n")
    i = 1
    for node in space.nodes_after_cutting:
        summary.write(str(i) + ") id:" + str(node.id) + ", stato:"+str(node.label)+ "\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(space.transitions_after_cutting)) + "\n")
    i = 1
    for t in space.transitions_after_cutting:
        summary.write(str(i) + ") " + str(t.source) + " -> " + str(t.label) +"-> " + str(t.destination) + "\n")
        i = i + 1
    summary.close()
    return space