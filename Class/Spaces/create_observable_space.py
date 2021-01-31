from graphviz import Digraph

from Class.Base.space import ObservableNode, Space, ObservableTransition
from Class.Utils.utils import remove_duplicated_transition_obs, remove_duplicate, find_node_by_id, find_node_by_id_and_index

# ------------ INTRO FUNCTION ------------
# This function draws the graphic of the behavioral space from an observation list and creates the space
# - filename: this is the name to save the graph image
# - obs: is the list of the observations
# - space: is the behavioral renominated space
def create_behavioral_space_from_obs(filename, obs, space, original_filename):

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
    f.render(directory="Output/"+original_filename+"/Behavioral_Space_Observable")

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

    g.render(directory="Output/"+original_filename+"/Behavioral_Space_Observable")

    obs_space = Space(obs_space_nodes, obs_space_transitions)

    summary = open("Output/"+original_filename+"/Behavioral_Space_Observable/space_summary.txt", "w")
    summary.write("Numero di nodi:" + str(len(obs_space_nodes)) + "\n")
    i = 1
    for node in obs_space_nodes:
        summary.write(str(i) + ") " + str(node.id)+", "+str(node.observation_index)+ "\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(obs_space_transitions)) + "\n")
    i = 1
    for t in obs_space_transitions:
        summary.write(str(i) + ") " + str(t.source.link_node.id)+ ", " + str(t.source.observation_index) + " -> " + str(t.label) + "-> " + str(t.destination.link_node.id)+ ", " + str(t.destination.observation_index) + "\n")
        i = i + 1
    summary.close()

    return obs_space



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

                elif edge.transition_link.observability_label == "-":
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
                if edge.transition_link.observability_label == "-":
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