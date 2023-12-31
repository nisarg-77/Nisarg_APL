import numpy as np


def evalSpice(file_name):
    # opening the file in reading mode while checking that it has valid name
    try:
        f = open(f"{file_name}", "r")
    except FileNotFoundError:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')

    # reading from the file line by line
    lines = f.readlines()
    branch = []
    for i in range(len(lines)):
        branch.append(lines[i].strip('\n'))

    # getting the indices within which circuit contents actually reside
    begin = -1
    end = -1
    for i in range(len(lines)):
        branch.append(lines[i].strip('\n'))
        if lines[i] == '.circuit\n':
            begin = i
        if lines[i] == '.end\n':
            end = i
    # if the file doesn't contain .begin or .end raising malformed error
    if begin == -1 or end == -1:
        raise ValueError('Malformed circuit file')
    for i in range(len(branch)):
        tempb = []
        tempb = branch[i].split('#')
        branch[i] = tempb[0]

    dic_elem = {}  # dictionary containing element name as key and list containing nodes and magnitude as its value
    node = []  # contains all the nodes
    for i in range(begin + 1, end):
        words = branch[i].split()
        tem_n1 = ''
        tem_n2 = ''
        if words[0][0] == "V" or words[0][0] == "I" or words[0][0] == "R":
            if words[0][0] == "V":
                if words[-2] == "ac":  # if voltage source is not dc source
                    raise ValueError('Malformed circuit file')
            if words[1] not in node:
                node.append(words[1])
            if words[2] not in node:
                node.append(words[2])
            if words[1] == 'GND':
                tem_n1 = 'GND'
            else:  # handling the case when node 1 is written as n1 instead of 1
                for j in range(len(words[1])):
                    if words[1][j] in '1234567890':
                        tem_n1 += f"{words[1][j]}"

            if words[2] == 'GND':
                tem_n2 = 'GND'
            else:
                for j in range(len(words[2])):
                    if words[2][j] in '1234567890':
                        tem_n2 += f"{words[2][j]}"

            temp_list = [words[-1], tem_n1, tem_n2]

            tem_d = {words[0]: temp_list}
            if words[0] in dic_elem:  # if a circuit element name is repeated
                raise ValueError('Malformed circuit file')
            dic_elem.update(tem_d)
        else:
            raise ValueError('Only V, I, R elements are permitted')

    if 'GND' in node:
        length = len(node) - 1
    else:
        length = len(node)
    # matrix formation
    for key, value in dic_elem.items():
        if key[0] == 'V':
            length += 1

    # forming the matrix according to kirchoff's current law
    conductance_matrix = np.zeros(shape=(length, length), dtype=float)
    target_matrix = np.zeros(shape=length, dtype=float)
    currents = []  # stores all the voltage sources for giving the second part of answer

    unknown_index = len(node) - 2  # it stores the row number from voltage difference equation occurs
    for key, value in dic_elem.items():
        # If the element is resistance
        if key[0] == 'R':
            try:
                if float(value[0]) == 0:  # if resitance is 0 setting conductance to a very high value
                    G = 1e10
                elif float(value[0]) > 0:
                    G = float(1 / float(value[0]))
                else:  # if R value is negative
                    raise ValueError('Malformed circuit file')
            except ValueError:
                raise ValueError('Malformed circuit file')
            node1 = value[1]
            node2 = value[2]
            if f"{node1}" != 'GND':
                conductance_matrix[int(node1) - 1][int(node1) - 1] += G
                if f"{node2}" != 'GND':
                    conductance_matrix[int(node2) - 1][int(node1) - 1] -= G
            if f"{node2}" != 'GND':
                conductance_matrix[int(node2) - 1][int(node2) - 1] += G
                if f"{node1}" != 'GND':
                    conductance_matrix[int(node1) - 1][int(node2) - 1] -= G

        # If element is a Current sourcee
        elif key[0] == 'I':
            node1 = value[1]
            node2 = value[2]
            try:
                value[0] = float(value[0])
            except ValueError:
                raise ValueError('Malformed circuit file')
            if f"{node1}" != 'GND':
                target_matrix[int(node1) - 1] -= value[0]
            if f"{node2}" != 'GND':
                target_matrix[int(node2) - 1] += value[0]
        # If the elment is a voltage source
        elif key[0] == 'V':
            node1 = value[1]
            node2 = value[2]
            unknown_index += 1
            currents.append(key)
            try:
                value[0] = float(value[0])
            except ValueError:
                raise ValueError('Malformed circuit file')
            target_matrix[unknown_index] += value[0]
            if f"{node1}" != 'GND':
                conductance_matrix[int(node1) - 1][int(unknown_index)] += 1
                conductance_matrix[unknown_index][int(node1) - 1] += 1
                if f"{node2}" != 'GND':
                    conductance_matrix[int(unknown_index)][int(node2) - 1] -= 1

            if f"{node2}" != 'GND':
                conductance_matrix[(int(node2) - 1)][int(unknown_index)] -= 1
                conductance_matrix[unknown_index][int(node2) - 1] -= 1

    # solving the matrix using gaussian elimination
    answer = gausselim(conductance_matrix, target_matrix)

    # forming the final answer
    nodal_answer = {}
    current_answer = {}

    c = 0
    for current in currents:
        tempc = {current: answer[len(node) - 1 + c]}
        current_answer.update(tempc)
        c += 1
    for nod in node:
        tempn = ''
        if nod == 'GND':
            tempd = {'GND': 0.0}
        else:
            for i in nod:  # handling the case when node 1 is written as n1 instead of 1
                if i in '1234567890':
                    tempn += i
            tempd = {nod: answer[int(tempn) - 1]}
        nodal_answer.update(tempd)

    return nodal_answer, current_answer


def gausselim(a, b):
    for row in range(len(a)):
        norm = a[row][row]
        if norm == 0:
            raise ValueError('Circuit error: no solution')
        for i in range(len(a[row])):
            a[row][i] /= norm
        b[row] = b[row] / norm
        for i in range(len(a)):
            if i != row:
                norm = a[i][row] / a[row][row]
                for j in range(len(a[i])):
                    a[i][j] = a[i][j] - (a[row][j] * norm)
                b[i] = b[i] - (b[row] * norm)
    return b


print(evalSpice("test_3.ckt"))
