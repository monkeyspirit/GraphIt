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


def link_to_a_final_obs(node, space_nodes):
    for child in node.reachable_nodes:
        child_array = child.split(", ")
        if find_node_by_id(int(child_array[0]), space_nodes) is not None and (
                find_node_by_id(int(child_array[0]), space_nodes)).link_node.isFinal:
            return 1


def link_to_a_final_obs_re(node, space_nodes):
    for child in node.reachable_nodes:
        child_array = child.split(", ")
        if  find_node_by_id_and_index(int(child_array[0]),int(child_array[1]), space_nodes) is not None and (
                find_node_by_id_and_index(int(child_array[0]), int(child_array[1]), space_nodes)).isFinal:
            return 1


def find_node_by_id(id, space_nodes):
    for node in space_nodes:
        if node.id == id:
            return node


def get_new_id_by_old_id(id, space_nodes):
    for node in space_nodes:
        if node.old_id == id:
            return node.id


def find_node_by_id_and_index(id, obs_index, space_nodes):
    for node in space_nodes:
        if node.id == id:
            if node.observation_index == obs_index:
                return node


def find_node_id_by_label(node_label, space_nodes):
    for node in space_nodes:
        if node_label == node.label:
            return node.id


def remove_duplicate(list_duplicated):
    res = []
    for i in list_duplicated:
        if i not in res:
            res.append(i)
    return res


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