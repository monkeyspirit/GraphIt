import copy
from tkinter import filedialog
from graphviz import Digraph
from Class.FSM import Edge
from Class.comportamentalSpace import Space, Node, ObservableNode, ObservableTransition, E_transition


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


def draw_FSM_graphic(fsm):
    f = Digraph('finite_state_machine', filename='fsm' + fsm.name, format='png')

    for state in fsm.states:
        f.node(state, shape='circle')

    for state in fsm.final_states:
        if state != "":
            f.node(state, shape='doublecircle')

    for edge_fsm in fsm.edges:
        f.edge(edge_fsm.source, edge_fsm.destination, edge_fsm.label)

    f.render(directory="Output/FSM_graph")


def draw_network_graphic(n1):
    f = Digraph('network', filename='network' + n1.fsms[0].name + n1.fsms[1].name, format='png')

    for fsm in n1.fsms:
        f.node(fsm.name, shape='box')

    for link in n1.links:
        f.edge(link.source, link.destination, link.name)

    f.render(directory="Output/Network_graph")


def draw_network_graphic_from_load_network(n1, filename):
    f = Digraph('network', filename='network' + filename, format='png')

    for fsm in n1.fsms:
        f.node(fsm.name, shape='box')

    for link in n1.links:
        f.edge(link.source, link.destination, link.name)

    f.render(directory="Output/Network_graph")


# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space and creates the space
# - filename: this is the name to save the graph image
# - n1: is the network
# - transitions: is the list of the transitions in the network
def create_behavioral_space(filename, n1, transitions):
    Node.count = -1
    # f is the graphviz component to plot the graph
    f = Digraph(filename, format='png')

    space_nodes = []
    space_transitions = []

    # ------------ SETUP ------------

    # Create the list of fsms: name + state's value
    fsms_states = ""
    fsms_states_list = {}
    for fsm in n1.fsms:
        fsms_states = fsms_states + " " + fsm.states[0]
        fsms_states_list[fsm.name] = fsm.states[0]

    # Create the list of links: name + state's value
    links_states = ""
    links_states_list = {}
    for link in n1.links:
        links_states = links_states + " " + link.state
        links_states_list[link.name] = link.state

    # Create the node label for graphviz: states' value + links' value
    node_label = fsms_states + " " + links_states

    # If a link is empty increase the value of c, if c = i the node is a final node
    i = 0
    c = 0
    for k_link, v_link in links_states_list.items():
        i = i + 1
        if v_link == "ϵ":
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
    find_nodes(node, f, n1, transitions, space_nodes, space_transitions)

    # "render" is the function to plot the graph, "directory" is the directory of the save
    f.render(directory="Output/Behavioral_Space")

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

    g.render(directory="Output/Behavioral_Space")

    # Call the function to add to each node the list of the reachable nodes
    organize_reachable_nodes(space_nodes)

    # Create the space and return it
    # - space_nodes: is the list of nodes in the space
    # - space_transitions: is the list of links between nodes in the space
    space = Space(space_nodes, space_transitions)

    return space


# ------------ INTRO FUNCTION ------------
# This is the recursive function to find nodes from a node in input
# - node: it is the starting point for the search
# - f: graphviz component
# - n1: the network
# - transitions: the list of transitions in the network
# - space_nodes: the nodes in the space at the time of the search
# - space_transitions: the transitions in the space at the time of the search
def find_nodes(node, f, n1, transitions, space_nodes, space_transitions):
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
        for fsm in n1.fsms:
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
                                    if link_state == "ϵ":
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
                                                    if input_event_value == "ϵ":
                                                        # Only if the value of the event is empty the transition can click because the link is EMPTY
                                                        # The transition can click, add to the list
                                                        apply_t.append(t)
                                    else:
                                        # FULL
                                        # this is the case where the link state is different from ϵ
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
                                                        if output_event_value == "ϵ":
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
                                                                    if output_event_value == "ϵ":
                                                                        # The transition can click, add to the list
                                                                        apply_t.append(t)
                                                                else:
                                                                    # Check the others links
                                                                    for name_link_inner, state_link_inner in node.links_states.items():
                                                                        # If the name of another link is the same of the output link
                                                                        if output_target_link_name == name_link_inner:
                                                                            if state_link_inner == "ϵ":
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
                    new_links[input_link] = "ϵ"
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
            for fsm in n1.fsms:
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
                if v_link == "ϵ":
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
            find_nodes(new_node, f, n1, transitions, space_nodes, space_transitions)


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


