import copy

from graphviz import Digraph

from Class.Base.FSM import Edge
from Class.Base.space import Node, Space

# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space and creates the space
# - filename: this is the name to save the graph image
# - n1: is the network
# - transitions: is the list of the transitions in the network
from Class.Utils.utils import find_node_by_id, \
    find_node_id_by_label, remove_duplicate


def create_behavioral_space(filename, network, transitions, original_filename):
    Node.count = -1
    # f is the graphviz component to plot the graph
    f = Digraph(filename, format='png')

    space_nodes = []
    space_transitions = []

    # ------------ SETUP ------------

    # Create the list of fsms: name + state's value
    fsms_states = ""
    fsms_states_list = {}
    for fsm in network.fsms:
        fsms_states = fsms_states + " " + fsm.states[0]
        fsms_states_list[fsm.name] = fsm.states[0]

    # Create the list of links: name + state's value
    links_states = ""
    links_states_list = {}
    for link in network.links:
        links_states = links_states + " " + link.state
        links_states_list[link.name] = link.state

    # Create the node label for graphviz: states' value + links' value
    node_label = fsms_states + " " + links_states

    # If a link is empty increase the value of c, if c = i the node is a final node
    i = 0
    c = 0
    for k_link, v_link in links_states_list.items():
        i = i + 1
        if v_link == "-":
            c = c + 1

    # Create the node for the space
    # - fsms_states_list: is the list of the states in the node (name + value)
    # - fsms_states_list: is the list of the links in the node (name + value)
    # - node_label: is the label of the node (fsms's value + links' value) for graphviz
    # - 1/0: if 1 the node is a final node, if 0 it is not a final node
    if c == i:
        node = Node(fsms_states_list, links_states_list, node_label, 1)
        f.node(node_label, shape='doublecircle')
    else:
        node = Node(fsms_states_list, links_states_list, node_label, 0)
        f.node(node_label, shape='circle')

    # Add the node to the space
    space_nodes.append(node)

    # ------------ RECURSION ------------
    find_nodes(node, f, network, transitions, space_nodes, space_transitions)

    # "render" is the function to plot the graph, "directory" is the directory of the save
    f.render(directory="Output/"+original_filename+"/Behavioral_Space")

    # The same space is printend also with the ID, not with LABEL
    # # g is another graphviz component
    g = Digraph(filename + "_id", format='png')

    for transition in space_transitions:
        g.edge(str(transition.source), str(transition.destination), transition.label)

    for node in space_nodes:
        if node.isFinal:
            g.node(str(node.id), shape="doublecircle")
        else:
            g.node(str(node.id), shape="circle")

    g.render(directory="Output/"+original_filename+"/Behavioral_Space")

    # Call the function to add to each node the list of the reachable nodes
    organize_reachable_nodes(space_nodes)

    # Create the space and return it
    # - space_nodes: is the list of nodes in the space
    # - space_transitions: is the list of links between nodes in the space
    space = Space(space_nodes, space_transitions)

    summary = open("Output/"+original_filename+"/Behavioral_Space/space_summary.txt", "w")
    summary.write("Numero di nodi:" + str(len(space_nodes)) + "\n")
    i = 1
    for node in space_nodes:
        summary.write(str(i) + ") id:" + str(node.id) + ", stato:"+str(node.label)+"\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(space_transitions)) + "\n")
    i = 1
    for t in space_transitions:
        summary.write(str(i) + ") " + str(t.source) + " -> " + str(t.label) +"-> " + str(t.destination) + "\n")
        i = i + 1
    summary.close()

    return space

# ------------ INTRO FUNCTION ------------
# This is the recursive function to find nodes from a node in input
# - node: it is the starting point for the search
# - f: graphviz component
# - n1: the network
# - transitions: the list of transitions in the network
# - space_nodes: the nodes in the space at the time of the search
# - space_transitions: the transitions in the space at the time of the search
def find_nodes(node, f, network, transitions, space_nodes, space_transitions):
    # ----------- FIRST PART -----------
    # Find the possible transitions that can click with the space's nodes' and links' states

    # Create the list where to add the transitions that can click
    apply_t = []

    # For each node in the space take the list of fsms --> for each fsm take the name and the state
    # - node.fsms_states.items(): is the list of the states, with their names and state values
    # - fsm_name: is the name of the fsm
    # - fsm_state: is the value of the state of the fsm
    for fsm_name, fsm_state in node.fsms_states.items():
        # For each fsm in the network
        for fsm in network.fsms:
            # If the name is the same use the information of fsm to find if there is an edge that corrisponds to a transition
            if fsm.name == fsm_name:
                # Watch in the edge list
                for edge in fsm.edges:
                    # If the source of the edge is the state of the fsm maybe a transition could click
                    if edge.source == fsm_state:
                        # For each transition in the network
                        for t in transitions:
                            # WARNING: transitions have unique names!
                            # If the label of the transition is the same of the edge it could click, check the links' states
                            if t.label == edge.label:
                                # - node.links_states.items(): is the list of the links, with their name and value
                                # link_name: is  the name of the link
                                # link_state: is the value of the state of the link
                                for link_name, link_state in node.links_states.items():
                                    # For each link we check if the link is empty
                                    if link_state == "-":
                                        # IF EMPTY
                                        # Check the input events
                                        if t.input == {}:
                                            # NO INPUT EVENTS
                                            # Check the output events
                                            if t.output == {}:
                                                # NO OUTPUT EVENTS
                                                # The transition can click, add to the list
                                                apply_t.append(t)
                                            else:
                                                # YES OUTPUT EVENTS
                                                # - t.output: the list of the output events: lin name + event's value
                                                # - target_link_name: the name of the link that the event refers to
                                                for target_link_name, none in t.output.items():
                                                    # Check the link name
                                                    if target_link_name == link_name:
                                                        # If the name of the link is the same of the output link
                                                        # The transition can click, add to the list
                                                        apply_t.append(t)
                                        else:
                                            # YES INPUT EVENTS
                                            # - t.input: the list of the input events: lin name + event's value
                                            # - target_link_name: the name of the link that the event refers to
                                            # - input_event_value: the value of the event
                                            for target_link_name, input_event_value in t.input.items():
                                                # Check the link name
                                                if target_link_name == link_name:
                                                    if input_event_value == "-":
                                                        # Only if the value of the event is empty the transition can click because the link is EMPTY
                                                        # The transition can click, add to the list
                                                        apply_t.append(t)
                                    else:
                                        # FULL
                                        # this is the case where the link state is different from -
                                        if t.input == {}:
                                            # NO INPUT EVENTS
                                            # Check the output events
                                            if t.output == {}:
                                                # NO OUTPUT EVENTS
                                                # The transition can click, add to the list
                                                apply_t.append(t)
                                            else:
                                                # YES OUTPUT EVENTS
                                                # - t.output: the list of the output events: lin name + event's value
                                                # - target_link_name: the name of the link that the event refers to
                                                # - output_event_value: the value of the event
                                                for target_link_name, output_event_value in t.output.items():
                                                    # Check the link name
                                                    if target_link_name == link_name:
                                                        if output_event_value == "-":
                                                            # Only if the value of the event is empty the transition can click because the link is FULL
                                                            # The transition can click, add to the list
                                                            apply_t.append(t)
                                        else:
                                            # YES INPUT EVENTS
                                            # - t.input: the list of the input events: lin name + event's value
                                            # - target_link_name: the name of the link that the event refers to
                                            # - input_event_value: the value of the event
                                            for target_link_name, input_event_value in t.input.items():
                                                # Check the link name
                                                if target_link_name == link_name:
                                                    # Check the link state and input event value required
                                                    if input_event_value == link_state:
                                                        # If the value in the link is te same required as input
                                                        # Check if the output event is empty and if it is not check if it is the same name
                                                        if t.output == {}:
                                                            # NO OUTPUT EVENTS
                                                            # The transition can click, add to the list
                                                            apply_t.append(t)
                                                        else:
                                                            # YES OUTPUT EVENTS
                                                            # - t.output: the list of the output events: lin name + event's value
                                                            # - output_target_link_name: the name of the link that the event refers to
                                                            # - output_event_value: the value of the event
                                                            for output_target_link_name, output_event_value in t.output.items():
                                                                # Check the link name
                                                                if output_target_link_name == link_name:
                                                                    # If the name of the link is the same of the output link
                                                                    if output_event_value == "-":
                                                                        # The transition can click, add to the list
                                                                        apply_t.append(t)
                                                                else:
                                                                    # Check the others links
                                                                    for name_link_inner, state_link_inner in node.links_states.items():
                                                                        # If the name of another link is the same of the output link
                                                                        if output_target_link_name == name_link_inner:
                                                                            if state_link_inner == "-":
                                                                                # The transition can click, add to the list
                                                                                apply_t.append(t)

    # Remove the double from the transitions list
    apply_t = remove_duplicate(apply_t)

    # ----------- SECOND PART -----------
    # Check the transitions that can click and update all the states in nodes

    # For every clickable transition
    for clickable_t in apply_t:

        # Create deep copy to not override the lists
        # In the new_... copy insert the update values
        new_fsms = copy.deepcopy(node.fsms_states)
        new_links = copy.deepcopy(node.links_states)
        # In the node... copy leave the old values
        node_links = copy.deepcopy(node.links_states)
        node_fsms = copy.deepcopy(node.fsms_states)

        # --------- UPDATE LINKS ---------
        # - node_links: list of the links
        # - link_name: name of the link
        # - link_state: state of the link
        for link_name, link_state in node_links.items():
            # - clickable_t.input: list of the input events of clickable_t
            # - input_link: name of the link that the event requires to
            for input_link, none in clickable_t.input.items():
                # Check the name of the link
                if input_link == link_name:
                    # Set the link empty in input, because if it is already empty it remains empty and if it is full becomes empty afer the clic
                    new_links[input_link] = "-"
            # - clickable_t.output: list of the output events of clickable_t
            # - output_link: name of the link that the event requires to
            # - output_event: value of the event
            for output_link, output_event in clickable_t.output.items():
                # Check the name of the link
                if output_link == link_name:
                    # Set the link state to the output event value
                    new_links[output_link] = output_event

        # --------- UPDATE STATES ---------
        # - node_fsms: list of the fsms
        # - name_fsm: name of the fsm
        # - state_fsm: state value of the fsm
        for name_fsm, state_fsm in node_fsms.items():
            # For the fsms in the network
            for fsm in network.fsms:
                # For the edge in the fsm in the network
                for edge in fsm.edges:
                    # If the names are equal AND the label of the edge is the label of the transition AND the source of the edge is the actual fsm (not the network one) state
                    if fsm.name == name_fsm and edge.label == clickable_t.label and edge.source == state_fsm:
                        # Set the fsm state to the edge destination
                        new_fsms[name_fsm] = edge.destination

        # ----------- THIRD PART -----------
        # (In part only for graphviz)
        # Prepare the string for the label
        # String of the status
        status = ""

        for none, fsm_state_value in new_fsms.items():
            status = status + " " + fsm_state_value

        links_status = ""
        for none, link_state_value in new_links.items():
            links_status = links_status + " " + link_state_value

        # Create the label of the new (maybe not, after the check) node
        # Ex: 20 30 e1 e3
        new_node_label = status + " " + links_status

        # space_nodes_old is the actual nodes' space
        # Prepare the labels string
        labels = []
        # Add all the nodes' labels in the list
        for space_node in space_nodes:
            labels.append(space_node.label)

        # Check if the node is already in the list
        if new_node_label in labels:
            # The node is already in the space, don't add it but only the transitions that start from it
            # Set the label of the edge with the label of the transition
            new_edge_label = clickable_t.label
            # Find the node in the space with its label
            node_id = find_node_id_by_label(new_node_label, space_nodes)
            # Create the new transition, like an edge because is more simple
            new_transition = Edge(node.id, new_edge_label, node_id)
            # Add the link to the real transition to the new "transition" (edge)
            new_transition.transition_link = clickable_t
            # Add to the space the new "transition" (edge)
            space_transitions.append(new_transition)
            # Add to the input node a child, the "new" (not new, we discovered it) node id
            node.reachable_nodes.append(node_id)
            # Add the new "transition" (edge) to the node
            node.edges.append(new_transition)
            # Add the edge to f for graphviz
            # WARNING! The order is different from the class Edge, destination and label are switched
            # - node.label: source
            # - new_node_label: destination
            # - clickable_t.label: label
            f.edge(node.label, new_node_label, clickable_t.label)
        else:
            # If a link is empty increase the value of c, if c = i the node is a final node
            i = 0
            c = 0
            for k_link, v_link in new_links.items():
                i = i + 1
                if v_link == "-":
                    c = c + 1

            # Create the node for the space
            # - new_fsms: is the list of the states in the node (name + value)
            # - new_links: is the list of the links in the node (name + value)
            # - new_node_label: is the label of the node (fsms's value + links' value) for graphviz
            # - 1/0: if 1 the node is a final node, if 0 it is not a final node
            if c == i:
                new_node = Node(new_fsms, new_links, new_node_label, 1)
                f.node(new_node_label, shape='doublecircle')
            else:
                new_node = Node(new_fsms, new_links, new_node_label, 0)
                f.node(new_node_label, shape='circle')

            # Set the label of the edge with the label of the transition
            new_edge_label = clickable_t.label
            # Create the new transition, like an edge because is more simple
            new_transition = Edge(node.id, new_edge_label, new_node.id)
            # Add the link to the real transition to the new "transition" (edge)
            new_transition.transition_link = clickable_t
            # Add to the space the new "transition" (edge)
            space_transitions.append(new_transition)
            # Add the new "transition" (edge) to the node
            node.edges.append(new_transition)
            # Add to the input node a child, the new node id
            node.reachable_nodes.append(new_node.id)
            # Add to the space the new node
            space_nodes.append(new_node)
            # Add the edge to f for graphviz
            # WARNING! The order is different from the class Edge, destination and label are switched
            # - node.label: source
            # - new_node_label: destination
            # - clickable_t.label: label
            f.edge(node.label, new_node_label, clickable_t.label)

            # Call the recursive function
            find_nodes(new_node, f, network, transitions, space_nodes, space_transitions)

# ---------------------------------------------------------------------------------------------
# ------------ INTRO FUNCTION ------------
# This is the function to find the reachable_nodes,nodes that are reachable from the input node
# - space_nodes: the nodes in the space at the time of the search
def organize_reachable_nodes(space_nodes):
    # For each node
    for node in space_nodes:

        # Create the list reachable_nodes
        reachable_list = []
        # For each reachable node in the list of reachable_nodes of a node
        for reach in node.reachable_nodes:
            # Add reach to the list
            reachable_list.append(reach)

            # Call the recursive function
            if find_node_by_id(reach, space_nodes) is not None:
                append_reachable_node(reachable_list, find_node_by_id(reach, space_nodes), space_nodes)
        # Update reachable_nodes in the node
        reachable_list = remove_duplicate(reachable_list)

        node.reachable_nodes = reachable_list

# ------------ INTRO FUNCTION ------------
# This is the recursive function to find the reachable_nodes
# - reachable_nodes: the list of reachable_nodes of a node
# - node: the node in input
# - space_nodes: the nodes in the space at the time of the search
def append_reachable_node(reachable_list, node, space_nodes):
    for reach in node.reachable_nodes:
        # If the child is already in the list
        if reach in reachable_list:
            # Find the child node
            if find_node_by_id(reach, space_nodes) is not None:
                reach_node = find_node_by_id(reach, space_nodes)
                # For all the reachable_nodes of the child node
                for reach_inner in reach_node.reachable_nodes:
                    # If the reachable_nodes are not in the list add them
                    if reach_inner not in reachable_list:
                        reachable_list.append(reach_inner)


        else:
            # Add the child
            reachable_list.append(reach)
            # Call the recursive
            append_reachable_node(reachable_list, find_node_by_id(reach, space_nodes), space_nodes)




