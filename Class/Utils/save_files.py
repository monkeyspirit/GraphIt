def save_renomination_file(space, path):
    out_file = open(path, "w")
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


def save_renomination_file_obs(space, path):
    out_file = open(path, "w")
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