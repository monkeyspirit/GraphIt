import copy

from graphviz import Digraph

from Class.Base.space import DiagnosiTransition
from Class.Utils.utils import remove_duplicated_transition, getNode_with_minimum_edges, remove_transition


def create_diagnosis_for_space_observable_renominated(filename, space):
    transitions = copy.deepcopy(space.transitions_after_cutting)
    e_transition_list = []

    for t in transitions:
        e_transition_list.append(DiagnosiTransition(t.relevance_label, (t.source.id, t.source.observation_index),
                                                    (t.destination.id, t.destination.observation_index)))
    for e_t in e_transition_list:
        e_t.list_label.append(e_t.label)

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
        e_t0 = DiagnosiTransition("ϵ", new_first_node, first_node)
        e_t0.list_label = ["ϵ"]
        e_transition_list.append(e_t0)
    else:
        new_first_node = first_node
        nodes.remove(first_node)

    # Step 2.1
    # Create a new final state if the number of final states is more than 1
    final_node = ()

    if len(final_nodes) > 1:
        final_node = ("qf", "-")
        for f in final_nodes:
            e_t1 = DiagnosiTransition("ϵ", f, final_node)
            e_t1.list_label = ["ϵ"]
            e_transition_list.append(e_t1)
    else:
        # Step 2.2
        # Create a new final state if the number of edge with the final states as source is more than 1
        c = 0
        for e_t in e_transition_list:
            if e_t.source == final_nodes[0]:
                c = 1

        if c == 1:
            final_node = ("qf", "-")
            e_t2 = DiagnosiTransition("ϵ", final_nodes[0], final_node)
            e_t2.list_label = ["ϵ"]
            e_transition_list.append(e_t2)

        else:
            final_node = final_nodes[0]
            nodes.remove(final_node)

    # Step 3
    # Eliminate all the intermediates states
    img = 0
    count = 1

    # Print the first
    label_out = ""

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

        if label_out != "":
            d.node(label_out, shape="circle")

        remove_duplicated_transition(e_transition_list)

        for t in e_transition_list:
            source = str(t.source[0]) + " " + str(t.source[1])
            destination = str(t.destination[0]) + " " + str(t.destination[1])
            d.edge(source, destination, t.label)

        d.render(directory="Output/"+filename+"/Diagnosi_steps/")

        img += 1
        count += 1
        semplify_paralle_path(e_transition_list)
        node = getNode_with_minimum_edges(nodes, e_transition_list)

        t_in_output = []
        auto_t = []
        t_in_input = []

        for t in e_transition_list:
            if t.destination == node:
                if t.source == node:
                    auto_t.append(t)
                else:
                    t_in_output.append(t)
            elif t.source == node:
                if t.destination == node:
                    auto_t.append(t)
                else:
                    t_in_input.append(t)

        for t_out in t_in_output:
            for t_in in t_in_input:
                new_list = []
                if not auto_t:
                    if t_out.label != "ϵ":
                        if t_in.label != "ϵ":
                            # label = t_out.label + "" + t_in.label
                            for o in t_out.list_label:
                                for i in t_in.list_label:
                                    if o != "ϵ":
                                        new_list.append(str(o)+""+str(i))
                                    else:
                                        new_list.append(i)
                            label = ""
                            for n in new_list:
                                label = label +"|"+n
                            label = label[1:]
                        else:
                            label = t_out.label
                            if t_out.list_label != []:
                                new_list = t_out.list_label
                            else:
                                new_list.append(label)
                    else:
                        if t_in.label == "ϵ":
                            label = "ϵ"
                            new_list.append("ϵ")
                        else:
                            label = t_in.label
                            if t_in.list_label != []:
                                new_list = t_in.list_label
                            else:
                                new_list.append(label)

                    new_t = DiagnosiTransition(label, t_out.source, t_in.destination)
                    new_t.list_label = new_list
                    e_transition_list.append(new_t)
                else:
                    for a_t in auto_t:

                        if a_t.label != "ϵ":
                            if t_out.label != "ϵ":
                                if t_in.label != "ϵ":
                                    label = t_out.label + t_in.label + "(" + a_t.label + ")*"
                                else:
                                    label = t_out.label + "(" + a_t.label + ")*"
                            else:
                                if t_in.label == "ϵ":
                                    label = "(" + a_t.label + ")*"
                                else:
                                    label = t_in.label + "(" + a_t.label + ")*"
                        else:
                            if t_out.label != "ϵ":
                                if t_in.label != "ϵ":
                                    label = t_out.label + t_in.label
                                else:
                                    label = t_out.label
                            else:
                                if t_in.label == "ϵ":
                                    label = "ϵ"
                                else:
                                    label = t_in.label

                        new_t2 = DiagnosiTransition(label, t_out.source, t_in.destination)
                        new_t2.list_label.append(label)
                        e_transition_list.append(new_t2)

                remove_transition(e_transition_list, t_in)

        label_out = str(node[0])+" "+str(node[1])
        nodes.remove(node)

        for t_out in t_in_output:
            remove_transition(e_transition_list, t_out)
        for t_in in t_in_input:
            remove_transition(e_transition_list, t_in)
        for a_t in auto_t:
            remove_transition(e_transition_list, a_t)

    remove_duplicated_transition(e_transition_list)

    exp = ""
    for t in e_transition_list:
         for l in t.list_label:
                exp = exp +"|"+l
    exp = exp [1:]
    d = Digraph(str(count), format='png')

    semplify_paralle_path(e_transition_list)
    d.node(label_out, shape="circle")

    for t in e_transition_list:
        source = str(t.source[0]) + " " + str(t.source[1])
        destination = str(t.destination[0]) + " " + str(t.destination[1])
        d.edge(source, destination, t.label)
    d.render(directory="Output/"+filename+"/Diagnosi_steps/")
    return img, exp


def semplify_paralle_path(e_transition_list):
    for t1 in e_transition_list:
        for t2 in e_transition_list:
            if t1 != t2:
                if t1.source == t2.source:
                    if t1.destination == t2.destination:

                        new_list_label = []
                        t1_list_label = t1.list_label
                        t2_list_label = t2.list_label

                        for l1 in t1_list_label:
                            if l1 not in new_list_label:
                                new_list_label.append(l1)

                        for l2 in t2_list_label:
                            if l2 not in new_list_label:
                                new_list_label.append(l2)


                        new_label =""
                        for l in new_list_label:
                            new_label = str(new_label) + "|"+str(l)
                        new_label = new_label[1:]
                        new_e_t = DiagnosiTransition(new_label, t1.source, t1.destination)
                        new_e_t.list_label = new_list_label
                        e_transition_list.append(new_e_t)
                        if t2 in e_transition_list:
                            e_transition_list.remove(t2)
                        if t1 in e_transition_list:
                            e_transition_list.remove(t1)