# ---------------------------------------------------------------------------------------------


# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space renominated and creates the renominated space
# - filename: this is the name to save the graph image
# - space: is the behavioral space
def create_behavioral_space_renominated(filename, space):
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

    # Print the graph
    f.render(directory="Output/Behavioral_Space_Renominated")
    # Save the file with the list of the renomination label, the old id, the nodes that are keeped and not

    save_renomination_file(space, "Output/Behavioral_Space_Renominated/RL_" + filename + ".txt")

    g = Digraph(filename+'_old_id', format='png')
    for node in space.nodes_after_cutting:
        if node.isFinal:
            g.node(str(node.old_id), shape="doublecircle")
        else:
            g.node(str(node.old_id), shape="circle")

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
    g.render(directory="Output/Behavioral_Space_Renominated")
    return space


# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space from an observation list and creates the space
# - filename: this is the name to save the graph image
# - obs: is the list of the observations
# - space: is the behavioral renominated space
def create_behavioral_space_from_obs(filename, obs, space):

    # Create the list of the nodes that are reached from the observations
    obs_space_nodes = []
    # Create the list of the transitions that are reached from the observations
    obs_space_transitions = []
    # Create the component for graphviz
    f = Digraph(filename, format='png')

    observation_index = 0
    first_node = space.nodes_after_cutting[0]
    new_node = ObservableNode(first_node, first_node.id, observation_index)

    find_obs_nodes(new_node, obs_space_nodes, obs_space_transitions, obs, space, 0)

    organize_reachable_nodes_obs(obs_space_nodes)

    obs_space_nodes, obs_space_transitions = cut_not_complete(obs, obs_space_nodes, obs_space_transitions)

    remove_duplicated_transition_obs(obs_space_transitions)
    for transition in obs_space_transitions:
        source = str(transition.source.id) + ", " + str(transition.source.observation_index)
        destination = str(transition.destination.id) + ", " + str(transition.destination.observation_index)
        f.edge(source, destination,
               label='<' + transition.label + " " + '<FONT COLOR="grey">' + str(
                   transition.observation_index) + '</FONT>' + " " + '<FONT COLOR="blue">' + str(
                   transition.observability_label) + '</FONT>>')

    for node in obs_space_nodes:
        if node.observation_index >= len(obs) and node.link_node.isFinal:
            node.isFinal = True

    for node in obs_space_nodes:
        label = str(node.id) + ", " + str(node.observation_index)
        if node.isFinal:
            f.node(label, shape="doublecircle")
        else:
            f.node(label, shape="circle")

    # Print the graph
    f.render(directory="Output/Behavioral_Space_Observable")

    g = Digraph(filename+'_state', format='png')
    for node in obs_space_nodes:
        if node.isFinal:
            g.node(node.link_node.label+", " + str(node.observation_index), shape="doublecircle")
        else:
            g.node(node.link_node.label+", " + str(node.observation_index), shape="circle")

    for transition in obs_space_transitions:

        source = str(transition.source.link_node.label)+ ", " + str(transition.source.observation_index)
        destination = str(transition.destination.link_node.label)+ ", " + str(transition.destination.observation_index)
        g.edge(source, destination,
               label='<' + transition.label + " " + '<FONT COLOR="grey">' + str(
                   transition.observation_index) + '</FONT>' + " " + '<FONT COLOR="blue">' + str(
                   transition.observability_label) + '</FONT>>')

    g.render(directory="Output/Behavioral_Space_Observable")

    obs_space = Space(obs_space_nodes, obs_space_transitions)

    return obs_space


def cut_not_complete(obs, nodes, transitions):
    l = len(obs)
    nodes_to_remove = []
    transitions_to_remove = []
    for node in nodes:
        if node.reachable_nodes != []:
            c = 0
            for reachable in node.reachable_nodes:
                reach_split = reachable.split(", ")
                if int(reach_split[1]) == l:
                    c = 1

            if c == 0:
                nodes_to_remove.append(node)

    nodes_to_remove = remove_duplicate(nodes_to_remove)

    new_list_node = []
    new_list_transitions = []

    for node in nodes:
        if node not in nodes_to_remove:
            new_list_node.append(node)

    for t in transitions:
        if t.source not in nodes_to_remove and t.destination not in nodes_to_remove:
            new_list_transitions.append(t)

    for new_node in new_list_node:
        new_reach = []
        if nodes_to_remove:
            for remove in nodes_to_remove:
                for child in new_node.reachable_nodes:
                    split = child.split(", ")
                    if remove.id != int(split[0]) and remove.observation_index != int(split[1]):
                        print(child)
                    new_reach.append(child)
        else:
            new_reach = new_node.reachable_nodes

        new_reach = remove_duplicate(new_reach)
        new_node.reachable_nodes = new_reach

    return [new_list_node, new_list_transitions]


# ------------ INTRO FUNCTION ------------
def find_obs_nodes(node, obs_space_nodes, obs_space_transitions, obs, space, i):
    observation_index = node.observation_index
    if node not in obs_space_nodes:
        obs_space_nodes.append(node)

    for edge in node.link_node.edges:
        if i == 0:
            if edge.transition_link.observability_label == obs[i]:
                if find_node_by_id(edge.destination, space.nodes_after_cutting) is not None:
                    next_node = ObservableNode(find_node_by_id(edge.destination, space.nodes_after_cutting),
                                               edge.destination, observation_index + 1)

                    obs_space_nodes.append(next_node)
                    reached = str(next_node.id) + ", " + str(observation_index + 1)
                    node.reachable_nodes.append(reached)

                    node.direct_reachable.append(reached)
                    new_transition = ObservableTransition(edge.transition_link.label, observation_index + 1, node,
                                                          next_node, edge.transition_link.observability_label,
                                                          edge.transition_link.relevance_label)
                    obs_space_transitions.append(new_transition)
                    find_obs_nodes(next_node, obs_space_nodes, obs_space_transitions, obs, space, i + 1)
        else:

            if i < len(obs):

                if edge.transition_link.observability_label == obs[i]:
                    if find_node_by_id(edge.destination, space.nodes_after_cutting) is not None:
                        next_node = ObservableNode(find_node_by_id(edge.destination, space.nodes_after_cutting),
                                                   edge.destination, observation_index + 1)

                        obs_space_nodes.append(next_node)

                        new_transition = ObservableTransition(edge.transition_link.label, observation_index + 1, node,
                                                              next_node, edge.transition_link.observability_label,
                                                              edge.transition_link.relevance_label)
                        obs_space_transitions.append(new_transition)
                        reached = str(next_node.id) + ", " + str(observation_index + 1)
                        node.reachable_nodes.append(reached)
                        node.direct_reachable.append(reached)
                        find_obs_nodes(next_node, obs_space_nodes, obs_space_transitions, obs, space, i + 1)

                elif edge.transition_link.observability_label == "ϵ":
                    # if find_node_by_id(edge.destination, space.nodes_after_cutting) is not None:
                    next_node = ObservableNode(find_node_by_id(edge.destination, space.nodes_after_cutting),
                                               edge.destination, observation_index)

                    reached = str(next_node.id) + ", " + str(observation_index)
                    node.reachable_nodes.append(reached)
                    node.direct_reachable.append(reached)
                    new_transition = ObservableTransition(edge.transition_link.label, observation_index, node,
                                                          next_node, edge.transition_link.observability_label,
                                                          edge.transition_link.relevance_label)
                    obs_space_transitions.append(new_transition)

                    present = 0
                    for double in obs_space_nodes:
                        if double.id == edge.destination:
                            if find_node_by_id_and_index(edge.destination, observation_index,
                                                         obs_space_nodes) in obs_space_nodes:
                                present = 1

                    if present != 1:
                        obs_space_nodes.append(next_node)
                        find_obs_nodes(next_node, obs_space_nodes, obs_space_transitions, obs, space, i)

            else:
                if edge.transition_link.observability_label == "ϵ":
                    if find_node_by_id(edge.destination, space.nodes_after_cutting) is not None:
                        next_node = ObservableNode(find_node_by_id(edge.destination, space.nodes_after_cutting),
                                                   edge.destination, observation_index)

                        reached = str(next_node.id) + ", " + str(observation_index)
                        node.reachable_nodes.append(reached)
                        node.direct_reachable.append(reached)
                        new_transition = ObservableTransition(edge.transition_link.label, observation_index, node,
                                                              next_node, edge.transition_link.observability_label,
                                                              edge.transition_link.relevance_label)
                        obs_space_transitions.append(new_transition)

                        present = 0
                        for double in obs_space_nodes:
                            if double.id == edge.destination:
                                if observation_index == find_node_by_id(edge.destination,
                                                                        obs_space_nodes).observation_index:
                                    present = 1

                        if present != 1:
                            obs_space_nodes.append(next_node)

                            find_obs_nodes(next_node, obs_space_nodes, obs_space_transitions, obs, space, i)


def organize_reachable_nodes_obs(obs_space_nodes):
    # For each node
    for node in obs_space_nodes:
        # Create the list reachable_nodes
        reachable_list = []
        # For each reachable node in the list of reachable_nodes of a node
        for reach in node.reachable_nodes:
            # Add reach to the list
            reachable_list.append(reach)
            array_reached = reach.split(",")

            # Call the recursive function
            if find_node_by_id(int(array_reached[0]), obs_space_nodes) is not None:
                append_reachable_node_obs(reachable_list,
                                          find_node_by_id_and_index(int(array_reached[0]), int(array_reached[1]),
                                                                    obs_space_nodes), obs_space_nodes)
        # Update reachable_nodes in the node
        reachable_list = remove_duplicate(reachable_list)

        node.reachable_nodes = reachable_list

    # ------------ INTRO FUNCTION ------------
    # This is the recursive function to find the reachable_nodes
    # - reachable_nodes: the list of reachable_nodes of a node
    # - node: the node in input
    # - space_nodes: the nodes in the space at the time of the search


def append_reachable_node_obs(reachable_list, node, space_nodes):
    for reach in node.reachable_nodes:
        # If the child is already in the list
        if reach in reachable_list:
            array_reached = reach.split(",")
            # Find the child node
            if find_node_by_id(int(array_reached[0]), space_nodes) is not None:
                reach_node = find_node_by_id_and_index(int(array_reached[0]), int(array_reached[1]), space_nodes)
                # For all the reachable_nodes of the child node
                for reach_inner in reach_node.reachable_nodes:
                    # If the reachable_nodes are not in the list add them
                    if reach_inner not in reachable_list:
                        reachable_list.append(reach_inner)


        else:

            array_reached = reach.split(",")
            if find_node_by_id_and_index(int(array_reached[0]), int(array_reached[1]),
                                         space_nodes) is not None:
                # Add the child
                reachable_list.append(reach)
                # Call the recursive
                append_reachable_node_obs(reachable_list,
                                          find_node_by_id_and_index(int(array_reached[0]), int(array_reached[1]),
                                                                    space_nodes), space_nodes)


# ---------------------------------------------------------------------------------------------

# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space from an observation list and creates the renominated space
# - filename: this is the name to save the graph image
# - space: is the behavioral observable renominated space
def create_behavioral_space_observable_renominated(filename, space, obs):
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

    f.render(directory="Output/Behavioral_Space_Observable_Renominated")
    save_renomination_file_obs(space, "Output/Behavioral_Space_Observable_Renominated/RL_" + filename + ".txt")
    return space


# ------------ INTRO FUNCTION ------------
# This function removes the duplicate from a list in input
def remove_duplicate(list_duplicated):
    res = []
    for i in list_duplicated:
        if i not in res:
            res.append(i)
    return res


# ------------ INTRO FUNCTION ------------
# This function returns 1 if one of the children of the node in input exists and it is a final node
def link_to_a_final(node, space_nodes):
    for child in node.reachable_nodes:
        if find_node_by_id(child, space_nodes) is not None and find_node_by_id(child, space_nodes).isFinal:
            return 1


def remove_duplicated_transition_obs(transitions):
    for t1 in transitions:
        for t2 in transitions:
            if t1 is not t2:
                if t1.label == t2.label:
                    source_t1 = str(t1.source.id) + ", " + str(t1.source.observation_index)
                    source_t2 = str(t2.source.id) + ", " + str(t2.source.observation_index)
                    if source_t1 == source_t2:
                        destination_t1 = str(t1.destination.id) + ", " + str(t1.destination.observation_index)
                        destination_t2 = str(t2.destination.id) + ", " + str(t2.destination.observation_index)
                        if destination_t1 == destination_t2:
                            transitions.remove(t2)


# ------------ INTRO FUNCTION ------------
# This function returns 1 if one of the children of the node in input exists and it is a final node
def link_to_a_final_obs(node, space_nodes):
    for child in node.reachable_nodes:
        child_array = child.split(", ")
        if find_node_by_id(int(child_array[0]), space_nodes) is not None and (
                find_node_by_id(int(child_array[0]), space_nodes)).link_node.isFinal:
            return 1


def link_to_a_final_obs_re(node, space_nodes):
    for child in node.reachable_nodes:
        child_array = child.split(", ")
        if find_node_by_id(int(child_array[0]), space_nodes) is not None and (
                find_node_by_id(int(child_array[0]), space_nodes)).isFinal:
            return 1


# ------------ INTRO FUNCTION ------------
# This function returns the node with the corresponding id
def find_node_by_id(id, space_nodes):
    for node in space_nodes:
        if node.id == id:
            return node


# ------------ INTRO FUNCTION ------------
# This function returns the node with the corresponding id
def find_node_by_id_and_index(id, obs_index, space_nodes):
    for node in space_nodes:
        if node.id == id:
            if node.observation_index == obs_index:
                return node


# ------------ INTRO FUNCTION ------------
# This function returns the node with the corresponding label
def find_node_id_by_label(node_label, space_nodes):
    for node in space_nodes:
        if node_label == node.label:
            return node.id


# ------------ INTRO FUNCTION ------------
# This function saves the file of the details about the renomination and the cut
def save_renomination_file(space, filename):
    out_file = open(filename, "w")
    out_file.write("-------------------------------------------\n")
    out_file.write("Nodi e transizioni mantenuti\n")
    out_file.write("-------------------------------------------\n")
    out_file.write("Stato del nodo   |      id (rinominato)    |     vecchio id  \n")

    for node in space.nodes_after_cutting:
        out_file.write(node.label + " \t" + str(node.id) + " \t" + str(node.old_id) + "\n")
    out_file.write("* gli id delle transizioni sono quelli della ridenominazione *\n")
    print_transition_pretty(space.transitions_after_cutting, out_file)

    out_file.write("\n----------------------------\n")
    out_file.write("Nodi e transizioni tagliate\n")
    out_file.write("----------------------------\n")

    out_file.write("Stato del nodo      |     id (vecchio)  \n")
    for node in space.cutted_nodes:
        out_file.write(node.label + " \t" + str(node.id) + "\n")
    out_file.write("* gli id delle transizioni NON sono quelli della ridenominazione\n sono quelli dello spazio originale *\n")
    print_transition_pretty(space.cutted_transitions, out_file)

    out_file.close()


def save_renomination_file_obs(space, filename):
    out_file = open(filename, "w")
    out_file.write("-------------------------------------------\n")
    out_file.write("Nodi e transizioni mantenuti\n")
    out_file.write("-------------------------------------------\n")
    out_file.write("id | indice di osservazione \n")

    for node in space.nodes_after_cutting:
        out_file.write(str(node.id) + " \t" + str(node.observation_index) + "\n")

    print_transition_pretty_obs(space.transitions_after_cutting, out_file)

    out_file.write("\n----------------------------\n")
    out_file.write("Nodi e transizioni tagliate\n")
    out_file.write("----------------------------\n")

    out_file.write("id | indice di osservazione \n")
    for node in space.cutted_nodes:
        out_file.write(str(node.id) + " \t" + str(node.observation_index) + "\n")

    print_transition_pretty_obs(space.cutted_transitions, out_file)

    out_file.close()


# ------------ INTRO FUNCTION ------------
# This is function is used to print with a better style the transition in the file of the renomination
def print_transition_pretty(transitions, out_file):
    out_file.write("\n--- Transizioni ---\n")
    out_file.write(" id sorgente | etichetta | id destinazione | et. oss. | et. ril.\n")
    for transition in transitions:
        if len(str(transition.transition_link.observability_label)) > 2:
            out_file.write(str(transition.source) + "\t   " + str(transition.label) + "\t      " + str(
                transition.destination) + "\t         " + str(
                transition.transition_link.observability_label) + "\t       " + str(
                transition.transition_link.relevance_label) + "\n")
        else:
            out_file.write(str(transition.source) + "\t   " + str(transition.label) + "\t      " + str(
                transition.destination) + "\t         " + str(
                transition.transition_link.observability_label) + "         " + str(
                transition.transition_link.relevance_label) + "\n")


def print_transition_pretty_obs(transitions, out_file):
    out_file.write("\n--- Transizioni ---\n")
    out_file.write(" id sorgente | etichetta | id destinazione | et. oss. | indice oss. | et. ril.\n")
    for transition in transitions:
        out_file.write(str(transition.source.id) + "\t   " + str(transition.label) + "\t      " + str(
            transition.destination.id) + " \t         " + str(
            transition.observability_label) + " \t              " + str(
            transition.observation_index) + " \t        " + str(
            transition.relevance_label) + "\n")


def create_diagnosis_for_space_observable_renominated(filename, space, obs):
    transitions = copy.deepcopy(space.transitions_after_cutting)
    e_transition_list = []

    for t in transitions:
        e_transition_list.append(E_transition(t.relevance_label, (t.source.id, t.source.observation_index),
                                              (t.destination.id, t.destination.observation_index)))

    nodes = []
    final_nodes = []
    for node in space.nodes_after_cutting:
        nodes.append((node.id, node.observation_index))
        if node.link_node.isFinal and not (node.id == 0 and node.observation_index == 0):
            final_nodes.append((node.id, node.observation_index))

    first_node = nodes[0]
    new_first_node = ()
    # Step 1
    # Create a first state if state 0 has more than 1 input edge
    c = 0
    for e_t in e_transition_list:
        if e_t.destination == first_node:
            c = 1

    if c == 1:
        new_first_node = ("q0", "-")
        e_transition_list.append(E_transition("ϵ", new_first_node, first_node))
    else:
        new_first_node = first_node
        nodes.remove(first_node)

    # Step 2.1
    # Create a new final state if the number of final states is more than 1
    final_node = ()

    if len(final_nodes) > 1:
        final_node = ("qf", "-")
        for f in final_nodes:
            e_transition_list.append(E_transition("ϵ", f, final_node))
    else:
        # Step 2.2
        # Create a new final state if the number of edge with the final states as source is more than 1
        c = 0
        for e_t in e_transition_list:
            if e_t.source == final_nodes[0]:
                c = 1

        if c == 1:
            final_node = ("qf", "-")
            e_transition_list.append(E_transition("ϵ", final_nodes[0], final_node))
        else:
            final_node = final_nodes[0]
            nodes.remove(final_node)

    # Step 3
    # Eliminate all the intermediates states
    img = 0
    count = 1

    # Print the first

    while len(nodes) > 0:

        d = Digraph(str(count), format='png')

        for n, k in nodes:
            label = str(n) + " " + str(k)
            d.node(label, shape="circle")

        if len(final_nodes) > 1:
            label = str(final_node[0]) + " " + str(final_node[1])
            d.node(label, shape="doublecircle")
        else:
            label = str(final_nodes[0][0]) + " " + str(final_nodes[0][1])
            d.node(label, shape="doublecircle")

        label = str(first_node[0]) + " " + str(first_node[1])
        d.node(label, shape="circle")

        remove_duplicated_transition(e_transition_list)

        for t in e_transition_list:
            source = str(t.source[0]) + " " + str(t.source[1])
            destination = str(t.destination[0]) + " " + str(t.destination[1])
            d.edge(source, destination, t.label)

        d.render(directory="Output/Diagnosi_steps")

        img += 1
        count += 1
        semplify_paralle_path(e_transition_list)
        node = getNode_with_minimum_edges(nodes, e_transition_list)

        input_t = []
        auto_t = []
        ouput_t = []

        for t in e_transition_list:
            if t.destination == node:
                if t.source == node:
                    auto_t.append(t)
                else:
                    input_t.append(t)
            elif t.source == node:
                if t.destination == node:
                    auto_t.append(t)
                else:
                    ouput_t.append(t)

        for t_i in input_t:
            for t_o in ouput_t:

                if not auto_t:
                    if t_i.label != "ϵ":
                        if t_o.label != "ϵ":
                            label = t_i.label + "" + t_o.label
                        else:
                            label = t_i.label
                    else:
                        if t_o.label == "ϵ":
                            label = "ϵ"
                        else:
                            label = t_o.label

                    e_transition_list.append(E_transition(label, t_i.source, t_o.destination))
                else:
                    for a_t in auto_t:

                        if a_t.label != "ϵ":
                            if t_i.label != "ϵ":
                                if t_o.label != "ϵ":
                                    label = t_i.label + t_o.label + "(" + a_t.label + ")*"
                                else:
                                    label = t_i.label + "(" + a_t.label + ")*"
                            else:
                                if t_o.label == "ϵ":
                                    label = "(" + a_t.label + ")*"
                                else:
                                    label = t_o.label + "(" + a_t.label + ")*"
                        else:
                            if t_i.label != "ϵ":
                                if t_o.label != "ϵ":
                                    label = t_i.label + t_o.label
                                else:
                                    label = t_i.label
                            else:
                                if t_o.label == "ϵ":
                                    label = "ϵ"
                                else:
                                    label = t_o.label

                        e_transition_list.append(E_transition(label, t_i.source, t_o.destination))

                remove_transition(e_transition_list, t_o)

        nodes.remove(node)

        for t_i in input_t:
            remove_transition(e_transition_list, t_i)
        for t_o in ouput_t:
            remove_transition(e_transition_list, t_o)
        for a_t in auto_t:
            remove_transition(e_transition_list, a_t)

    remove_duplicated_transition(e_transition_list)

    exp = ""
    for t in e_transition_list:
        if exp == "":
            exp = t.label

        else:
            if t.label != "ϵ":
                exp = exp + "|" + t.label
            else:
                exp = exp

    d = Digraph(str(count), format='png')
    semplify_paralle_path(e_transition_list)
    for t in e_transition_list:
        source = str(t.source[0]) + " " + str(t.source[1])
        destination = str(t.destination[0]) + " " + str(t.destination[1])
        d.edge(source, destination, t.label)
    d.render(directory="Output/Diagnosi_steps")
    return img, exp


def remove_duplicated_transition(e_transition_list):
    for t1 in e_transition_list:
        for t2 in e_transition_list:
            if t1 is not t2:
                if t1.label == t2.label:
                    if t1.source == t2.source:
                        if t1.destination == t2.destination:
                            e_transition_list.remove(t2)


def remove_transition(e_transition_list, t):
    for e_t in e_transition_list:
        if e_t.label == t.label:
            if e_t.source == t.source:
                if e_t.destination == t.destination:
                    e_transition_list.remove(e_t)


def semplify_paralle_path(e_transition_list):
    for t1 in e_transition_list:
        for t2 in e_transition_list:
            if t1 != t2:
                if t1.source == t2.source:
                    if t1.destination == t2.destination:
                        label = ""
                        if t1.label == "ϵ":
                            if t2.label == "ϵ":
                                label = "ϵ"
                            else:
                                label = t2.label + "|ϵ"
                        else:
                            if t2.label == "ϵ":
                                label = t1.label + "|ϵ"
                            else:
                                label = t1.label + "|" + t2.label

                        e_transition_list.append(E_transition(label, t1.source, t1.destination))
                        if t2 in e_transition_list:
                            e_transition_list.remove(t2)
                        if t1 in e_transition_list:
                            e_transition_list.remove(t1)


def getNode_with_minimum_edges(nodes, e_transition_list):
    min_node = nodes[0]

    min_t = count_edges_in_node(min_node, e_transition_list)

    for node in nodes:
        if node != min_node:
            if count_edges_in_node(node, e_transition_list) < min_t:
                min_node = node

    return min_node


def count_edges_in_node(node, e_transition_list):
    min_i = 0
    # min_o = 0
    for e_t in e_transition_list:
        # if node == e_t.source:
        #     min_o += 1
        if node == e_t.destination:
            min_i += 1

    return min_i


def draw_comportamental_space(name, space):
    g = Digraph(name, format='png')

    for transition in space.transitions:
        g.edge(str(transition.source), str(transition.destination), transition.label)

    for node in space.nodes:
        if node.isFinal:
            g.node(str(node.id), shape="doublecircle")
        else:
            g.node(str(node.id), shape="circle")

    g.render(directory="Output/Behavioral_Space")
